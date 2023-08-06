from sly import Parser
import sys
from .mylexer import MyLexer
from colorama import Fore,Style


class MyParser(Parser):
    tokens = MyLexer.tokens

    # traitement des priorités

    precedence = (
        ('nonassoc', '<', 'PE', '>', 'GE','EGL', 'NE','TANTQUE'),
        ('nonassoc', 'OCCUR','CONCA', 'DOUBLE','ECRIS', 'QUIT'),
        ('left', '+', '-',"TYPE"),
        ('left', '*', '/', '%','x' ),
        ('right', '^'),
        ('right', 'UMINUS')

    )

    debugfile = 'parser.out'

    # fonction d'initialisation
    def __init__(self):
        self.env = {}

    # fonction qui traite les espaces en les ignorant
    @_('')
    def statement(self, p):
        pass

    @_('QUIT')
    def statement(self, p):
        return sys.exit("vous êtes sorti du programme")

    @_('POUR variable FLECHE expr ALORS statement')
    def statement(self, p):
        return 'for_loop', ('for_loop_setup', p.variable, p.expr), p.statement

    @_('SI condition ALORS statement SINON statement')
    def statement(self, p):
        return 'if_stmt', p.condition, ('branch', p.statement0, p.statement1)

    @_('TANTQUE condition ALORS statement')
    def statement(self, p):
        return 'while_stmt', p.condition, ('branch', p.statement0)

    @_('FONC NOM "("  ")" ":" statement')
    def statement(self, p):
        return 'fun_def', p.NOM, p.statement

    @_('FONC NOM "(" NOM ")" ":" statement')
    def statement(self, p):
        return 'fun_def', p.NOM0, ('parm', p.NOM1, p.statement)

    @_('OCCUR URL CHAINE')
    def statement(self, p):
        return 'occur', p.URL, p.CHAINE

    @_('NOM "("  ")"')
    def statement(self, p):
        return 'fun_call', p.NOM

    @_('NOM "(" variable ")"')
    def statement(self, p):
        return 'fun_call_params', p.NOM, p.variable

    @_('variable')
    def statement(self, p):
        return p.variable

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr EGL expr',
       'expr PE expr',
       'expr GE expr',
       'expr NE expr',
       'expr ">" expr',
       'expr "<" expr',
       )
    def condition(self, p):
        return p[1], p.expr0, p.expr1

    @_('NOM "=" expr')
    def variable(self, p):
        return 'variable', p.NOM, p.expr

    @_('DOUBLE expr')
    def expr(self, p):
        return 'dbl', p.expr

    @_('TYPE expr')
    def expr(self, p):
        return 'tp', p.expr

    @_('CHAINE')
    def expr(self, p):
        return 'str', p.CHAINE

    # construire l'arbre des opérateurs arithmétiques
    @_('expr "+" expr',
       'expr "-" expr',
       'expr "x" expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr "^" expr',
       'expr "%" expr',
       )
    def expr(self, p):
        return p[1], p.expr0, p.expr1

    # traitement du '-' unaire
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr[1]

    # d'autres opérations
    @_('ECRIS expr')
    def expr(self, p):
        return 'ecr', p.expr

    @_('CONCA CHAINE CHAINE')
    def expr(self, p):
        return ('conca', p.CHAINE0, p.CHAINE1)

    @_('NOM')
    def expr(self, p):
        return 'var', p.NOM

    @_('NUM')
    def expr(self, p):
        return 'num', p.NUM

    @_('FLOAT')
    def expr(self, p):
        return 'flt', p.FLOAT

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    def error(self, p):
        if p:
            print(Fore.BLUE + "erreur de syntaxe au token", str(p.value) + Style.RESET_ALL)
        else:
            print("Syntax error at EOF")

if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()
    env = {}
    while True:
        try:
            text = input('YACC> ')
        except EOFError:
            break
        if text:
            try:
                tree = parser.parse(lexer.tokenize(text))
                print(tree)
            except AttributeError as err:
                print(repr(err))
                continue
