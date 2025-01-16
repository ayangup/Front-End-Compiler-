# Token class, represents each token with a type and their value.
class Token:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"< {self.type} , {self.value} >"
    
# TokenType class types to represent all the types of tokens accepted in JSON.
class TokenType:
    LCURLY = 'LCURLY'       # '{'
    RCURLY = 'RCURLY'       # '}'
    LSQUARE = 'LSQUARE'     # '['
    RSQUARE = 'RSQUARE'     # ']'
    COMMA = 'COMMA'         # ','
    COLON = 'COLON'         # ':'
    STRING = 'STRING'       # Tree leaves or node names
    NUMBER = 'NUMBER'       # Edge lengths or numeric values
    BOOL = 'BOOL'           # 'True or False'
    NULL = 'NULL'           # 'null'
    EOF = 'EOF'             # End of input

# LexerError class for any errors that are encountered.
class LexerError(Exception):
    pass

# jsonLexer class to implement the lexical analysis of the input.
class jsonLexer:

    # stores the input text and starts with the postion at 0.
    def __init__(self, input_text):
        self.input = input_text
        self.position = 0
        self.current_char = self.input[self.position] if self.input else None

    # goes to the next character in the input
    def advance(self):
        self.position += 1
        self.current_char = self.input[self.position] if self.position < len(self.input) else None

    # skips the whitespace characters.
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # recognizes and tokenizes the string enclosed in double quotes ("").
    def recognize_string(self):
        result = ''
        self.advance()

        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()

        if self.current_char == '"':
            self.advance()
            return Token(TokenType.STRING, result)
        else:
             raise LexerError("String is unfinished")

    # recognizes and tokenizes the numbers, including integers and decimal.
    def recognize_number(self):
        result = ''
        if self.current_char == '-':
            result += self.current_char
            self.advance()
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, float(result))
    
    # recognizes and tokenizes boolean values and null.
    def recognize_keyword(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()

        if result == 'true':
            return Token(TokenType.BOOL, True)
        
        elif result == 'false':
            return Token(TokenType.BOOL, False)
        
        elif result == 'null':
            return Token(TokenType.NULL, None)
        
        else:
            raise LexerError(f"Unknown keyword: {result}")
        
    # this method is to get the next character or token from the input.
    def get_next_token(self):
        self.skip_whitespace()

        if self.current_char is None:
            return Token(TokenType.EOF, None)
        
        if self.current_char == "{":
            self.advance()
            return Token(TokenType.LCURLY, '{')
        
        if self.current_char == "}":
            self.advance()
            return Token(TokenType.RCURLY, '}')
        
        if self.current_char == "[":
            self.advance()
            return Token(TokenType.LSQUARE, '[')
        
        if self.current_char == "]":
            self.advance()
            return Token(TokenType.RSQUARE, ']')
        
        if self.current_char == ',':
            self.advance()
            return Token(TokenType.COMMA,',')
        
        if self.current_char == ':':
            self.advance()
            return Token(TokenType.COLON, ':')
        
        if self.current_char == '"':
            return self.recognize_string()
        
        if self.current_char.isdigit() or self.current_char == '-':
            return self.recognize_number()
        
        if self.current_char.isalpha():
            return self.recognize_keyword()
        
        raise LexerError(f"Unexpected character '{self.current_char}' at position {self.position}")

# testing code block to run the Lexer using the valid JSON formatted input.
if __name__ == "__main__":
    input_text = '{"name": "Ayan", "age": 18, "is_studying": true, "grades": [90, 90.8, 89], "job": null}'
    lexer = jsonLexer(input_text) 

    while True:
        token = lexer.get_next_token()
        print(token)
        if token.type == TokenType.EOF:
            break 
