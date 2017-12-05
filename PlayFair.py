from string import ascii_uppercase

matrix = [[1 for _ in range(5)] for _ in range(5)]

key1 = 'HELLO'
key2 = 'HASHEMITE'

alpha = list(ascii_uppercase)


def already_exist(text, letter):
    flag = False
    for x in range(len(text)):
        if str(text[x]) == str(letter):
            flag = True
    return flag


def text_to_list(text):
    result = []
    for x in range(len(text)):
        if text[x] is ' ':
            continue
        elif already_exist(result, text[x].upper()):
            continue
        else:
            result.append(text[x].upper())
    for w in range(26):
        if alpha[w] == 'J':
            continue
        elif already_exist(result, alpha[w]):
            continue
        else:
            result.append(alpha[w])
    return result


def update_matrix(text):
    count = 0
    for x in range(5):
        for y in range(5):
            if count is len(text):
                break
            else:
                matrix[x][y] = text[count]
                count += 1


def arrange(text):
    values = []
    result = []
    for y in range(len(text)):
        if text[y] != ' ':
            result.append(text[y])
    for x in range(0, len(result), 2):
        if x + 1 is len(result):
            if (x + 1) % 2 is 0 and result[x] == result[x - 1]:
                values.append('X')
                values.append(result[x])
                values.append('X')
                break
            elif (x + 1) % 2 is 0 and result[x] != result[x - 1]:
                values.append(result[x])
                break
            else:
                values.append(result[x])
                values.append('X')
                break
        elif result[x] == result[x + 1]:
            flag = result[x] == result[x - 1] or result[x] == result[x + 1]
            values.append(result[x])
            values.append('X')
            values.append(result[x + 1])
            if x + 1 is len(result) - 1:
                values.append('X')
            elif flag:
                values.append('X')
        else:
            values.append(result[x])
            values.append(result[x + 1])
    return values


def search(letter):
    location = []
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == letter:
                location.append(r)
                location.append(c)
    return location


def encrypt(key, msg):
    text = text_to_list(key)
    update_matrix(text)
    final_plain = arrange(msg)
    cipher_text = []
    for x in range(0, len(final_plain), 2):
        first = search(final_plain[x])
        second = search(final_plain[x + 1])
        if first[0] is second[0]:
            if first[1] + 1 is 5:
                first[1] = 0
                second[1] = second[1] + 1
            elif second[1] + 1 is 5:
                second[1] = 0
                first[1] = first[1] + 1
            else:
                first[1] = first[1] + 1
                second[1] = second[1] + 1
        elif first[1] is second[1]:
            if first[0] + 1 is 5:
                first[0] = 0
                second[0] = second[0] + 1
            elif second[0] + 1 is 5:
                second[0] = 0
                first[0] = first[0] + 1
            else:
                first[0] = first[0] + 1
                second[0] = second[0] + 1
        else:
            temp = first[1]
            first[1] = second[1]
            second[1] = temp
        cipher_text.append(matrix[first[0]][first[1]])
        cipher_text.append(matrix[second[0]][second[1]])
    return cipher_text


def decrypt(cipher):
    text_to_list(cipher)
    return ""


plainText = ''
cipherText = ''

while True:
    case = input("Enter 0 for Plain Text, 1 for Cipher Text: ")
    if case is '0':
        plainText = input("Please Enter a Plain Text? ")
        plainText = str(plainText.upper())
        print('Your plain text: ', plainText)
        cipher1 = encrypt(key1, plainText)
        cipher2 = encrypt(key2, cipher1)
        print('You cipher text: ', cipher2)
        break
    elif case is '1':
        cipherText = input("Please Enter a Cipher Text? ")
        decrypt(cipherText)
        break
    else:
        print("please provide a valid input..")


