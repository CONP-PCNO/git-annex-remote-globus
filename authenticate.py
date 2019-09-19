import globus_sdk

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

# create an endpoint:
ep_data = {
    "DATA_TYPE": "endpoint",
    "display_name": 'name',
    "DATA": [
        {
            "DATA_TYPE": "server",
            "hostname": "gridftp.globusid.org",
        },
    ],
}
create_result = tc.create_endpoint(ep_data)
endpoint_id = create_result["id"]


# high level interface; provides iterators for list responses
print("My Endpoints:")
print(endpoint_id)
for ep in tc.endpoint_search(filter_scope="my-endpoints", num_results=None):
    print('{0} has ID {1}'.format(ep['display_name'], ep['id']))
