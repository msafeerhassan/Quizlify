# retireve questions from json -> ask user about his question choices -> present questions accordinly -> track time -> 1 point if succeed, -1 if fail -> add features: leaderboard, score saving, interactive console ui, AI based questions etc using HCAI

import json, random
from inputimeout import inputimeout, TimeoutOccurred

userOption = ""
userScore = 0
maxTime = 15

def chooseFieldDocument():
    while True:
        field = int(input("""Choose the general field of quiz:
                  1. Science
                  2. Python
                  Your Choice: """))
        if field == 1:
            field = "Science"
            break
        elif field == 2:
            field = "Python"
            break
        else:
            print("Error: Please either choose 1 or 2!")
            pass
    return field

def chooseDifficulty():
    while True:
        difficulty = int(input("""Choose the difficulty level:
                           1. Easy
                           2. Medium
                           3. Hard
                           Your Choice: """))
        if difficulty == 1:
            difficulty = "Easy"
            break
        elif difficulty == 2:
            difficulty = "Medium"
            break
        elif difficulty == 3:
            difficulty = "Hard"
            break
        else:
            print("Error: Please either choose 1, 2 or 3!")
            pass
    return difficulty

def openQuestionsFile():
    try:
        with open('questions.json', 'r',) as file:
            rawData = json.load(file)
    except FileNotFoundError:
        print("Error: The file doesn't exist")
    except json.JSONDecodeError:
        print("Error: Can't Decode the JSON File")
    return rawData

def retrieveQuestions(jsonData, category, difficultyLevel):
    questionsList = []
    for i in jsonData["questions"]:
        if i['category'].lower() == category.lower() and i['difficulty'].lower() == difficultyLevel.lower():
            questionsList.append(i)
        else:
            continue
    
    return questionsList

def randomizeList(questionsList):
    length = len(questionsList)
    randomList = random.sample(questionsList, k=length)
    return randomList

def mainDocument():
    global userScore, userOption, maxTime
    field = chooseFieldDocument()
    difficulty = chooseDifficulty()
    rawData = openQuestionsFile()
    for question in randomizeList(retrieveQuestions(rawData, field, difficulty)):
        print(question['question'])
        optionsDict = question['options']
        keys = list(optionsDict.keys())
        values = list(optionsDict.values())
        for i in range(4):
            print(f"Option {keys[i]}: {values[i]}")
        print("Time: 15 seconds")
        try:
            while True:
                userOption = inputimeout(prompt="Correct Option: ", timeout=15)
                if userOption.upper() != "A" and userOption.upper() != "B" and userOption.upper() != "C" and userOption.upper() != "D":
                    print("Invalid Option Selected!")
                    pass
                else:
                    print(f"You selected option {userOption.upper()}")
                    break
        except TimeoutOccurred:
            print("\nTime's up!!")
            userOption = "TIMEUP"
        
        if userOption == "TIMEUP":
            print("You didn't selected any option :(\n5 Points Deducted")
            userScore -= 5
        elif userOption.upper() == question['answer']:
            print("Correct Answer!\n15 Points Awarded")
            userScore += 15
        else:
            print("Oh! Wrong Option :(\n5 Points Deducted")
            userScore -= 5

mainDocument()

print(f"Final Score: {userScore}")