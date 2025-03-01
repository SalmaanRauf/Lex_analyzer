Rat25S Compiler Project – Lexical Analyzer
===========================================

Directory Structure:
--------------------
Rat25S_Compiler_Project/
├── docs/
│   ├── Cover_Page.txt
│   └── Documentation.txt
├── src/
│   └── main.py
├── tests/
│   ├── test1.txt
│   ├── test2.txt
│   └── test3.txt
└── README.txt

How to Run:
-----------
1. Open a terminal in the project folder.

2. Run the program with a test file:
   Example:
       python src/main.py tests/test1.txt

3. The program creates "output.txt" in the main folder.
   Check this file to see the tokens.

4. You can also try tests/test2.txt and tests/test3.txt for more examples.

About the Project:
-----------------
- This is our implementation of a lexical analyzer for the Rat25S language
- We used a DFSM (Deterministic Finite State Machine) approach to recognize identifiers, integers, and real numbers
- The main.py file has comments explaining how everything works
- Make sure to keep the folders organized as shown above

