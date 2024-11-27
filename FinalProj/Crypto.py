ValidTokens = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "/"]

# ===== GENERAL FUNCTIONS =====
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

# ===== SHIFT CIPHER FUNCTIONS =====
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

def AffineCipher(tokens):
    alpha = None
    beta = None
    ciphertext = []

    while alpha is None:
        try:
            alpha = int(input("Alpha: "))
            if(alpha < 0 or alpha > 12):
                print("alpha must be 0 - 12")
                alpha = None
        except ValueError:
            print("Please use valid integer (0 - 12)")

    while beta is None:
        try:
            beta = int(input("Beta: "))
            if(beta < 0 or beta > 12):
                print("beta must be 0 - 12")
                beta = None
        except ValueError:
            print("Please use valid integer (0 - 12)")

    for token in tokens:
        tokenIndex = ValidTokens.index(token)
        ciphertext.append(ValidTokens[(tokenIndex + beta) % 13])

    print(ciphertext)
    return ciphertext

def VigCipher(tokens):
    cipherText = []

    passPhrase = None
    passTokens = None

    while passPhrase is None:
            passPhrase = input("Passphrase: ")
            passTokens = GetInput(passPhrase, -1)

    for i in range(len(tokens)):
        shiftAmount = ValidTokens.index(passTokens[i % len(passTokens)])
        cipheredToken = ShiftChar(tokens[i], shiftAmount)
        cipherText.append(cipheredToken)

    print(cipherText)
    return cipherText

# ===== PLAYFAIR FUNCTIONS =====
def FixPlayfairCipherTokens(tokens):
    fixedTokens = []

    # Process tokens and handle duplicates
    for token in tokens:
        if token == '/':
            token = 'A'
        fixedTokens.append(token)

    # Fix to even length by appending a filler token if needed
    if len(fixedTokens) % 2 != 0:
        fixedTokens.append('/')

    # Create tuples of consecutive tokens
    tokenPairs = [(fixedTokens[i], fixedTokens[i + 1]) for i in range(0, len(fixedTokens), 2)]

    return tokenPairs

def InitializePlayfairArray():
    passPhrase = input("Enter key: ")
    passTokens = GetInput(passPhrase, -1)

    # Parse the expression and remove duplicates
    newPassTokens = []

    for token in passTokens:
        # Handle character collision
        if(token == '/'):
            token = 'A'

        # Append non-duplicates
        if(token not in newPassTokens):
            newPassTokens.append(token)

    # Create the array and fill with 'None'
    rows = 3
    cols = 4
    myArr = [[None for _ in range(cols)] for _ in range(rows)]

    # Place newPassTokens into the first n positions of the array
    row = 0
    col = 0

    for token in newPassTokens:
        myArr[row][col] = token

        col += 1

        if(col == cols):
            col = 0
            row += 1

            if(row == rows):
                break

    # Add remaining ValidTokens that are not already in newPassTokens
    for token in ValidTokens:
        if token not in newPassTokens:
            myArr[row][col] = token
            col += 1
            if col == cols:
                col = 0
                row += 1
                if row == rows:
                    break

    return myArr

def FindPlayfairArrCoords(token, arr):
    coords = []

    for line in arr:
        if(token in line):
            coords.append(arr.index(line))

    coords.append(arr[coords[0]].index(token))

    return coords

def PlayfairCipher(tokens):
    cipherText = []

    # Initalize the encryption array
    encryptionArr = InitializePlayfairArray()

    # Fix input
    tokenPairs = FixPlayfairCipherTokens(tokens)

    for pair in tokenPairs:
        t1coords = FindPlayfairArrCoords(pair[0], encryptionArr)
        t2coords = FindPlayfairArrCoords(pair[1], encryptionArr)

        # Handle same row (replace with char to right)
        if(t1coords[0] == t2coords[0]):
            cipherText.append(encryptionArr[t1coords[0]][(t1coords[1] + 1) % 4])
            cipherText.append(encryptionArr[t2coords[0]][(t2coords[1] + 1) % 4])

        # Handle same col (replace with char to bottom)
        elif(t1coords[1] == t2coords[1]):
            cipherText.append(encryptionArr[(t1coords[0] + 1) % 3][t1coords[1]])
            cipherText.append(encryptionArr[(t2coords[0] + 1) % 3][t2coords[1]])

        # Handle different row and col
        else:
            cipherText.append(encryptionArr[t1coords[0]][t2coords[1]])
            cipherText.append(encryptionArr[t2coords[0]][t1coords[1]])

    print(cipherText)
    return cipherText

# ===== ADFGX FUNCTIONS =====
def GetLabelsFromADFGXMatrix(token, matrix):
    coords = []

    # Handle character collision
    if(token == '/'):
        token = 'A'

    # Get coords of token
    for line in matrix:
        if(token in line):
            coords.append(matrix.index(line))
            break
    coords.append(matrix[coords[0]].index(token))

    # print(str(token) + str(coords))

    # Translate coordinates to pitch pairs
    labels = []

    match (coords[0]):
        case 0:
            labels.append('C')
        case 1:
            labels.append('Eb')
        case 2:
            labels.append('F')
        case _:
            print("Invalid coords[0]: " + str(coords[0]))

    match (coords[1]):
        case 0:
            labels.append('Gb')
        case 1:
            labels.append('G')
        case 2:
            labels.append('Bb')
        case 3:
            labels.append('/')
        case _:
            print("Invalid coords[1] " + str(coords[1]))

    return labels

def SortArrBasedOnFirstVal(arr):
    retArr = []

    for row in arr:
        # If retArr is empty, add the first row
        if not retArr:
            retArr.append(row)
        else:
            curIndex = 0
            while curIndex < len(retArr):
                # Compare positions in ValidTokens
                if ValidTokens.index(retArr[curIndex][0]) < ValidTokens.index(row[0]):
                    curIndex += 1
                else:
                    # Insert row at the correct position
                    retArr.insert(curIndex, row)
                    break
            else:
                # Append row if it belongs at the end
                retArr.append(row)

    return retArr

def ADFGXCipher(tokens):
    cipherText = []

    encryptionMatrix = [['A', 'Bb', 'B', 'C'], ['Db', 'D', 'Eb', 'E'], ['F', 'Gb', 'G', 'Ab']]

    pitchPairs = []

    for token in tokens:
        pitchPairs.append(GetLabelsFromADFGXMatrix(token, encryptionMatrix))
    
    passPhrase = input("key: ")
    passTokens = GetInput(passPhrase, -1)

    # setup partial encryption array 1
    pe1Arr = []
    for token in passTokens:
        pe1Arr.append([token])

    # print(pitchPairs)

    pitchIndex = 0
    # Insert pitch pairs into the array
    for i in range(len(pitchPairs)):
        tok1 = pitchPairs[i][0]
        tok2 = pitchPairs[i][1]

        # Insert first token
        pe1Arr[pitchIndex].append(tok1)

        # Increment the index
        pitchIndex = (pitchIndex + 1) % len(pe1Arr)

        # Insert second token
        pe1Arr[pitchIndex].append(tok2)

        # Increment index
        pitchIndex = (pitchIndex + 1) % len(pe1Arr)

    # Sort it based on pitch value
    encryptedArr = SortArrBasedOnFirstVal(pe1Arr)

    # Insert from encryptedArr to the ciphertext. ignoring the key headers
    for row in encryptedArr:
        cipherText.extend(row[1:])

    print(cipherText)
    return cipherText

# ===== Hill Cipher =====
def HillCipher(tokens):
    cipherText = []

    # Get the dimension
    dimension = None
    while(dimension is None):
        try:
            dimension = int(input("Dimension of array: "))
        except ValueError:
            dimension = None
            print("Invalid dimension")

    # Get the passphrase tokens
    passTokens = None
    while(passTokens is None):
        passPhrase = input("Enter a " + str(dimension * dimension) + " note melody: ")
        passTokens = GetInput(passPhrase, (dimension * dimension))

    # Make the encryption array
    encryptArr = [[0] * dimension for _ in range(dimension)]

    # Populate encryption array
    for i in range(dimension):
        for j in range(dimension):
            encryptArr[i][j] = passTokens[(i * dimension) + j]

    # Split the plaintext into n vectors with size dimension
    curIndex = 0
    ptVectors = []

    while curIndex < len(tokens):
        vector = []
        for i in range(dimension):
            if curIndex < len(tokens):
                vector.append(tokens[curIndex])
                curIndex += 1
            else:
                # Pad with '/' if we run out of tokens
                vector.append('/')

        # Add the vector to the list of vectors
        ptVectors.append(vector)

    # Do matrix multiplication, store in ciphertext
    for vec in ptVectors:
        for i in range(dimension):
            total = 0
            for j in range(dimension):
                total += ValidTokens.index(vec[j]) * ValidTokens.index(encryptArr[i][j])
            cipherText.append(ValidTokens[total % 13])

    print(cipherText)
    return(cipherText)

# Main Program
tokens = None  # Initialize tokens

print("Welcome to the musical encryption program. Enter the number for the type of encryption you would like to do!")
print("1) Caesar Cipher")
print("2) Vigenere Cipher")
print("3) Affine Cipher")
print("4) Hill Cipher")
print("5) Playfair Cipher")
print("6) ADFGX Cipher")

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
        AffineCipher(tokens)
    case 4:
        HillCipher(tokens)
    case 5:
        PlayfairCipher(tokens)
    case 6:
        ADFGXCipher(tokens)
    case _:
        print("Unkown token entered")