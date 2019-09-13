import os

from globus_sdk.exc import GlobusSDKUsageError


def _on_windows():
    """
    Per python docs, this is a safe, reliable way of checking the platform.
    sys.platform offers more detail -- more than we want, in this case.
    """
    return os.name == "nt"


class LocalGlobusConnectPersonal(object):
    r"""
    A LocalGlobusConnectPersonal object represents the available SDK methods
    for inspecting and controlling a running Globus Connect Personal
    installation.

    These objects do *not* inherit from BaseClient and do not provide methods
    for interacting with any Globus Service APIs.
    """

    def __init__(self):
        self._endpoint_id = None

    @property
    def endpoint_id(self):
        """
        :type: string

        The endpoint ID of the local Globus Connect Personal endpoint
        installation.

        This value is loaded whenever it is first accessed, but saved after
        that.

        Usage:

        >>> from globus_sdk import TransferClient, LocalGlobusConnectPersonal
        >>> local_ep = LocalGlobusConnectPersonal()
        >>> ep_id = local_ep.endpoint_id
        >>> tc = TransferClient(...)  # needs auth details
        >>> for f in tc.operation_ls(ep_id):
        >>>     print("Local file: ", f["name"])

        You can also reset the value, causing it to load again on next access,
        with ``del local_ep.endpoint_id``
        """
        if self._endpoint_id is None:
            try:
                if _on_windows():
                    appdata = os.getenv("LOCALAPPDATA")
                    if appdata is None:
                        raise GlobusSDKUsageError(
                            "LOCALAPPDATA not detected in Windows environment"
                        )
                    fname = os.path.join(appdata, "Globus Connect\\client-id.txt")
                else:
                    fname = os.path.expanduser("~/.globusonline/lta/client-id.txt")
                with open(fname) as fp:
                    self._endpoint_id = fp.read().strip()
            except IOError as e:
                # no such file or directory
                if e.errno == 2:
                    pass
                else:
                    raise

        return self._endpoint_id

    @endpoint_id.deleter
    def endpoint_id(self):
        """
        Deleter for LocalGlobusConnectPersonal.endpoint_id
        """
        self._endpoint_id = None
