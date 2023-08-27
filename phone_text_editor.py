#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 19:30:38 2023

@author: adi
"""

################################################################################
# CSE 231 Project 9
#Write a function that prompts user to input valid filename to open it. If filename is invalid then error message is printed and user is prompted to enter a valid one.
#Write a read functions such that it returns a set of words. Have to omit words with punctuatoin between but not words that are wrapped by or has a punctuation in the beginning or end.
#Write fill_completions function which that returns a dictionary of dictionaries of words which are arranged by the placement of a given letter at a specified index.
#Write find_completions function that returns a dictionary of words that have a prefix which is used to search though the indexed words from the previous fucntion.
#The main rquires to call the functoins based on the what is inputted for the prefix.
################################################################################
'''
Main data structure is a dictionary
   word_dic[(i,ch)] = set of words with ch at index i
'''
import string

def open_file():
    # Write a function that prompts user to input valid filename to open it. If filename is invalid then error message is printed and user is prompted to enter a valid one.
    while True:
        file_name = input("\nInput a file name: ")
        try:
            fp = open(file_name, encoding = 'UTF-8')
            return fp # returns filepointer
        except: # incase of invalid filename inputted
            print("\n[Error]: no such file")


def read_file(fp):
    #This functions  returns a set of words. Have to omit words with punctuatoin between but not words that are wrapped by or has a punctuation in the beginning or end. 
    set_word1=set()
    set_word2=set()
    for line in fp:
        line = line.split()#split the line seperated by spacing
        for word in line:
            word = word.strip(string.punctuation).lower()#removes the wrapped punctuation
            if len(word)>1: # check if word lenght is more than 1
                if word[-1] in string.punctuation:#checks if the last element of string is a punctuation
                    word = word[:-1]
                    set_word1.add(word) #adds all the words that had a punctuation without the punctuation
                if word[-1] not in string.punctuation: # returns rest of the words
                    set_word2.add(word)

            set3 = set_word1.union(set_word2) # finds intersection of the 2 sets to eliminate reoccuring words

    list1= list(set3) 
    for word in list1:
        for ch in word:
            if ch in string.punctuation:
                try:
                    set3.remove(word)# removes with punctuation inbetween the word with punctuation.
                except:
                    continue
        continue
    return set3


def fill_completions(words):
    # The fill_completions function returns a dictionary of dictionaries of words which are arranged by the placement of a given letter at a specified index.
    dict_word={}
    set_keys=set()
    for element in words:
        element=element.lower()
        for i, ch in enumerate(element):
            if (i,ch) not in dict_word:
                dict_word[(i,ch)] = set() # checks if the index and character in the dictionary and if not returns empty set
    for key in dict_word:
        for element in words:
            element=element.lower()
            for i, ch in enumerate(element):
                if key[0] == i and key[1] == ch:# checks if the indexing of the words form the argument matches the index and character of the key.
                    dict_word[key].add(element)
    return dict_word


def find_completions(prefix,word_dic):
    # This function that returns a dictionary of words that have a prefix which is used to search though the indexed words from the previous fucntion.
    if len(prefix) == 0:# returns empty set if no prefix is inputted.
        return set()
    if len(prefix) == 1:# returns a set of words that beings with that letter since the prefix length is only one.
        if (0,prefix) in word_dic.keys():
            set_words = word_dic[(0,prefix)]
        return set_words

    elif len(prefix) > 1:
        list_sets=[]
        for index,val in enumerate(prefix):
            if (index,val) in word_dic.keys():# if the key and index match with the key values of the word_dic dictionary.
                set_words = word_dic[(index,val)]#the values are intialized as set of words which is then appended to a list
                list_sets.append(set_words)
        result = list_sets[0]
        for i in list_sets[1:]:
            result = result&i
        return result
    




def main(): 
    #The main rquires to call the functoins based on the what is inputted for the prefix.      
    fp = open_file()
    set_words = read_file(fp)
    word_dic= fill_completions(set_words)
    while True:
        prefix = input("\nEnter a prefix (# to quit): ")
        if prefix == "#":#quits program
            print("\nBye")
            break
        else:
            pre = ""
            for i,val in enumerate(prefix):
                for key in word_dic.keys():
                    if i == key[0] and val == key[1]:#slicing by checking if index and value/ch matches the key of the word_dic's keys.
                        pre = pre+val # stores the words that meets the condition
            if pre != prefix:            
                print("\nThere are no completions.")
            else:
                sorted_list = sorted(find_completions(prefix,word_dic))# sorts the list of the words that satisfy the condition in alphabetical order
                if len(sorted_list) == 0:
                    print("\nThere are no completions.") 
                else:
                    res = ", ".join(sorted_list) # joins the words using join function
                    print(f"\nThe words that completes {prefix} are: {res}")
                    
                    
                    
            



if __name__ == '__main__':
    main()