from __future__ import annotations

from gql import gql, Client as gqlClient
from gql.transport.aiohttp import AIOHTTPTransport

import json
import os
import warnings
from urllib import request, error as urlib_error

PROPERTIES_KEY = 'properties'


class Client:
    """
    The client can be used to create entities, events and to generate recommendations.
    """
    def __init__(self, url: str = None, api_key: str = None, stage: str = "dev"):
        url = url or os.getenv('TEAREX_URL') or 'https://api.tearex.ai/graphql'

        headers = {'x-api-key': os.getenv('TEAREX_API_KEY') or ''}

        transport = AIOHTTPTransport(url=url, headers=headers)
        self.client = gqlClient(transport=transport, fetch_schema_from_transport=True)

        self.stage = stage

    async def create_entity(self, entity: dict) -> dict:
        """
        Create an entity
        :param entity: dict with properties:
            - id: id from your database
            - label: label of the entity e.g. "Person" or "Product"
            - properties: dict with properties of the entity
        :return: created entity
        """
        query = gql(
            """
            mutation createEntity($entity: EntityInput, $stage: String) {
              createEntity(entity: $entity, stage: $stage) {
                id
                label
                properties
              }
            }  
            """)

        params = {
            "entity": self._stringify_properties(entity),
            "stage": self.stage
        }

        result = (await self.client.execute_async(query, variable_values=params))
        result = result['createEntity']

        result[PROPERTIES_KEY] = json.loads(result[PROPERTIES_KEY])

        return result

    async def delete_entity(self, entity):
        query = gql(
            """
            mutation deleteEntity($entity: EntityInput, $stage: String) {
              deleteEntity(entity: $entity, stage: $stage) {
                id,
                properties
              }
            }
            """)

        params = {
            "entity": self._stringify_properties(entity),
            "stage": self.stage
        }

        result = (await self.client.execute_async(query, variable_values=params))
        result = result['deleteEntity']

        return result

    async def batch_create_entities(self, entities: list) -> list:
        """
        Create a batch of entities
        """
        query = gql(
            """
            mutation batchCreateEntities($entities: [EntityInput], $stage: String) {
              batchCreateEntities(entities: $entities, stage: $stage) {
                id
                label
                properties
              }
            }  
            """)

        params = {
            "entities": [self._stringify_properties(entity) for entity in entities],
            "stage": self.stage
        }

        results = (await self.client.execute_async(query, variable_values=params))
        results = results['batchCreateEntities']

        for result in results:
            result[PROPERTIES_KEY] = json.loads(result[PROPERTIES_KEY])

        return results

    async def create_event(self, in_entity: dict, event: dict | str, out_entity: dict) -> dict:
        """
        Create an event
        :param in_entity: entity that is the source of the event
        :param event: event dict
            - weight: weight of the event
            - label: label of the event e.g. "Buy" or "Sell"
            - properties: dict with properties of the event
            - directed: boolean
            - decay: Decay object with decay parameters: type and rate
            or string. If string it is treated as the label.
        :param out_entity: entity that is the target of the event
        :return: created event
        """
        query = gql(
            """
            mutation createEvent($inEntity: EntityInput, $event: EventInput, $outEntity: EntityInput, $stage: String) {
              createEvent(inEntity: $inEntity, event: $event, outEntity: $outEntity, stage: $stage) {
                label
              }
            }
            """)

        event = self._stringify_properties(event) if isinstance(event, dict) else dict(label=event)

        params = {
            "inEntity": self._stringify_properties(in_entity),
            "event": event,
            "outEntity": self._stringify_properties(out_entity),
            "stage": self.stage
        }

        result = (await self.client.execute_async(query, variable_values=params))
        result = result['createEvent']

        return result

    async def batch_create_events(self, events: list) -> list:
        """
        Create a batch of events and embed them in a batch
        """
        query = gql(
            """
            mutation batchCreateEvents($events: [BatchEventInput], $stage: String) {
              batchCreateEvents(events: $events, stage: $stage) {
                label
              }
            }  
            """)

        params = {
            "events": [dict(
                inEntity=self._stringify_properties(event[0]),
                event=self._stringify_properties(event[1]) if isinstance(event[1], dict) else dict(label=event[1]),
                outEntity=self._stringify_properties(event[2])
            ) for event in events],
            "stage": self.stage
        }

        results = (await self.client.execute_async(query, variable_values=params))
        results = results['batchCreateEvents']

        return results

    async def delete_event(self, in_entity: dict, event: dict | str, out_entity: dict) -> dict:
        """
        Delete an event
        :param in_entity: entity that is the source of the event
        :param event: event dict
            - weight: weight of the event
            - label: label of the event e.g. "Buy" or "Sell"
            - properties: dict with properties of the event
            - directed: boolean
            - decay: Decay object with decay parameters: type and rate
            or string. If string it is treated as the label.
        :param out_entity: entity that is the target of the event
        :return: created event
        """
        query = gql(
            """
            mutation deleteEvent($inEntity: EntityInput, $event: EventInput, $outEntity: EntityInput, $stage: String) {
              deleteEvent(inEntity: $inEntity, event: $event, outEntity: $outEntity, stage: $stage) {
                label
              }
            }
            """)

        event = self._stringify_properties(event) if isinstance(event, dict) else dict(label=event)

        params = {
            "inEntity": self._stringify_properties(in_entity),
            "event": event,
            "outEntity": self._stringify_properties(out_entity),
            "stage": self.stage
        }

        result = (await self.client.execute_async(query, variable_values=params))
        result = result['deleteEvent']

        return result

    async def recommend(self, entity, label, limit=10, query=None):
        """
        Find similar entities to the given entity
        :param entity: entity for which similar entities are to be found
        :param label: label of the entity that is to be found e.g. "Person" or "Product"
        :param limit: number of similar entities to be found
        :param query: query to be used for finding similar entities
        :return: list of similar entities with scores
        """
        gqlquery = gql(
            """
            query getSimilar($entity: EntityInput, $target: String $filter: FilterInput, $stage: String) {
              similar(entity: $entity, target: $target, filter: $filter, stage: $stage) {
                entity {
                    id
                    label
                    properties
                }
                score
              }
            }
            """)

        params = {
            "entity": self._stringify_properties(entity),
            "target": label,
            "filter": {
                "limit": limit,
                "query": query
            },
            "stage": self.stage
        }

        result = (await self.client.execute_async(gqlquery, variable_values=params))
        result = result['similar']

        return self._parse_response(result)

    @staticmethod
    def _stringify_properties(obj: dict) -> dict:
        """
        Parse properties of an entity or event
        :param obj: dict with key "properties"
        :return: dict with properties as string
        """
        obj_param = {
            **obj,
        }

        if PROPERTIES_KEY in obj:
            obj_param[PROPERTIES_KEY] = json.dumps(obj[PROPERTIES_KEY])

        return obj_param

    @staticmethod
    def _parse_response(response, key="entity") -> list[dict]:
        """
        Parse response from graphql query to have the properties as dict
        :param response:
        :param key:
        :return: list of dicts with properties as dict
        """
        for i in range(len(response)):
            r = response[i][key]

            if PROPERTIES_KEY in r:
                response[i][key] = {
                    **r,
                    PROPERTIES_KEY: json.loads(r[PROPERTIES_KEY])
                }

        return response
