from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
import base64




def deocodeGlobalId(encoded_string):
    # encoded_string = id
    decoded_bytes = base64.b64decode(str(encoded_string))
    decoded_string = decoded_bytes.decode('utf-8')
    decode=decoded_string.split(':')[1]
    return decode

    # print(decoded_string.split(':')[1])

def login(obj,username,password):
    # error=[]
    login=[]
    try:
        user=obj.objects.get(username=username)
        user.last_login=timezone.now()
        user.save()
        # user=authenticate(username=user.username,password=password)
        users=user.check_password(password)
        if users:
            login.append({'message':"Login successfull","user":user,})
            login.append({'message1':"Login successfull","user1":user,})
            login.append({'message':"Password not match","field":"password"})
            return login
        else:
            login.append({'message':"Password not match","field":"password"})
            return login
    except obj.DoesNotExist:
        login.append({'message':"Username not found","field":"username"})
        return login
