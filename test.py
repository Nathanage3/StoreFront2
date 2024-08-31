import os
from dotenv import load_dotenv
from decouple import config

load_dotenv()

name_2 = config('NAME')

secret_key = os.getenv('STRIPE_SECRET_KEY')
name = os.environ.get('NAME')

secret_key_2 = config('STRIPE_SECRET_KEY')
print("secret_key {}:".format(secret_key))
print(os.getenv('STRIPE_SECRET_KEY'))

print("name from dotenv :{}".format(name))
print('name from decouple : {}'.format(name_2))