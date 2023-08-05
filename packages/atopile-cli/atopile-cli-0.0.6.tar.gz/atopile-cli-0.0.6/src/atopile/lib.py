import logging
from pathlib import Path
from typing import List

import yaml

from .config import ATOPILE_DIR
from .utils import AtopileError
from .git_resource import GitResource, GitRepoStore

log = logging.getLogger(__name__)

library_path = ATOPILE_DIR / 'library'
library_store = GitRepoStore(library_path).load()

def generate_table_rows(entry: GitResource, libs: List[Path]) -> str:
    ouptut = ''
    for lib in libs:
        # format name and uri
        name = f'{entry.slim_remote}/{lib.name}'
        name = name.replace('/', '{slash}')
        uri = str((entry.local / lib).absolute())
        ouptut += f'  (lib (name "{name}")(type "KiCad")(uri "{uri}")(options "")(descr ""))\n'
    return ouptut

def dump_libs(entries: List[GitResource], where: Path):
    sym_lib_table = '(sym_lib_table\n'
    fp_lib_table = '(fp_lib_table\n'
    for entry in entries:
        sym_libs = entry.local.glob('**/*.kicad_sym')
        mod_libs = entry.local.glob('**/*.kicad_mod')
        sym_lib_table += generate_table_rows(entry, sym_libs)
        fp_lib_table += generate_table_rows(entry, mod_libs)

    sym_lib_table += ')\n'
    fp_lib_table += ')\n'

    with (where / 'sym-lib-table').open('w') as f:
        f.write(sym_lib_table)

    with (where / 'fp-lib-table').open('w') as f:
        f.write(fp_lib_table)

def add_lib(path: str, subproject_pattern: str, project_dir: Path):
    # clone stuff and/or add it to the tracker
    new_entry = library_store.get(path)
    
    # add it to the project lib list
    config_path = project_dir / '.atopile.yaml'
    try: 
        with config_path.open() as f:
            config_data = yaml.safe_load(f)
    except FileNotFoundError:
        config_data = {}

    all_subproject_libs = config_data.get('libs') or {}
    if '*' not in subproject_pattern:
        subproject_pattern = ('**/*' + subproject_pattern + '*.kicad_pro')

    for subproject in project_dir.glob(subproject_pattern):
        if subproject.suffix != '.kicad_pro':
            log.error(f'{str(subproject)} isn\'t a valid sub-project')
            raise AtopileError

        libs = all_subproject_libs.get(subproject) or []
        if new_entry.slim_remote not in libs:
            libs.append(new_entry.slim_remote)
        all_subproject_libs[str(subproject.relative_to(project_dir))] = libs

        # update the symbol and component linking files
        libs = [entry for entry in library_store.entries if entry.slim_remote in libs]
        dump_libs(libs, subproject.parent)

    config_data['libs'] = all_subproject_libs

    with config_path.open('w') as f:
        yaml.safe_dump(config_data, f)
