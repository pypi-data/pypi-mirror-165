from typing import Dict, Generator, Tuple

import treq
from twisted.internet import defer
from twisted.python import log


# https://${CI_HOST}${CI_HOOK}?p=https://${PHORGE_HOST}&t=${target.phid}&id=${build.id}&i=${initiator.phid}&c=${buildable.commit}&d=${buildable.diff}&r=${buildable.revision}&u=${repository.uri}&v=${repository.vcs}&ts=${step.timestamp}
class PhorgeController(object):
    """
    Helper class implementing a tiny subset of Phorge's API.
    """

    def __init__(self, host: str, credentials: str):
        self.host = host if host.startswith("https://") else f"https://{host}"
        self.credentials = credentials

    @defer.inlineCallbacks
    def _post(self, api: str, data: str = "") -> Generator:
        # THIS IS TERRIBLE
        d = "api.token={}&{}".format(self.credentials, data).encode("ascii")
        req = yield treq.post(
            self.host + "/api/" + api,
            data=d,
            headers={
                "Accept": "application/json",
                b"Content-Type": b"application/x-www-form-urlencoded",
            },
        )
        res = yield req.json()
        if res["error_code"]:
            log.msg("Phorge error", res)
            raise RuntimeError("Got a Phorge error")
        res = res["result"]
        defer.returnValue(res)

    @defer.inlineCallbacks
    def _searchOne(self, api: str, data: str = "") -> Generator:
        res = yield self._post(api, data)
        if not res.get("data", []):
            log.msg("Couldn't find ", api, data)
            raise RuntimeError("Couldn't find on Phorge")
        defer.returnValue(res["data"][0])

    def searchUser(self, phid: str) -> defer.Deferred:
        constraints = "constraints[phids][0]={}"
        return self._searchOne("user.search", constraints.format(phid))

    def searchBuild(self, build_id: str) -> defer.Deferred:
        constraints = "constraints[ids][0]={}"
        return self._searchOne(
            "harbormaster.build.search", constraints.format(build_id)
        )

    def searchBuildable(self, phid: str) -> defer.Deferred:
        constraints = "constraints[phids][0]={}"
        return self._searchOne(
            "harbormaster.buildable.search", constraints.format(phid)
        )

    def searchCommit(self, phid: str) -> defer.Deferred:
        constraints = "constraints[phids][0]={}"
        return self._searchOne("diffusion.commit.search", constraints.format(phid))

    @defer.inlineCallbacks
    def searchPhid(self, phid: str) -> Generator:
        constraints = "phids[0]={}"
        res = yield self._post("phid.query", constraints.format(phid))
        defer.returnValue(res[phid])

    @defer.inlineCallbacks
    def notifyBuild(self, phid: str, status: str) -> Generator:
        res = yield self._post(
            "harbormaster.sendmessage",
            "buildTargetPHID={}&type={}".format(phid, status),
        )
