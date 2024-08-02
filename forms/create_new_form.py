from authentication import get_form_service

# def add_question():

def create_form(title:str, desc:str, questions:list):
    form_service = get_form_service()
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
    return res.writeControl != None


# test
# create_form("my test form", "testytesty", [])