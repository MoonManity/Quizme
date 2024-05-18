import os
import json
import random
import simple_term_menu as stm

def getQueue(file):
    with open(file, "r") as f:
        contents = f.read()
        return json.loads(contents)

class Tracker():
    def __init__(self, questions):
        self.chosenItem = None
        self.playing = True
        self.bank = questions
        self.correct = 0
        self.asked = 0
        self.currentTerm = None

    def pickTerm(self):
        term = random.choice(self.bank)
        self.currentTerm = term

    def handleAnswerChoices(self, term):
        self.asked += 1
        choices = [ "A" , "B" , "C" , "D" ]
        menu = stm.TerminalMenu(
                [f"{choices[count-1]}: {i}" for count, i in enumerate(self.currentTerm["answers"])],
                title=None,
                menu_cursor_style=("fg_blue","bold"),
                menu_highlight_style=("underline",),
                cursor_index=1
            )
        self.chosenItem = choices[menu.show()]

    def handleUserAnswer(self):
        if self.chosenItem == self.currentTerm['correct']:
            self.correct += 1
            termCount = self.bank.count(self.currentTerm)

            for count, i in enumerate(self.bank):
                if i == self.currentTerm:
                    self.bank.pop(count)
                    break

            self.output(["Correct!", f"Score: {self.correct}/{self.asked}"])
            input()
            os.system("clear")
        else:
            if self.bank.count(self.currentTerm) < 8:
                self.bank.append(self.currentTerm)
            self.output(["Incorrect.", "Press 'enter' for the next question"])
            input()
            os.system("clear")

    
    def output(self, items):
        width = 50
        if type(items) == list:
            print('┌' + '─' * width + '┐')
            for i in items:
                print("|", i.center(48, " "), "|")
            print("".join('└' + '─' * width + '┘'))
        else:
            print('┌' + '─' * width + '┐')
            print("|", items.center(48, " "), "|")
            print('└' + '─' * width + '┘')
