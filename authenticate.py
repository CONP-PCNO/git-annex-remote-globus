import globus_sdk
import os.path as op
import hashlib
import wget
import os
import subprocess
import globus_sdk.base as base
import json
from globus_sdk import LocalGlobusConnectPersonal

# LOCAL GLOBUS CONNECT PERSONAL
#  https://github.com/globus/globus-sdk-python


def get_endpoint_id():
    for ep in tc.endpoint_search(filter_fulltext='FRDR-Prod-2', num_results=None):
        print('{0} has ID {1}'.format(ep['display_name'], ep['id']))
        return ep['id']


server = 'https://2a9f4.8443.dn.glob.us'
lookup_url = {}


def get_path_content(ep_id, path):
    for en in tc.operation_ls(ep_id, path=path, num_results=None):
        # update last path
        new_path = op.join(path, en['name'])
        # if your last join is a file
        if en['type'] == 'file':
            # get full url where to download the file
            url = server + str(new_path.split('~')[1])
            result = subprocess.Popen(['curl', '-s', url], stdout=subprocess.PIPE)
            out, _ = result.communicate()
            hash_content = hashlib.sha256(out).hexdigest()
            print(hash_content, new_path)


            #result=subprocess.check_call("chmod u+rx hash.sh; ./hash.sh '%s'" % url, shell=True, stdout=subprocess.PIPE)
            # get_hash256sum(url)
            # save filename as download operation may alter it
            # filename = url.split('/')[-1]
            # download file in given directory
            # wget.download(url=url, out=folder)
            # # get file local path
            # local_path = op.join(folder, filename)
            #
            # # generate hash to content
            # with open(local_path, 'rb') as content:
            #     content_bytes = content.read()
            #     content_hash = str(hashlib.sha256(content_bytes).hexdigest())
            #     lookup_url[content_hash] = str(new_path.split('~')[1])

        else:
            get_path_content(ep_id, new_path)
    # write dict on file
    # print(lookup_url)


def get_hash256sum(url):
    subprocess.run(['bash', 'hash.sh', url], shell=True)


CLIENT_ID = '01589ab6-70d1-4e1c-b33d-14b6af4a16be'

client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow()

authorize_url = client.oauth2_get_authorize_url()
print('Please go to this URL and login: {0}'.format(authorize_url))

# this is to work on Python2 and Python3 -- you can just use raw_input() or
# input() for your specific version
get_input = getattr(__builtins__, 'raw_input', input)
auth_code = get_input(
    'Please enter the code you get after login here: ').strip()
token_response = client.oauth2_exchange_code_for_tokens(auth_code)

globus_auth_data = token_response.by_resource_server['auth.globus.org']
globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']

# most specifically, you want these tokens as strings
AUTH_TOKEN = globus_auth_data['access_token']
TRANSFER_TOKEN = globus_transfer_data['access_token']


# a GlobusAuthorizer is an auxiliary object we use to wrap the token. In
# more advanced scenarios, other types of GlobusAuthorizers give us
# expressive power
# An authorizer instance used for all calls to Globus Transfer
authorizer = globus_sdk.AccessTokenAuthorizer(TRANSFER_TOKEN)
tc = globus_sdk.TransferClient(authorizer=authorizer)

# GET THE FRDR-Prod-2 ID (This is what we need)

frdr_id = get_endpoint_id()
ser = tc.get_endpoint(frdr_id)
print(ser['https_server'])

# url1 = 'https://2a9f4.8443.dn.glob.us/5/published/publication_170/submitted_data/2015_12_11_cortex/2015_12_11_cortex.json'
# base_path = '/~/5/published/publication_170/submitted_data/'
#
# folder = 'output'
# if os.path.isdir(folder):
#     for file in os.listdir(folder):
#         file_path = op.join(folder, file)
#         try:
#             # assume there will be only files
#             if os.path.isfile(file_path):
#                 os.unlink(file_path)
#         except Exception as e:
#             print(e)
# else:
#     os.makedirs(folder)
#
# get_path_content(frdr_id, base_path)


