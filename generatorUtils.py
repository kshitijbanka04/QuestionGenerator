import math
import random
from random import randrange
import numpy as np

def conversionUtil(totalMarks, easyPerc, medPerc, hardPerc):
    fEasyMarks, intEasyMarks = math.modf((int(easyPerc) * totalMarks)/100)
    fMedMarks,intMedMarks = math.modf((int(medPerc) * totalMarks)/100)
    fHardMarks,intHardMarks = math.modf((int(hardPerc) * totalMarks)/100)
    if(fEasyMarks == 0 and fMedMarks == 0 and fHardMarks == 0):
    #TODO Raise exception
        return intEasyMarks, intMedMarks, intHardMarks
    
    else:
        return -1, -1, -1
        #TODO Raise exception
        
def randomPickUtil(optionList):
    randomVal = randrange(len(optionList))
    return(optionList[randomVal])

def generateQuestionPaperUtil(optionList):
    easyList = convertToArrayUtil(randomPickUtil(optionList["Easy"]))
    medList = convertToArrayUtil(randomPickUtil(optionList["Medium"]))
    hardList = convertToArrayUtil(randomPickUtil(optionList["Hard"]))
    
    questionPaper = easyList + medList + hardList
    random.shuffle(questionPaper)
    print(questionPaper)
    
    
def convertToArrayUtil(difficultyList):
    tempArray = list()
    for i in range(len(difficultyList)):
        for j in range(len(difficultyList[i])):
            tempArray.append(difficultyList[i][j])
            
    return tempArray
    
    
    
    
        