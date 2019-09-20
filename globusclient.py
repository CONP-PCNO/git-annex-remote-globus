import globus_sdk


class GlobusClient:

    authorizer = None

    def __init__(self, client_id):
        self.client_id = client_id
        self.client = globus_sdk.NativeAppAuthClient(self.client_id)

    def ask_for_tokens(self, refresh=None):
        if refresh:
            self.client.oauth2_start_flow(refresh_tokens=True)
        else:
            self.client.oauth2_start_flow()

        authorize_url = self.client.oauth2_get_authorize_url()
        print('Please go to this URL and login: {0}'.format(authorize_url))

        # this is to work on Python2 and Python3 -- you can just use raw_input() or
        # input() for your specific version
        get_input = getattr(__builtins__, 'raw_input', input)
        auth_code = get_input(
            'Please enter the code you get after login here: ').strip()
        token_response = self.client.oauth2_exchange_code_for_tokens(auth_code)
        return token_response

    def get_transfer_tokens(self):

        token_response = self.ask_for_tokens()
        globus_auth_data = token_response.by_resource_server['auth.globus.org']
        globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']

        # most specifically, you want these tokens as strings
        return globus_auth_data['access_token'], globus_transfer_data['access_token']

    def get_refresh_tokens(self):
        """
        Gets tokens that never expire unless revoked and which can be used to get new Access Tokens
        whenever those do expire.
        :return:
            *transfer_rt*: refresh token for globus transfer service
            *transfer_at*: access token for globus transfer service
            *expires_as_s*: expiration time in seconds
        """
        # add flag for refresh token
        token_response = self.ask_for_tokens(refresh=True)
        # obtain data for the Globus Transfer service
        globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
        # extract refresh token and access token abbr. as RT and AT
        transfer_rt = globus_transfer_data['refresh_token']
        transfer_at = globus_transfer_data['access_token']
        expires_at_s = globus_transfer_data['expires_at_seconds']
        return transfer_rt, transfer_at, expires_at_s

    def get_authorizer(self, *params, refresh=None):
        if refresh:
            return globus_sdk.RefreshTokenAuthorizer(
                params[0], self.client, access_token=params[1], expires_at=params[2])
        else:
            return globus_sdk.AccessTokenAuthorizer(params[1])

