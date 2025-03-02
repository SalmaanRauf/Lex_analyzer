# rat25s lexical analyzer
# cs323 compiler project - assignment 1
#
# this program reads a rat25s source file, tokenizes it using dfsm-based methods
# for identifiers, integers, and reals, and writes out the tokens and lexemes to an output file.

import sys

# define the sets of keywords, operators, and separators for rat25s
KEYWORDS = ["integer", "function", "if", "else", "endif", "while", "endwhile", "return", "scan", "print"]
OPERATORS = {"<=", ">=", "==", "<>", "=", "+", "-", "*", "/", "<", ">"}
SEPARATORS = {"(", ")", "{", "}", ";", ","}

class Token:
    # class to hold a token type and its lexeme
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme

    def __str__(self):
        return f"{self.token_type:15s} {self.lexeme:15s}"

def is_keyword(lexeme):
    # return true if lexeme is a keyword, false otherwise
    return lexeme in KEYWORDS

def skip_whitespace_and_comments(source, index):
    # skip over white spaces and comments.
    # comments are enclosed in [* and *].
    # returns the updated index.
    while index < len(source):
        # skip whitespace
        if source[index].isspace():
            index += 1
            continue
        # check for comment start: [*
        if source[index] == '[' and index + 1 < len(source) and source[index+1] == '*':
            index += 2  # skip "[*"
            # skip until "*]" is found
            while index < len(source) and not (source[index-1] == '*' and source[index] == ']'):
                index += 1
            index += 1  # skip the closing ']'
            continue
        break
    return index

def lexer(source, index):
    # lexical analyzer function that implements a dfsm for identifiers,
    # integers, and reals. it returns a token and the new index position.
    index = skip_whitespace_and_comments(source, index)
    if index >= len(source):
        return None, index

    current_char = source[index]

    # dfsm for identifiers: starts with a letter, then letters/digits/underscore.
    if current_char.isalpha():
        start = index
        index += 1
        while index < len(source) and (source[index].isalnum() or source[index] == '_'):
            index += 1
        lexeme = source[start:index]
        token_type = "keyword" if is_keyword(lexeme) else "identifier"
        return Token(token_type, lexeme), index

    # dfsm for integers and reals:
    if current_char.isdigit():
        start = index
        index += 1
        while index < len(source) and source[index].isdigit():
            index += 1
        # check for real number: dot followed by at least one digit.
        if index < len(source) and source[index] == '.':
            # look ahead for at least one digit after the dot
            if index + 1 < len(source) and source[index+1].isdigit():
                index += 1  # consume the dot
                while index < len(source) and source[index].isdigit():
                    index += 1
                lexeme = source[start:index]
                return Token("real", lexeme), index
            else:
                # dot without following digit: treat as integer (or error)
                lexeme = source[start:index]
                return Token("integer", lexeme), index
        else:
            lexeme = source[start:index]
            return Token("integer", lexeme), index

    # check for operators (including multi-character operators)
    if current_char in "+-*/=<>":
        # check for two-character operators
        if index + 1 < len(source):
            two_chars = current_char + source[index + 1]
            if two_chars in OPERATORS:
                return Token("operator", two_chars), index + 2
        
        # single character operator
        if current_char in OPERATORS:
            return Token("operator", current_char), index + 1
    
    # check for separators
    if current_char in SEPARATORS:
        return Token("separator", current_char), index + 1

    # if the character doesn't match any known token category, mark it as unknown.
    token = Token("unknown", current_char)
    index += 1
    return token, index

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_source_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        with open(input_file, 'r') as f:
            source = f.read()
    except IOError:
        print("Error: Could not open the input file.")
        sys.exit(1)

    tokens = []
    index = 0
    while index < len(source):
        result = lexer(source, index)
        if result is None:
            break
        token, index = result
        if token is None:
            break
        tokens.append(token)

    # write tokens to output file "output.txt"
    try:
        with open("output.txt", "w") as outfile:
            outfile.write(f"{'Token':15s} {'Lexeme':15s}\n")
            outfile.write("-" * 30 + "\n")
            for token in tokens:
                outfile.write(str(token) + "\n")
    except IOError:
        print("Error: Could not write to output.txt")
        sys.exit(1)

    print("Lexical analysis complete. See output.txt for results.")

if __name__ == "__main__":
    main()
