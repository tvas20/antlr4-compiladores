grammar Arithmetic;

// Regras do Parser
expr: term ( (PLUS | MINUS) term )* ;
term: factor ( (MUL | DIV) factor )* ;
factor: INT | LPAREN expr RPAREN ;

// Regras do Lexer
PLUS: '+' ;
MINUS: '-' ;
MUL: '*' ;
DIV: '/' ;
INT: [0-9]+ ;
LPAREN: '(' ;
RPAREN: ')' ;
WS: [ \t\r\n]+ -> skip ;

// Novas Regras do Parser
program: statement+ ;
statement: assignment | expr ;
assignment: VAR ASSIGN expr ;

// Novas Regras do Lexer
VAR: [a-zA-Z]+ ;
ASSIGN: '=' ;