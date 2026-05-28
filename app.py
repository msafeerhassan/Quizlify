# retireve questions from json -> ask user about his question choices -> present questions accordinly -> track time -> 1 point if succeed, -1 if fail -> add features: leaderboard, score saving, interactive console ui, AI based questions etc using HCAI

import json, random, time
from inputimeout import inputimeout, TimeoutOccurred

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

maxTime = 15

try:
    with open('questions.json', 'r',) as file:
        rawData = json.load(file)
except FileNotFoundError:
    print("Error: The file doesn't exist")
except json.JSONDecodeError:
    print("Error: Can't Decode the JSON File")

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

userOption = ""
userScore = 0

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
            if userOption.upper() != "A" and userOption.upper() != "B" and userOption.upper() != "C" and userOption.upper != "D":
                print("Invalid Option Selected!")
                pass
            else:
                print(f"You selected option {userOption.upper()}")
                break
    except TimeoutOccurred:
        print("\nTime's up!!")
        userOption = 0
    if str(userOption.upper()) == question['answer']:
        print("Correct Answer!\n15 Points Awarded")
        userScore += 15
    elif str(userOption.upper()) != question['answer']:
        print("Oh! Wrong Answer :(\n5 Points Deducted")
        print(f"Correct Option: {question['answer']}")
        userScore -= 5
    elif str(userOption) == "0":
        print("You didn't selected any Option.\n5 Points Deducted")
    else:
        print("Invalid Option.")


print(userScore)