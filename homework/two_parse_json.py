import json

JSON_TEXT = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'


def get_message(json_text=JSON_TEXT,message_num=2):
    obj = json.loads(json_text)
    if message_num > len(obj['messages']) or message_num <=0:
        return f'There is no message number "{message_num}"'
    else:
        return obj['messages'][message_num-1]['message']


print(get_message())