# Input: a string with only English letters and whitespace
# Task: return the string with vowels capitalized and consonants decapitalized

def vowel(line):
    vowels = ('a', 'e', 'i', 'o', 'u')
    return "".join([x.upper() if x in vowels else x.lower() for x in line])
