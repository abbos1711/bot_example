import random, string

num_digits = random.randint(2, 4)
num_symbols = random.randint(2, 3)

def generate_normal(length):
    password = ""

    for digits_i in range(num_digits):
        password = password + random.choice(string.digits)

    for punctuation_i in range(num_symbols):
        password = password + random.choice(string.punctuation)

    for index in range(length - num_digits - num_symbols):
        password = password + random.choice(string.ascii_letters)

    password = ''.join(random.sample(password, len(password)))
    return password



