def vowel(line):
    vowels = ('a', 'e', 'i', 'o', 'u')
    return "".join([x.upper() if x.lower() in vowels
                    else x.lower() for x in line])


if __name__ == '__main__':
    print(vowel(input()))
