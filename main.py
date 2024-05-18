import quizer as q

#This is a test change for Github push
def main():
    questions = q.getQueue("file.json")
    tracker = q.Tracker(questions)
    while tracker.bank:
        term = tracker.pickTerm()
        tracker.output(tracker.currentTerm["question"])
        tracker.handleAnswerChoices(term)
        tracker.handleUserAnswer()

if __name__ == "__main__":
    main()

