import argparse




if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    print(args.file)

    output_file = open("task_4_1_result.txt","w+")

def removeBackN(input):
    output =""
    for char in input:
        if(not char=="\n"):
            output=char
    return output

def calculateAlphas(char , arrayOfStrings ):
    alphas = []
    index = len(char)
    for string in arrayOfStrings:
        i = 0
        bool = True
        while (i<index):
            if(len(char)>len(string)):
                bool = False
                break
            if(not char[i]== string[i]):
                bool = False
                break
            if(char[i] == string[i]):
                i+=1
        if(bool):
            alphas.append(string[index:len(string)])
    return  alphas
def calculateBetas(char , arrayOfStrings):
    betas = []
    index = len(char)
    for string in arrayOfStrings:
        i = 0
        bool = True
        if(len(char)> len(string)):
            bool = True
        if(char == string[0:index]):
            bool = False
        if(bool):
            betas.append(string)
    return  betas



def eliminateImmediateLeftRecursion(char ,setOfRules):
    output = dict()
    alphas = calculateAlphas(char,setOfRules)
    if(len(alphas)==0):
        output.update({char:setOfRules})
        return output

    betas = calculateBetas(char,setOfRules)
    originalRuleModified = []
    newCharacterNewRules = []
    newDashedChar = char + "'"
    for rule in betas :
        originalRuleModified.append(rule+ newDashedChar)
    for rule in alphas :
        newCharacterNewRules.append(rule + newDashedChar)
    newCharacterNewRules.append("epsilon")
    output.update({char : originalRuleModified} )
    output.update({newDashedChar : newCharacterNewRules})
    return  output


def performSubstitution(rule , setOfRules, key):
    newSetOfRules = []
    for i in setOfRules:
        placeHolder = rule
        placeHolder = placeHolder.replace(key,i)
        #print(placeHolder)
        newSetOfRules.append(placeHolder)
    return  newSetOfRules


def keyGivenIndex(index,x):
    i = 0
    for key,value in x.items():
        if index == i:
            return key
        i+=1
    return None

def removeDuplicates(arr):
    arr2 = []
    for element in arr :
        if(not arr2.__contains__(element)):
            arr2.append(element)
    return arr2


with open(args.file,"r")as file :
    field = ""
    rules = []
    finalizedRules = dict()
   # for line in file:
    #    rule =  line.split(" ")
     #   newRule =[]
      #  for alpha in rule:
       #     out = removeBackN(alpha)
        #    newRule.append(out)
        #rules = rules + newRule
    for line in file :
        rule = line.splitlines()
        rules = rules + rule
    for rule in rules:
        currentRule = rule.split(" ")
        i = 0
        currentLeftVariable = "" # LeftMost variable to be appended as the index in the dictionary
        currentCompleteRightRule = [] # The Complete Right Rule to be added to the dictionary
        leftMostVariable = ""
        rightRule = ""
        indexofColon = currentRule.index(":")
        while(i<len(currentRule)):
            if(not currentRule[i]==":" and i<indexofColon):
                leftMostVariable = leftMostVariable+currentRule[i]
            if(currentRule[i]==":"):
                currentLeftVariable = leftMostVariable
            if(not currentRule[i]=="|" and i > indexofColon):
                rightRule = rightRule + currentRule[i]
            if(currentRule[i]=="|" and i>indexofColon):
                currentCompleteRightRule.append(rightRule)
                rightRule = ""
            i+=1
        currentCompleteRightRule.append(rightRule)
        finalizedRules.update({currentLeftVariable:currentCompleteRightRule})
    #Finished Parsing Input Here and placed it into Finalized Rules

    #Started with Left Recursion Elimination Algorithm
    print(finalizedRules)
    i = 0
    newRules = dict()
    visitedKeys = []
    for key,items in finalizedRules.items():
        j = 0
        AiKey = keyGivenIndex(i , finalizedRules)
        AiRules = finalizedRules[key]
        AiNewRules = []
        while(j<=i-1):
            AjKey = keyGivenIndex(j,finalizedRules)
            #AiRules = newRules[AiKey] We want to read the New Rules on the fly
            AjRules = finalizedRules[AjKey]
            print("AI Rules " + str(AiRules))
            lengthOfAiKey = len(AiKey)
            lengthOfAjKey = len(AjKey)
            arrayOfSubstitutions= []
            for rule in AiRules:

                if(visitedKeys.__contains__(AjKey)):
                    AjRules = newRules[AjKey]
               # print(AjRules)
                if(rule[0:lengthOfAiKey]==AjKey):
                    arr = performSubstitution(rule , AjRules,AjKey)
                    arrayOfSubstitutions = arrayOfSubstitutions + arr
                else:
                    arrayOfSubstitutions.append(rule)
            print("Array of Substitutions " + str(arrayOfSubstitutions))
            AiNewRules = arrayOfSubstitutions
            AiNewRules = removeDuplicates(AiNewRules)
           # print("Ai New rules ")
            print(AiNewRules)
            #Perform substitution with each rule of Aj in rules of Ai
            AiRules = AiNewRules
            j+=1
        if(not len(AiNewRules)==0):
            newRules.update({AiKey:AiNewRules})
        else:
            AiNewRules = AiRules
        newRules.update(eliminateImmediateLeftRecursion(AiKey,AiNewRules))

       # newRules.update(eliminateImmediateLeftRecursion(AiKey,finalizedRules[AiKey]))
        visitedKeys.append(AiKey)
        i+=1
    print(newRules)

   # for key,idx in newRules.items():
    #    for char in key:
     #       output_file.write(char + " ")
      #  output_file.write(": ")
       # for string in idx:
        #    if string == "epsilon":
         #       output_file.write("epsilon" + " ")
          #  elif not (string== idx[len(idx)-1]):
           #     for element in string :
            #       output_file.write(element + " ")
             #   output_file.write("| ")
           # else:
            #    for element in string :
             #      idxOfElement = string.index(element)
              #     if(idxOfElement< len(string)-1):
               #        if not string[idxOfElement+1]=="'":
                #          output_file.write(element + " ")
                 #      else:
                  #         output_file.write(element + "'")

       # output_file.write("\n")

    for key,index in newRules.items():
        for char in key :
            i = key.index(char)
            if(i < len(key)-1 and key[i+1] == "'") :
                output_file.write(char + "'"+" ")
            elif (char=="'"):
                break
            else:
                output_file.write(char + " ")
        output_file.write(": ")

        for string in  index :

            if string== "epsilon":
                output_file.write("epsilon"+ " ")
            elif ( not string  == index[len(index)-1]):
                  i= 0
                  while(i<len(string)-1):
                      if(i==len(string)-1 and not i =="'"):
                          output_file.write(string[i])
                      elif(i==len(string)-1 and i=="'"):
                          print("hello")
                      elif (i<len(string)-1 and string[i+1]=="'"):
                          output_file.write(string[i]+"")
                      elif(i<len(string)-1 and not string[i+1]=="'"):
                          output_file.write(string[i]+ " ")
                      i+=1
                  output_file.write(string[i] + " | ")
            else:
                  i= 0
                  while(i<len(string)-1):
                      if(i==len(string)-1 and not i =="'"):
                          output_file.write(string[i])
                      elif(i==len(string)-1 and i=="'"):
                          print("hello")
                      elif (i<len(string)-1 and string[i+1]=="'"):
                          output_file.write(string[i]+"")
                      elif(i<len(string)-1 and not string[i+1]=="'"):
                          output_file.write(string[i]+ " ")
                      i+=1
                  output_file.write(string[i])
        output_file.write("\n")



             #     while(i<len(string):
               #     j = string.index(character)
                #    print(i)
               ##     if(i<len(string)-1 and string[i+1]== "'"):
                 #       output_file.write(string[i])
                 #   elif (character == "'"):
                  #      output_file.write("'"+ " ")
                 #   else:
                 #       output_file.write(character + " ")
                 # output_file.write("| ")
            #else:
             #   for character in string:
              #      i = string.index(character)
               #     if(i<len(string)-1 and string[i+1]== "'"):
                #        output_file.write(string[i])
                 #   elif (character == "'"):
                  #      output_file.write("'"+ " ")
                   # else:
                    #    output_file.write(character + " ")











