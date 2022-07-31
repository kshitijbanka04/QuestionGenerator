import json
from os import path
from random import randrange
from generatorUtils import *

file = open("questions.json")
data = json.load(file)
file.close()
questionBank = dict()
dp = [[]]
difficulty = ["Easy", "Medium", "Hard"]
    
    #NEED To write logger function

    #NOTE For the first computation we have nothing in the data base so initially solving it with a DP approach

    #Done: 1. First sort the questions into 3 seperate sub-dictionaries based on the difficulty 
    #Done: 2. Record the input of the difficulty of marks that is required will get the input from command line 
    #Done: 3. Traverse through this sub dictionary and find all the possible combinations of questions that sum up to that value
    #Done: 4. Store this list of lists in an dictionary again 
    #Done: 5. Put randomized list in the quetion paper then for all the categories and there you have your answer
    #Done: 6. Randomize the question paper
    #NOTE: For second computation onwards

    #TODO: 6. To search throught the existing db and use that 
    #TODO: 7. If present just use that list of lists in a randomized manner ---------------------- Aim to save computation
    #TODO: 8. If not present I will just look at the value that is required if its greater than the max value in db then will use
    #TODO: 9. First find the number and subtract the max marks question from that category and see if that exist in our db -------- Need to do some kind of recursion memoized dp here

    #NOTE: Can jagged array be used? ----- I guess so 
    
    #NOTE: Few things to keep in mind: Memoization would have extra auxilary stack space so we can use tabular form to get the answer and 
    #to optimize the space even more we can use the prev and cur 1D arrays instead of a complete 2D array but in this case I guess we can not use the prev and curr concept as we need to 
    #store the keys and not just count it


    # 10 + 8 + 7 = 25, 8 ----------- consider next turn 33 aajaata h toh we can use 25+8 = 33 we can solve the duplicate issues by checking that question present in the qictionary or not
possible_solution = dict()
possible_solution["Easy"] = list()
possible_solution["Medium"] = list()
possible_solution["Hard"] = list()
def appendToExhaustiveList(listOfSolution, difficulty):
    possible_solution[difficulty].append(listOfSolution)

def storeSolutionList(levelBank, i, sum, listOfSolution, difficulty):
    #We traverse back from last index to first and this is the edge case
    if(i == 0 and sum !=0 and dp[0][sum]):
        listOfSolution.append(levelBank[i])
        appendToExhaustiveList(listOfSolution, difficulty)
        listOfSolution = []
        return
    if(i==0 and sum==0):
        appendToExhaustiveList(listOfSolution, difficulty)
        listOfSolution = []
        return
    
    if(dp[i-1][sum]):
        tempList = []
        tempList.extend(listOfSolution)
        storeSolutionList(levelBank, i-1, sum, tempList, difficulty)

    if(sum>=levelBank[i]["marks"] and dp[i-1][sum-levelBank[i]["marks"]]):
        listOfSolution.append(levelBank[i])
        storeSolutionList(levelBank, i-1, sum-levelBank[i]["marks"], listOfSolution, difficulty)
        

def findSets(levelMarks, levelBank, difficulty):
    n = len(levelBank)
    if(n==0 or levelMarks<0):
        return "Error"
    global dp
    dp = [[False for i in range(levelMarks+1)] for j in range(n)]  #Initialize all to false
    #Define the base case
    for i in range(n):
        dp[i][0] = True
    if(levelBank[0]["marks"]<=levelMarks):
        dp[0][levelBank[0]["marks"]] = True
    
    for i in range(1, n):
        for j in range(0, levelMarks+1):
            if(levelBank[i]["marks"]<=levelMarks):
                dp[i][j] = (dp[i-1][j] or dp[i-1][j-levelBank[i]["marks"]])
            else:
                dp[i][j] = dp[i-1][j]
    if(dp[n-1][levelMarks]==False):
        raise Exception("No questions sum upto the given requirement")
    listOfSolution = []
    storeSolutionList(levelBank, n-1, levelMarks, listOfSolution, difficulty)

def preprocess():
    questionBank["Easy"] = list()
    questionBank["Medium"] = list()
    questionBank["Hard"] = list()
    easySum = medSum = hardSum = 0
    
    for i in range(len(data)):
        questionRow = dict()
        questionRow["questionId"] = list()
        if(data[i]["Difficulty"] == "Easy"):
            questionRow["questionId"].append(data[i]["question_id"])
            questionRow["marks"] = data[i]["Marks"]
            questionBank["Easy"].append(questionRow)
            easySum += data[i]["Marks"]
        elif(data[i]["Difficulty"] == "Medium"):
            questionRow["questionId"].append(data[i]["question_id"])
            questionRow["marks"] = data[i]["Marks"]
            questionBank["Medium"].append(questionRow)
            medSum += data[i]["Marks"]
        else:
            questionRow["questionId"].append(data[i]["question_id"])
            questionRow["marks"] = data[i]["Marks"]
            questionBank["Hard"].append(questionRow)
            hardSum += data[i]["Marks"]
        
    return easySum, medSum, hardSum


# Need to write the CLI arguments for the smooth running
def searchList(cachedList, marks, difficulty):
    for i in range(len(cachedList)):
        if(cachedList[i]["marks"]==marks):
            possible_solution[difficulty] = cachedList[i]["questionId"]
            return True
            #TODO Select amonsgt the list of lists in random
        else:
            findSets(marks, questionBank[difficulty], difficulty)
            return False
             
        
def main():
    totalMarks = input("Enter the total marks:")
    easyPerc = input("Enter percentage of marks allotted to easy level questions:")
    medPerc = input("Enter percentage of marks allotted to medium level questions:")
    hardPerc = input("Enter percentage of marks allotted to hard level questions:")
    
    try:
        easyMarks, medMarks, hardMarks = conversionUtil(int(totalMarks), easyPerc, medPerc, hardPerc)
        print(easyMarks, medMarks, hardMarks)
    except Exception as e:
        print(e)
        return
    
    easySum, medSum, hardSum = preprocess()
    if(easySum<int(easyMarks) or medSum<int(medMarks) or hardSum<int(hardMarks)):
        print("Please pass in valid inputs, the previous inputs are more than the marks present in the Question Bank")
        return
    else:
        try:
            if(path.exists("Easy.json") and path.exists("Med.json") and path.exists("Hard.json")):
                #TODO: Make use of LRU CACHE and also find If not found we need to go the other way round bby finding the complete solution
                file = open("Easy.json")
                easyCachedList = json.load(file)
                file.close()
                file = open("Med.json")
                medCachedList = json.load(file)
                file.close
                file = open("Hard.json")
                hardCachedList = json.load(file)
                file.close
                searchList(easyCachedList, int(easyMarks), "Easy")
                searchList(medCachedList, int(medMarks), "Medium")
                searchList(hardCachedList, int(hardMarks), "Hard")
                generateQuestionPaperUtil(possible_solution)
            else:
                #This would just run in the first case as we wont be having any cached data
                findSets(int(easyMarks), questionBank["Easy"], "Easy")
                findSets(int(medMarks), questionBank["Medium"], "Medium")
                findSets(int(hardMarks), questionBank["Hard"], "Hard")
                generateQuestionPaperUtil(possible_solution)
                
        except Exception as e:
            print(e)
            return
    # print(possible_solution)
    
main()