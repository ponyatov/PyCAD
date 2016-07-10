import wx

class AST:
    def __init__(self,V):
        self.tag=self.__class__.__name__.lower() ; self.val=V ; self.nest=[]
    def push(self,o):
        self.nest.append(o) ; return self
    def head(self):
        return "<%s:%s>"%(self.tag,self.val)
    def dump(self,depth=0):
        S="\n" + "\t"*depth + self.head()
        for i in self.nest: S += i.dump(depth+1)
        return S
    def __repr__(self):
        return self.dump()
    def __add__(self,o):
        return OP("+").push(self).push(o)
    def __mul__(self,o):
        return OP("*").push(self).push(o)

class SYM(AST): pass
class STR(AST): pass
class INT(AST):
    def __init__(self,V): AST.__init__(self,V) ; self.val=int(self.val)
    def __neg__(self): self.val = - self.val ; return self
class NUM(AST):
    def __init__(self,V): AST.__init__(self,V) ; self.val=float(self.val)
    def __neg__(self): self.val = - self.val ; return self

class OP(AST): pass

##print NUM(2) + AST(3) * NUM(4)

##### lexer

t_ignore = ' \t\r\n'
def t_COMMENT(t):
    r'\#[^\n]*'

tokens = ('SYM','INT','NUM','LP','RP','ADD','SUB','MUL','DIV')

t_LP = r'\('
t_RP = r'\)'

def t_NUM(t):
    r'[0-9]+(\.[0-9]*|[eE][\+\-]?[0-9]+)'
    t.value = NUM(t.value) ; return t
def t_INT(t):
    r'[0-9]+'
    t.value = INT(t.value) ; return t
def t_SYM(t):
    r'[a-zA-Z0-9]+'
    t.value = SYM(t.value) ; return t

def t_ADD(t):
    r'\+'
    t.value = OP(t.value) ; return t
def t_SUB(t):
    r'\-'
    t.value = OP(t.value) ; return t
def t_MUL(t):
    r'\*'
    t.value = OP(t.value) ; return t
def t_DIV(t):
    r'\/'
    t.value = OP(t.value) ; return t

def t_error(t):
    print 'error',t
    t.lexer.skip(1)
    
import ply.lex ; lexer = ply.lex.lex()

##### parser

glob = {}

precedence = (
    ('left','ADD','SUB'),
    ('left','MUL','DIV'),
    ('left','PFX')
    )

def p_main(t):
    'main : ex'
    print t[1]

def p_sym(t):
    'ex : SYM '
    t[0] = t[1]
def p_num(t):
    '''ex : NUM
        | INT'''
    t[0] = t[1]
def p_paren(t):
    'ex : LP ex RP'
    t[0] = OP("()").push(t[2])
def p_ex(t):
    '''ex : ex ADD ex
        | ex SUB ex
        | ex MUL ex
        | ex DIV ex '''
    t[0] = t[2].push(t[1]).push(t[3])
def p_uplus(t):
    'ex : ADD ex %prec PFX'
    t[0] = t[2]
def p_uminus(t):
    'ex : SUB ex %prec PFX'
    t[0] = -t[2]
    
def p_error(t):
    print 'error',t

import ply.yacc ; parser = ply.yacc.yacc()

parser.parse('''
# comment
2+3.4*-5e+6
''')
