from typing import TYPE_CHECKING, Any, Dict, Generator, Iterable, List, Optional

import treq
from buildbot import config
from buildbot.process import results
from buildbot.reporters.base import ReporterBase
from buildbot.reporters.generators.build import BuildStatusGenerator
from buildbot.reporters.message import MessageFormatterFunction
from twisted.internet import defer
from twisted.python import log

from buildbot_phorge.utils import PhorgeController


class PhorgeReporter(ReporterBase):
    name = "PhorgeReporter"
    secrets = ["token"]
    neededDetails = dict(wantProperties=True)

    def checkConfig(
        self,
        token: str,
        host: str,
        generators: Optional[Iterable[BuildStatusGenerator]] = None,
        *args: Any,
        **kwargs: Any
    ) -> None:
        if generators is None:
            generators = self._create_default_generators()
        if not host:
            config.error("You must define Phorge host")
        if not token:
            config.error("You must define the conduit API token")
        super().checkConfig(generators=generators, *args, **kwargs)

    def _create_default_generators(self) -> List[BuildStatusGenerator]:
        formatter = MessageFormatterFunction(lambda context: context["build"], "json")
        return [BuildStatusGenerator(message_formatter=formatter, report_new=True)]

    @defer.inlineCallbacks
    def reconfigService(
        self,
        token: str,
        host: str,
        generators: Optional[Iterable[BuildStatusGenerator]] = None,
        *args: Any,
        **kwargs: Any
    ) -> Generator:
        self.token = yield self.renderSecrets(token)
        self.host = host

        if generators is None:
            generators = self._create_default_generators()
        yield super().reconfigService(generators=generators, *args, **kwargs)

    def buildStarted(self, key: str, build: str) -> None:
        pass

    def _matches_host(self, build: Dict[str, Any]) -> bool:
        o: bool = self.host == build.get("properties", dict()).get(
            "phorge_host", ("", "")
        )[0]
        return o

    def filterBuilds(self, build: Dict[str, Any]) -> bool:
        log.msg("Filtering build", build)
        o: bool = super().filterBuilds(build) and self._matches_host(build)
        return o

    @defer.inlineCallbacks
    def sendMessage(self, reports: Iterable[Any]) -> Generator:
        log.msg("Sending info build", reports)

        res = None
        for report in reports:
            for build in filter(
                lambda x: x.get("complete") and self._matches_host(x), report["builds"]
            ):
                phorge = PhorgeController(self.host, self.token)
                phid = build["properties"]["phorge_target_phid"][0]
                status = "pass" if build["results"] == results.SUCCESS else "fail"
                log.msg("Sending phid", status, phid)
                res = yield phorge.notifyBuild(phid, status)
        defer.returnValue(res)
