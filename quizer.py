import os
import sqlite3 as sql
from typing import Dict
import json
import random
import simple_term_menu as stm


class Tracker():
    def __init__(self, file):
        self.file = file
        self.chosenItem: None|str = None
        self.playing: bool = True
        self.bank: str = self.getQueue()
        self.correct: int = 0
        self.asked: int = 0
        self.currentQuestion = None
        self.missed = [] #list 
        self.topics = [] #List[Dict[str: int]]
        self.topicsLog = {} #List[Dict[str: int]]

    def pickQuestion(self) -> None:
        question = random.choice(self.bank)
        self.currentQuestion = question
        self.logTopic()
        self.output(self.currentQuestion["question"])

    def handleAnswerChoices(self, term) -> None:
        self.asked += 1
        choices = ["A","B","C","D"]
        menu = stm.TerminalMenu(
                [f"{i}: {self.currentQuestion['answers'][i]}" for count, i in enumerate(self.currentQuestion["answers"])],
                title=None,
                menu_cursor_style=("fg_blue","bold"),
                menu_highlight_style=("underline",),
                cursor_index=1
            )
        self.chosenItem = choices[menu.show()]
        os.system("clear")

    def handleUserAnswer(self) -> None:
        if self.gradeAnswer(): self.output(["Correct!", f"Score: {self.correct}/{self.asked}"])
        else: self.output(["Incorrect.", f"Score: {self.correct}/{self.asked}" ,"Press 'enter' for the next question"])
        input()
        os.system("clear")

    def gradeAnswer(self) -> bool:
        if self.chosenItem == self.currentQuestion['correct_answer']:
            self.correct += 1
            for count, i in enumerate(self.bank):
                if i == self.currentQuestion:
                    self.bank.pop(count)
                    break
            return True
        else:
            self.recordIncorrect()
            if self.bank.count(self.currentQuestion) <= 3: self.bank.append(self.currentQuestion)
            return False

    def recordIncorrect(self) -> None:
        cur = self.currentQuestion
        self.topicsLog[cur["topic"]]["missed"] += 1
        if cur["question"] not in self.topicsLog[cur["topic"]]["missed_questions"]:
            self.topicsLog[cur["topic"]]["missed_questions"].append(cur["question"])

    def getTopicStats(self) -> None:
        pass

    def logTopic(self) -> None:
        if self.currentQuestion["topic"] not in self.topics:
            self.topics.append(self.currentQuestion["topic"])
            self.topicsLog[self.currentQuestion["topic"]] = { "asked": 1, "missed": 0, "missed_questions": [] }

        else: self.topicsLog[self.currentQuestion["topic"]]["asked"] += 1

    def getQueue(self) -> list | Dict:
        with open(self.file, "r") as f:
            contents = f.read()
            return json.loads(contents)

    def output(self, items) -> None:
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
