#pip install fbchat
#git clone git://github.com/carpedm20/fbchat.git
from fbchat import Client
from fbchat.models import *



client = Client('uid', 'pw')
session_cookies = client.getSession()
client.setSession(session_cookies)

print(client.uid)
users = client.searchForUsers('lol')
user=users[0]
print("User's ID:{}".format(user.uid))
print("User's name: {}".format(user.name))
print("User's profile picture URL: {}".format(user.photo))
print("User's main URL: {}".format(user.url))
#lient.send(Message(text='bla'), thread_id=user.uid, thread_type=ThreadType.USER)

print(client.fetchThreadMessages(thread_id=user.uid,limit=5))
messages=client.fetchThreadMessages(thread_id=user.uid,limit=5)
print(messages[3])
