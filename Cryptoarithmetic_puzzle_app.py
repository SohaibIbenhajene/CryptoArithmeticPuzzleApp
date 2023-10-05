from simpleai.search import CspProblem, backtrack
import streamlit as st

#input_str = input("Enter a CryptoArithmetic puzzle in the format 'TO + GO = OUT':").upper()
input_str = st.text_input("Enter a CryptoArithmetic puzzle in the format 'TO + GO = OUT':").upper()
# Initialize the domain and seen set
domains = {}
seen = set()
# Split the input string, so you get all of the words in a list
words = input_str.split()

def extract_letters(input_str, seen=None):
    # If seen has not been initialized, then initialize it
    if seen is None:
        seen = set()

    # Base case: if the input string is empty, return an empty list
    if len(input_str) == 0:
        return []

    # Check if the first character is a letter and also not in the seen set
    if input_str[0].isalpha() and input_str[0] not in seen:
        # Add the letter to the seen set
        seen.add(input_str[0])
        # Add it to the end result and call the function again
        return [input_str[0]] + extract_letters(input_str[1:], seen)
    else:
        # If it's not a letter, skip it and continue with the rest of the string
        return extract_letters(input_str[1:], seen)

# Change the list into a tuple so it can't be changed
variables = tuple(extract_letters(input_str))

# Iterate through each variable
for variable in variables:
    for word in words:
        # Check which letters are the first of the words and add them to the seen set
        if word[0] == variable and word[0] not in seen:
            seen.add(word[0])

    # If the letter is in the seen set, make the range from 1 to 10 because the first letter can't be 0
    if variable in seen:
        domains[variable] = list(range(1, 10))
        # Otherwise make the range for the letter from 0 to 10
    else:
        domains[variable] = list(range(0, 10))

# The unique constraint to make sure there are no double letters in the variables tuple
def constraint_unique(variables, values):
    return len(values) == len(set(values))

# The constraint to create the formula
def constraint_add(variables, values):
    # Initialize the variables
    factor1 = factor2 = result = ""
    i = 0

    # Loop trough all the words from the input but skip one each time to only get the words
    for word in words[0::2]:
        for letter in word:
            # Make sure you get the correct letter index according to the input and get the values of this letter
            number = str(values[variables.index(letter)])
            # Use the counter to fill up the right variable trough each loop
            if i == 0:
                factor1 += number
            elif i == 1:
                factor2 += number
            elif i == 2:
                result += number
        i += 1
    # Return the correct formula according to what you filled into the input
    return (int(factor1) + int(factor2)) == int(result)

constraints = [
    (variables, constraint_unique),
    (variables, constraint_add),
]

problem = CspProblem(variables, domains, constraints)

output = backtrack(problem)
#print('\nSolutions:', output)
st.write('\nSolutions:', output)