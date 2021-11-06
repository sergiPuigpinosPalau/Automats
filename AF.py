#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

AT = {}
alfabet = []
finalStates = []

debug = 0

def read():
    global AT
    f = open("./AFS")
    for line in f:
        l = line.split(',')
        other = "NONE"
        if len(l) == 4:
            other = l[3].rstrip()
        addToAF(AT, l[0], l[1], l[2].rstrip(), other)
    print(AT)
    print("finalstates")
    print(finalStates)
    print("alfabet")
    print(alfabet)

def addToAF(inputAT, state, letter="", value="", other=""):
    if letter == "":
        inputAT[state] = {}
    elif state not in inputAT:
        inputAT[state] = {letter:[value]}
    else:
        dictState = inputAT[state]
        if letter in dictState:
            dictState[letter].append(value)
        else:
            dictState[letter] = [value]
    if inputAT == AT:
        if letter not in alfabet and letter != "":
            alfabet.append(letter)
        if other == "F" and other not in finalStates:
            finalStates.append(state)    

def readLetter(inputAT, state, letter):  
    if state not in inputAT:
        return -1       
    dictState = inputAT[state]
    if letter in dictState:
        return dictState[letter]
    else:
        return -2

def recursiveRead(word, states):
    if debug:
        print("WORD: "+word+" STATES: "+str(states))
    stateCounter = 1
    #Base case
    #Check if they are finals in case of recursive
    if not word:
        return states in finalStates
    #Recursive case
    for state in states:
        if debug:
            print("LOOP STATES: "+state)
        wordCounter = 1
        currentState = state
        for letter in word:
            rtVal = readLetter(AT, currentState, letter)
            if rtVal == -2:
                #print("Letter doesn't go to any state")
                break
            if debug:
                print("RTVAL: "+str(rtVal))
            if len(rtVal) > 1:
                #If it returns more than one state, check their paths and if one leads to a final state exit
                if not recursiveRead(word[wordCounter:], rtVal):
                    break
                else:
                    return True
            elif len(rtVal) == 1:
                currentState = rtVal[0]
            #Check if final
            if debug:
                print("wordCounter: "+str(wordCounter))
            if wordCounter == len(word) and stateCounter == len(states):
                return currentState in finalStates
            wordCounter += 1
        stateCounter += 1 
    return False         

def determine():
    global AT, finalStates
    newAT = {}
    newFinalStates = []
    addToAF(newAT, "0")
    pendingStates = list(newAT)
    while pendingStates: 
        if debug:
            print("PENDING:"+str(pendingStates))      
        for state in list(pendingStates):
            pendingStates = []
            subStates = state.split(".")
            for letter in alfabet:
                newState = ""
                alreadyInState = []
                for subState in subStates:
                    rtStates = readLetter(AT, subState, letter)
                    if rtStates == -2:
                        continue
                    for rtState in rtStates:
                        #Avoid repeating numbers
                        if rtState not in alreadyInState:
                            newState += rtState+"."
                    alreadyInState = rtStates 
                newState = newState[:-1] 
                #Add conection to the parent
                addToAF(newAT, state, letter, newState)
                if newState not in list(newAT):
                    #Add state into the new AT
                    addToAF(newAT, newState)
                    pendingStates.append(newState) 
                    #Check if new state is final state
                    newSubStates = newState.split(".")
                    for newSubState in newSubStates:
                        if newSubState in finalStates:
                            newFinalStates.append(newState)
                            break 
                if debug:            
                    print("final state")
                    print(newState)
    print(newAT)
    AT = newAT
    print("Final states: ", str(newFinalStates))
    finalStates = newFinalStates

def commands():
    global AT, debug
    exit = 0
    while(exit==0):
        command = input("Insert instruction: \n")
        if command == "quit":
            exit = 1
        elif command == "debug":
            debug = 1
            pass
        elif command == "read_letter":
            stateAndLetter = input("Insert state and letter\n")
            l = stateAndLetter.split(",")
            rtVal = readLetter(AT, l[0], l[1])  
            if rtVal == -1:
                print("State not valid")
            elif rtVal == -2:
                print("letter not in dictionary")
            else:
                print(rtVal)
        elif command == "determine":
            determine() 
        elif command == "read_word":
            while 1:
                word = input("Insert word\n")
                if word == "quit":
                    break
                print("RESULT: "+str(recursiveRead(word, "0")))                

def main():
    read()
    commands()

main()
