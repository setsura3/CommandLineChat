import json
import socket

from collections import defaultdict

# usr status control
online_users = defaultdict(dict)

print(online_users)

# bind IP
chat_server = socket.socket()
chat_server.bind(('0.0.0.0', 8000))
chat_server.listen()

#better dict
user_msg = defaultdict(dict)

def handle_socket(socket, addr):
    while True:
        chat_data = socket.recv(1024)
        json_data = json.loads(chat_data.decode("utf8"))
        action = json_data.get("action", "")
        if action == "login":
            online_users[json_data["user"]] = socket
            socket.send("Login Successful".encode("utf8"))

        elif action == "list_user":
            # return users currently online
            all_users = [user for user, socket in online_users.items()]
            socket.send(json.dumps(all_users.encode("utf8")))

        elif action == "history_msg":
            socket.send(json.dumps(user_msg.get(json_data["user"],[])).encode("utf8"))

        elif action == "send_msg":
            if json_data["to"] in online_users:
                online_users[json_data["to"]].send(json.dumps(json_data).encode("utf8"))
                user_msg[json_data["to"]].append(json_data)

        elif action == "exit":
            del online_users[json_data["user"]]
            socket.send("Logout Successful").encode("utf8")



