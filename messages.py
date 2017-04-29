# messages.py

import json
from datetime import datetime

# Converts JSON string to dictionary probably.
def json_str_to_dict(str):
    # Initialize JSON decoder function.
    decoder = json.JSONDecoder()

    # Decode information into dictionary.
    return decoder.decode(str)

# Converts python data structure (list/tuple/dict) to json string.
def dict_to_json_str(thing):
    # Initialize JSON encoder function.
    encoder = json.JSONEncoder()

    # Encode into JSON string.
    return encoder.encode(thing)

# Create a message to be sent.
def create_msg(usr_str, msg_str, flag):
    dict = {}
    dict['flag'] = flag
    dict['user'] = usr_str
    dict['message'] = msg_str
    dict['time'] = str(datetime.now().time())
    # dict['fname'] = person.FName or however we store the name
    # dict['lname'] = person.Lname...
    # dict['...'] = ....
    #
    # stuff
    #
    # etc
    return dict_to_json_str(dict)
