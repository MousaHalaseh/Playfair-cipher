from string import ascii_uppercase
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Initializing the matrix to be used in the En/Decryption processes
matrix = [[1 for _ in range(5)] for _ in range(5)]

# Initializing constant keys to be used in the process
KEY1 = 'HELLO'
KEY2 = 'HASHEMITE'
plainText = None
cipherText = None

alpha = list(ascii_uppercase)


def already_exist(text, letter):
    # This function receives a list along with a letter
    # returns True if the letter's found in the list
    flag = False
    for x in range(len(text)):
        if str(text[x]) == str(letter):
            flag = True
    return flag


def text_to_list(text):
    # This function prepares a list from the key to be inserted into the matrix
    result = []
    for x in range(len(text)):
        # can't contain a blank space
        if text[x] is ' ':
            continue
            # J letter will be replaced with an I
        elif text[x] is 'J':
            result.append('I')
            # If the letter has already been added to the list then it will be, of course, ignored
        elif already_exist(result, text[x].upper()):
            continue
        else:
            result.append(text[x].upper())
    # after the key is added we will continue to add the rest of the alphabets
    for w in range(26):
        if alpha[w] == 'J':
            continue
        elif already_exist(result, alpha[w]):
            continue
        else:
            result.append(alpha[w])
    return result


def update_matrix(text):
    # This function takes the key-list and put it in a 5*5 matrix
    count = 0
    for x in range(5):
        for y in range(5):
            if count is len(text):
                break
            else:
                matrix[x][y] = text[count]
                count += 1


def arrange(text):
    # This function intends to find all the cases where we need to separate the letters with an X
    # and arrange the list so that it would be ready to be encrypted
    values = []
    result = []
    # This loop assures that the plain-text does not contain a blank space or J letter
    for y in range(len(text)):
        if text[y] != ' ':
            if text[y] == 'J':
                result.append('I')
            else:
                result.append(text[y])
    # This loop will append an X if it encounters same two letters in a single pair
    for x in range(0, len(result), 2):
        if x + 1 is len(result):
            if x % 2 is 1 and result[x] == result[x - 1]:
                values.append('X')
                values.append(result[x])
                values.append('X')
                break
            elif x % 2 is 1 and result[x] != result[x - 1]:
                values.append(result[x])
                break
            else:
                values.append(result[x])
                values.append('X')
                break
        elif result[x] == result[x + 1]:
            flag = result[x] == result[x - 1]
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
    # This function will return an integer list of size 2, that contains the letter indices in the matrix
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

    # after we get an arranged message to encrypt and a matrix to count on
    # the following piece of code will apply the PlayFair ciphering rules
    for x in range(0, len(final_plain), 2):
        first = search(final_plain[x])
        second = search(final_plain[x + 1])

        # If the two letters are in the same row we will shift them to the right by one index
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

        # If the two letters are in the same column we will shift them down by one index
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

        # Otherwise we will shift the column index from the first to the second and vice versa
        else:
            temp = first[1]
            first[1] = second[1]
            second[1] = temp

        # and finally we append the result to the final list to return
        cipher_text.append(matrix[first[0]][first[1]])
        cipher_text.append(matrix[second[0]][second[1]])
    return cipher_text


def decrypt(key, cipher):
    text = text_to_list(key)
    update_matrix(text)
    plain_text = []

    # after we update the matrix with the intended key
    # the following piece of code will apply the PlayFair deciphering rules
    for x in range(0, len(cipher), 2):
        first = search(cipher[x])
        second = search(cipher[x + 1])

        # If the two letters are in the same row we will shift them to the left by one index
        if first[0] is second[0]:
            if first[1] is 0:
                first[1] = 4
                second[1] = second[1] - 1
            elif second[1] is 0:
                second[1] = 4
                first[1] = first[1] - 1
            else:
                first[1] = first[1] - 1
                second[1] = second[1] - 1

        # If the two letters are in the same column we will shift them up by one index
        elif first[1] is second[1]:
            if first[0] is 0:
                first[0] = 4
                second[0] = second[0] - 1
            elif second[0] is 0:
                second[0] = 4
                first[0] = first[0] - 1
            else:
                first[0] = first[0] - 1
                second[0] = second[0] - 1

        # Otherwise we will shift the column index from the first to the second and vice versa
        else:
            temp = first[1]
            first[1] = second[1]
            second[1] = temp

        # and finally we append the result to the final list to return
        plain_text.append(matrix[first[0]][first[1]])
        plain_text.append(matrix[second[0]][second[1]])
    return plain_text


def removeX(text):
    # This function is to be used after the decryption process
    #  to remove the leading X in between the letters that has been added in arrange() before the encryption
    final_text = []
    # This flag variable is used to make sure we don't remove an X letter that is part of the original message
    flag = False
    for y in range(len(text)):
        if y is 0:
            final_text.append(text[y])
        elif y is len(text) - 1:
            if flag:
                continue
            else:
                final_text.append(text[y])
        elif text[y] == 'X':
            if text[y - 1] == text[y + 1]:
                flag = True
                continue
            elif flag:
                flag = False
                continue
            else:
                final_text.append(text[y])
        else:
            final_text.append(text[y])

    return final_text


def set_window():
    # Setting up the Gtk window for the GUI
    window = MainGUI()
    window.connect('delete_event', Gtk.main_quit)
    window.resize(600, 400)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.set_border_width(20)
    window.show_all()
    Gtk.main()


class MainGUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Play Fair')

        # creating text fields for the user input
        self.encrypt_text = Gtk.Entry()
        self.decrypt_text = Gtk.Entry()

        # creating labels for the text fields
        self.encrypt_label = Gtk.Label()
        self.encrypt_label.set_text('Plain Text: ')

        self.decrypt_label = Gtk.Label()
        self.decrypt_label.set_text('Cipher Text: ')

        # creating buttons
        self.encrypt_button = Gtk.Button('Encrypt Me!')
        self.encrypt_button.connect('clicked', self.encrypt_event)

        self.decrypt_button = Gtk.Button('Decrypt Me!')
        self.decrypt_button.connect('clicked', self.decrypt_event)

        # creating Boxes
        self.encrypt_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.encrypt_box.pack_start(self.encrypt_label, True, True, 0)
        self.encrypt_box.pack_start(self.encrypt_text, True, True, 0)
        self.encrypt_box.pack_start(self.encrypt_button, True, True, 0)

        self.decrypt_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.decrypt_box.pack_start(self.decrypt_label, True, True, 0)
        self.decrypt_box.pack_start(self.decrypt_text, True, True, 0)
        self.decrypt_box.pack_start(self.decrypt_button, True, True, 0)

        # setting up the Grid layout
        self.encrypt_layout = Gtk.Grid()
        self.encrypt_layout.add(self.encrypt_box)

        self.decrypt_layout = Gtk.Grid()
        self.decrypt_layout.add(self.decrypt_box)

        # main container for the stack
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.add(self.box)

        # setting up a Stack
        scene = Gtk.Stack()
        scene.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        scene.set_transition_duration(250)

        scene.add_titled(self.encrypt_layout, "encrypt_layout", "Encryption")
        scene.add_titled(self.decrypt_layout, "decrypt_layout", "Decryption")

        # setting up a Stack Switcher
        stage = Gtk.StackSwitcher()
        stage.set_stack(scene)
        self.box.pack_start(stage, True, True, 0)
        self.box.pack_start(scene, True, True, 0)

    def encrypt_event(self, widget):
        # Storing the user input and applying the encryption process
        plainText = str(self.encrypt_text.get_text()).upper()
        cipher1 = encrypt(KEY1, plainText)
        cipher2 = encrypt(KEY2, cipher1)

        # considering that encrypt() returns a list of strings
        # This loop will take each element and put it into a string variable(to be displayed on the Gtk.Entry)
        st = ""
        for y in range(len(cipher2)):
            st += cipher2[y]

        # Setting up the Gtk output dialog
        encryption_dialog = Gtk.Dialog("Output")
        encryption_dialog.resize(300, 200)

        # Setting up the Gtk.Entry to display the final output in
        encryption_output = Gtk.Entry()
        encryption_output.set_text(st)
        encryption_output.set_editable(False)
        encryption_dialog.vbox.pack_start(encryption_output, True, True, 80)

        encryption_output.show()
        encryption_dialog.run()
        encryption_dialog.destroy()

        # clearing the user entry after each submission
        self.encrypt_text.set_text('')

    def decrypt_event(self, widget):
        # Storing the user input and applying the decryption process
        cipherText = str(self.decrypt_text.get_text()).upper()
        plain1 = decrypt(KEY2, cipherText)
        plain2 = decrypt(KEY1, plain1)

        # getting back the original plain-text
        plain3 = removeX(plain2)

        # The following for loop will to check if there's an I in the final text
        # so that we will display a note to the user that it might be a J
        flag = False
        jnote = ''
        for x in range(len(plain2)):
            if plain2[x] == 'I':
                flag = True
        if flag:
            jnote = 'Note that the \'I\' might be a \'J\''

        # considering that decrypt() returns a list of strings
        # This loop will take each element and put it into a string variable(to be displayed on the Gtk.Entry)
        st2 = ""
        for y in range(len(plain3)):
            st2 += plain3[y]

        # Setting up the Gtk output dialog
        decryption_dialog = Gtk.Dialog("Output")
        decryption_dialog.resize(300, 200)

        # Setting up the Gtk.Entry to display the final output in
        decryption_output = Gtk.Entry()
        decryption_output.set_text(st2)
        decryption_output.set_editable(False)
        decryption_dialog.vbox.pack_start(decryption_output, True, True, 80)
        decryption_output.show()

        # Setting up a label to display the note in it (if needed)
        note = Gtk.Label()
        note.set_text(jnote)
        decryption_dialog.vbox.pack_start(note, True, True, 80)
        note.show()

        decryption_dialog.run()
        decryption_dialog.destroy()

        # clearing the user entry after each submission
        self.decrypt_text.set_text('')


set_window()

