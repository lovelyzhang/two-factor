import random


def generate_code():
    codes = [str(random.randint(0, 9)) for i in range(6)]
    return "".join(codes)
