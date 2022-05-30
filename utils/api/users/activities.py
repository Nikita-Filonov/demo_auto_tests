from http import HTTPStatus

from assertions import validate_json, assert_attr, assert_response_status
from requests import Response

from models.users.activity import Activities


def check_activity_response(activity_response: Response, activity_payload: dict, model: Activities):
    """
    :param model:
    :param activity_response: Activity response which should contains info about activity. For example
    json of such response might look like:
    {
        'id': 'c3f5320c-24b6-42ad-b21c-e0c7dfef6297',
        'type': 2,
        'ltiVersion': 3,
        'code': 'u6q7mR',
        'name': 'uJ3gIcHdl3j9LIxPv6klxgbG6HLWEy',
        'description': 'Description',
        'content': 'content',
        'toolUrl': 'https://host.docker.internal:5003/launch/bef4ce09-3d1d-441c-bad4-1f13b9dadc8f',
        'toolResourceId': '28004244-aec6-4b0a-bd9f-ecf23bc60cd6',
        'tenantId': '39e7fbd8-c4f3-456a-a744-dd43862ba8d3'
    }

    :param activity_payload: Dictionary with activity properties. You can get this payload from
    Activities model, ``Activities.manager.to_json``
    :return:

    Can be used to check activity response. Will check status code, schema, and all properties
    """
    activity_json_response = activity_response.json()

    assert_response_status(activity_response.status_code, HTTPStatus.OK)
    validate_json(activity_json_response, model.manager.to_schema)
    assert_attr(activity_json_response['name'], activity_payload['name'], model.name.json)
    assert_attr(activity_json_response['description'], activity_payload['description'], model.description.json)
    assert_attr(activity_json_response['type'], activity_payload['type'], model.type.json)
    assert_attr(activity_json_response['code'], activity_payload['code'], model.code.json)
    assert_attr(activity_json_response['tenantId'], activity_payload['tenantId'], model.tenant_id.json)
    assert_attr(activity_json_response['toolResourceId'], activity_payload['toolResourceId'],
                model.tool_resource_id.json)
