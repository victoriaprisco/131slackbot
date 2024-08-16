from googleapiclient.discovery import build
import json

def get_list_of_values(question_id, response_list):
    converter = lambda response: response["answers"][question_id]["textAnswers"]["answers"][0]["value"]
    return [converter(response) for response in response_list]
    
def get_all_question_body_and_id(items_array):
    print(items_array)
    converter = lambda item: { "body": item["title"], "id": item["questionItem"]["question"]["questionId"]} if "questionItem" in item.keys() else {"body": "", "item": ""}
    return [converter(item) for item in items_array]

def get_specific_question(question_body, questions):
    return list(filter(lambda q: q["body"] == question_body, questions))

def get_question_list(form_id, creds):
    service = build('forms', 'v1', credentials=creds)
    questions = service.forms().get(formId=form_id).execute()
    if (questions["items"] == None):
        print("error getting questions from form")
        return None
    return get_all_question_body_and_id(questions["items"])

def read_form(form_id, question_body, creds):
    service = build('forms', 'v1', credentials=creds)
    questions = get_question_list(form_id, creds)
    q = get_specific_question(question_body, questions)
    responses = service.forms().responses().list(formId=form_id).execute()
    return get_list_of_values(q[0]["id"], responses["responses"])

def compare_with_roster(responses):
    roster = json.load(open("roster.json"))["current_roster"]
    missing = []
    for ta in roster:
        if not ta in (response.title().strip() for response in responses):
            missing.append(ta)
    return missing  