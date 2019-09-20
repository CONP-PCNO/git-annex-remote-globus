#!/usr/bin/env python
# git-annex external special remote program for Globus data repository
# 
# This is an addition to git-annex's built-in directory special remotes.
# 
# Install in PATH as git-annex-remote-directory
#
# TODO: Add Copyright

import sys, os, errno

from shutil import copyfile
import globus_sdk
from globusclient import GlobusClient
from annexremote import Master
from annexremote import ExportRemote
from annexremote import SpecialRemote
from annexremote import RemoteError, ProtocolError


class GlobusRemote(SpecialRemote):

    """This is the class of Globus remotes."""

    client_id = '01589ab6-70d1-4e1c-b33d-14b6af4a16be'

    def __init__(self, annex):
        super(GlobusRemote, self).__init__(annex)
        self.directory = ''
        self.refresh_token = None
        self.access_token = None
        self.expire_at_s = None
        self.auth_token = None
        self.transfer_token = None
        self.globus_client = GlobusClient(self.client_id)
        self._setup()

    def _setup(self):
        self.refresh_token, self.access_token, self.expire_at_s = self.globus_client.get_refresh_tokens()
        # self.auth_token, self.transfer_token = self.globus_client.get_transfer_tokens()

    def initremote(self):

        # TODO need to think on how to make this call relevant and indempotent to users.
        #  Think of scenarios of many users and many sessions. Do they need different tokens?

        """Requests the remote to initialize itself. Idempotent call"""

        # for now we assume to work with refresh tokens, so when instantiated they should last
        if not self.auth_token and not self.transfer_token:
            self._setup()

    def prepare(self):
        # self.auth_token, self.transfer_token = globus_client.get_transfer_tokens()
        # print(self.auth_token, self.transfer_token)
        print(self.refresh_token, self.access_token, self.expire_at_s)
        # this should open a session with Globus. Tokens get generated and we make sure they do not expire until the
        # session ends
        authorizer = self.globus_client.get_authorizer(self.refresh_token, self.access_token, self.expire_at_s, refresh=True)
        # authorizer = globus_sdk.AccessTokenAuthorizer(str(self.transfer_token))

        tc = globus_sdk.TransferClient(authorizer)

        for ep in tc.endpoint_search(filter_scope="my-endpoints", num_results=None):
            print('{0} has ID {1}'.format(ep['display_name'], ep['id']))

        # self.directory = self.annex.getconfig('directory')
        # if not self.directory:
        #     # we may assume it is your current directory
        #     print("j")
        
    def transfer_store(self, key, filename):
        # location = self._calclocation(key)
        # self._do_store(key, filename, location)
        pass

    def transfer_retrieve(self, key, filename):
        # location = self._calclocation(key)
        # self._do_retrieve(key, location, filename)
        pass

    def checkpresent(self, key):
        # location = self._calclocation(key)
        # return self._do_checkpresent(key, location)PREPARE
        pass

    def remove(self, key):
        # location = self._calclocation(key)
        # self._do_remove(key, location)
        pass

    ## Export methods
    # def transferexport_store(self, key, local_file, remote_file):
    #     location = '/'.join((self.directory, remote_file))
    #     self._do_store(key, local_file, location)
    #
    # def transferexport_retrieve(self, key, local_file, remote_file):
    #     location = '/'.join((self.directory, remote_file))
    #     self._do_retrieve(key, location, local_file)
    #
    # def checkpresentexport(self, key, remote_file):
    #     location = '/'.join((self.directory, remote_file))
    #     return self._do_checkpresent(key, location)
    #
    # def removeexport(self, key, remote_file):
    #     location = '/'.join((self.directory, remote_file))
    #     self._do_remove(key, location)
    #
    # def removeexportdirectory(self, remote_directory):
    #     location = '/'.join((self.directory, remote_directory))
    #     try:
    #         os.rmdir(location)
    #     except OSError as e:
    #         if e.errno != errno.ENOENT:
    #             raise RemoteError(e)
    #
    # def renameexport(self, key, filename, new_filename):
    #     oldlocation = '/'.join((self.directory, filename))
    #     newlocation = '/'.join((self.directory, new_filename))
    #     try:
    #         os.rename(oldlocation, newlocation)
    #     except OSError as e:
    #         raise RemoteError(e)
    #
    # def _mkdir(self, directory):
    #     try:PREPARE
    #         os.makedirs(directory)
    #     except OSError as e:
    #         if e.errno != errno.EEXIST:
    #             raise RemoteError("Failed to write to {}".format(directory))
    #
    # def _calclocation(self, key):
    #     return "{dir}/{hash}{key}".format(
    #                     dir=self.directory,
    #                     hash=self.annex.dirhash(key),
    #                     key=key)
    #
    # def _info(self, message):
    #     try:
    #         self.annex.info(message)
    #     except ProtocolError:
    #         print(message)
    #
    # def _do_store(self, key, filename, location):
    #     self._mkdir(os.path.dirname(location))
    #     templocation = '/'.join((self.directory,
    #                             'tmp',
    #                             key))
    #     self._mkdir(os.path.dirname(templocation))
    #     try:
    #         copyfile(filename, templocation)
    #         os.rename(templocation, location)
    #     except OSError as e:
    #         raise RemoteError(e)
    #     try:
    #         os.rmdir(os.path.dirname(templocation))
    #     except OSError:
    #         self._info("Could not remove tempdir (Not empty)")
    #
    # def _do_retrieve(self, key, location, filename):rt
    #     try:
    #         copyfile(location, filename)
    #     except OSError as e:
    #         raise RemoteError(e)
    #
    # def _do_checkpresent(self, key, location):
    #     if not os.path.exists(self.directory):
    #         raise RemoteError("this remote is not currently available")
    #     return os.path.isfile(location)
    #
    # def _do_remove(self, key, location):
    #     if not os.path.exists(self.directory):
    #         raise RemoteError("this remote is not currently available")
    #     try:
    #         os.remove(location)
    #     except OSError as e:
    #         # It's not a failure to remove a file that is not present.
    #         if e.errno != errno.ENOENT:
    #             raise RemoteError(e)


def get_versions():
    # TODO: to be implemented
    pass


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'setup':
            with open(os.devnull, 'w') as devnull:
                master = Master(devnull)
                remote = GlobusRemote(master)
                remote.setup()
            return
        elif sys.argv[1] == 'version':
            print(os.path.basename(__file__), get_versions()['this'])
            print("Using AnnexRemote", get_versions()['annexremote'])
            return
    else:
        output = sys.stdout
        sys.stdout = sys.stderr

        master = Master(output)
        remote = GlobusRemote(master)
        master.LinkRemote(remote)
        master.Listen()


if __name__ == "__main__":
    main()        
