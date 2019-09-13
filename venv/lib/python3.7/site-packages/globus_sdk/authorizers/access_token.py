import logging

from globus_sdk.authorizers.base import GlobusAuthorizer
from globus_sdk.utils.string_hashing import sha256_string

logger = logging.getLogger(__name__)


class AccessTokenAuthorizer(GlobusAuthorizer):
    """
    Implements Authorization using a single Access Token with no Refresh
    Tokens. This is sent as a Bearer token in the header -- basically
    unadorned.

    **Parameters**

        ``access_token`` (*string*)
          An access token for Globus Auth
    """

    def __init__(self, access_token):
        logger.info(
            (
                "Setting up an AccessTokenAuthorizer. It will use an "
                "auth type of Bearer and cannot handle 401s."
            )
        )
        self.access_token = access_token
        self.header_val = "Bearer %s" % access_token

        self.access_token_hash = sha256_string(self.access_token)
        logger.debug('Bearer token has hash "{}"'.format(self.access_token_hash))

    def set_authorization_header(self, header_dict):
        """
        Sets the ``Authorization`` header to
        "Bearer <access_token>"
        """
        logger.debug(
            (
                "Setting AccessToken Authorization Header: "
                '"Bearer token has hash "{}"'
            ).format(self.access_token_hash)
        )
        header_dict["Authorization"] = self.header_val
