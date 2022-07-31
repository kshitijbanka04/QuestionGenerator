import math
import random
import json
from os import path
from random import randrange
from typing import final
import numpy as np

def conversionUtil(totalMarks, easyPerc, medPerc, hardPerc):
    fEasyMarks, intEasyMarks = math.modf((int(easyPerc) * totalMarks)/100)
    fMedMarks,intMedMarks = math.modf((int(medPerc) * totalMarks)/100)
    fHardMarks,intHardMarks = math.modf((int(hardPerc) * totalMarks)/100)
    if(fEasyMarks == 0 and fMedMarks == 0 and fHardMarks == 0):
        return intEasyMarks, intMedMarks, intHardMarks
    else:
        raise Exception("Please enter percentages such that the mark distribution is in integers")
        
def randomPickUtil(optionList):
    randomVal = randrange(len(optionList))
    return(optionList[randomVal]["questionId"])

def storeList(difficultyList, filename):
    jsonList = list()
    jsonDict = dict()
    jsonDict["questionId"] = list()
    jsonDict["marks"] = difficultyList[0]["marks"]
    for i in range(len(difficultyList)):
        jsonDict["questionId"].append(difficultyList[i]["questionId"])
    
    if(path.exists(filename)):
        file = open(filename)
        jsonList = json.load(file)
    
    jsonList.append(jsonDict)
    with open(filename, "w") as cachedfile:
        json.dump(jsonList, cachedfile)

def generateQuestionPaperUtil(optionList):
    # easyList = convertToListofList(optionList["Easy"])
    # medList = convertToListofList(optionList["Medium"])
    # hardList = convertToListofList(optionList["Hard"])
    
    # storeList(easyList, "Easy.json")
    # storeList(medList, "Med.json")
    # storeList(hardList, "Hard.json")
    
    # easySet = randomPickUtil(easyList)
    # medSet = randomPickUtil(medList)
    # hardSet = randomPickUtil(hardList)

    if(isinstance(optionList["Easy"][0][0], str)):
        randomVal = randrange(len(optionList["Easy"]))
        easySet = optionList["Easy"][randomVal]
    else:
        easyList = convertToListofList(optionList["Easy"])
        storeList(easyList, "Easy.json")
        easySet = randomPickUtil(easyList)
    if(isinstance(optionList["Medium"][0][0], str)):
        randomVal = randrange(len(optionList["Medium"]))
        medSet = optionList["Medium"][randomVal]
    else:
        medList = convertToListofList(optionList["Medium"])
        storeList(medList, "Med.json")
        medSet = randomPickUtil(medList)
    if(isinstance(optionList["Hard"][0][0], str)):
        randomVal = randrange(len(optionList["Hard"]))
        hardSet = optionList["Hard"][randomVal]
    else:
        hardList = convertToListofList(optionList["Hard"])
        storeList(hardList, "Hard.json")
        hardSet = randomPickUtil(hardList)
    questionPaper = easySet + medSet + hardSet
    random.shuffle(questionPaper)
    print("Question paper is :", questionPaper)
        
    
def convertToListofList(difficultyList):
    finalList = list()
    for i in range(len(difficultyList)):
        tempDict = convertToDictUtil(difficultyList[i])
        finalList.append(tempDict)
    return finalList

def convertToDictUtil(difficultyList):
    tempDict = dict()
    tempArray = list()
    marksSum = 0
    for i in range(len(difficultyList)):
        for j in range(len(difficultyList[i]["questionId"])):
            tempArray.append(difficultyList[i]["questionId"][j])
        marksSum += difficultyList[i]["marks"]
    tempDict["questionId"] = tempArray
    tempDict["marks"] = marksSum
            
    return tempDict

    
    
    
    
        