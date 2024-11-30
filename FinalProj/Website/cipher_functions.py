from midiutil.MidiFile import MIDIFile

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
def CaesarCipher(tokens, inKey):
    print("Cipher")
    cipherText = []  # Initialize an empty list for the cipher text

    # Get valid key
    key = ValidTokens.index(inKey[0])

    # Loop through each token and shift it using ShiftChar
    for token in tokens:
        cipheredToken = ShiftChar(token, key)
        cipherText.append(cipheredToken)

    return cipherText

def AffineCipher(tokens, alpha, beta):
    print("Affine")
    ciphertext = []

    # Convert alpha to an integer
    alpha = ValidTokens.index(alpha[0])

    # Convert beta to an integer
    beta = ValidTokens.index(beta[0])

    # c = ax + b (mod 13)
    for token in tokens:
        tokenIndex = (ValidTokens.index(token) * alpha)
        ciphertext.append(ValidTokens[(tokenIndex + beta) % 13])

    return ciphertext

def VigCipher(tokens, passTokens):
    print("Vig")
    cipherText = []

    for i in range(len(tokens)):
        shiftAmount = ValidTokens.index(passTokens[i % len(passTokens)])
        cipheredToken = ShiftChar(tokens[i], shiftAmount)
        cipherText.append(cipheredToken)

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

def InitializePlayfairArray(passPhrase):
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

def PlayfairCipher(tokens, passPhrase):
    print("Playfair")
    cipherText = []

    # Initalize the encryption array
    encryptionArr = InitializePlayfairArray(passPhrase)

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
            labels.append('A')
        case 1:
            labels.append('C')
        case 2:
            labels.append('D')
        case _:
            print("Invalid coords[0]: " + str(coords[0]))

    match (coords[1]):
        case 0:
            labels.append('Eb')
        case 1:
            labels.append('F')
        case 2:
            labels.append('G')
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

def ADFGXCipher(tokens, passPhrase):
    print("ADFGX")
    cipherText = []

    encryptionMatrix = [['A', 'Bb', 'B', 'C'], ['Db', 'D', 'Eb', 'E'], ['F', 'Gb', 'G', 'Ab']]

    pitchPairs = []

    for token in tokens:
        pitchPairs.append(GetLabelsFromADFGXMatrix(token, encryptionMatrix))
    
    passTokens = GetInput(passPhrase, -1)

    # setup partial encryption array 1
    pe1Arr = []
    for token in passTokens:
        pe1Arr.append([token])

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

    return cipherText

# ===== Hill Cipher =====
def HillCipher(tokens, dimension, passTokens):
    print("Hill")
    cipherText = []

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

    return(cipherText)