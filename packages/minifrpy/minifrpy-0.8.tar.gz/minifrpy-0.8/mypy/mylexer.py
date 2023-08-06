# importer le lexer de SLY
from sly import Lexer

# définir la classe mylexer
class MyLexer(Lexer):
    # déclarer une liste de TOKENS
    tokens = {NOM, NUM, CHAINE, ECRIS, CONCA,TANTQUE,
              DOUBLE, FLOAT, TYPE, SI, ALORS,
              SINON, EGL, FONC, POUR, FLECHE, OCCUR, URL,PE,GE,NE}

    # litéral ingoré
    ignore = '\t\n '

    # litéraux d'un caractères
    literals = {'=', '+', '-', '/', 'x','*', '^', '(', ')', '%', ':', ',', ';','>','<','&','|'}

    # Definir les tokens par des regex
    # l'ordre est important le premier regex qui match sera utilisé
    EGL = r'=='
    FLECHE = r'->'
    PE = r'<='
    GE = r'>='
    NE = r'!='
    # la definition des identifiants appelés NOM dans ce programme doit être faite après les strings (chaine)
    CHAINE = r'\".*?\"'
    def CHAINE(self, t):
        # convertir en un float en python
        t.value = (t.value)
        return t
    URL = r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}'

    # Règle de base pour l'identification des identifiants
    NOM = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # spécification des mots clef
    NOM['sinon'] = SINON
    NOM['si'] = SI
    NOM['conca'] = CONCA
    NOM['alors'] = ALORS
    NOM['fonc'] = FONC
    NOM['pour'] = POUR
    NOM['occur'] = OCCUR
    NOM['ecris'] = ECRIS
    NOM['type'] = TYPE
    NOM['double'] = DOUBLE
    NOM['tantque'] = TANTQUE




    # Ignorer les commentaires
    ignore_comment = r'(#.*)'


    # fonction qui detecte un float et retourne sa valeur
    # il falait absolument commencer par traiter les floats avant les entiers
    @_(r'([0-9]*\.[1-9]+)([Ee][+-]?[0-9]+)?')
    def FLOAT(self, t):
        # convertir en un float en python
        t.value = float(t.value)
        return t

    # fonction qui detecte un nombre et retourne sa valeur
    @_(r'\d+')
    def NUM(self, t):
        # convertir en un entier en python
        t.value = int(t.value)
        return t

    # fonction qui qui traite les sauts de ligne
    # afin de renvoyer le numéro de ligne d'erreurs
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno = t.value.count('\n')


    # fonction qui traite (ignore) les commentaires
    @_(r'//.*')
    def COMMENT(self, t):
        pass

    # traitement des erreurs
    def error(self, t):
        print("caractère non permis '%s'" % str(t.value)[0])
        self.index += 1

if __name__ == '__main__':
    lexer = MyLexer()
    env = {}
    while True:
        try:
            text = input('LEX > ')
        except EOFError:
            break
        if text:
                lex = lexer.tokenize(text)
                for token in lex:
                    print(token)
