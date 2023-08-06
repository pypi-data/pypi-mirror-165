# This file is generated from the openapi spec
import json
from dataclasses import dataclass, asdict
from typing import cast, List, Dict, Optional, Union
import requests

from .helpers import to_value


@dataclass
class Foo:
    hello: str
    api_version: int


@dataclass
class ApiResult:
    message: str


@dataclass
class ApiError:
    message: str


@dataclass
class Policy:
    filename: Optional[str]
    src: str


@dataclass
class GetPolicyResult:
    policy: Optional[Policy]


@dataclass
class Value:
    type: Optional[str]
    id: Optional[str]


@dataclass
class Fact:
    predicate: str
    args: List[Value]


@dataclass
class Role:
    actor_type: str
    actor_id: str
    role: str
    resource_type: str
    resource_id: str


@dataclass
class Relation:
    from_type: str
    from_id: str
    relation: str
    to_type: str
    to_id: str


@dataclass
class AuthorizeResult:
    allowed: bool


@dataclass
class AuthorizeQuery:
    actor_type: str
    actor_id: str
    action: str
    resource_type: str
    resource_id: str
    context_facts: List[Fact]
    explain: bool


@dataclass
class AuthorizeResourcesResult:
    results: List[Value]


@dataclass
class AuthorizeResourcesQuery:
    actor_type: str
    actor_id: str
    action: str
    resources: List[Value]
    context_facts: List[Fact]


@dataclass
class ListResult:
    results: List[str]


@dataclass
class ListQuery:
    actor_type: str
    actor_id: str
    action: str
    resource_type: str
    context_facts: List[Fact]


@dataclass
class ActionsResult:
    results: List[str]


@dataclass
class ActionsQuery:
    actor_type: str
    actor_id: str
    resource_type: str
    resource_id: str
    context_facts: List[Fact]


@dataclass
class StatsResult:
    num_roles: int
    num_relations: int
    num_facts: int
    recent_authorizations: int


@dataclass
class Query:
    fact: Fact
    context_facts: List[Fact]


@dataclass
class QueryResult:
    results: List[Fact]


class API:
    def __init__(self, url="https://cloud.osohq.com", api_key=None):
        self.url = url
        self.api_base = "api"
        if api_key:
            self.token = api_key
        else:
            raise ValueError("Must set an api_key")

    def _handle_result(self, result):
        if not result.ok:
            code, text = result.status_code, result.text
            msg = f"Got unexpected error from Oso Service: {code}\n{text}"
            raise Exception(msg)
        try:
            return result.json()
        except json.decoder.JSONDecodeError:
            return result.text

    def _default_headers(self):
        return {
            "Authorization": f"Basic {self.token}",
            "User-Agent": "Oso Cloud (python)",
            "X-OsoApiVersion": "0",
        }

    def _do_post(self, url, params, json):
        return requests.post(
            url, params=params, json=json, headers=self._default_headers()
        )

    def _do_get(self, url, params, json):
        return requests.get(
            url, params=params, json=json, headers=self._default_headers()
        )

    def _do_delete(self, url, params, json):
        return requests.delete(
            url, params=params, json=json, headers=self._default_headers()
        )

    def hello(self):
        params = None
        json = None
        result = self._do_get(f"{self.url}/{self.api_base}/", params=params, json=json)
        response = self._handle_result(result)
        return Foo(**response)

    def get_policy(self):
        params = None
        json = None
        result = self._do_get(
            f"{self.url}/{self.api_base}/policy", params=params, json=json
        )
        response = self._handle_result(result)
        return GetPolicyResult(**response)

    def post_policy(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/policy", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    # NOTE: the args stuff here doesn not show up in the openapi spec
    # so we don't codegen this correctly
    def get_facts(self, predicate, *args):
        params = {}
        params["predicate"] = predicate
        for i, arg in enumerate(args):
            if arg.type is not None:
                params[f"args.{i}.type"] = arg.type
            if arg.id is not None:
                params[f"args.{i}.id"] = arg.id
        json = None
        result = self._do_get(
            f"{self.url}/{self.api_base}/facts", params=params, json=json
        )
        response = self._handle_result(result)
        result = []
        for item in response:
            result.append(Fact(**item))
        return result

    def post_facts(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/facts", params=params, json=json
        )
        response = self._handle_result(result)
        return Fact(**response)

    def delete_facts(self, data):
        params = None
        json = asdict(data)
        result = self._do_delete(
            f"{self.url}/{self.api_base}/facts", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def get_inspect(self, tag, id):
        params = {}
        params["tag"] = tag
        params["id"] = id
        json = None
        result = self._do_get(
            f"{self.url}/{self.api_base}/inspect", params=params, json=json
        )
        response = self._handle_result(result)
        result = []
        for item in response:
            result.append(Fact(**item))
        return result

    def get_roles(self, actor_type, actor_id, role, resource_type, resource_id):
        params = {}
        params["actor_type"] = actor_type
        params["actor_id"] = actor_id
        params["role"] = role
        params["resource_type"] = resource_type
        params["resource_id"] = resource_id
        json = None
        result = self._do_get(
            f"{self.url}/{self.api_base}/roles", params=params, json=json
        )
        response = self._handle_result(result)
        result = []
        for item in response:
            result.append(Role(**item))
        return result

    def post_roles(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/roles", params=params, json=json
        )
        response = self._handle_result(result)
        return Role(**response)

    def delete_roles(self, data):
        params = None
        json = asdict(data)
        result = self._do_delete(
            f"{self.url}/{self.api_base}/roles", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def get_relations(self, object_type, object_id, relation):
        params = {}
        params["object_type"] = object_type
        params["object_id"] = object_id
        params["relation"] = relation
        json = None
        result = self._do_get(
            f"{self.url}/{self.api_base}/relations", params=params, json=json
        )
        response = self._handle_result(result)
        result = []
        for item in response:
            result.append(Relation(**item))
        return result

    def post_relations(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/relations", params=params, json=json
        )
        response = self._handle_result(result)
        return Relation(**response)

    def delete_relations(self, data):
        params = None
        json = asdict(data)
        result = self._do_delete(
            f"{self.url}/{self.api_base}/relations", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def post_bulk_load(self, data):
        params = None
        json = list(map(asdict, data))
        result = self._do_post(
            f"{self.url}/{self.api_base}/bulk_load", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def post_bulk_delete(self, data):
        params = None
        json = list(map(asdict, data))
        result = self._do_post(
            f"{self.url}/{self.api_base}/bulk_delete", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def post_authorize(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/authorize", params=params, json=json
        )
        response = self._handle_result(result)
        return AuthorizeResult(**response)

    def post_authorize_resources(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/authorize_resources", params=params, json=json
        )
        response = self._handle_result(result)
        return AuthorizeResourcesResult(**response)

    def post_list(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/list", params=params, json=json
        )
        response = self._handle_result(result)
        return ListResult(**response)

    def post_actions(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/actions", params=params, json=json
        )
        response = self._handle_result(result)
        return ActionsResult(**response)

    def post_query(self, data):
        params = None
        json = asdict(data)
        result = self._do_post(
            f"{self.url}/{self.api_base}/query", params=params, json=json
        )
        response = self._handle_result(result)
        return QueryResult(
            [
                Fact(fact["predicate"], [Value(**arg) for arg in fact["args"]])
                for fact in response["results"]
            ]
        )

    def get_stats(self):
        params = None
        json = None
        result = self._do_get(
            f"{self.url}/{self.api_base}/stats", params=params, json=json
        )
        response = self._handle_result(result)
        return StatsResult(**response)

    def clear_data(self):
        params = None
        json = None
        result = self._do_post(
            f"{self.url}/{self.api_base}/clear_data", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def list_backups(self):
        params = None
        json = None
        result = self._do_get(
            f"{self.url}/{self.api_base}/backups", params=params, json=json
        )
        response = self._handle_result(result)
        result = []
        for item in response:
            result.append(ApiResult(**item))
        return result

    def create_backup(self):
        params = None
        json = None
        result = self._do_post(
            f"{self.url}/{self.api_base}/backups", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def delete_backup(self, backup_key):
        params = None
        json = None
        result = self._do_delete(
            f"{self.url}/{self.api_base}/backups/{backup_key}", params=params, json=json
        )
        response = self._handle_result(result)
        return ApiResult(**response)

    def restore_from_backup(self, backup_key):
        params = None
        json = None
        result = self._do_post(
            f"{self.url}/{self.api_base}/backups/{backup_key}/restore",
            params=params,
            json=json,
        )
        response = self._handle_result(result)
        return ApiResult(**response)
