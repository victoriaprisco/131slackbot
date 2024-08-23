

def has_profile_picture(profile):
    return 'https://avatars.slack-edge.com' in profile["image_24"]

def check_all_users_profile_pictures(bolt_app):
    res = bolt_app.client.users_list()
    those_who_dont = []
    for user in res["members"]:
        if not has_profile_picture(user["profile"]):
            those_who_dont.append(user["profile"]["real_name_normalized"])
    return those_who_dont