ValidTokens = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "/"]

def GetInput(inString, numTokens):
    validChars = "ABCDEFGb/ "
    tokens = []  # Initialize an empty list to store tokens

    i = 0
    while i < len(inString):
        tmp = inString[i]

        # Ignore spaces
        if tmp == ' ':
            i += 1
            continue

        # Handle invalid characters
        if tmp not in validChars:
            print("Invalid input! Try again.")
            return None

        # Handle accidental (e.g., 'b' after a note)
        if (i + 1 < len(inString)) and inString[i + 1] == 'b':
            tmp += inString[i + 1]
            i += 1  # Increment i to skip the accidental

        # Check if the token is valid
        if tmp not in ValidTokens:
            print("Invalid token! Try again.")
            return None

        # Add the token to the list
        tokens.append(tmp)

        # Increment for the next iteration
        i += 1

    # Allow any size when size is -1
    if(numTokens == -1):
        return tokens

    # Ensure correct number of tokens before returning
    if len(tokens) != numTokens:
        print("Incorrect number of tokens!")
        return None
    
    return tokens  # Return the list of tokens

def ShiftChar(token, key):
    # Find the index of the token in ValidTokens
    tokenIndex = ValidTokens.index(token)

    # Apply the shift (Caesar cipher)
    cipherIndex = (tokenIndex + key) % len(ValidTokens)

    # Return the shifted token
    return ValidTokens[cipherIndex]


def CaesarCipher(tokens):
    cipherText = []  # Initialize an empty list for the cipher text

    # Get valid key
    key = None
    while key is None:
        try:
            key = int(input("Enter a key (0-13): "))
            if key < 0 or key > 13:
                print("Key must be between 0 and 13.")
                key = None
        except ValueError:
            print("Please enter a valid integer.")

    # Loop through each token and shift it using ShiftChar
    for token in tokens:
        cipheredToken = ShiftChar(token, key)
        cipherText.append(cipheredToken)

    print("Ciphered text:", cipherText)
    return cipherText

def VigCipher(tokens):
    cipherText = []

    passPhrase = None
    passTokens = None
    while passPhrase is None:
            passPhrase = input("Passphrase: ")
            passTokens = GetInput(passPhrase, -1)

    for i in range(len(tokens)):
        cipheredToken = ShiftChar(tokens[i], ValidTokens.index(passPhrase[i % len(passPhrase)]))
        cipherText.append(cipheredToken)

    print("Ciphered text:", cipherText)
    return cipherText


# Main Program
tokens = None  # Initialize tokens

print("Welcome to the musical encryption program. Enter the number for the type of encryption you would like to do!")
print("1) Caesar Cipher")
print("2) Vigenere Cipher")
print("3) Affine Cipher")
print("4) Hill Cipher")
print("5) One-time Pad")
print("6) Playfair Cipher")
print("7) ADFGX Cipher")

cipher = int(input("> "))

# Continue polling until valid input gotten
while tokens is None:
    inString = input("Enter melody: ")

    tokens = GetInput(inString, 8)

match cipher:
    case 1:
        CaesarCipher(tokens)
    case 2:
        VigCipher(tokens)
    case 3:
        print("Affine")
    case 4:
        print("Hill")
    case 5:
        print("One-time pad")
    case 6:
        print("Playfair")
    case 7:
        print("ADFGX")
    case _:
        print("Unkown token entered")
