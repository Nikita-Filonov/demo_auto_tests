import uuid

from base.api.users.resource_libraries.resource_libraries import get_resource_libraries, get_resource_library, \
    create_resource_library, update_resource_library, delete_resource_library, get_resource_libraries_query
from base.api.users.resource_libraries.resource_libraries_checks import is_resource_library_created, \
    is_resource_library_updated, is_resource_library_deleted
from models.users.resource_libraries import ResourceLibrariesLTI13
from settings import LAB_APPLICATION_USER

resource_library_id = uuid.uuid4()
resource_library_payload = ResourceLibrariesLTI13

resource_library_methods = [
    {'method': get_resource_libraries, 'args': (), 'key': 'resource_libraries.get_resource_libraries'},
    {'method': get_resource_library, 'args': (resource_library_id,), 'key': 'resource_libraries.get_resource_library'},
    {'method': create_resource_library, 'args': (resource_library_payload,),
     'key': 'resource_libraries.create_resource_library'},
    {'method': update_resource_library, 'args': (resource_library_id, resource_library_payload),
     'key': 'resource_libraries.update_resource_library'},
    {'method': delete_resource_library, 'args': (resource_library_id,),
     'key': 'resource_libraries.delete_resource_library'},
    {'method': is_resource_library_created, 'args': (resource_library_id,),
     'key': 'resource_libraries.is_resource_library_created'},
    {'method': is_resource_library_updated, 'args': (resource_library_id,),
     'key': 'resource_libraries.is_resource_library_updated'},
    {'method': is_resource_library_deleted, 'args': (resource_library_id,),
     'key': 'resource_libraries.is_resource_library_deleted'},
    {'method': get_resource_libraries_query, 'args': ('?skip=0&take=10&requireTotalCount=true',),
     'key': 'resource_libraries.get_resource_libraries_query'}
]

RESOURCE_LIBRARIES_LIMIT = 5
RESOURCE_LIBRARIES_VIRTUAL_LAB = {
    "authUrl": "https://identity.alms.dev.alemira.com/",
    "url": f"https://lab.dev.alemira.com/api/labs/?limit={RESOURCE_LIBRARIES_LIMIT}&offset=0&public=True",
    "user": LAB_APPLICATION_USER['user'],
    "password": LAB_APPLICATION_USER['password'],
}
