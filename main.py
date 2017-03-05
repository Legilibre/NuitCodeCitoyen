import json
import sys
from define_action import DefineAction
from take_action import TakeAction

if __name__=="__main__":

    try:
        json_file = sys.argv[1]
        laws_folder = sys.argv[2]
    except:
        json_file = 'example_data/example_9.json' 
        laws_folder = "example_data/law_data/"

    with open(json_file) as data_file:
        data = json.load(data_file)

    define_it = DefineAction(path_origin=laws_folder)
    context = define_it.defineAction(data)

    take_it = TakeAction(json_path='in.json')
    initial_content, result_action = take_it.take_action(context)

    # print("----- INITIAL ------")
    # print(initial_content)
    # print("----- RESULT ------")
    print(result_action)

