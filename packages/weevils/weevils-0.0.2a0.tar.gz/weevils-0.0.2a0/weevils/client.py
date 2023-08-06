import sys
from http import HTTPStatus
from typing import List, Union
from uuid import UUID

import pkg_resources
from requests.sessions import Session

from .exceptions import EntityConflict, EntityNotFound, WeevilsAPIException
from .models import GitHost, Job, Weevil, WeevilBase, WeevilsCore

VERSION = pkg_resources.get_distribution("weevils").version

_python_version = ".".join(str(v) for v in sys.version_info[:2])
DEFAULT_USER_AGENT = f"Weevils Client v{VERSION} ({_python_version})"

WEEVILS_API = "https://api.weevils.io"
WEEVILS_SANDBOX_API = "https://api.sandbox.weevils.io"


class WeevilsClient(WeevilsCore):
    def __init__(
        self, token: str, *, api_url: str = WEEVILS_API, user_agent: str = DEFAULT_USER_AGENT, session: Session = None
    ):
        """
        Required parameters:

        :param token:
            The API token made at https://weevils.io/tokens to access the API

        Optional parameters:

        :param api_url:
            The base API URL. The default is for live weevils.io, but you can switch this to the sandbox URL
            for testing and development
        :param user_agent:
            Override the default user agent to send in requests
        :param session:
            Use this to override the default requests Session object
        """
        self._token = token

        api_url = api_url or self.api_url
        if not api_url.endswith("/"):
            api_url = f"{api_url}/"
        self._base_url = api_url

        self._session = session or Session()

        # set default headers including auth
        self._session.headers.update(
            {
                "User-Agent": user_agent,
                "Authorization": f"Token {self._token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        # memoised shortcuts; will be loaded if needed
        self._github: GitHost = None
        self._bitbucket: GitHost = None

    def _from_dict(self, _):
        # nothing to implement here, just required for ABC compliance
        pass

    # ---
    # Host methods
    # ---

    def list_hosts(self) -> List[GitHost]:
        """
        List all hosts available to the Weevils user account - both publicly available hosts
        and any privately configured hosts

        :return:
            A list of all hosts with which the current Weevils account can interact
        """
        return [self._make_obj(GitHost, host_data) for host_data in self._get("hosts/").json()]

    def get_host(self, slug_or_pk: Union[str, UUID]) -> GitHost:
        if not slug_or_pk:
            raise ValueError("Must specify a host ID or slug")
        try:
            return self._make_obj(GitHost, self._get(f"hosts/{slug_or_pk}/"))
        except WeevilsAPIException as ex:
            if ex.status_code == HTTPStatus.NOT_FOUND:
                raise EntityNotFound("host", slug_or_pk)
            raise

    # shortcuts:

    @property
    def github(self) -> GitHost:
        if self._github is None:
            self._github = self.get_host("github")
        return self._github

    @property
    def bitbucket(self) -> GitHost:
        if self._bitbucket is None:
            self._bitbucket = self.get_host("bitbucket")
        return self._bitbucket

    # ---
    # Weevil methods
    # ---

    def create_weevil(self, name: str, base: Union[UUID, WeevilBase], script: str, *, slug: str = None) -> Weevil:
        base_id = base if isinstance(base, UUID) else base.id
        data = {"name": name, "base_id": str(base_id), "script": script}
        if slug:
            # TODO: some validation here to reject bad slugs before the server has to
            data["slug"] = slug

        resp = self._post("weevils/", HTTPStatus.CONFLICT, data=data)
        if resp.status_code == HTTPStatus.CONFLICT:
            raise EntityConflict(resp.json()["error"])

        return self._make_obj(Weevil, resp.json())

    def update_weevil(self, weevil: Union[UUID, Weevil], script: str) -> Weevil:
        weevil_id = weevil if isinstance(weevil, UUID) else weevil.id
        resp = self._post(f"weevils/{weevil_id}/", data={"script": script})
        return self._make_obj(Weevil, resp.json())

    def list_bases(self) -> WeevilBase:
        resp = self._get("weevils/bases")
        return [self._make_obj(WeevilBase, base) for base in resp.json()]

    def get_weevil(self, weevil_id: UUID) -> Weevil:
        return self._make_obj(Weevil, self._get(f"weevils/{weevil_id}/"))

    def list_weevils(self) -> List[Weevil]:
        resp = self._get("weevils/")
        return [self._make_obj(Weevil, weev) for weev in resp.json()]

    # ---
    # Job methods
    # ---

    def get_job(self, job_id: UUID) -> Job:
        return self._make_obj(Job, self._get(f"jobs/{job_id}/"))


class WeevilsSandboxClient(WeevilsClient):
    """
    This is a convenient shortcut class to get a client pointing at the Weevils sandbox
    API.

    Note: Using the `from_env` class and setting environment variables is a better method
    for easily switching using environment variables rather than needing to have logic in
    the code to choose a client class
    """

    def __init__(self, token: str, *, user_agent: str = None, session: Session = None):
        super().__init__(token, api_url=WEEVILS_SANDBOX_API, session=session, user_agent=user_agent)
