import re

class TakeAction(object):
    def __init__(self, json_path=None):
        # Path to json that describes the action
        self.json_path = json_path

        # Element to parse in order
        self.elemTypes = [  'header1_reference',
                            'header2_reference',
                            'header3_reference',
                            'alinea_reference',
                            'sentence_reference',
                            'words-reference']

        # TODO: Find a cleaner way of matching what's between a context without taking
        # the context in the match
        self.regexps = { 
                    'header1_reference': r'(?=((\n|^)#\w(.|\n)*?)(\n#\w|$))',
                    # From : (textStart or \n) and one #
                    # To   : next header 1 or EOF

                    'header2_reference': r'(?=((\n|^)##\w(.|\n)*?)(\n#{1,2}\w|$))',
                    # From : (textStart or \n) and two #
                    # To   : next header 1 or 2 or EOF

                    'header3_reference': r'(?=((\n|^)###\w(.|\n)*?\n)(\n#{1,3}\w|$))',
                    # From : (textStart or \n) and three #
                    # To   : next header from 1 to 3 or EOF

                    'alinea_reference' : r'(?=(\n\n[^#].*?(\n\n|$)))',
                    # from : \n\n and not starting with #
                    # to   : \n\n or endoffile

                    'sentence_reference' : r'([A-ZÀÀÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏ].*?\.)',
                    # from : MAJ 
                    # to   : .

                    'words-reference' : r'(\b\w.*?\b)'
                    # from : " " 
                    # to   : " "

                    # More Info : https://docs.python.org/2/library/re.html
                    }

    def set_json_path(self, json_path):
        self.json_path = json_path

    def open_article_file(self, path):
        with open(path, 'r') as toto_file:
            content = toto_file.read()

        self.content = content
        return content

    def find(self, elem, content, target='1', index=(0,-1)):
        sub_content = content[index[0]:index[1]]

        if target.isdigit():
            regexp = self.regexps[elem]
            target = int(target)
        else:
            regexp = r'\b('+target+r')\b'

        match = re.finditer(re.compile(regexp, re.UNICODE), sub_content)

        if match:
            try:
                if type(target) == int:
                    m = list(match)[target-1] 
                else:
                    # else if "defendu" , returns first match
                    m = list(match)[0]

                begining = m.start()+index[0]
                end = m.start()+len(m.group(1))+index[0]
                return begining, end 
            except:
                print("[ERREUR] \"{}\" \"{}\" n'existe pas ! ".format(elem, target))


    def act(self, content, action, index, args=None):
        modif = None
        do = {
                'replace' : args,
                'delet' : "",
                'add_before' : args+" "+content[index[0]:index[1]],
                'add_after' : content[index[0]:index[1]]+" "+args
                }

        modif = do[action]  

        new_content = content[0:index[0]]+modif+content[index[1]:-1]
        return new_content

    def take_action(self, context):
        index = (0, -1)
        search = []

        path = context['path']+'.md'
        action = context['editType'] 
        # Can be: 'delet', 'replace', 'add_before', 'add_after'

        args = context['definition']

        for elem in self.elemTypes :
            if elem in context:
                search.append((elem, context[elem]))

        content = self.open_article_file(path)

        # Search contains how to search for wanted modification
        # ex: [('header1_reference', '1'), ('sentence_reference', '1'), ("word_reference", 'est')]
        for search_elem in search:
            elem=search_elem[0]

            if len(search_elem) == 2:
                target = search_elem[1]
            else : 
                target = '-1'

            index = self.find(elem, content, target=target, index=index)

        result_action = self.act(content, action=action, index=index, args=args)

        return(content, result_action)


if __name__=="__main__":
    pass

    # ------ UNI TESTS -------
    # index = find('a_phrase', content, rank=1)
    # print(index)

    # index_context = find("défendu", content,  index=index)
    # index_no_context = find("défendu", content, rank=1)
    # print(index_context)
    # print(index_no_context)

    # result_action = act(content, action="delet", index=index_context, args="autorisé")
    # print(result_action)
