
import asyncio
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Set

import aiodocker
import yaml
from attr import define

from . import scan
from .utils import SubLog, AtopileError
from .stages import File, Stage, StageDef
from .tree import TreeView

program_log = logging.getLogger(__name__)

@define
class Build:
    docker: aiodocker.Docker
    build_graph: scan.BuildGraph
    log: SubLog
    job_semaphores: asyncio.locks.Semaphore
    project_dir: Path
    done: List[str] = []

    def check_previously_done(self):
        hashes_path = self.project_dir / 'build' / '.hashes.yaml'
        if not hashes_path.exists():
            return
        with hashes_path.open('r') as f:
            existing_hashes = yaml.safe_load(f) or {}

        stages = self.build_graph.stages
        possibly_done = set(existing_hashes.keys()).intersection(stages.keys())
        current_hashes = {k: stages[k].compute_hash() for k in possibly_done}

        for io in current_hashes:
            if existing_hashes[io] == current_hashes[io]:
                self.done.append(io)

    def mark_stage_done(self, stage_ref: str):
        """
        Mark a stage done, assert it's outputs were generated, else raise an error
        """
        for output_node in self.build_graph.get_outputs(stage_ref):
            output = self.build_graph.nodes[output_node]['io']
            if not output.exists():
                self.log.error(f'{stage_ref} didn\'t produce {str(output_node)} as expected')
            else:
                self.done.append(output_node)
        self.done.append(stage_ref)

    def get_ready_to_run_stages(self) -> Dict[str, Stage]:
        ready_to_run = {}
        for stage_ref, stage in self.build_graph.stages.items():
            upstream = self.build_graph.direct_upstream_nodes(stage_ref)
            for ref in upstream:
                node = self.build_graph.nodes[ref]
                if ref not in self.done:
                    if node['type'] == scan.NodeType.IO and isinstance(node['io'], scan.File):
                        pass
                    else:
                        # something part of build-time isn't ready quite yet
                        break
            else:
                # everything below is ready
                ready_to_run[stage_ref] = stage
        return ready_to_run

    async def _run_stage(self, stage_ref: str):
        async with self.job_semaphores:
            build_dir = self.project_dir / 'build' / stage_ref
            build_dir.mkdir(parents=True, exist_ok=True)
            stage = self.build_graph.stages[stage_ref]
            inputs = self.build_graph.get_inputs(stage_ref)
            
            # run the stage
            log = await stage.run(self.docker, inputs)
            print(log)

            # check whether it ran properly
            if not log:
                self.log.error(f'{stage_ref} failed')
                print(self.log)
                raise AtopileError

            # copy files to dist
            for output_name, dist_location in stage.dist.items():
                if output_name in stage.outputs:
                    output_paths = stage.outputs[output_name].fs_location
                    pass
                else:
                    output_paths = list(build_dir.glob(output_name))
                    if not output_paths:
                        self.log.warning(f'Couldn\'t dist {output_name}')
                        continue

                if not isinstance(output_paths, list):
                    output_paths = [output_paths]

                for output_path in output_paths:
                    dist = self.project_dir / 'dist'
                    if dist_location:
                        dist = dist / dist_location
                    dist.mkdir(parents=True, exist_ok=True)
                    shutil.copy(str(output_path), str(dist / output_path.name))

            # mark the stage done so others depending on it can run
            self.mark_stage_done(stage_ref)
            if not self.build_graph.log:
                print(self.build_graph.log)
                raise ValueError

    async def run(self, until_dead: bool = False):
        self.check_previously_done()

        remaining_stages = set(self.build_graph.stages.keys()).difference(self.done)
        stage_runner_tasks: Dict[str, asyncio.Task] = {}

        # as long as there's stuff to do
        while remaining_stages:
            # check on existing tasks
            for stage_ref in list(stage_runner_tasks.keys()):
                task = stage_runner_tasks[stage_ref]
                if task.done():
                    del stage_runner_tasks[stage_ref]
                    ex = task.exception()
                    if ex:
                        self.log.error(f'{stage_ref} failed with exception {repr(ex)}')
            
            # cancel remaining tasks
            if not until_dead and not self.log:
                for task in stage_runner_tasks.values():
                    if not task.done():
                        task.cancel()
                break

            # schedule new tasks
            ready_to_run = set(self.get_ready_to_run_stages().keys())
            ready_and_unscheduled = ready_to_run.intersection(remaining_stages)
            for stage_ref in ready_and_unscheduled:
                task = asyncio.create_task(self._run_stage(stage_ref))
                # await self._run_stage(stage_ref)
                stage_runner_tasks[stage_ref] = task
                remaining_stages.remove(stage_ref)
            
            # polling rate limiter
            await asyncio.sleep(1)

        # wait for them all to finish
        await asyncio.gather(*list(stage_runner_tasks.values()))
        await self.docker.close()
        return self.log

    @classmethod
    def from_build_graph(cls, build_graph: scan.BuildGraph, project_dir: Path, workers: int = 8):
        try:
            docker = aiodocker.Docker()
        except ValueError:
            program_log.error('Docker isn\'t running')
            raise

        job_semaphores = asyncio.locks.Semaphore(workers)
        log = SubLog(build_graph.name)

        return cls(
            docker=docker,
            build_graph=build_graph,
            log=log,
            job_semaphores=job_semaphores,
            project_dir=project_dir,
        )

def build(task: str, project_dir: Path):
    config_path = project_dir / '.atopile.yaml'

    with config_path.open() as f:
        config_data: dict = yaml.safe_load(f)

    project_name = config_data.get('name') or 'untitled'
    print(f'Building {project_name}!')

    task_data = config_data.get('tasks', {}).get(task)
    if not task_data:
        program_log.error(f'Nothing to do for task {task}')
        raise AtopileError

    stages = Stage.from_config_data(task_data, project_dir)
    build_graph = scan.BuildGraph.from_stages(config_data['name'], stages, project_dir)

    print('=== Build Tree ===')
    tree_view = TreeView.from_build_graph(build_graph)
    tree_view.show()

    build = Build.from_build_graph(build_graph, project_dir)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(build.run(project_dir))

    print(build.log)

    loop.close()
