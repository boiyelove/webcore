import random
import hashlib
from datetime import datetime
from django.contrib.auth.models import User
from .models import EmailConfirmed

def code_generator(codepulse):
	code = hashlib.sha1(str(random.random()).encode())
	code.update(codepulse.encode())
	code.update(str(datetime.utcnow()).encode())
	code = code.hexdigest()
	return code

def verify_email(email):
	EmailVerification.objects.get_or_create(email = email)