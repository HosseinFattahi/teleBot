
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
import csv
#python pip install pandas
import pandas as pd
import time
import random




api_id = input(print('enter api id'))
api_hash = input(print('enter api hash'))

phone = input(print('enter phone num'))

client = TelegramClient(phone, api_id, api_hash)



#----------------------------------------------------------------
def TakeAllMember():

    chats = []
    last_date = None
    chunk_size = 200
    groups=[]
    
    result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat:
                groups.append(chat)
        except:
            continue

    print('Choose a group to scrape members from:')
    i=0
    for g in groups:
        print(str(i) + '- ' + g.title)
        i+=1

    g_index = input("Enter a Number: ")
    target_group=groups[int(g_index)]

    print('Fetching Members...')
    all_participants = []
    print(target_group) 
    try:
        all_participants = client.get_participants(target_group,aggressive=True)
    except:
        pass
    print('Saving In file...')
    with open("members.csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username','userid', 'accesshash','name','group', 'groupid'])
        for user in all_participants:
            if user.username:
                username= user.username
            else:
                username= ""
            if user.first_name:
                first_name= user.first_name
            else:
                first_name= ""
            if user.last_name:
                last_name= user.last_name
            else:
                last_name= ""
            name= (first_name + ' ' + last_name).strip()
            writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
    print('Members scraped successfully.')

#------------------------------------------------------------------
def entermember(members):
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]
    
    result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat:
                groups.append(chat)
        except:
            continue

    print('Choose a group to enter member:')
    i=0
    for g in groups:
        print(str(i) + '- ' + g.title)
        i+=1

    g_index = input("Enter a Number: ")
    target_group=groups[int(g_index)]
    target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
    
    for i in range(len(members.userid)):
        try:
            user_to_add = InputPeerUser(members.userid[i], members.accesshash[i])
            client(InviteToChannelRequest(target_group_entity,[user_to_add]))
            print("Waiting for 15-40 Seconds...")
            time.sleep(random.randrange(15, 40))
        except PeerFloodError:
            print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.") 
            continue
        except:
            print("Unexpected Error")
            continue
 




client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))



TakeAllMember()
entermember(pd.read_csv("members.csv"))



#-------------------


