# AYAN GUPTA
# B00962542

import json

# This class is to represent the type and value of the tokens used.
class Token:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value


# This class represents all the types of tokens.
class TokenType:
    LCURLY = 'LCURLY'  
    RCURLY = 'RCURLY'
    COLON = 'COLON'   
    COMMA = 'COMMA'       
    LSQUARE = 'LSQUARE'
    RSQUARE = 'RSQUARE' 
    STRING = 'STRING'     
    NUMBER = 'NUMBER'     
    EOF = 'EOF'           


# This class divides the JSON input into tokens for parsing.
class Lexer:

    # This sets the lexer with the input string.
    def __init__(self, inp):
        self.input = inp
        self.position = 0
        self.current_chr = self.input[self.position]
        self.tokens = []


    # This tokenizes the input into JSON tokens.
    def tokenize_input(self):
        while self.current_chr is not None:
            if self.current_chr in ' \t\n':
                self.next_pos()
                continue

            if self.current_chr == '{':
                self.tokens.append(Token(TokenType.LCURLY, '{'))
                self.next_pos()
                continue

            if self.current_chr == '}':
                self.tokens.append(Token(TokenType.RCURLY, '}'))
                self.next_pos()
                continue

            if self.current_chr == ':':
                self.tokens.append(Token(TokenType.COLON, ':'))
                self.next_pos()
                continue

            if self.current_chr == ',':
                self.tokens.append(Token(TokenType.COMMA, ','))
                self.next_pos()
                continue

            if self.current_chr == '[':
                self.tokens.append(Token(TokenType.LSQUARE, '['))
                self.next_pos()
                continue

            if self.current_chr == ']':
                self.tokens.append(Token(TokenType.RSQUARE, ']'))
                self.next_pos()
                continue

            if self.current_chr == '"':
                self.tokens.append(self.type_string())
                continue

            if self.current_chr.isdigit() or self.current_chr == '-':
                self.tokens.append(self.type_number())
                continue

            if self.current_chr in".+":
                self.type_number()
                self.next_pos()
                continue
        self.tokens.append(Token(TokenType.EOF, None))


    # This moves to the nexr character in the input.
    def next_pos(self):
        self.position += 1

        # Updates the current character if the end of the input is not reached.
        if self.position < len(self.input):
            self.current_chr = self.input[self.position]

        # This makes the current character None, if the end of the input is reached.
        else:
            self.current_chr = None


    # This gets the JSON string type token.
    def type_string(self):
        structure = ''
        self.next_pos() 

        while self.current_chr != '"' and self.current_chr is not None:
            structure += self.current_chr
            self.next_pos()
        self.next_pos()  
        return Token(TokenType.STRING, structure)


    # This gets the JSON number type token.
    def type_number(self):
        
        num = ''
        deci = False
        if self.current_chr == '+':
            raise Exception(f"Type 3 Error: Invalid leading '+' in number '{self.current_chr}'.")

        while self.current_chr is not None and (self.current_chr.isdigit() or self.current_chr in '.-'):
            if self.current_chr == '.':
                
                # This condition checks for invalid decimal points. 
                if deci:
                    raise Exception(f"Type 1 Error: Invalid decimal number '{num + '.'}'.")  
                deci = True
                if not num or (len(num) == 1 and num in "-"):
                    raise Exception(f"Type 1 Error: Invalid decimal number '{num + '.'}'.") 
            num += self.current_chr
            self.next_pos()
        
        if num.endswith('.'):
            raise Exception(f"Type 1 Error: Invalid decimal number '{num}'.")
        
        if '.' in num and len(num.split('.')) == 2 and not num.split('.')[1]:
            raise Exception(f"Type 1 Error: Invalid decimal number '{num}'.")
        
        # This condition checks for leading 0's.
        if num.startswith('0') and len(num) > 1 and not num.startswith('0.'):
            raise Exception(f"Type 3 Error: Invalid number with leading zeros '{num}'.")

        return Token(TokenType.NUMBER, num)


# This class parses tokens to make a Dictionary.
class Parser:

    # This is for the reserved words that cannot be used as keys.
    reserved_keys = {"true", "false"}  

    # This is for the reserved words that cannot be used as strings anywhere.
    reserved_strings = {"true", "false"}  

    # This sets the parser with the tokens.
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]


    # This gets the next token.
    def get_next_token(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = Token(TokenType.EOF, None)


    # This accepts the token if it matches the required token type.
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.get_next_token()
        else:
            raise Exception(f"Expected token {token_type}, got {self.current_token.type}")


    # This is where the starting of parsing a value starts.
    def parse(self):
        return self.obj_parsed()


    # This parses a Dictionary that is enclosed within the curly brackets.
    def obj_parsed(self):
        obj = {}
        self.eat(TokenType.LCURLY)

        # This checks for unique keys in the dictionary.
        unique_keys = set()  
        while self.current_token.type != TokenType.RCURLY:
            
            self.parsing_key=True
            key = self.str_parsed()
            self.parsing_key=False

            # This condition checks if the key is empty in Dictionary.
            if not key.strip():
                raise Exception("Type 2 Error: Empty key in Dictionary.")

            # This condition checks if the key has reserved words like true or false.
            if key in self.reserved_keys:
                raise Exception(f"Type 4 Error: Reserved word '{key}' cannot be a dictionary key.")

            # This condition checks if the key is unique and not repeated in Dictionary.
            if key in unique_keys:
                raise Exception(f"Type 5 Error: Duplicate key '{key}' in Dictionary.")
            unique_keys.add(key)
            
            self.eat(TokenType.COLON)
            value = self.value_parse()
            obj[key] = value

            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)

            elif self.current_token.type != TokenType.RCURLY:
                raise Exception(f"Unexpected token {self.current_token.type} in dictionary")
            
        self.eat(TokenType.RCURLY)
        return obj


    # This parses JSON string token.
    def str_parsed(self):
        token = self.current_token
        
        if token.type != TokenType.STRING:
            raise Exception(f"Expected STRING, got {token.type}")
        if self.parsing_key:
            
            if token.value in {"true", "false"}:
                raise Exception(f"Type 4 Error: Reserved word '{token.value}' cannot be a dictionary key.")
        else:
            if token.value in self.reserved_strings:
                raise Exception(f"Type 7 Error: Reserved word '{token.value}' cannot be used as a string anywhere.")

        self.get_next_token()
        return token.value


    # This parses JSON value which of a valid JSON value type.
    def value_parse(self):
        token = self.current_token

        if token.type == TokenType.STRING:
            return self.str_parsed()

        elif token.type == TokenType.NUMBER:
            number_value=self.num_check(token.value)
            self.get_next_token()
            return number_value

        elif token.type == TokenType.LCURLY:
            return self.obj_parsed()

        elif token.type == TokenType.LSQUARE:
            return self.list_parsed()

        else:
            raise Exception(f"Unexpected token {token.type} in value")


    # This checks if the valid JSON number is given in the input.
    def num_check(self, num):

        # This condition checks if JSON numbers have a leading '+' sign.
        if num.startswith('+'):
            raise Exception(f"Type 3 Error: Invalid leading '+' in number '{num}'.")

        if '.' in num:
            divs = num.split('.')
            if len(divs) != 2 or not divs[0].isdigit() or not divs[1].isdigit():
                raise Exception(f"Type 1 Error: Invalid decimal number '{num}'.")

        if num.startswith('0') and len(num) > 1 and not num.startswith('0.'):
            raise Exception(f"Type 3 Error: Invalid number with leading zeros '{num}'.")
        
        if num.startswith('+') and not ('e' in num or 'E' in num):
            raise Exception(f"Type 3 Error: Invalid leading '+' in number '{num}'.")

        return float(num) if '.' in num else int(num)


    # This parses JSON array that is enclosed within square brackets.
    def list_parsed(self):
        self.eat(TokenType.LSQUARE)
        mylist = []
        element_type = set() 

        while self.current_token.type != TokenType.RSQUARE:
            value = self.value_parse()
            mylist.append(value)
            element_type.add(type(value))

            if len(element_type) > 1:
                raise Exception(f"Type 6 Error: Inconsistent types in list: {mylist}.")

            if self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
            elif self.current_token.type != TokenType.RSQUARE:
                raise Exception(f"Unexpected token {self.current_token.type} in list")

        self.eat(TokenType.RSQUARE)
        return mylist


# This is for constructing an Abstract Syntax Tree structures for the semantically correct input format.
def abstract_tree_structure(obj, indent = 0):
    structure = ""
    indent_str = " " * indent
    if isinstance(obj, dict):
        structure += f"{indent_str}Dictionary\n"
        structure += f"{indent_str}{{\n"
        for key, value in obj.items():
            structure += f"{indent_str}   pair\n"
            structure += f"{indent_str}      key\n"
            structure += f"{indent_str}         STRING: {key}\n"
            structure += f"{indent_str}      value\n"
            structure += abstract_tree_structure(value, indent + 1)
        structure += f"{indent_str}}}\n"

    elif isinstance(obj, list):
        structure += f"{indent_str}    list\n"
        structure += f"{indent_str}    [\n"
        for item in obj:
            structure += abstract_tree_structure(item, indent + 1)
        structure += f"{indent_str}    ]\n"

    elif isinstance(obj, str):
        structure += f"{indent_str}        STRING: {obj}\n"

    elif isinstance(obj, (int, float)):
        structure += f"{indent_str}        NUMBER: {obj}\n"

    return structure


# This writes the abstract syntax tree structure to the output text files.
def write_abstract_tree_to_file(parsed_json, filename):
    parse_tree = abstract_tree_structure(parsed_json)
    with open(filename, 'w') as file:
        file.write(parse_tree)
    print(f"Parse tree saved to {filename}")


# This writes the error of the input files with the semantic errors into the output error text files.
def write_error_to_file(error_message, filename):
    with open(filename, 'a') as file:
        file.write(f"{error_message}\n")
    print(f"Error logged to {filename}")


# This manages and process the input and output files. 
def main():
    input_file=[]
    output_json_file=[]
    output_error_file=[]

    # This manages the filenames for the input and output files.
    for i in range(10):
        input_file.append("in"+str(i)+".txt")
        output_json_file.append("resultAST"+str(i)+".txt")
        output_error_file.append("output_error"+str(i)+".txt")
        
        # This opens the input file and reads the inputs inside the input files.
        try:
            with open(input_file[i], 'r') as file:
                input_json = file.read()

            lexer = Lexer(input_json)
            lexer.tokenize_input()
            tokens = lexer.tokens
        
            parser = Parser(tokens)
            parsed_json = parser.parse()
            write_abstract_tree_to_file(parsed_json,output_json_file[i])

        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(error_message)
            write_error_to_file(error_message,output_error_file[i])

# This runs the main method when the program is executed.
if __name__ == '__main__':
    main()
    