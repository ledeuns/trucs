# tested with M1 K1+K2 K3 (K6,K7) ((K8) K9+(K10)) (K4-K5)        -K11

tokens = (
    'NAME','COG','MCOG'
    )

literals = ['+','-',',','(',')']

# Tokens
t_NAME = r'^M\d+'
t_COG = r'K\d+'
t_MCOG = r'[ \t]-K\d+'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    if (t.value[0] != " " and t.value[0] != "\t"):
        print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

def isInDatabase(k):
    # K10 is not in the list
    l = ['K1','K2','K3','K6','K8','K9','K7','K4','K5','K11']
    if k in l:
        return True
    else: return False

# Parsing rules
def p_statement_expr(p):
    'statement : NAME expression'
    print p[1]+'=['+p[2]+']'

def p_expression_operation(p):
    '''expression : expression '+' expression
                  | expression '-' expression                  
                  | expression ',' expression'''
    p[0] = p[1]+p[2]+p[3]

def p_expression_cog(p):
    '''expression : COG'''
    if (isInDatabase(p[1])):
        print(p[1]+' detected')
        p[0] = p[1]
    else:
        print(p[1]+' not detected')
        p[0] = ''

def p_expression_mcog(p):
    '''expression : MCOG'''
    p[1] = p[1][1:]
    if (isInDatabase((p[1][1:]))):
        print((p[1][1:])+' detected')
        p[0] = p[1]
    else:
        print(p[1]+' not detected')
        p[0] = ''

def p_expression_group(p):
    "expression : '(' expression ')'"
    print("found parenthesis for : "+p[2])
    p[0] = '('+p[2]+')'

def p_expression_list(p):
    "expression : expression expression"
    p[0] = p[1]+' '+p[2]

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('parser > ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)
