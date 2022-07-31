import json
from generatorUtils import *

file = open("questions.json")
data = json.load(file)
file.close()
questionBank = dict()
dp = [[]]
    
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
        listOfSolution.append(levelBank[i]["questionId"])
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
        listOfSolution.append(levelBank[i]["questionId"])
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
        print("No questions sum upto the given requirement")
        #TODO: Error Handling
        return
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

def paperGenerator(easy, med, hard):
    # Write the DP problem here but a bit modified according to the value
    listOfEasySet = findSets(easy, questionBank["Easy"], "Easy")
    listOfMedSet = findSets(med, questionBank["Medium"], "Medium")
    listOfHardSet = findSets(hard, questionBank["Hard"], "Hard")

# Need to write the CLI arguments for the smooth running
def main():
    totalMarks = input("Enter the total marks:")
    easyPerc = input("Enter percentage of marks allotted to easy level questions:")
    medPerc = input("Enter percentage of marks allotted to medium level questions:")
    hardPerc = input("Enter percentage of marks allotted to hard level questions:")
    
    easyMarks, medMarks, hardMarks = conversionUtil(int(totalMarks), easyPerc, medPerc, hardPerc)
    print(easyMarks, medMarks, hardMarks)
    
    easySum, medSum, hardSum = preprocess()
    if(easySum<int(easyMarks) or medSum<int(medMarks) or hardSum<int(hardMarks)):
        print("Please pass in valid inputs, the previous inputs are more than the marks present in the Question Bank")
    else:
        paperGenerator(int(easyMarks), int(medMarks), int(hardMarks))
    # print(possible_solution)
    questionPaper = list()
    generateQuestionPaperUtil(possible_solution)
main()