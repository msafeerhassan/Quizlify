# retireve questions from json -> ask user about his question choices -> present questions accordinly -> track time -> 1 point if succeed, -1 if fail -> add features: leaderboard, score saving, interactive console ui, AI based questions etc using HCAI

import json, random, os
from inputimeout import inputimeout, TimeoutOccurred
from openrouter import OpenRouter
from dotenv import load_dotenv

load_dotenv()

userOption = ""
userScore = 0
maxTime = 15

def userNameAsk():
    while True:
        userName = str(input("Enter your name: "))
        if userName == "" or len(userName) <= 2:
            print("Please enter your name!")
            pass
        else:
            return userName

def userIntentAsk(username):
    while True:
        userIntent = int(input(f"""Hey {username}, would you like to:
                               1. Play Game against Document Questions
                               2. Play Game against AI
                               3. Check Leaderboard
                               4. Exit
                               Your Choice: """))
        if userIntent == 4:
            print("Exiting...")
            exit()
        elif userIntent == 1 or userIntent == 2 or userIntent ==3:
            return userIntent
        else:
            print("Error: Please either choose from 1, 2, 3 or 4.")
            pass

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

def openSampleQuestionsFile():
    try:
        with open('sample.json', 'r',) as file:
            rawData = json.load(file)
    except FileNotFoundError:
        print("Error: The file doesn't exist")
    except json.JSONDecodeError:
        print("Error: Can't Decode the JSON File")
    return rawData

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

def saveScore(username, score):
    scoreDict = {}
    try:
        with open('score.txt', 'r') as scoreFile:
            lines = scoreFile.readlines()
            for line in lines: 
                line = line.strip()
                if ":" in line:
                    lineParts = line.split(":")
                    existName = lineParts[0]
                    existScore = int(lineParts[1])
                    scoreDict[existName] = existScore
    except FileNotFoundError:
        pass

    if username in scoreDict:
        scoreDict[username] += score
    else:
        scoreDict[username] = score
    
    try:
        with open('score.txt', 'w') as scoreFile:
            for name, finalScore in scoreDict.items():
                scoreFile.write(f"{name}:{finalScore}\n")
        print("Score Recorded Successfully!")
    except Exception as e:
        print(f"Error: {e}")

def leaderboard():
    try:
        with open('score.txt', 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("No file found :(")
        return
    
    print("LEADERBOARD:")

    for line in lines:
        line = line.strip()
        if ":" in line:
            lineParts = line.split(":")
            name = lineParts[0]
            score = lineParts[1]

            print(f"{name} -> {score} Points")
    print("\n")

def callAI(topic, difficulty, jsonData):
    client = OpenRouter(
        api_key= os.getenv("API_KEY"),
        server_url="https://ai.hackclub.com/proxy/v1"
    )
    prompt = f"Generate 5 MCQs on {topic} ({difficulty} difficulty). Respond ONLY in this JSON format: {jsonData}"
    response = client.chat.send(
        model="qwen/qwen3-32b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=False,
    )
    data = response.choices[0].message.content
    return json.loads(data)

def mainAIBasedGamePlay(userName):
    global userScore, userOption, maxTime
    userScore = 0
    field = str(input("Enter the general field of quiz like Coding, Science, Astronomy etc: "))
    difficulty = chooseDifficulty()
    rawData = callAI(field, difficulty, openSampleQuestionsFile())
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
    saveScore(userName, userScore)

def mainDocumentBasedGamePlay(userName):
    global userScore, userOption, maxTime
    userScore = 0
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
    saveScore(userName, userScore)

def playAgainAsk():
    while True:
        consent = str(input("Would you like to play again (y/n): "))
        if consent.lower() != "y" and consent.lower() != "n":
            print("Please either choose Y or N!")
            pass
        elif consent.lower() == "y":
            return True
        elif consent.lower() == "n":
            exit()

userName = userNameAsk()
userIntent = userIntentAsk(userName)

if userIntent == 1:
    while True:
        mainDocumentBasedGamePlay(userName)
        if playAgainAsk() == True:
            pass
        else:
            break
elif userIntent == 2:
    while True:
        mainAIBasedGamePlay(userName)
        if playAgainAsk() == True:
            pass
        else:
            break
elif userIntent == 3:
    leaderboard()
else: pass