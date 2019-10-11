#!/usr/bin/env python
# git-annex external special remote program for Globus data repository
# 
# This is an addition to git-annex's built-in directory special remotes.
# 
# Install in PATH as git-annex-remote-directory
#
# TODO: Add Copyright

import sys, os, errno
import wget

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
        self.directory = None
        self.refresh_token = None
        self.access_token = None
        self.expire_at_s = None
        self.auth_token = None
        self.transfer_token = None
        self.globus_client = GlobusClient(self.client_id)
        # for now we can call it from here, we can make a separate command call if required, to complete the setup
        self._setup()

    def _setup(self):
        print("Im in setup")
        # set up to be completed, may be useful to store tokens in a token.json file. After this, initremote starts
        # this is about authorization and having all credentials in place to use the special remote
        self.auth_token, self.transfer_token = self.globus_client.get_transfer_tokens()
        # self.auth_token, self.transfer_token = self.globus_client.get_transfer_tokens()

        # POTENTIAL PROCESS TO CHECK FOR CREDENTIALS AND AUTH
        # self.auth.LoadCredentialsFile('token.json')
        #
        # if self.auth.credentials is None:
        #     self.auth.CommandLineAuth()
        # elif self.auth.access_token_expired:
        #     self.auth.Refresh()
        # else:
        #     self.auth.Authorize()
        #
        # self.auth.SaveCredentialsFile('token.json')
        # print(
        #     "Setup complete. An auth token was stored in token.json. Now run 'git annex initremote' with your
        #     desired parameters. If you don't run it from the same folder, specify via token=path/to/token.json")

    def initremote(self):
        print("I am in initremote")
        # TODO need to think on how to make this call relevant and indempotent to users.
        #  Think of scenarios of many users and many sessions. Do they need different tokens?

        """Requests the remote to initialize itself. Idempotent call"""

        # for now we assume to work with refresh tokens, so when instantiated they should last
        if not self.auth_token and not self.transfer_token:
            self._setup()
        print(self.auth_token, self.transfer_token)

    def prepare(self):
        # ask git - annex for its configuration
        self.directory = self.annex.getconfig('directory')
        print("I am in prepare")
        authorizer = self.globus_client.get_authorizer(self.auth_token, self.transfer_token)
        tc = globus_sdk.TransferClient(authorizer)
        frdr_endpoint = tc.endpoint_search(filter_fulltext='FRDR-Prod-2', num_results=None)
        path = 'https://2a9f4.8443.dn.glob.us/5/published/publication_170/submitted_data/2015_11_18_cortex/2015_11_18_cortex.json'
        print(self.directory)
        # self.directory = self.annex.getconfig('directory')
        # if not self.directory:
        #     # we may assume it is your current directory
        #     print("j")
        
    def transfer_store(self, key, filename):
        # TODO: decide what to do with this
        print("File cannot be stored in dataset")
        location = self._calclocation(key)
        # self._do_store(key, filename, location)
        pass

    def transfer_retrieve(self, key, filename):
        location = self._calclocation(key)
        return self._do_retrieve(location, filename)

    def checkpresent(self, key):
        location = self._calclocation(key)
        return self._do_checkpresent(key, location)

    def remove(self, key):
        # location = self._calclocation(key)
        # self._do_remove(key, location)
        pass

    def _calclocation(self, key):
        # return '/'.join((self.directory, filename=hashkey))
        # which is the same as:
        return "{dir}/{hash}{key}".format(
            dir=self.directory,
            hash=self.annex.dirhash(key),
            key=key)

    # TODO: decorate it to return multiple files in multiple locations
    def _do_retrieve(self, location, filename):
        # build path with file to be retrieved
        path = '/'.join((location, filename))
        try:
            wget.download(url=path)
        except OSError as e:
            raise RemoteError(e)

    def _do_checkpresent(self, key, location):
        if not os.path.exists(self.directory):
            raise RemoteError("this remote is not currently available")
        return os.path.isfile(location)

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
