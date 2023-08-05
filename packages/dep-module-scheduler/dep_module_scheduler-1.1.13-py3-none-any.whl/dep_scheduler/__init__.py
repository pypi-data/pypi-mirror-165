"""Dep scheduler module."""

from dataclasses import dataclass
from typing import Dict, Tuple, Callable, List, Optional
from logging import getLogger

from spec.types import Module, Environment # noqa

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import STATE_STOPPED

TypeScheduledJob = Tuple[Callable, str, Dict]
TypeSchedule = List[TypeScheduledJob]


log = getLogger(__name__)


@dataclass
class Scheduler(Module):
    """Scheduler module."""

    persistent: bool = False
    options: Dict = None

    job_store_alias: str = 'default'
    job_store_type: str = None
    job_store_options: Dict = None

    defined_jobs: TypeSchedule = None

    __scheduler__: AsyncIOScheduler = None

    def get_job_defaults(self) -> Dict:
        """Get scheduler job defaults options."""

        job_options = {
            'coalesce': True,
            'misfire_grace_time': 120,
            'replace_existing': True
        }

        if self.options:
            job_options.update(self.options)

        return job_options

    async def prepare(self, scope):
        """Prepare scheduler."""

        self.__scheduler__ = AsyncIOScheduler(
            job_defaults=self.get_job_defaults(),
        )

        if self.persistent:
            self.__scheduler__.add_jobstore(
                alias=self.job_store_alias,
                jobstore=self.job_store_type,
                **self.job_store_options,
            )
        else:
            self.__scheduler__.add_jobstore(
                alias=self.job_store_alias,
                jobstore='memory',
            )

        if self.defined_jobs:
            for job in self.defined_jobs:
                self.__scheduler__.add_job(job[0], job[1], **job[2])

        self.__scheduler__.start()

    async def health(self, scope) -> bool:
        """Health."""
        try:
            log.warning('Scheduler', extra={'schedule': self.jobs})
        except Exception as any_exc:
            log.error(f'Scheduler {any_exc}')
            return False
        return True

    @property
    def jobs(self) -> Dict:
        """Current jobs."""
        with self.__scheduler__._jobstores_lock:  # noqa
            if self.suspend:
                return self.pending_jobs
            else:
                return self.active_jobs

    @property
    def scheduler(self) -> AsyncIOScheduler:
        """Get scheduler."""
        return self.__scheduler__

    @property
    def suspend(self) -> bool:
        """Scheduler suspend."""
        return  self.__scheduler__.state == STATE_STOPPED

    @property
    def active_jobs(self) -> Dict:
        """Active jobs."""
        jobs = []
        actives = {'jobs': jobs, 'status': 'active'}
        jobstores = dict(self.__scheduler__._jobstores)  # noqa
        for alias, store in sorted(jobstores.items()):
            active_jobs = store.get_all_jobs()
            if active_jobs:
                for job in active_jobs:
                    jobs.append({'job': job, 'alias': alias})
        return actives

    @property
    def pending_jobs(self) -> Dict:
        """Pending jobs."""
        jobs = []
        pending = {'jobs': jobs, 'status': 'pending'}
        pending_jobs = self.__scheduler__._pending_jobs  # noqa
        if self.suspend and pending_jobs:
            for job, _alias, _re in pending_jobs:
                jobs.append({'job': job, 'alias': _alias})
        return pending
