import json
import copy
#Maybe replace pprint with something to PDF
from pprint import pprint
from pathlib import Path


#Start venv
#source ./.venv/bin/activate

def open_file():
    with open('./test_input/conv001', 'r', encoding='utf-8') as file:
        cur_convs = json.load(file)
        get_mapping(cur_convs)

def get_mapping(convs):
    for conv in convs:
        cur_map = conv.get('mapping')
        print(conv.get('title'))
        add_title(conv.get('title'))
        #print(list(cur_map.keys()))
        
        data = handle_map(cur_map)

def handle_map(map):
    #Mapping needs to be done via parent field. 
    msg_list = list(map.keys())
    # print(msg_list)
    #print(map.get(msg_list[0])) #dict type

    #Map has no msgs TODO: Can this happen? idk, track
    if not msg_list:
        raise AssertionError("msg_list is empty")
    
    #Remove client-created-root from msg_list. TODO: Might be a bad idea, track
    msg_list.remove('client-created-root')

    #Message handling
    msg_node = "" #Empty string to track current message
    msg_tree = [] #Empty list that becomes our sorted tree
    #Find msg with parent == client-created-root. That msg will be the root 
    while msg_list:
        for msg in msg_list:
            #print(msg)
            msg_parent = map.get(msg).get('parent')
            if msg_parent == 'client-created-root':
                msg_tree.append(msg)
                msg_list.remove(msg)
                msg_node = map.get(msg).get('id')
                break

            #Doesn't handle multiple children here. Might not even be needed. TODO: Change if needed. 
            if msg_parent == msg_node:
                msg_tree.append(msg)
                msg_list.remove(msg)
                msg_node = map.get(msg).get('id')
            
            # print("list: ", msg_list)
            # print("tree: ", msg_tree)
            # print("node: ", msg_node)
            # print("msg: ", msg)

    #Process msg_tree
    # print(msg_tree)
    for item in msg_tree:
        extract_info(item, map)

def extract_info(cur_msg, map):
    msg = map.get(cur_msg)
    #print(msg.get('message'))
    #print(parts)

    if not msg.get('message'):
        return

    #Only get message author and output
    author = msg.get('message').get('author').get('role')
    parts = msg.get('message').get('content').get('parts')

    add_author_parts(author, parts)

def add_title(title):
    #Format output to be written
    formatted_output = f"Title: {title}\n"

    #Create folder/directory for specific converstation TODO: Get info from open_file
    path = Path("./outputs/conv001")
    path.mkdir(parents=True, exist_ok=True)

    #Raw Text
    try:
        with open("./outputs/conv001/conv001_raw", "x", encoding="utf-8") as file:
            file.write(formatted_output)
    except:
        with open("./outputs/conv001/conv001_raw", "a", encoding="utf-8") as file:
            file.write(formatted_output)

def add_author_parts(author, parts):
    #Think raw + formatted output. pprint+raw text for now. PDF later? TODO: Talk to JH about this
    if author == None or parts == None:
        print("haha")
        return

    #Format output to be written
    formatted_output = f"Author: {author}\nMessage: {parts}\n"

    #Create folder/directory for specific converstation TODO: Get info from open_file
    path = Path("./outputs/conv001")
    path.mkdir(parents=True, exist_ok=True)

    #Raw Text
    try:
        with open("./outputs/conv001/conv001_raw", "x", encoding="utf-8") as file:
            file.write(formatted_output)
    except:
        with open("./outputs/conv001/conv001_raw", "a", encoding="utf-8") as file:
            file.write(formatted_output)

#TODO: Make it auto exit and stuff. Add main or whatever that thing is
open_file()