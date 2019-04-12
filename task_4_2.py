import argparse
from difflib import SequenceMatcher




if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()



    output_file = open("task_4_2_result.txt","w+")

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
def findCommonPrefixes(string , arr):
    out = []
    for item in arr:
        if item == string:
            out.insert(arr.index(item),"")
        else:
            match = ""
            i = 0
            length = len(item)
            while(i<length):
                if(i<len(string) and item[i]==string[i]):
                    match = match+item[i]
                else:
                    break
                i+=1
            out.append(match)
    return out

def findCommonPrefixes2(string,arr):
    arr2 = findCommonPrefixes(string,arr)
    match = ""
    for item in arr2:
        if(not item==""):
            match = item
            break
    arr2[arr.index(string)] = match
    return arr2

def findLengthOfCommonPrefix(arr):
    number = 0
    for item in arr:
        if not item=="":
            number+=1
    return number

def selectAGoodString(arr):
    output = ""
    for item in arr :
        output = item
        currentPrefixArray = findCommonPrefixes(item,arr)
        if(findLengthOfCommonPrefix(currentPrefixArray)>0):
            return output
    return output





def getIndexOfANonEmptyCell(arr):
    i = 0
    while(i<len(arr)):
        if(not arr[i]==""):
            return i
        else:
            i+=1
    return None

#Returns the list of remaining Characters after taking Common Factors

def takeCommonFactors(arrayOfOriginalStrings , arrayOfCommonFactors):
    out = []
    i = 0
    currentPrefix = max(arrayOfCommonFactors,key=len)
    while(i<len(arrayOfCommonFactors)):
        string = ""
        if not arrayOfCommonFactors[i]=="":
            string = arrayOfOriginalStrings[i]
            if(string==currentPrefix):
                string= ""
            if(not string==currentPrefix and string[0:len(currentPrefix)]==currentPrefix):
                string = string[len(currentPrefix):len(string)]
                #out.append(string[len(currentPrefix):len(string)])
            if arrayOfCommonFactors[i]==arrayOfOriginalStrings[i]:
                    string= "epsilon"
                    #out.append(string)
        out.append(string)
        i+=1
    return out



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

    print (finalizedRules)
    #bool = True
    allZeros = False
    condition = True
    prefixesDict = dict()
    newCharacterSymbol = keyGivenIndex(0,finalizedRules)
    while (condition):
        newGeneratedRules = dict()
        lengthOfRules = len(finalizedRules)
        i = 0
        while(i<lengthOfRules):
            aGoodString = selectAGoodString(finalizedRules[keyGivenIndex(i,finalizedRules)])
            #No good strings so that means that we cant take any more common factors from this rule so the old rule will be = to the new rule
            if(aGoodString == ""):
                i=i+1
            else:
                arrayOfCommonFactors = findCommonPrefixes2(aGoodString,finalizedRules[keyGivenIndex(i,finalizedRules)])
                arrayOfRemainingChars = takeCommonFactors(finalizedRules[keyGivenIndex(i,finalizedRules)],arrayOfCommonFactors)
                #indexOfGoodString = arrayOfRemainingChars.index(aGoodString)
                #AGoodCommonFactor = ""
                #for item in arrayOfCommonFactors:
                 #   if(not item==""):
                  #      AGoodCommonFactor = item
               #arrayOfRemainingChars[indexOfGoodString]= AGoodCommonFactor
                #newCharacterSymbol = keyGivenIndex(i,finalizedRules) + "'"
                newCharacterSymbol = newCharacterSymbol+"'"
                #print(newCharacterSymbol)
                #Creation of New Rules
                newRuleRightSide = []
                oldRuleRightSide = []
                j = 0
                while(j<len(arrayOfRemainingChars)):
                    if(finalizedRules[keyGivenIndex(i,finalizedRules)][j]==arrayOfRemainingChars[j]):
                        oldRuleRightSide.append(arrayOfRemainingChars[j])
                    if(not arrayOfRemainingChars[j]=="" and not finalizedRules[keyGivenIndex(i,finalizedRules)][j]==arrayOfRemainingChars[j]):
                        newRuleRightSide.append(arrayOfRemainingChars[j])
                    j+=1

                currentPrefix = ""
                for string in arrayOfCommonFactors:
                    if not string=="":
                        currentPrefix=string
                        break
                j = 0
                while(j<len(arrayOfCommonFactors)):
                    originalArray = finalizedRules[keyGivenIndex(i,finalizedRules)]
                    if(arrayOfCommonFactors[j]==""):
                        oldRuleRightSide.append(originalArray[j])
                    else:
                        if arrayOfCommonFactors[j] == currentPrefix :
                            oldRuleRightSide.append(currentPrefix+"" + newCharacterSymbol)

                    j+=1

               # print("New Rule Right Side = " + str(newRuleRightSide))
                #print("Old Rule Right Side = " + str(oldRuleRightSide))
                newGeneratedRules.update({keyGivenIndex(i,finalizedRules):oldRuleRightSide})
                newGeneratedRules.update({newCharacterSymbol:newRuleRightSide})
                i+=1

                #Check that Remaining rules are presented in new Generated Rules
            if(len(newGeneratedRules)==0):
                newGeneratedRules = finalizedRules
            else:
                for key,value in finalizedRules.items():
                    if(finalizedRules.__contains__(key) and newGeneratedRules.__contains__(key)):
                        finalizedRules.update({key: newGeneratedRules[key]})
            #Finalized Rules has updated Rules but Not the new Rules , We need a loop for the newly created Rules Too

        for key,value in newGeneratedRules.items():
            if( not finalizedRules.__contains__(key)):
                finalizedRules.update({key:value})

        for x,y in finalizedRules.items():
            y = removeDuplicates(y)
            finalizedRules[x] = y
        print(finalizedRules,"X")
        bool = False
        print(finalizedRules)
        for key,value in finalizedRules.items():
            currentArray = finalizedRules[key]
            if(len(currentArray)>0):
                 currentArray = findCommonPrefixes2(currentArray[0],currentArray)
                 print(currentArray)
            else:
                bool = False
                break
            if(findLengthOfCommonPrefix(currentArray)>0):
                #finalizedRules = newGeneratedRules
                print(findLengthOfCommonPrefix(currentArray))
                bool = True
                break
            bool = True
        if(not bool):
            condition= False



            #We need to check that all Common Prefixes for all rules length is 0 then we are done




        #allZeros = True
        #if all Zeroes mean that there are no remaining common factors so we can now terminate this loop and print rules
        # if there are remaining zeroes then the operation must go on on the new set of rules
        #bool= False
    new2 =dict()
    for key,idx in newGeneratedRules.items():
        currentArray = newGeneratedRules[key]
        currentArray = removeDuplicates(currentArray)
        if(currentArray.__contains__("epsilon")):
            currentArray.remove("epsilon")
            currentArray.append("epsilon")
        new2.update({key:currentArray})
        if(len(idx)==0):
            new2.pop(key)

    print(new2)

    for key,index in new2.items():
      if(len(index)>0):
        for char in key :
            i = key.index(char)
            if(i < len(key)-1 and key[i+1] == "'") :
                print("XXX")
               # output_file.write(char + "'"+" ")

            elif (char=="'"):
                break
            else:
                print("XXXX")
                #output_file.write(char + " ")
        output_file.write(key + " : ")

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




