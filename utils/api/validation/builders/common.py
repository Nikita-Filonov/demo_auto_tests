from itertools import zip_longest
from typing import Dict, List

import allure
from api_manager import Entities
from models_manager import Field

from utils.api.validation.messages.property.entity_already_exists_property_validation_message import \
    EntityAlreadyExistsPropertyValidationMessage
from utils.api.validation.messages.property.property_is_null_validation_message import PropertyIsNullValidationMessage
from utils.api.validation.messages.property.referenced_entity_does_not_exist_property_validation_message import \
    ReferencedEntityDoesNotExistPropertyValidationMessage
from utils.api.validation.messages.property.string_property_too_long_validation_message import \
    StringPropertyTooLongValidationMessage
from utils.api.validation.validation_result import ValidationResult
from utils.utils import deep_get


def build_unique_validation_message(
        fields: List[Field],
        entity: Entities,
        entity_payload: dict,
        keys: List[List[str]] = None
) -> Dict[str, List[str]]:
    """Used to build unique validation messages"""
    with allure.step('Building "unique" validation messages'):
        validation_result = ValidationResult()

        for field, list_of_keys in zip_longest(fields, keys or []):
            value = deep_get(entity_payload, *list_of_keys) if list_of_keys else entity_payload[field.json]
            message = EntityAlreadyExistsPropertyValidationMessage(entity.value, field.json, value)
            validation_result.add_message(message)

    return validation_result.simplify()


def build_ref_does_not_exists_validation_message(
        property_name: str,
        entity: Entities,
        referenced_entity_name: Entities,
        referenced_entity_key: str,
        referenced_value: str
):
    """User to build referenced entity does not exist validation message"""
    with allure.step('Building "referenced entity does not exist" validation messages'):
        validation_result = ValidationResult()
        message = ReferencedEntityDoesNotExistPropertyValidationMessage(
            property_name,
            entity.value,
            referenced_entity_name.value,
            referenced_entity_key,
            referenced_value
        )
        validation_result.add_message(message)

    return validation_result.simplify()


def build_null_validation_message(fields: List[Field]) -> Dict[str, List[str]]:
    """Used to build null validation messages"""
    with allure.step('Building "null" validation messages'):
        validation_result = ValidationResult()

        for field in fields:
            message = PropertyIsNullValidationMessage(field.json)
            validation_result.add_message(message)

    return validation_result.simplify()


def build_max_length_validation_message(fields: List[Field]) -> Dict[str, List[str]]:
    """Used to build max length validation messages"""
    with allure.step('Building "max length" validation messages'):
        validation_result = ValidationResult()

        for field in fields:
            message = StringPropertyTooLongValidationMessage(property_name=field.json, limit=field.max_length)
            validation_result.add_message(message)

    return validation_result.simplify()
