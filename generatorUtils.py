import math
import random
import json
from os import path
from random import randrange
from typing import final
import numpy as np

#Method to convert from percentage to marks
def conversionUtil(totalMarks, easyPerc, medPerc, hardPerc):
    fEasyMarks, intEasyMarks = math.modf((int(easyPerc) * totalMarks)/100)
    fMedMarks,intMedMarks = math.modf((int(medPerc) * totalMarks)/100)
    fHardMarks,intHardMarks = math.modf((int(hardPerc) * totalMarks)/100)
    if(fEasyMarks == 0 and fMedMarks == 0 and fHardMarks == 0):
        return intEasyMarks, intMedMarks, intHardMarks
    else:
        raise Exception("Please enter percentages such that the mark distribution is in integers")
      
#Method to pick random list from a list of lists  
def randomPickUtil(optionList):
    randomVal = randrange(len(optionList))
    return(optionList[randomVal]["questionId"])

#Method to store back the value in json 
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

#Method generates the question paper
def generateQuestionPaperUtil(optionList):
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
        
#Util function to convert into specific input  
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

    
    
    
    
        