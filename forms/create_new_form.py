from googleapiclient.discovery import build

# def add_question():

def create_form(title:str, desc:str, questions:list, creds:object):
    # form_service = authentication.get_form_service()
    form_service = build('forms', 'v1', credentials=creds)
    update_body = {
        "requests": [
            {
                "updateFormInfo": {
                    "info": {
                        "title": title,
                        "description": desc,
                    },
                    "updateMask": "*"
                }
            },
            # {
            #     "createItem": {
            #         "item": questions,
            #     }
            # }
        ],
    }
    res = form_service.forms().create(body={"info": {"title": title} }).execute()
    res = (
        form_service.forms()
        .batchUpdate(formId=res["formId"], body=update_body)
        .execute()
    )
    print(res)
    return res['writeControl'] != None


# test
# create_form("my test form", "testytesty", [])