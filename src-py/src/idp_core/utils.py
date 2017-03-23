import datetime

from oidc_provider.models import Client as OIDCClient
from oidc_provider.lib.utils.token import create_token, create_id_token


def get_oidc_client(user, client_id=None):
    clients = OIDCClient.objects.filter(
        rpinfo__isnull=True
    ) | OIDCClient.objects.filter(
        rpinfo__user=user.business.parent_user
    )
    if client_id:
        return clients.get(client_id=client_id)
    return clients


def issue_jwt(user, customer):
    recent_token = create_token(
        user=user,
        client=customer,
        scope=["openid"]
    )
    id_token_dic = create_id_token(
        user=user,
        aud=customer.client_id,
        nonce=None,
        at_hash=recent_token.at_hash,
        request=None,
        scope=recent_token.scope,
    )
    id_token_dic.update(user.business.get_extra_data())
    recent_token.id_token = id_token_dic
    recent_token.expires_at = datetime.datetime.fromtimestamp(
        id_token_dic.get('exp')
    )
    recent_token.save()
    return recent_token
