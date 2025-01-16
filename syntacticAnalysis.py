# AYAN GUPTA
# B00962542

# This class is to represent the type and value of the tokens used.
class Token:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value

# This class represents all the types of tokens.
class TokenType:
    LCURLY = 'LCURLY'
    RCURLY = 'RCURLY'
    LSQUARE = 'LSQUARE'
    RSQUARE = 'RSQUARE'
    COMMA = 'COMMA'
    COLON = 'COLON'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    BOOL = 'BOOL'
    NULL = 'NULL'
    EOF = 'EOF'

# This class is for tokenizing the input from the input file.
class Lexer:
    def __init__(self, filePath):
        self.tokensUsed = []
        self.position = 0
        self.load_tokens(filePath)

    # this method reads and tokenizes the input from the input text file.
    def load_tokens(self, filePath):
        with open(filePath, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("<") and line.endswith(">"):
                    content = line[1 : -1].split(", ")
                    token_type = content[0]
                    if token_type == "[":
                        self.tokensUsed.append(Token(TokenType.LSQUARE, "["))
                    elif token_type == "]":
                        self.tokensUsed.append(Token(TokenType.RSQUARE, "]"))
                    elif token_type == ",":
                        self.tokensUsed.append(Token(TokenType.COMMA, ","))
                    elif token_type == "STR":
                        self.tokensUsed.append(Token(TokenType.STRING, content[1] if len(content) > 1 else None))
                    elif token_type == "INT":
                        self.tokensUsed.append(Token(TokenType.NUMBER, content[1] if len(content) > 1 else None))
                    else:
                        print(f"Token type is unknown {token_type}")

        self.tokensUsed.append(Token(TokenType.EOF, None))

    # this method gets the next token.
    def get_next_token(self):
        if self.position < len(self.tokensUsed):
            token = self.tokensUsed[self.position]
            self.position += 1
            return token
        return Token(TokenType.EOF, None)

# This class represents the nodes in the parse tree.
class Node:
    def __init__(self, label = None, value = None, is_leaf = False):
        self.label = label
        self.value = value
        self.children = []
        self.is_leaf = is_leaf
    
    # this method adds the child node to the current node.
    def add_child(self, child):
        self.children.append(child)

    # this method prints the parse tree
    def print_tree(self, depth = 0, file = None):
        indent = "  " * depth
        line = " "
        if self.label == "value" and not self.is_leaf:
            line = (f"{indent}value\n")
        elif self.is_leaf:
            if self.value is not None:
                line = (f"{indent}{self.label}: {self.value}\n")
            else:
                line = (f"{indent}{self.label}\n")
        else:
            line = (f"{indent}{self.label}\n")

        if file:
            file.write(line)

        for child in self.children:
            child.print_tree(depth + 1, file)

# This class parses the tokens into the parse tree.
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.get_next_token()

    # this method is to get the next token from the lexer.
    def get_next_token(self):
        self.current_token = self.lexer.get_next_token()

    # this method basically accepts or consumes the token if it matches the required token type.
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.get_next_token()
        else:
            # raise Exception(f"Expected token {token_type}, got {self.current_token.type}")
            self.error(f"Expected token {token_type}, got {self.current_token.type}")
            self.recover()
    
    def error(self, message):
        print(f"Error : {message}")

    def recover(self):
        recovered_tokens = {TokenType.RSQUARE, TokenType.COMMA, TokenType.EOF}
        while self.current_token.type not in recovered_tokens:
            self.get_next_token()        
    
    # this method is where the starting of parsing a value starts.
    def parse(self):
        return self.value()
    
    # this method is used to parse values.
    def value(self):
        if self.current_token.type == TokenType.LSQUARE:
            return self.listOfJSON()
        elif self.current_token.type == TokenType.STRING:
            node = Node(is_leaf = True, label = "STRING", value = self.current_token.value)
            self.eat(TokenType.STRING)
            valueOfNode = Node(label = "value")
            valueOfNode.add_child(node)
            return valueOfNode
        elif self.current_token.type == TokenType.NUMBER:
            node = Node(is_leaf=True, label = "NUMBER", value=self.current_token.value)
            self.eat(TokenType.NUMBER)
            valueOfNode = Node(label="value")
            valueOfNode.add_child(node)
            return valueOfNode
        else:
            raise Exception(f"Unexpected token {self.current_token.type} in value")
    
    # this method is to parse the list which contains JSON values.
    def listOfJSON(self):
        valueOfNode = Node(label="value")
        listOfNode = Node(label="list")
        valueOfNode.add_child(listOfNode)

        self.eat(TokenType.LSQUARE)
        listOfNode.add_child(Node(is_leaf=True, label="["))

        while self.current_token.type != TokenType.RSQUARE:
            listOfNode.add_child(self.value())

            if self.current_token.type == TokenType.COMMA:
                listOfNode.add_child(Node(is_leaf=True, label=","))
                self.eat(TokenType.COMMA)

        listOfNode.add_child(Node(is_leaf=True, label="]"))
        self.eat(TokenType.RSQUARE)
        
        return valueOfNode

# this is the main method, it is for running the lexer and the parser, this method prints the parse tree in the output file.
def main():

    # relative path to the input text file.
    filePath = 'input_tokens.txt'
    lexer = Lexer(filePath)
    parser = Parser(lexer)
    tree = parser.parse()

    # this prints the output of the parse tree into the output text file.
    with open("parseTree_output.txt", "w") as file:
        tree.print_tree(file = file)
    print("\nParse tree printed in parseTree_output.txt\n")

if __name__ == "__main__":
    main()
