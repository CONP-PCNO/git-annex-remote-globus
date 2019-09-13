import json

from globus_sdk.response import GlobusHTTPResponse


class TransferResponse(GlobusHTTPResponse):
    """
    Base class for :class:`TransferClient <globus_sdk.TransferClient>`
    responses.
    """

    def __str__(self):
        # Make printing responses more convenient. Relies on the
        # fact that Transfer API responses are always JSON.
        return json.dumps(self.data, indent=2)
