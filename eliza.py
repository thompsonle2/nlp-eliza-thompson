# python command line regex chatbot

import re

# Create dictionary with keys as regex
# Capture pattern into register
pattern_responses = {
    r'/\b[hH]i|[hH]ey|[hH]ello\b/' : 'Hello! My name is Eliza. What is your name?'
    r'/\b()\b/' : 'Nice to meet you, '
}

default = "I'm sorry, I don't understand that. Could you please rephrase?"

def getEliza(userInput):
    userInput = userInput