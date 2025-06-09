from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor: # Visitor para a árvore de sintaxe abstrata 
    def __init__(self):
        self.memory = {}  # Armazena variáveis

    def visit(self, ctx): # Método genérico para visitar os nós da árvore
        if isinstance(ctx, ArithmeticParser.ExprContext): # Método para visitar expressões
            return self.visitExpr(ctx)
        elif isinstance(ctx, ArithmeticParser.TermContext): # Método para visitar termos
            return self.visitTerm(ctx)
        elif isinstance(ctx, ArithmeticParser.FactorContext): # Método para visitar fatores
            return self.visitFactor(ctx)
        elif isinstance(ctx, ArithmeticParser.ProgramContext): # Método para visitar programas
            return self.visitProgram(ctx)
        elif isinstance(ctx, ArithmeticParser.StatementContext): # Método para visitar declarações
            return self.visitStatement(ctx)
        elif isinstance(ctx, ArithmeticParser.AssignmentContext): # Método para visitar atribuições
            return self.visitAssignment(ctx)
        
    def visitProgram(self, ctx): # Método para visitar o programa
        result = None
        for statement in ctx.statement():
            result = self.visit(statement)
        return result
    
    def visitStatement(self, ctx): # Método para visitar declarações
        if ctx.assignment():
            return self.visit(ctx.assignment())
        else:
            return self.visit(ctx.expr())
        
    def visitAssignment(self, ctx): # Método para visitar atribuições
        var_name = ctx.VAR().getText()
        value = self.visit(ctx.expr())
        self.memory[var_name] = value
        return value
    
    def visitExpr(self, ctx): # Método para visitar expressões
        result = self.visit(ctx.term(0)) # Começa com o primeiro termo
        for i in range(1, len(ctx.term())): # Itera sobre os termos restantes
            if ctx.getChild(i * 2 - 1).getText() == '+': # Se o operador for '+', soma o termo atual ao resultado
                result += self.visit(ctx.term(i)) 
            else: # Se o operador for '-', subtrai o termo atual do resultado
                result -= self.visit(ctx.term(i))
        return result 

    def visitTerm(self, ctx): # Método para visitar termos
        result = self.visit(ctx.factor(0))
        for i in range(1, len(ctx.factor())): # Itera sobre os fatores restantes
            if ctx.getChild(i * 2 - 1).getText() == '*': # Se o operador for '*', multiplica o fator atual ao resultado
                result *= self.visit(ctx.factor(i))
            else: # Se o operador for '/', divide o fator atual do resultado
                result /= self.visit(ctx.factor(i))
        return result

    def visitFactor(self, ctx): # Método para visitar fatores
        #TODO lidar com variáveis e atribuições. Você precisará armazenar variáveis em um dicionário e atualizá-las conforme as atribuições forem feitas.
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.VAR():
            var_name = ctx.VAR().getText()
            if var_name in self.memory:
                return self.memory[var_name]
            else:
                raise Exception(f"Variável '{var_name}' não definida.")
        else:
            return self.visit(ctx.expr())

def repl():
    visitor = ArithmeticVisitor()

    print("Digite expressões ou atribuições (ex: x = 2 + 3). Digite 'sair' para encerrar.")
    while True:
        try:
            expression = input(">> ")
            if expression.strip().lower() in ["sair", "exit", "quit"]:
                break
            if not expression.strip():
                continue

            lexer = ArithmeticLexer(InputStream(expression))
            stream = CommonTokenStream(lexer)
            parser = ArithmeticParser(stream)
            tree = parser.program()
            result = visitor.visit(tree)
            print(result)

        except:
            break

if __name__ == '__main__':
    repl()