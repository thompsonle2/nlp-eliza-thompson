# python command line regex chatbot

import re

class Eliza:

    def __init__(self):

        self.greet = "Eliza: Hello! My name is Eliza. What is your name?\n"
        self.exitcmd = [r'bye', r'goodbye', r'leave me alone', r'see ya']
        self.neg = [r'never mind', r'move on', r'forget it', r'no', r'nothing', r'go away']
        self.name = None
        self.askedName = False
        # Create dictionary with keys as regex
        # key = pattern : vals = list of regex that match pattern

        self.patterns = {
            "neg_emotion":
                [r"\b(?P<emotion>sad|depressed|angry|mad|upset|lonely|irritated)\b"],
            "relationship":
                [r"\b(?P<relation>family|relationship|boyfriend|girlfriend|partner|spouse|friend|mom|mother|dad|father)\b"],
            "desire":
                [r"\b(want|need|think) (?P<desire>.+)"],
            "need":
                [r"\bneed\s+(?P<need>.+)"],
            "interest":
                [r"\b(like|enjoy|love)\s+(?P<interest>.+)"],
            "fear":
                [r"\b(afraid|fear|scared)\s+(of\s+)?(?P<fear>.+)"],
            "belief":
                [r"\b(think|believe|feel)\s+(that\s+)?(?P<belief>.+)"]
        }


    def chat(self):
        user = input(self.greet)

        if re.fullmatch(r"[A-Za-z]+", user):
            self.name = user.capitalize()
            print(f"Nice to meet you, {self.name}.")

        if self.check_exit(user):
            return

        print("What would you like to talk about?")
        user = input(f"[{self.name}]: ")

        #check if they mentioned keyword instead
        pattern, word = self.subject(user)
        if pattern != "_":
            self.matchPattern(pattern, word)

        self.handle_chat(user)

    def handle_chat(self, user):
        while True:
            if self.check_exit(user):
                break
            pattern, word = self.subject(user)
            self.matchPattern(pattern, word)
            # if pattern != "_":
            #     self.matchPattern(pattern)
        user = input(f"{self.name}> ")

    def matchPattern(self, pattern, word):

        if pattern == 'neg_emotion':
            print(f"What is causing you to feel {word['neg_emotion']}?")
        elif pattern == 'relationship':
            print(f"Tell me more about your {word['relation']}")
        elif pattern == 'desire':
            print(f"Why do you {word['desire']}?")
        elif pattern == 'need':
            print(f"Why do you need {word['need']}?")
        elif pattern == 'interest':
            print(f"What do you enjoy about {word['interest']}?")
        elif pattern == 'fear':
            print(f"What about {word['fear']} makes you feel afraid?")
        elif pattern == 'belief':
            print(f"Why do you believe that {word['belief']}?")
        else:
            print("Please, tell me more.")

# what user wants to talk about

    def subject(self, user):
        user = user.lower()
        if self.check_neg(user):
            return "_", None
        for pattern, expressions in self.patterns.items(): # [key,val]
            for reg in expressions:
                match = re.search(reg, user)
                if match:
                    ######################
                    word = match.groupdict
                    return pattern, word
        print("I'm sorry, I don't understand that. Could you please rephrase?")
        user = input(f"[{self.name}]: ")
        return self.subject(user)

    def check_neg(self, user):
        for negative in self.neg:
            found = re.search(negative, user)
            if found:
                print("What would you like to talk about instead?\n")
                return True
        return False

    def check_exit(self, user):
        for exit in self.exitcmd:
            found = re.search(exit, user)
            if found:
                print("Goodbye!")
                return True
        return False

    def __call__(self):
        self.chat()

eliza = Eliza()
eliza()


