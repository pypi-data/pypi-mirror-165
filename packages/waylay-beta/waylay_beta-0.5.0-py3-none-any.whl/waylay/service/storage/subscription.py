"""REST definitions for the 'subscription' entity of the 'storage' service."""
from urllib.parse import quote

from waylay.service import WaylayResource
from waylay.service import decorators


BUCKET_NAME_ARG = {
    'name': 'bucket_name',
    'type': 'str',
    'description': 'Name of a Waylay storage bucket.',
    'examples': ['assets', 'public']
}
SUBSCRIPTION_ID_ARG = {
    'name': 'subscription_id',
    'type': 'str',
    'description': 'The identifier of a subscription.',
    'examples': ['my_notification_subscription_349']
}
ADDITIONAL_FILTER_PARAMS_ARG = {
    'name': 'params',
    'type': 'dict',
    'description': (
        "Additional parameters, like 'prefix', 'suffix', 'event_type', "
        "'channel_type', 'channel_id', that may filter subscriptions. "
        "See API documentation."
    )
}
SUBSCRIPTION_ENTITY_BODY = {
    'name': 'body',
    'type': 'dict',
    'description': 'A JSON representation of a subscription. See API documentation.'
}


class SubscriptionResource(WaylayResource):
    """REST Resource for the 'subscription' entity of the 'storage' service."""

    link_roots = {
        'doc': '${doc_url}/api/storage/?id=',
        'apidoc':  '${root_url}/docs#/subscription/',
        'openapi': '${root_url}/openapi.json'
    }
    actions = {
        'list': {
            'method': 'GET', 'url': '/subscription/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_path_decorator(['subscriptions']),
            ],
            'arguments': [BUCKET_NAME_ARG, ADDITIONAL_FILTER_PARAMS_ARG],
            'description': 'List available subscriptions for a given bucket.',
            'links': {
                'doc': 'list-bucket-subscriptions',
                'apidoc': 'query_subscriptions_subscription__bucket_name__get',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}')}/get"
            }
        },
        'get': {
            'method': 'GET', 'url': '/subscription/{}/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'arguments': [BUCKET_NAME_ARG, SUBSCRIPTION_ID_ARG],
            'description': 'Retrieve the representation of a notification subscription.',
            'links': {
                'doc': 'get-subscription',
                'apidoc': 'get_subscription_subscription__bucket_name___id__get',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}/{id}')}/get"
            }
        },
        'create': {
            'method': 'POST', 'url': '/subscription/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'arguments': [BUCKET_NAME_ARG, SUBSCRIPTION_ENTITY_BODY],
            'description': 'Create a new notification subscription.',
            'links': {
                'doc': 'create-subscription',
                'apidoc': 'post_subscription_subscription__bucket_name__post',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}/{id}')}/post"
            }
        },
        'replace': {
            'method': 'PUT', 'url': '/subscription/{}/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'arguments': [BUCKET_NAME_ARG, SUBSCRIPTION_ID_ARG, SUBSCRIPTION_ENTITY_BODY],
            'description': 'Create or Replace the definition of a notification subscription.',
            'links': {
                'doc': 'update-subscription',
                'apidoc': 'put_subscription_subscription__bucket_name___id__put',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}/{id}')}/put"
            }
        },
        'remove': {
            'method': 'DELETE', 'url': '/subscription/{}/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'arguments': [BUCKET_NAME_ARG, SUBSCRIPTION_ID_ARG],
            'description': 'Remove a notification subscription.',
            'links': {
                'doc': 'delete-subscription',
                'apidoc': 'delete_subscription_subscription__bucket_name___id__delete',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}/{id}')}/delete"
            }

        },
        'remove_all': {
            'method': 'DELETE', 'url': '/subscription/{}', 'decorators': [
                decorators.exception_decorator,
                decorators.return_body_decorator,
            ],
            'arguments': [BUCKET_NAME_ARG, ADDITIONAL_FILTER_PARAMS_ARG],
            'description': 'Remove all notification subscription that satisfy a query.',
            'links': {
                'doc': 'delete-subscriptions',
                'apidoc': 'delete_subscriptions_subscription__bucket_name__delete',
                'openapi': f"#/paths/{quote('/subscription/{bucket_name}')}/delete"
            }
        },
    }
