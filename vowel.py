# Input: a string with only English letters and whitespace
# Task: capitalize vowels and decapitalize consonants in the string

def vowel(line):
    vowels = ('a', 'e', 'i', 'o', 'u')
    return "".join([x.upper() if x in vowels else x.lower() for x in line])
