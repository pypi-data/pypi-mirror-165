from typing import Any, Dict, Generator, List, Tuple
from uuid import uuid4

from buildbot.plugins import webhooks
from buildbot.process.properties import Properties
from twisted.internet import defer
from twisted.python import log
from twisted.web.iweb import IRequest

from buildbot_phorge.utils import PhorgeController


class PhorgeHook(webhooks.base):
    @defer.inlineCallbacks
    def getChanges(self, request: IRequest) -> Generator:
        # Check secret (Phorge uses HTTP Basic Auth)
        try:
            phorge_host = request.getUser().decode("utf-8")
            phorge_secret = request.getPassword().decode("utf-8")
        except:
            raise ValueError("Invalid Authentication")

        if not phorge_host or not phorge_secret:
            raise ValueError("Missing Authentication")
        p = Properties()
        p.master = self.master
        phorge_credentials: Tuple[str, str] = self.options.get(
            "credentials", dict()
        ).get(phorge_host, ("", ""))
        expected_secret_value = yield p.render(phorge_credentials[0])

        if phorge_secret != expected_secret_value:
            raise ValueError("Invalid Authentication")

        repository = request.args.get(b"u", [b""])[0].decode("utf-8")
        build_target_phid = request.args.get(b"t", [b""])[0].decode("utf-8")
        # ATM we need to know the repo from here
        # TODO: see if we can figure it out form the PHID
        assert repository, "No repository URL was passed"
        # We need to know the phorge host
        assert phorge_host, "Phorge Host parameter missing"
        phorge_build_id = request.args.get(b"id", [b""])[0].decode("utf-8")
        assert phorge_build_id, "Build ID parameter missing"
        assert build_target_phid, "Build Target PHID parameter is missing"

        # Get token + controller
        phorge_token = yield p.render(phorge_credentials[1])
        phorge = PhorgeController(phorge_host, phorge_token)

        # Get build data from Phorge
        build = yield phorge.searchBuild(phorge_build_id)
        build_phid = build["phid"]
        log.msg("GOTPHORGE", build_phid, build)

        # Get author
        # author_phid = build["fields"]["initiatorPHID"]
        # author = yield phorge.searchUser(author_phid)
        # author = author["fields"]["username"]
        # log.msg("GOTPHORGE", author)

        # Get Buildable data
        buildable_phid = build["fields"]["buildablePHID"]
        buildable = yield phorge.searchBuildable(buildable_phid)
        log.msg("GOTPHORGE", buildable)

        # Get change data
        change_phid = buildable["fields"]["objectPHID"]
        if not change_phid.startswith("PHID-CMIT-"):
            log.msg("PHID not supported yet", change_phid)
            raise NotImplementedError("No support for {} yet".format(change_phid))

        change_meta = yield phorge.searchPhid(change_phid)
        revlink = change_meta["uri"]
        revision_name = change_meta["fullName"]

        if change_phid.startswith("PHID-CMIT-"):
            revision = yield phorge.searchCommit(change_phid)
            comments = revision["fields"]["message"]
            author = revision["fields"]["author"]["raw"]
            committer = revision["fields"]["committer"]["raw"]
            revision = revision["fields"]["identifier"]

        when = float(
            build["fields"].get("dateModified", build["fields"]["dateCreated"])
        )

        # These fields are not supported yet.
        # Maybe they never will be.
        files: List[Any] = []
        branch = None
        category = None
        properties = {
            "phorge_uuid": str(uuid4()),
            "phorge_repository": repository,
            "phorge_host": phorge_host,
            "phorge_build_id": phorge_build_id,
            "phorge_target_phid": build_target_phid,
            # '_phorge_notified': False,
        }
        print("PROPS", properties)
        project = ""
        codebase = None
        chdict = dict(
            author=author,
            committer=committer,
            files=files,
            comments=comments,
            revision=revision,
            when_timestamp=when,
            branch=branch,
            category=category,
            revlink=revlink,
            properties=properties,
            repository=repository,
            project=project,
            codebase=codebase,
        )
        log.msg("CHANGE", chdict)

        defer.returnValue(([chdict], None))
