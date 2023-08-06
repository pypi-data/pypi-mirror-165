import logging
from hashlib import sha1
from operator import contains
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import urlsplit

import git
import yaml
from attr import define

from atopile.utils import add_file_to_hash

log = logging.getLogger(__name__)

def split_path(path: str) -> Tuple[str, str]:
    sections = path.split('/')
    for i, section in enumerate(sections):
        if section.endswith('.git'):
            remote_path = '/'.join(sections[:i+1])
            internal_path = '/'.join(sections[i+1:])
            break
    else:
        remote_path = path
        internal_path = ''

    return remote_path, internal_path

@define
class GitResource:
    local: Path
    sshy: bool
    netloc: str
    remote_path: str

    @property
    def sshy_remote(self) -> str:
        return f'git@{self.netloc}:{self.remote_path}'

    @property
    def httpsy_remote(self) -> str:
        return f'https://{self.netloc}/{self.remote_path}'

    @property
    def remote(self) -> str:
        if self.sshy:
            return self.sshy_remote
        else:
            return self.httpsy_remote

    @property
    def slim_remote(self):
        return self.netloc + '/' + self.remote_path

    @property
    def sha1(self):
        return sha1(self.slim_remote.encode()).digest().hex()

    def clone(self) -> git.Repo:
        if not self.local.exists():
            self.local.mkdir(parents=True)

        try:
            repo = git.Repo.clone_from(self.remote, self.local)
        except git.GitCommandError as ex:
            if 'port 443' in ex.stderr and 'Failed to connect' in ex.stderr:
                http_remote = self.remote.replace('https://', 'http://')
                repo = git.Repo.clone_from(http_remote, self.local)
            else:
                log.error(f'{self.remote} isn\'t a git repo, doesn\'t exist or isn\'t accessible')
                raise
        return repo

    def update(self) -> git.Repo:
        repo = git.Repo(self.local)
        repo.remotes.origin.fetch()
        repo.remotes.origin.pull()
        return repo

    def check_local(self) -> bool:
        try:
            repo = git.Repo(self.local)
        except git.InvalidGitRepositoryError:
            log.error(f'local points to {str(self.local)}, but that isn\'t a git repo')
            raise
        except git.NoSuchPathError:
            log.info(f'Local copy of {self.slim_remote} not found')
            return False
        else:
            return True

    @classmethod
    def partial_from_url(cls, url: str):
        """
        Create a partial GitResource from a URL, missing the local path.
        """
        if url.startswith('https://'):
            netloc, path = urlsplit(url)[1:3]
            path = path.lstrip('/')
            sshy = False
        elif url.startswith('git@'):
            raise NotImplementedError('Only https:// URLs are supported')
        else:
            netloc, path = url.split('/', 1)
            sshy = False

        # http:// gitlab.coilchain.org/ mawildoer/build-wrapper.git/ kibot-build
        # git@ gitlab.coilchain.org: mawildoer/build-wrapper.git/ kibot-build
        # gitlab.coilchain.org /untitled/build-wrapper.git/ kibot-build
            
        remote_path, _ = split_path(path)
        return cls(local=None, sshy=sshy, netloc=netloc, remote_path=remote_path)

    @classmethod
    def from_remote(cls, url: str, store_path: Path) -> 'GitResource':
        resource = cls.partial_from_url(url)
        # get the directory name to clone into
        # using a hash here to get a unique with safe (hex chars)
        resource.local = store_path / resource.sha1
        return resource
    
    @classmethod
    def from_local(cls, local: Path) -> 'GitResource':
        try:
            repo = git.Repo(local)
        except git.InvalidGitRepositoryError:
            log.error(f'{local} isn\'t a git repo')
            raise

        # get the directory the repo is in
        resource = cls.partial_from_url(repo.remote().url)
        resource.local = Path(repo.working_tree_dir)
        return resource

@define
class GitRepoStore:
    store_path: Path
    TRACKER_NAME = '.tracker.yaml'
    entries: List[GitResource] = []

    @property
    def slim_remotes(self):
        return [entry.slim_remote for entry in self.entries]

    @property
    def tracker_path(self) -> Path:
        return self.store_path / self.TRACKER_NAME

    def get_by_slim_remote(self, slim_remote: str) -> GitResource:
        for entry in self.entries:
            if entry.slim_remote == slim_remote:
                return entry
        return None

    def scan_local(self):
        if not self.store_path.exists():
            return

        for dir in self.store_path.iterdir():
            if dir.is_dir():
                try:
                    repo = git.Repo(dir)
                except git.InvalidGitRepositoryError:
                    continue
                else:
                    self.add_local(dir)

    def load(self) -> 'GitRepoStore':
        # load from tracker file
        try:
            with self.tracker_path.open() as f:
                tracker_data = yaml.safe_load(f) or {}
        except FileNotFoundError:
            pass
        else:
            self.entries = []
            for entry in tracker_data:
                resource = GitResource.partial_from_url(entry['remote'])
                resource.local = Path(entry['local'])
                self.entries.append(resource)

        # detect if there are duplicates
        slim_remotes = set(self.slim_remotes)
        if len(self.entries) != len(slim_remotes):
            log.error('Duplicate entries found in tracker')
            raise ValueError('Duplicate entries found in tracker')

        self.save()

        return self
        
    def save(self):
        tracker_data = []
        for entry in self.entries:
            tracker_data.append({
                'local': str(entry.local),
                'remote': entry.remote,
            })

        if not self.store_path.exists():
            self.store_path.mkdir(parents=True)
        with self.tracker_path.open('w') as f:
            yaml.safe_dump(tracker_data, f)

    def get(self, path: str, auto_pull: bool = True) -> GitResource:
        remote_path, _ = split_path(path)
        slim_remotes = {e.slim_remote: e for e in self.entries}
        if remote_path in slim_remotes:
            return slim_remotes[remote_path]
        else:
            if auto_pull:
                log.info(f'{remote_path} not found in tracker, pulling from remote')
                return self.pull_remote(path)

    def add_local(self, local: Path) -> GitResource:
        new_entry = GitResource.from_local(local)
        if new_entry.slim_remote in self.slim_remotes:
            log.warning(f'{new_entry.slim_remote} already exists in the store')
            return

        self.entries.append(new_entry)
        self.save()
        return new_entry

    def pull_remote(self, remote: str) -> GitResource:
        new_entry = GitResource.from_remote(remote, self.store_path)
        if new_entry.slim_remote in self.slim_remotes:
            log.warning(f'{new_entry.slim_remote} already exists in the store')
            return

        new_entry.clone()
        self.entries.append(new_entry)
        self.save()
        return new_entry

    def add(self, path: str):
        if Path(path).exists():
            self.add_local(path)
        else:
            self.pull_remote(path)

    def replace(self, path: str):
        if Path(path).exists():
            replacement_entry = GitResource.from_local(path)
        else:
            replacement_entry = GitResource.from_remote(path, self.store_path)

        if replacement_entry.slim_remote not in self.slim_remotes:
            log.warning(f'{replacement_entry.slim_remote} doesn\'t exist in the store')
            self.entries.append(replacement_entry)
            return

        old_entry = self.get_by_slim_remote(replacement_entry.slim_remote)
        log.info(f'Replacing {old_entry.local} with {replacement_entry.local}')
        self.entries.remove(old_entry)
        self.entries.append(replacement_entry)
        self.save()
