import json

def get_users_ids(users):
    user_lookup = {}
    for user in users:
        user_lookup[user["profile"]["real_name_normalized"]] = user["id"]
    return user_lookup 

def get_all_users(bolt_app):
    f = open("id_map.json", "r+")
    dump = json.load(f)
    if len(dump) == 0:
        res = bolt_app.client.users_list()
        users = res["members"]
        new_map = get_users_ids(users)
        f.write(json.dumps(new_map))
        f.close()
        return new_map
    return dump

def get_user_id (bolt_app, user_full_name):
    return get_all_users(bolt_app).get(user_full_name)