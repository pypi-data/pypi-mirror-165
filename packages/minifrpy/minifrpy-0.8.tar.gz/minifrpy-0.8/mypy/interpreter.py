#!/usr/bin/env python3

from mypy.execute import *
from mypy.mylexer import MyLexer
from mypy.mypy_errors import Error,ParseError

if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    env = {}
    while True:
        try:
            text = input('mypy> ')
        except EOFError:
            break
        if text:
            try:
                tree = parser.parse(lexer.tokenize(text))
            except(AttributeError) as err:
                print(repr(err))
                continue
            try:
                Execute(tree, env)
            except (ZeroDivisionError,IndexError) as err:
                print(repr(err))
                continue
            except:
                print("erreur innatendue")
                continue
