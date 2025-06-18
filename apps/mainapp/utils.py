import random
from datetime import datetime, timedelta


def generate_card_number():
    return '4400' + str(random.randint(111111111111, 999999999999))

def get_expire():
    now = datetime.now()
    return now + timedelta(1095)