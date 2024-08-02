from oauth2client import file

def get_token():
    store = file.Storage("token.json")
    creds = store.get()
    return creds.access_token
