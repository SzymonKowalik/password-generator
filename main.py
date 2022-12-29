import configparser
from string import ascii_lowercase, ascii_uppercase, digits
import random
import pyperclip
from os.path import exists

special_characters = '!@#$%^&*()'
config = configparser.ConfigParser()

# Read config file, create if not exists
if exists('./config.ini'):
    config.read('./config.ini')
else:
    config['Length'] = {
        'NumberOfLetters': 8,
    }

    config['Characters'] = {
        'ascii_lowercase': 'yes',
        'ascii_uppercase': 'yes',
        'digits': 'yes',
        'special_characters': 'yes'
    }

    with open('config.ini', 'w') as file:
        config.write(file)

# Get characters chosen from config file
available_characters = []
for k, v in config['Characters'].items():
    if v == 'yes':
        available_characters.append(eval(f'{k}'))


# Generates password with given length and character sets
# Minimal password length is at least one from every character set
def generate_password(length, characters):
    password = []
    for char_set in characters:
        password += random.choice(char_set)
    while len(password) <= int(length):
        password += random.choice(''.join(characters))
    random.shuffle(password)
    return ''.join(password)


length = config['Length']['NumberOfLetters']
repeat = True

if len(available_characters) == 0:
    raise Exception('No characters chosen.')

if int(length) < len(available_characters):
    raise Exception('Your password is too short.')

# Regenerate password until user is happy and copy it to clipboard
while repeat:
    password = generate_password(length, available_characters)
    print(f'\nGenerated password is: {password}')
    user_input = input('Regenerate password? Enter `y` to do it: ')
    if user_input != 'y':
        pyperclip.copy(password)
        repeat = False
