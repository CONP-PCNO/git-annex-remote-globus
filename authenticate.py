import globus_sdk

CLIENT_ID = '01589ab6-70d1-4e1c-b33d-14b6af4a16be'

client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow()

authorize_url = client.oauth2_get_authorize_url()
print('Please go to this URL and login: {0}'.format(authorize_url))
