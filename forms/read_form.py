from googleapiclient.discovery import build
import json

def get_list_of_values(question_id, response_list):
    converter = lambda response: response["answers"][question_id]["textAnswers"]["answers"][0]["value"]
    return [converter(response) for response in response_list]
    
def get_all_question_body_and_id(items_array):
    converter = lambda item: { "body": item["title"], "id": item["questionItem"]["question"]["questionId"]}
    return [converter(item) for item in items_array]

def get_specific_question(question_body, questions):
    return list(filter(lambda q: q["body"] == question_body, questions))
# {'formId': '1AHGp3LEh0W5LncNSh3TNFkYkKesz9iHzHJ1HNjmEg1g', 
# 'info': 
#   {'title': 'my test form', 
#   'description': 'testytesty', 
#   'documentTitle': 'Untitled form'}, 
# 'settings': {}, 
# 'revisionId': '00000008', 
# 'responderUri': 'https://docs.google.com/forms/d/e/1FAIpQLScRSXTtGUv7viyHYfKDLxMQ4vG9cLlc2TL29Z18EkFZmET2QA/viewform', 
# 'items': [{'itemId': '0118ffd0', 'title': 'yes', 'questionItem': {'question': {'questionId': '3fd3be6b', 'textQuestion': {}}}}]}
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
    print(f"questions: {questions}")
    q = get_specific_question(question_body, questions)
    responses = service.forms().responses().list(formId=form_id).execute()
    print(responses)
    return get_list_of_values(q[0]["id"], responses["responses"])
    # print(get_token.get_token())
    # responses = get(f'https://forms.googleapis.com/v1/forms/{form_id}/responses', headers={"Authorization": f'Bearer {get_token.get_token()}'})
    # print("ReadForm request:", responses.reason, responses.status_code)
    # if (responses.status_code == 200):
    #     responses_list = json.loads(responses._content)['responses']
    #     return get_list_of_values(responses_list)

    # else:
    #     print("ERROR")
    #     return "An error occurred"

# test
# read_form("15DwXWVX5rJu7BTHy2vC3fNiO3cFKlU-dgVYSN7RapdU")