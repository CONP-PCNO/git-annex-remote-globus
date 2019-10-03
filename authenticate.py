import globus_sdk
import json


def get_endpoint_id():
    for ep in tc.endpoint_search(filter_fulltext='FRDR-Prod-2', num_results=None):
        print('{0} has ID {1}'.format(ep['display_name'], ep['id']))
        return ep['id']


def get_path_content(ep_id):
    print("In get path content - ls")
    for en in tc.operation_ls(ep_id, path="/~/5/published/publication_170/submitted_data/"):
        print(en)


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

print(AUTH_TOKEN)
print(TRANSFER_TOKEN)

# a GlobusAuthorizer is an auxiliary object we use to wrap the token. In
# more advanced scenarios, other types of GlobusAuthorizers give us
# expressive power
# An authorizer instance used for all calls to Globus Transfer
authorizer = globus_sdk.AccessTokenAuthorizer(TRANSFER_TOKEN)
tc = globus_sdk.TransferClient(authorizer=authorizer)

# CREATE AN ENDPOINT
ep_data = {
    "DATA_TYPE": "endpoint",
    "display_name": 'test',
    "DATA": [
        {
            "DATA_TYPE": "server",
            "hostname": "gridftp.globus.org",
        },
    ],
}
create_result = tc.create_endpoint(ep_data)

# GET THE FRDR-Prod-2 ID (This is what we need)

frdr_id = get_endpoint_id()
get_path_content(frdr_id)


# IMPORTANT PAGES: https://docs.globus.org/globus-connect-server-installation-guide/
# https://docs.globus.org/globus-connect-server-v5-installation-guide/#_creating_a_storage_gateway_using_the_posix_storage_connector
#
# # high level interface; provides iterators for list responses
# reqs = tc.endpoint_get_activation_requirements(endpoint_id)
# print(reqs['activated'])
# print(reqs)
# file = open('tmp.json', 'r')
#
# reqs = json.load(file)
# print(type(reqs))

# ACTIVATION (pause for now)
# To active an endpoint, clients should get the activation requirements for the endpoint (either explicitly or from
# the autoactivate result), pick an activation method, and fill in values for the chosen activation method.
# The requirements for the other methods not being used must be removed before submitting the request.
# https://docs.globus.org/api/transfer/endpoint_activation/
# r = tc.endpoint_autoactivate(endpoint_id, if_expires_in=3600)
#
# if r["code"] == "AutoActivationFailed":
#     print("Endpoint requires manual activation, please open "
#           "the following URL in a browser to activate the "
#           "endpoint:")
#     print("https://app.globus.org/file-manager?origin_id=%s"
#           % endpoint_id)
    # For python 2.X, use raw_input() instead
    # input("Press ENTER after activating the endpoint:")
    # r = tc.endpoint_autoactivate(endpoint_id, if_expires_in=3600)


# TRY AND NAVIGATE IN THE ENDPOINT PATH AND RETRIVE DATA
