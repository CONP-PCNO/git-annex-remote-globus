import logging

from globus_sdk.authorizers.base import GlobusAuthorizer

logger = logging.getLogger(__name__)


class NullAuthorizer(GlobusAuthorizer):
    """
    This Authorizer implements No Authentication -- as in, it ensures that
    there is no Authorization header.
    """

    def set_authorization_header(self, header_dict):
        """
        Removes the Authorization header from the given header dict if one was
        present.
        """
        logger.debug("NullAuthorizer: ensuring there is no Authorization")
        header_dict.pop("Authorization", None)
