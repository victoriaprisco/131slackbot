from forms import authentication
from requests import get
from forms import get_token
import json

def get_list_of_values(response_list):
    converter = lambda response: response["answers"]["3fd3be6b"]["textAnswers"]["answers"][0]["value"]
    return [converter(response) for response in response_list]
    

def read_form(form_id):
    authentication.get_form_service()
    responses = get(f'https://forms.googleapis.com/v1/forms/{form_id}/responses', headers={"Authorization": f'Bearer {get_token.get_token()}'})
    print("ReadForm request:", responses.reason, responses.status_code)
    if (responses.status_code == 200):
        responses_list = json.loads(responses._content)['responses']
        return get_list_of_values(responses_list)
    else:
        print("ERROR")
        return "An error occurred"

# test
# read_form("1AHGp3LEh0W5LncNSh3TNFkYkKesz9iHzHJ1HNjmEg1g")