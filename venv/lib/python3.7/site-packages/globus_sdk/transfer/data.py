"""
Data helper classes for constructing Transfer API documents. All classes should
extend ``dict``, so they can be passed seamlessly to
:class:`TransferClient <globus_sdk.TransferClient>` methods without
conversion.
"""
from __future__ import unicode_literals

import logging

from globus_sdk.base import safe_stringify

logger = logging.getLogger(__name__)


class TransferData(dict):
    r"""
    Convenience class for constructing a transfer document, to use as the
    `data` parameter to
    :meth:`submit_transfer <globus_sdk.TransferClient.submit_transfer>`.

    At least one item must be added using
    :meth:`add_item <globus_sdk.TransferData.add_item>`.

    If ``submission_id`` isn't passed, one will be fetched automatically. The
    submission ID can be pulled out of here to inspect, but the document
    can be used as-is multiple times over to retry a potential submission
    failure (so there shouldn't be any need to inspect it).

    **Parameters**

      ``transfer_client`` (:class:`TransferClient <globus_sdk.TransferClient>`)
        A ``TransferClient`` instance which will be used to get a submission ID
        if one is not supplied. Should be the same instance that is used to
        submit the transfer.

      ``source_endpoint`` (*string*)
        The endpoint ID of the source endpoint

      ``destination_endpoint`` (*string*)
        The endpoint ID of the destination endpoint

      ``label`` (*string*) [optional]
        A string label for the Task

      ``submission_id`` (*string*) [optional]
        A submission ID value fetched via
        :meth:`get_submission_id \
        <globus_sdk.TransferClient.get_submission_id>`. Defaults to using
        ``transfer_client.get_submission_id``

      ``sync_level`` (*int* or *string*) [optional]
        ``"exists"``, ``"size"``, ``"mtime"``, or ``"checksum"``
        For compatibility, this can also be ``0``, ``1``, ``2``, or ``3``

        The meanings are as follows:

        ``0``, ``exists``
          Determine whether or not to transfer based on file existence. If the
          destination file is absent, do the transfer.

        ``1``, ``size``
          Determine whether or not to transfer based on the size of the file. If
          destination file size does not match the source, do the transfer.

        ``2``, ``mtime``
          Determine whether or not to transfer based on modification times. If source
          has a newer modififed time than the destination, do the transfer.

        ``3``, ``checksum``
          Determine whether or not to transfer based on checksums of file contents. If
          source and destination contents differ, as determined by a checksum of their
          contents, do the transfer.

      ``verify_checksum`` (*bool*) [default: ``False``]
        When true, after transfer verify that the source and destination file
        checksums match. If they don't, re-transfer the entire file and keep
        trying until it succeeds.

        This will create CPU load on both the origin and destination of the transfer,
        and may even be a bottleneck if the network speed is high enough.

      ``preserve_timestamp`` (*bool*) [default: ``False``]
        When true, Globus Transfer will attempt to set file timestamps on the
        destination to match those on the origin.

      ``encrypt_data`` (*bool*) [default: ``False``]
        When true, all files will be TLS-protected during transfer.

      ``deadline`` (*string* or *datetime*) [optional]
        An ISO-8601 timestamp (as a string) or a datetime object which defines
        a deadline for the transfer. At the deadline, even if the data transfer
        is not complete, the job will be canceled.
        We recommend ensuring that the timestamp is in UTC to avoid confusion
        and ambiguity.

        Examples of ISO-8601 timestamps include ``2017-10-12 09:30Z``,
        ``2017-10-12 12:33:54+00:00``, and ``2017-10-12``

      ``recursive_symlinks`` (*string*) [default: ``"ignore"``]
        Specify the behavior of recursive directory transfers when encountering
        symlinks. One of ``"ignore"``, ``"keep"``, or ``"copy"``. ``"ignore"``
        skips symlinks, ``"keep"`` creates symlinks at the destination matching
        the source (without modifying the link path at all), and ``"copy"``
        follows symlinks on the source, failing if the link is invalid.

    Any additional parameters are fed into the dict being created verbatim.

    **Examples**

    See the
    :meth:`submit_transfer <globus_sdk.TransferClient.submit_transfer>`
    documentation for example usage.

    **External Documentation**

    See the
    `Task document definition \
    <https://docs.globus.org/api/transfer/task_submit/#document_types>`_
    and
    `Transfer specific fields \
    <https://docs.globus.org/api/transfer/task_submit/#transfer_specific_fields>`_
    in the REST documentation for more details on Transfer Task documents.
    """

    def __init__(
        self,
        transfer_client,
        source_endpoint,
        destination_endpoint,
        label=None,
        submission_id=None,
        sync_level=None,
        verify_checksum=False,
        preserve_timestamp=False,
        encrypt_data=False,
        deadline=None,
        recursive_symlinks="ignore",
        **kwargs
    ):
        source_endpoint = safe_stringify(source_endpoint)
        destination_endpoint = safe_stringify(destination_endpoint)
        logger.info("Creating a new TransferData object")
        self["DATA_TYPE"] = "transfer"
        self["submission_id"] = (
            submission_id or transfer_client.get_submission_id()["value"]
        )
        logger.info("TransferData.submission_id = {}".format(self["submission_id"]))
        self["source_endpoint"] = source_endpoint
        logger.info("TransferData.source_endpoint = {}".format(source_endpoint))
        self["destination_endpoint"] = destination_endpoint
        logger.info(
            "TransferData.destination_endpoint = {}".format(destination_endpoint)
        )
        self["verify_checksum"] = verify_checksum
        logger.info("TransferData.verify_checksum = {}".format(verify_checksum))
        self["preserve_timestamp"] = preserve_timestamp
        logger.info("TransferData.preserve_timestamp = {}".format(preserve_timestamp))
        self["encrypt_data"] = encrypt_data
        logger.info("TransferData.encrypt_data = {}".format(encrypt_data))
        self["recursive_symlinks"] = recursive_symlinks
        logger.info("TransferData.recursive_symlinks = {}".format(recursive_symlinks))

        if label is not None:
            self["label"] = label
            logger.debug("TransferData.label = {}".format(label))

        if deadline is not None:
            self["deadline"] = str(deadline)
            logger.debug("TransferData.deadline = {}".format(deadline))

        # map the sync_level (if it's a nice string) to one of the known int
        # values
        # you can get away with specifying an invalid sync level -- the API
        # will just reject you with an error. This is kind of important: if
        # more levels are added in the future this method doesn't become
        # garbage overnight
        if sync_level is not None:
            sync_dict = {"exists": 0, "size": 1, "mtime": 2, "checksum": 3}
            self["sync_level"] = sync_dict.get(sync_level, sync_level)
            logger.info(
                "TransferData.sync_level = {} ({})".format(
                    self["sync_level"], sync_level
                )
            )

        self["DATA"] = []

        self.update(kwargs)
        for option, value in kwargs.items():
            logger.info(
                "TransferData.{} = {} (option passed in via kwargs)".format(
                    option, value
                )
            )

    def add_item(self, source_path, destination_path, recursive=False, **params):
        """
        Add a file or directory to be transfered. If the item is a symlink
        to a file or directory, the file or directory at the target of
        the symlink will be transfered.

        Appends a transfer_item document to the DATA key of the transfer
        document.
        """
        source_path = safe_stringify(source_path)
        destination_path = safe_stringify(destination_path)
        item_data = {
            "DATA_TYPE": "transfer_item",
            "source_path": source_path,
            "destination_path": destination_path,
            "recursive": recursive,
        }
        item_data.update(params)

        logger.debug(
            'TransferData[{}, {}].add_item: "{}"->"{}"'.format(
                self["source_endpoint"],
                self["destination_endpoint"],
                source_path,
                destination_path,
            )
        )
        self["DATA"].append(item_data)

    def add_symlink_item(self, source_path, destination_path):
        """
        Add a symlink to be transfered as a symlink rather than as the
        target of the symlink.

        Appends a transfer_symlink_item document to the DATA key of the
        transfer document.
        """
        source_path = safe_stringify(source_path)
        destination_path = safe_stringify(destination_path)
        item_data = {
            "DATA_TYPE": "transfer_symlink_item",
            "source_path": source_path,
            "destination_path": destination_path,
        }
        logger.debug(
            'TransferData[{}, {}].add_symlink_item: "{}"->"{}"'.format(
                self["source_endpoint"],
                self["destination_endpoint"],
                source_path,
                destination_path,
            )
        )
        self["DATA"].append(item_data)


class DeleteData(dict):
    r"""
    Convenience class for constructing a delete document, to use as the
    `data` parameter to
    :meth:`submit_delete <globus_sdk.TransferClient.submit_delete>`.

    At least one item must be added using
    :meth:`add_item <globus_sdk.DeleteData.add_item>`.

    If ``submission_id`` isn't passed, one will be fetched automatically. The
    submission ID can be pulled out of here to inspect, but the document
    can be used as-is multiple times over to retry a potential submission
    failure (so there shouldn't be any need to inspect it).

    **Parameters**

      ``transfer_client`` (:class:`TransferClient <globus_sdk.TransferClient>`)
        A ``TransferClient`` instance which will be used to get a submission ID
        if one is not supplied. Should be the same instance that is used to
        submit the deletion.

      ``endpoint`` (*string*)
        The endpoint ID which is targeted by this deletion Task

      ``label`` (*string*) [optional]
        A string label for the Task

      ``submission_id`` (*string*) [optional]
        A submission ID value fetched via
        :meth:`get_submission_id \
        <globus_sdk.TransferClient.get_submission_id>`. Defaults to using
        ``transfer_client.get_submission_id``

      ``recursive`` (*bool*) [default: ``False``]
        Recursively delete subdirectories on the target endpoint

      ``deadline`` (*string* or *datetime*) [optional]
        An ISO-8601 timestamp (as a string) or a datetime object which defines
        a deadline for the transfer. At the deadline, even if the data deletion
        is not complete, the job will be canceled.
        We recommend ensuring that the timestamp is in UTC to avoid confusion
        and ambiguity.

        Examples of ISO-8601 timestamps include ``2017-10-12 09:30Z``,
        ``2017-10-12 12:33:54+00:00``, and ``2017-10-12``

    **Examples**

    See the :meth:`submit_delete <globus_sdk.TransferClient.submit_delete>`
    documentation for example usage.

    **External Documentation**

    See the
    `Task document definition \
    <https://docs.globus.org/api/transfer/task_submit/#document_types>`_
    and
    `Delete specific fields \
    <https://docs.globus.org/api/transfer/task_submit/#delete_specific_fields>`_
    in the REST documentation for more details on Delete Task documents.
    """

    def __init__(
        self,
        transfer_client,
        endpoint,
        label=None,
        submission_id=None,
        recursive=False,
        deadline=None,
        **kwargs
    ):
        endpoint = safe_stringify(endpoint)
        logger.info("Creating a new DeleteData object")
        self["DATA_TYPE"] = "delete"
        self["submission_id"] = (
            submission_id or transfer_client.get_submission_id()["value"]
        )
        logger.info("DeleteData.submission_id = {}".format(self["submission_id"]))
        self["endpoint"] = endpoint
        logger.info("DeleteData.endpoint = {}".format(endpoint))
        self["recursive"] = recursive
        logger.info("DeleteData.recursive = {}".format(recursive))

        if label is not None:
            self["label"] = label
            logger.debug("DeleteData.label = {}".format(label))

        if deadline is not None:
            self["deadline"] = str(deadline)
            logger.debug("DeleteData.deadline = {}".format(deadline))

        self["DATA"] = []

        self.update(kwargs)
        for option, value in kwargs.items():
            logger.info(
                "DeleteData.{} = {} (option passed in via kwargs)".format(option, value)
            )

    def add_item(self, path, **params):
        """
        Add a file or directory or symlink to be deleted. If any of the paths
        are directories, ``recursive`` must be set True on the top level
        ``DeleteData``. Symlinks will never be followed, only deleted.

        Appends a delete_item document to the DATA key of the delete
        document.
        """
        path = safe_stringify(path)
        item_data = {"DATA_TYPE": "delete_item", "path": path}
        item_data.update(params)
        logger.debug('DeleteData[{}].add_item: "{}"'.format(self["endpoint"], path))
        self["DATA"].append(item_data)
