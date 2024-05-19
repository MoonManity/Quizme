import quizer as q

def main():
    tracker = q.Tracker("file.json")
    while tracker.bank:
        question = tracker.pickQuestion()
        tracker.handleAnswerChoices(question)
        tracker.handleUserAnswer()

    for i in tracker.topicsLog:
        for j in tracker.topicsLog[i]["missed_questions"]:
            print(j)

if __name__ == "__main__":
    main()

