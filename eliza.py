# python command line regex therapist chatbot

import re

class Eliza:

    def __init__(self):

        self.greet = "Eliza: Hello! My name is Eliza. What is your name?\n"
        self.exitcmd = [r'\bbye\b', r'\bgoodbye\b', r'\bleave me alone\b', r'\bsee ya\b', r'\bgo away\b']
        self.neg = [r'\bnever mind\b', r'\bmove on\b', r'\bforget it\b', r'\bno\b', r'\bnothing\b']
        self.name = None
        self.askedName = False
        # Create dictionary with keys as regex
        # key = pattern : vals = list of regex that match pattern

        self.patterns = {
            "neg_emotion":
                [r"\b(?:am|feel)\s+(?P<emotion>sad|depressed|angry|mad|upset|lonely|irritated)\b"],
            "fear":
                [r"\b(?:am\s+)?(?:afraid|fear|scared)\s+(of\s+)?(?P<fear>.+)"],
            "relationship":
                [r"\bmy\s+(?P<relation>family|relationship|boyfriend|girlfriend|partner|spouse|friend|mom|mother|dad|father)\b"],
            "desire":
                [r"\bwant\s+(?P<desire>.+)"],
            "need":
                [r"\bneed\s+(?P<need>.+)"],
            "interest":
                [r"\b(?:like|enjoy|love)\s+(?P<interest>.+)"],
            "belief":
                [r"\b(?:think|believe|feel)\s+(that\s+)?(?P<belief>.+)"]
        }

        # pronoun reflections
        self.reflections = {
            "i" : "you",
            "me" : "you",
            "my" : "you",
            "mine" : "yours",
            "am" : "are",
            "you" : "I",
            "your" : "my",
            "yours" : "mine"
        }

    def matchPattern(self, pattern, word):

        if pattern == 'neg_emotion':
            print(f"What is causing you to feel like you are {word['emotion']}?")
        elif pattern == 'relationship':
            print(f"Tell me more about your {word['relation']}")
            # pronoun reflections with temp variable for all below
        elif pattern == 'fear':
            swapped = self.reflect(word['fear'])
            print(f"What about {swapped} makes you feel afraid?")
        elif pattern == 'desire':
            swapped = self.reflect(word['desire'])
            print(f"Why do you want {swapped}?")
        elif pattern == 'need':
            swapped = self.reflect(word['need'])
            print(f"Why do you need {swapped}?")
        elif pattern == 'interest':
            swapped = self.reflect(word['interest'])
            print(f"What do you enjoy about {swapped}?")
        elif pattern == 'belief':
            swapped = self.reflect(word['belief'])
            print(f"Why do you believe that {swapped}?")
        else:
            print("Please, tell me more.")

# talk to bot

    def chat(self):
        user = input(self.greet)

        if re.fullmatch(r"[A-Za-z]+", user):
            self.name = user.capitalize()
            print(f"Nice to meet you, {self.name}.")

        if self.check_exit(user):
            return

        print("What would you like to talk about?")
        user = input(f"[{self.name}]: ")

        self.handle_chat(user)

    def handle_chat(self, user):
        while True:
            if self.check_exit(user):
                break
            pattern, word = self.subject(user)

            if pattern != "_":
                self.matchPattern(pattern, word)
            user = input(f"[{self.name}]: ")

# swap pronouns
    def reflect(self, text):
        pattern = r'\b(?:' + '|' .join(map(re.escape, self.reflections.keys())) + r')\b'
        return re.sub(pattern, lambda m: self.reflections[m.group(0).lower()], text, flags=re.IGNORECASE)

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
                    word = match.groupdict()
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


