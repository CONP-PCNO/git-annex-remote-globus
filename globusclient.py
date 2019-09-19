import globus_sdk


class GlobusClient:

    def __init__(self, client_id):
        self.client_id = client_id

    def get_transfer_tokens(self):
        client = globus_sdk.NativeAppAuthClient(self.client_id)
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
        return globus_auth_data['access_token'], globus_transfer_data['access_token']

    def get_refresh_tokens(self):
        pass