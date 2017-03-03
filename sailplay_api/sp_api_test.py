import sailplay_api

api_connector = sailplay_api.api_connector("XXXX", "XXXXXXXX", "XXXX")

print("Logging in")
token = api_connector.login()
if token is not False:
	print("\tToken: %s " % token)
else:
	print("\tError")
	exit(1)

print("Getting info")
user_info = api_connector.users_info(phone="XXXXXXXXXXX")
if user_info is not False:
	print("\t%s" % user_info)
else:
	print("\tError")
