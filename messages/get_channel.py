def get_users_ids(users):
    user_lookup = {}
    for user in users:
        user_lookup[user["profile"]["real_name_normalized"]] = user["id"]
    return user_lookup

def get_all_users(bolt_app):
    res = bolt_app.client.users_list()
    users = res["members"]
    return get_users_ids(users)

def get_user_id (bolt_app, user_full_name):
    return get_all_users(bolt_app).get(user_full_name)
