#-*- coding: utf-8 -*-

import json

class DefineAction:

    def __init__(self, path_origin=None):
        self.context = {'path': path_origin}

        self.ref_types = [
            'code-reference',
            'book-reference',
            'law-reference',
            'title-reference',
            'article-reference',
            'header1-reference',
            'header2-reference',
            'header3-reference',
            'alinea-reference',
            'sentence-reference',
            'words-reference',
            'incomplete-reference'
        ]

        self.visitors = {
            'edit': self.visit_edit_node,
            'code-reference': self.visit_code_reference_node,
            'book-reference': self.visit_book_reference_node,
            'law-reference': self.visit_law_reference_node,
            'title-reference': self.visit_title_reference_node,
            'article-reference': self.visit_article_reference_node,
            'header1-reference': self.visit_header1_reference_node,
            'header2-reference': self.visit_header2_reference_node,
            'header3-reference': self.visit_header3_reference_node,
            'alinea-reference': self.visit_alinea_reference_node,
            'sentence-reference': self.visit_sentence_reference_node,
            'words-reference': self.visit_words_reference_node,
            'words': self.visit_words_definition_node,
        }

    def set_path_origin(self, path_origin):
        self.context = {'path': path_origin}

    def visit_code_reference_node(self, node):
        self.context['path'] = self.context['path'] + node['codeName'] + '/'

    def visit_book_reference_node(self, node):
        print('code book ref')

    def visit_law_reference_node(self, node):
        print('law article ref')

    def visit_title_reference_node(self, node):
        print('visiting title ref')

    def visit_article_reference_node(self, node):
        self.context['path'] = self.context['path'] + node['id']

    def visit_header1_reference_node(self, node):
        print('visiting header1 ref')

    def visit_header2_reference_node(self, node):
        print('visiting header2 ref')

    def visit_header3_reference_node(self, node):
        print('visiting header3 ref')

    def visit_alinea_reference_node(self, node):
        print('visiting alinea ref')

    def visit_sentence_reference_node(self, node):
        print('visiting sentence ref')

    def visit_words_reference_node(self, node):
        if 'type' in node and node['type'] == 'quote':
            self.context['words-reference'] = node['words']
        if 'children' in node:
            for child in node['children']:
                self.visit_words_reference_node(child)

    def visit_edit_node(self, node):
        self.context['editType'] = node['editType']

    def visit_words_definition_node(self, node):
        if 'type' in node and node['type'] == 'quote':
            self.context['definition'] = node['words'] 
        if 'children' in node:
            for child in node['children']:
                self.visit_words_definition_node(child)


    def visit_node(self, node):
        if 'type' in node and node['type'] in self.visitors:
            self.visitors[node['type']](node)

        if 'children' in node:
            for child in node['children']:
                self.visit_node(child)

    def defineAction(self, data):
        self.visit_node(data)
        return self.context

if __name__ == '__main__':
    with open('in.json') as data_file:
        data = json.load(data_file)
    example = DefineAction('./')
    res = example.defineAction(data)
    print(res)
