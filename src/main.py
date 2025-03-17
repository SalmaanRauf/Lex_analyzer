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
    
    # FSM for whitespace and comments:
    # State 0: Initial state
    # State 1: Saw '[', looking for '*'
    # State 2: Inside comment, looking for '*'
    # State 3: Inside comment, saw '*', looking for ']'
    
    state = 0
    while index < len(source):
        if state == 0:  # Initial state
            if source[index].isspace():
                index += 1
                continue
            elif source[index] == '[':
                state = 1
                index += 1
                continue
            else:
                break
        elif state == 1:  # Saw '[', looking for '*'
            if source[index] == '*':
                state = 2
                index += 1
                continue
            else:
                # Not a comment, go back to initial state
                state = 0
                break
        elif state == 2:  # Inside comment, looking for '*'
            if source[index] == '*':
                state = 3
                index += 1
                continue
            else:
                index += 1
                continue
        elif state == 3:  # Inside comment, saw '*', looking for ']'
            if source[index] == ']':
                state = 0  # Comment ended, back to initial state
                index += 1
                continue
            else:
                state = 2  # Not end of comment, go back to looking for '*'
                index += 1
                continue
    return index

def lexer(source, index):
    # lexical analyzer function that implements a dfsm for identifiers,
    # integers, and reals. it returns a token and the new index position.
    index = skip_whitespace_and_comments(source, index)
    if index >= len(source):
        return None, index

    current_char = source[index]

    # FSM for identifiers:
    # State 0: Initial state
    # State 1: Saw a letter (accepting state)
    # State 2: Saw letter followed by letter/digit/underscore (accepting state)
    #
    # Transitions:
    # State 0 --letter--> State 1
    # State 1 --letter/digit/underscore--> State 2
    # State 2 --letter/digit/underscore--> State 2
    if current_char.isalpha():  # State 0 -> State 1
        start = index
        index += 1
        # State 1 or 2 -> State 2 (loop)
        while index < len(source) and (source[index].isalnum() or source[index] == '_'):
            index += 1
        lexeme = source[start:index]
        # In accepting state (1 or 2), determine token type
        token_type = "keyword" if is_keyword(lexeme) else "identifier"
        return Token(token_type, lexeme), index

    # FSM for integers and reals:
    # State 0: Initial state
    # State 1: Saw digit(s) (accepting state for integers)
    # State 2: Saw digit(s) followed by '.'
    # State 3: Saw digit(s) followed by '.' followed by digit(s) (accepting state for reals)
    #
    # Transitions:
    # State 0 --digit--> State 1
    # State 1 --digit--> State 1
    # State 1 --'.'--> State 2
    # State 2 --digit--> State 3
    # State 3 --digit--> State 3
    if current_char.isdigit():  # State 0 -> State 1
        start = index
        index += 1
        # State 1 -> State 1 (loop)
        while index < len(source) and source[index].isdigit():
            index += 1
        
        # Check for transition to real number: State 1 -> State 2 -> State 3
        if index < len(source) and source[index] == '.':  # State 1 -> State 2
            # Look ahead for at least one digit after the dot
            if index + 1 < len(source) and source[index+1].isdigit():  # State 2 -> State 3
                index += 1  # consume the dot
                # State 3 -> State 3 (loop)
                while index < len(source) and source[index].isdigit():
                    index += 1
                lexeme = source[start:index]
                return Token("real", lexeme), index  # Accepting state for reals
            else:
                # dot without following digit: treat as integer (or error)
                lexeme = source[start:index]
                return Token("integer", lexeme), index  # Accepting state for integers
        else:
            # No dot: remain in State 1 (integer)
            lexeme = source[start:index]
            return Token("integer", lexeme), index  # Accepting state for integers

    # FSM for operators:
    # State 0: Initial state
    # State 1: Saw potential operator character (accepting state for single-char operators)
    # State 2: Saw two-character operator (accepting state for two-char operators)
    #
    # Transitions:
    # State 0 --operator char--> State 1
    # State 1 --matching second char--> State 2
    if current_char in "+-*/=<>":  # State 0 -> State 1
        # Check for two-character operators: State 1 -> State 2
        if index + 1 < len(source):
            two_chars = current_char + source[index + 1]
            if two_chars in OPERATORS:  # Valid two-char operator
                return Token("operator", two_chars), index + 2  # Accepting state for two-char operators
        
        # Single character operator: remain in State 1
        if current_char in OPERATORS:
            return Token("operator", current_char), index + 1  # Accepting state for single-char operators
    
    # FSM for separators:
    # State 0: Initial state
    # State 1: Saw separator character (accepting state)
    #
    # Transitions:
    # State 0 --separator char--> State 1
    if current_char in SEPARATORS:  # State 0 -> State 1
        return Token("separator", current_char), index + 1  # Accepting state for separators

    # If the character doesn't match any known token category, mark it as unknown.
    # This is effectively a catch-all state in our FSM
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
