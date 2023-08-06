""" This module provides the object structures for entities in the weevils API, including methods to mutate
    or fetch related entities """

# modelled on github3.py
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, Dict, Iterable, Optional, Union
from urllib.parse import urljoin
from uuid import UUID

from requests import Response
from requests.exceptions import ConnectionError

from .exceptions import EntityNotFound, WeevilsAPIConnectionError, WeevilsAPIException

Data = Dict[str, Any]


class WeevilsCore(ABC):
    def __init__(self, data: Data, parent_obj: "WeevilsCore"):
        self._session = parent_obj._session
        self._base_url = parent_obj._base_url
        self._from_dict(data)
        self._data = data

    def _request(
        self, method: str, path: str, *handled_status: Iterable[int], query: Data = None, data: Data = None
    ) -> Response:

        url = urljoin(self._base_url, path.lstrip("/"))
        if handled_status is None:
            handled_status = ()

        try:
            resp = self._session.request(method, url, params=query, json=data)
        except ConnectionError as ex:
            raise WeevilsAPIConnectionError(self._base_url) from ex

        if resp.status_code not in handled_status:
            raise WeevilsAPIException(resp)
        return resp

    def _get(self, path: str, query: Data = None, *handled_status: Iterable[int]) -> Response:
        handled_status = (HTTPStatus.OK, HTTPStatus.NOT_FOUND) + (handled_status or ())
        resp = self._request("GET", path, *handled_status, query=query)
        if resp.status_code == HTTPStatus.NOT_FOUND:
            raise EntityNotFound
        return resp

    def _post(self, path: str, *handled_status: Iterable[int], data: Data = None) -> Response:
        handled_status = (HTTPStatus.OK, HTTPStatus.CREATED) + (handled_status or ())
        return self._request("POST", path, *handled_status, data=data)

    def _delete(self, path: str) -> Response:
        return self._request("DELETE", path, HTTPStatus.OK)

    def _make_obj(self, model_cls, data: Union[Data, Response]) -> "WeevilsCore":
        if isinstance(data, Response):
            data = data.json()
        if not isinstance(data, dict):
            raise ValueError(f"Can't handle data structure {data}")
        return model_cls(data, self)

    @abstractmethod
    def _from_dict(self, data: Data):
        raise NotImplementedError

    @property
    def raw(self) -> Data:
        return self._data


class GitHost(WeevilsCore):
    id: UUID
    name: str
    slug: str
    private: bool

    def _from_dict(self, data: Data):
        self.id = UUID(data["id"])
        self.name = data["name"]
        self.slug = data["slug"]
        self.private = data["private"]

    def repository(self, owner_name: str, name: str) -> "Repository":
        """
        Fetch a repository by the name of its owner and the repository name.

        Note: repositories can be renamed on a git host, so consider using the weevils.io ID
              instead via repository_by_id

        :param owner_name:
            The account name of the repository owner (user or organisation)
        :param name:
            The name of the repository itself
        :return:
            A Repository object model
        """
        if None in (owner_name, name):
            raise ValueError("owner_name and name cannot be None")
        return self._make_obj(Repository, self._get(f"hosts/{self.slug}/repos/{owner_name}/{name}/"))

    def repository_by_id(self, repository_id: UUID) -> "Repository":
        """
        Fetch a repository by its ID on weevils.io

        :param repository_id:
            The unique identifier of the repository on weevils
        :return:
            A Repository object model
        """
        if repository_id is None:
            raise ValueError("repository_id cannot be None")
        return self._make_obj(Repository, self._get(f"hosts/{self.slug}/repos/{repository_id}/"))


class Account(WeevilsCore):
    id: UUID
    name: str

    def _from_dict(self, data: Data):
        self.id = UUID(data["id"])
        self.name = data["name"]

    def list_repos(self) -> Iterable["Repository"]:
        raise NotImplementedError


class Repository(WeevilsCore):
    id: UUID
    owner: Account
    host: GitHost
    private: bool

    def _from_dict(self, data: Data):
        self.id = UUID(data["id"])
        self.owner = self._make_obj(Account, data["owner"])
        self.host = self._make_obj(GitHost, data["host"])
        self.private = data["private"]


class Job(WeevilsCore):
    id: UUID
    output: str
    status: Optional[str]
    repository: Repository

    def _from_dict(self, data: Data):
        self.id = UUID(data["id"])
        self.status = data["status"]
        self.output = data["output"]
        self.repository = self._make_obj(Repository, data["repository"])


class WeevilBase(WeevilsCore):
    id: UUID
    name: str
    slug: str

    def _from_dict(self, data: Data):
        self.id = UUID(data["id"])
        self.name = data["name"]
        self.slug = data["slug"]


class Weevil(WeevilsCore):
    id: UUID
    name: str
    slug: str
    script: str

    def _from_dict(self, data: Data):
        self.id = UUID(data["id"])
        self.name = data["name"]
        self.slug = data["slug"]
        self.script = data["script"]

    def run(self, repository: Union[UUID, Repository]) -> Job:
        if repository is None:
            raise ValueError("Repository cannot be None")

        repository_id = getattr(repository, "id", repository)
        return self._make_obj(Job, self._post(f"weevils/{self.id}/run/{repository_id}/"))

    def watch(self, repository_id: UUID):
        pass
