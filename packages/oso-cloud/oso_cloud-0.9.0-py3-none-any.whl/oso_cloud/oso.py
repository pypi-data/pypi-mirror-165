import json
from typing import cast, Dict, Optional
from dataclasses import asdict

from . import api
from .helpers import (
    to_value,
    from_value,
    map_facts_to_params,
    map_params_to_facts,
)


class Oso:
    def __init__(self, url="https://cloud.osohq.com", api_key=None):
        self.api = api.API(url, api_key)

    def authorize(self, actor, action, resource, context_facts=[]):
        actor_typed_id = to_value(actor)
        resource_typed_id = to_value(resource)
        data = api.AuthorizeQuery(
            actor_typed_id.type,
            actor_typed_id.id,
            action,
            resource_typed_id.type,
            resource_typed_id.id,
            map_params_to_facts(context_facts),
            False,
        )
        result = self.api.post_authorize(data)
        return result.allowed

    def authorize_resources(self, actor, action, resources, context_facts=[]):
        def key(e) -> str:
            if isinstance(e, dict):
                e = to_value(e)
            return f"{e.type}:{e.id}"

        if not resources or len(resources) == 0:
            return []

        resources_extracted = [to_value(r) for r in resources]
        actor_typed_id = to_value(actor)
        data = api.AuthorizeResourcesQuery(
            actor_typed_id.type,
            actor_typed_id.id,
            action,
            resources_extracted,
            map_params_to_facts(context_facts),
        )
        result = self.api.post_authorize_resources(data)
        if len(result.results) == 0:
            return []

        results_lookup = {}
        for r in result.results:
            k = key(r)
            if not results_lookup.get(k, None):
                results_lookup[k] = True

        return list(
            filter(
                lambda r: results_lookup.get(key(to_value(r)), None),
                resources,
            )
        )

    def list(self, actor, action, resource_type, context_facts=[]):
        actor_typed_id = to_value(actor)
        data = api.ListQuery(
            actor_typed_id.type,
            actor_typed_id.id,
            action,
            resource_type,
            map_params_to_facts(context_facts),
        )
        result = self.api.post_list(data)
        return result.results

    def actions(self, actor, resource, context_facts=[]):
        actor_typed_id = to_value(actor)
        resource_typed_id = to_value(resource)
        data = api.ActionsQuery(
            actor_typed_id.type,
            actor_typed_id.id,
            resource_typed_id.type,
            resource_typed_id.id,
            map_params_to_facts(context_facts),
        )
        result = self.api.post_actions(data)
        return result.results

    def tell(self, predicate, *args):
        args = list(map(to_value, args))
        fact = api.Fact(predicate, args)
        result = self.api.post_facts(fact)
        return result

    def bulk_tell(self, facts):
        result = self.api.post_bulk_load(map_params_to_facts(facts))
        return result

    def delete(self, predicate, *args):
        args = list(map(to_value, args))
        fact = api.Fact(predicate, args)
        result = self.api.delete_facts(fact)
        return result

    def bulk_delete(self, facts):
        result = self.api.post_bulk_delete(map_params_to_facts(facts))
        return result

    # NOTE: the args stuff here doesn not show up in the openapi spec
    # so we don't codegen this correctly
    def get(self, predicate=None, *args):
        args = [to_value(a) for a in args]
        result = self.api.get_facts(predicate, *args)
        return map_facts_to_params(result)

    def policy(self, policy):
        policy = api.Policy("", policy)
        return self.api.post_policy(policy)

    def query(self, predicate, *args):
        args = [to_value(a) for a in args]
        result = self.api.post_query(api.Query(api.Fact(predicate, args), []))
        return map_facts_to_params(result.results)
