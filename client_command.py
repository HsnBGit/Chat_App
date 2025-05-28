import xmlrpc.client
import threading
import time


class ChatClient:
    def __init__(self):
        self.server = xmlrpc.client.ServerProxy("http://localhost:8888")  # This si the server addrease
        self.running = False # this is used to track if the server are running (is the client is connected)
        self.chat_room = "" 
        self.username = ""
        self.lock = threading.Lock() # which will be used for thread synchronization to avoid issues 
        self.previous_messages = set()  # Store seen messages

    def connect(self):
        self.username = input("Enter your username: ")
        self.chat_room = input("Enter the chat room: ")
        if not self.username or not self.chat_room:
            print("Username and room cannot be empty!")
            return
        
        response = self.server.connect_function(self.chat_room, self.username) # here i will go to the server_chat 
        # then access the functions inside it 
        print(response)
        self.running = True # this is like i say that the client is here (connected) 

        threading.Thread(target=self.poll_messages, daemon=True).start() # a new thread is started


    def send_message(self):
        message = input("Enter your message: ")
        if message:
            with self.lock: #  to synchronize access to the server, ensuring no other threads are trying to access the server at the same time.
                response = self.server.say_function(self.chat_room, self.username, message)
            print(response)


    def get_users(self):
        with self.lock: #  to synchronize access to the server, ensuring no other threads are trying to access the server at the same time.
            users = self.server.who_function(self.chat_room)
        if users:
            print(f"Online Users: {', '.join(users)}")
        else:
            print("Online Users: None")


    def clear_chat_history(self):
        with self.lock: #  to synchronize access to the server, ensuring no other threads are trying to access the server at the same time.
            response = self.server.clear_chat_history(self.chat_room)
        print(response)


    def leave_chat(self):
        with self.lock: #  to synchronize access to the server, ensuring no other threads are trying to access the server at the same time.
            response = self.server.leave_function(self.chat_room, self.username)
        self.running = False # this is to say the client is not connected to the server
        print(response)


    def poll_messages(self):
        while self.running:
            with self.lock:
                messages = self.server.get_messages(self.chat_room)
            # Filter messages that have not been seen before.
            new_messages = [msg for msg in messages if msg not in self.previous_messages]
            if new_messages:
                for msg in new_messages:
                    print(msg)
                    self.previous_messages.add(msg)
            time.sleep(2)  # Delay between polls to avoid excessive API calls.
 


    def start(self):
        print("Welcome to the Chatting Application!!")
        while True:
            if not self.running:
                print("\nMenu:")
                print("1. Connect to a chat room")
                print("2. Exit")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.connect()
                elif choice == '2':
                    break
                else:
                    print("Invalid choice. Try again.")
            else:
                print("\nOptions:")
                print("1. Send Message")
                print("2. Get Online Users")
                print("3. Clear Chat History")
                print("4. Leave Chat")
                print("5. Exit")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.send_message()
                elif choice == '2':
                    self.get_users()
                elif choice == '3':
                    self.clear_chat_history()
                elif choice == '4':
                    self.leave_chat()
                elif choice == '5':
                    self.leave_chat()
                    break
                else:
                    print("Invalid choice. Please try again.")


client = ChatClient()
client.start()
