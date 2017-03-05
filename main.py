import json
from take_action import TakeAction
from define_action import DefineAction

if __name__=="__main__":
    with open('example_data/example_9.json') as data_file:
        data = json.load(data_file)

    define_it = DefineAction(path_origin="example_data/law_data/")
    context = define_it.defineAction(data)

    take_it = TakeAction(json_path='in.json')
    initial_content, result_action = take_it.take_action(context)

    print("----- INITIAL ------")
    print(initial_content)
    print("----- RESULT ------")
    print(result_action)

