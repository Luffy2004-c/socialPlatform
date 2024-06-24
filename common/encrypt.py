import hashlib
from django.conf import settings

# 原始消息
message = "Hello, world!"


def encrypt(pwd: str) -> str | None:
    salt = settings.SECRET_KEY
    salted_message = salt + pwd
    hash_object = hashlib.sha256()
    hash_object.update(salted_message.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig
