from ehelply_bootstrapper.utils.state import State
from boto3.dynamodb.types import Binary
from boto3.dynamodb.conditions import Key
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from ehelply_bootstrapper.utils.cryptography import Encryption


class Attribute(BaseModel):
    key: str
    value: Any


class Dynamo:
    def __init__(
            self,
            table_name: str,
            p_keys: List[str],
            encrypted_dict_keys: List[str] = None,
            return_model=None,
            sub_table: Optional[str] = None,
            encryption: Encryption = None
    ) -> None:
        self.dynamodb = State.aws.make_resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)
        self.p_keys: List[str] = p_keys
        self.sub_table: Optional[str] = sub_table
        self.encrypted_keys: List[str] = encrypted_dict_keys
        if self.encrypted_keys is None:
            self.encrypted_keys = []
        self.encryption = encryption
        self.model = return_model

    def __clean_empty(self, d):
        if not isinstance(d, (dict, list)):
            return d
        if isinstance(d, list):
            return [v for v in (self.__clean_empty(v) for v in d) if v]
        return {k: v for k, v in ((k, self.__clean_empty(v)) for k, v in d.items()) if v}

    def __make_subtable_pkey_value(self, value: str) -> str:
        return f"{self.sub_table}-{value}" if self.sub_table else value

    def __make_subtable_pkey_values(self, pkey_values: List[str]) -> List[str]:
        subtable_pkeys: List[str] = []
        for pkey in pkey_values:
            subtable_pkeys.append(self.__make_subtable_pkey_value(pkey))
        return subtable_pkeys

    def __generate_keys(self, values: List[Any]) -> Dict[str, Any]:
        keys: Dict[str, Any] = {}
        for index, value in enumerate(values):
            keys[self.p_keys[index]] = self.__make_subtable_pkey_value(value)
        return keys

    def __generate_update_expression(self, attributes: List[Attribute]) -> str:
        update_expression: str = "SET "
        for attribute in attributes:
            update_expression += f"{attribute.key.lower()} = :{attribute.key.lower()}, "
        if len(attributes) > 0:
            update_expression = update_expression[0:-2]
        return update_expression

    def __generate_update_expression_values(self, attributes: List[Attribute]) -> dict:
        update_values: dict = {}
        for attribute in attributes:
            update_values[f":{attribute.key.lower()}"] = attribute.value
        return update_values

    def __encrypt_as_needed(self, attributes: List[Attribute] | dict):
        # Support encrypted keys / attributes
        if isinstance(attributes, dict):
            for key in self.encrypted_keys:
                if key in attributes:
                    attributes[key] = self.encryption.encrypt(attributes[key])
        else:
            for attribute in attributes:
                if attribute.key in self.encrypted_keys:
                    attribute.value = self.encryption.encrypt(attribute.value)

    def process_response(self, response):
        response_items = []
        for response_item in response['Items']:
            response_items.append(self.process_response_item(response_item))

        return response_items

    def process_response_item(self, response_item):
        # Support encrypted keys/attributes
        for key in self.encrypted_keys:
            if key in response_item and isinstance(response_item[key], Binary):
                response_item[key] = self.encryption.decrypt_dict(response_item[key].value)

        # Support subtables
        for pkey in self.p_keys:
            if pkey in response_item and isinstance(response_item[pkey], str):
                response_item[pkey] = response_item[pkey][len(self.sub_table) + 1:]

        if self.model:
            response_item = self.model(**response_item)

        return response_item

    def query(self, **query):
        response = self.table.query(**query)
        return self.process_response(response)

    def create_item(self, pkey_values: List[Any], attributes: dict):
        keys = self.__generate_keys(pkey_values)

        self.__encrypt_as_needed(attributes)

        self.table.put_item(
            Item={**attributes, **keys}
        )

    def get_item(self, pkey_values: List[Any]):
        keys = self.__generate_keys(pkey_values)

        response = self.table.get_item(
            Key=keys
        )

        return self.process_response_item(response['Item'])

    def get_items(self, pkey_values: List[Any]):
        expression = None
        for key_name, value in self.__generate_keys(pkey_values).items():
            key_expression = Key(key_name).eq(value)
            if not expression:
                expression = key_expression
            else:
                expression = expression & key_expression

        return self.query(
            KeyConditionExpression=expression
        )

    def delete_item(self, pkey_values: List[Any]):
        keys = self.__generate_keys(pkey_values)
        self.table.delete_item(
            Key=keys
        )

    def update_item(self, pkey_values: List[Any], attributes_to_update: List[Attribute]):
        keys = self.__generate_keys(pkey_values)

        self.__encrypt_as_needed(attributes_to_update)

        update_expression = self.__generate_update_expression(attributes_to_update)
        update_values = self.__generate_update_expression_values(attributes_to_update)

        self.table.update_item(
            Key=keys,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=update_values
        )

    def add_to_item_attribute(self, pkey_values: List[Any], attribute: Attribute):
        keys = self.__generate_keys(pkey_values)

        update_values = self.__generate_update_expression_values([attribute])

        self.table.update_item(
            Key=keys,
            UpdateExpression=f"SET {attribute.key.lower()} = {attribute.key.lower()} + :{attribute.key.lower()}",
            ExpressionAttributeValues=update_values
        )

    def subtract_from_item_attribute(self, pkey_values: List[Any], attribute: Attribute):
        keys = self.__generate_keys(pkey_values)

        update_values = self.__generate_update_expression_values([attribute])

        self.table.update_item(
            Key=keys,
            UpdateExpression=f"SET {attribute.key.lower()} = {attribute.key.lower()} - :{attribute.key.lower()}",
            ExpressionAttributeValues=update_values
        )

    def write_batch(self, messages: list):
        with self.table.batch_writer(overwrite_by_pkeys=self.p_keys) as batch:
            for message in messages:
                if isinstance(message, BaseModel):
                    message = message.dict()

                if not isinstance(message, dict):
                    raise Exception("Message is not of type dict")

                message = self.__clean_empty(message)

                # Support subtables
                for pkey in self.p_keys:
                    if pkey in message:
                        message[pkey] = self.__make_subtable_pkey_value(message[pkey])

                # Support encrypted keys / attributes
                for key in self.encrypted_keys:
                    if key in message:
                        message[key] = self.encryption.encrypt(message[key])

                try:
                    batch.put_item(Item=message)
                except:
                    pass

    def delete_batch(self, keys: list):
        with self.table.batch_writer(overwrite_by_pkeys=self.p_keys) as batch:
            for key in keys:
                if isinstance(key, BaseModel):
                    key = key.dict()

                if not isinstance(key, dict):
                    raise Exception("Message is not of type dict")

                key = self.__clean_empty(key)

                # Support subtables
                for pkey in self.p_keys:
                    if pkey in key:
                        key[pkey] = self.__make_subtable_pkey_value(key[pkey])

                # Support encrypted keys
                for ekey in self.encrypted_keys:
                    if ekey in key:
                        key[ekey] = self.encryption.encrypt(key[ekey])

                try:
                    batch.delete_item(Key=key)
                except:
                    pass
