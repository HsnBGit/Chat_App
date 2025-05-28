from xmlrpc.server import SimpleXMLRPCServer
import threading # this is used to let me run the server in a separate thread to allow concurrent execution

class ChatServer:
    def __init__(self): # Constructor  
        self.chat_rooms = {}
        self.chat_history = {}
        
        
    def connect_function(self, room, username):
        if room not in self.chat_rooms:
            self.chat_rooms[room] = {}    # So here it will set a new room inside the dic put the room dic
            self.chat_history[room] = [] # this is the same thing it will store a list instead of a dic
            
        if username in self.chat_rooms[room]:
            return f"The user: {username} is already in this room ({room})."
        
        self.chat_rooms[room][username] = True  # the true to check if the user are in teh rooms are not True for yes False for No
        self.chat_history[room].append(f"The user: {username} has joined this room ({room}).")
        
        return f"The user: {username} has joined this room ({room})."


    def leave_function(self, room, username):
        if (room in self.chat_rooms) and (username in self.chat_rooms[room]): # here to check if the username is in the chatroom[room] why 
            #bc it is dic so we need to search about the keys that is why, and if the room in chat_rooms just like this bc we are search about the keys 
            del self.chat_rooms[room][username] # the del function used to remove an items from the dic, so we are removing the username
            self.chat_history[room].append(f"The user: {username} unfortunately left the room ({room}) :(")
            return f"The user: {username} unfortunately left the room ({room}) :("
        return f"Ohh No the user: {username} is not in this room ({room}) :) ." # the above return will run fi the user is in the room if not the second will be run


    def say_function(self, room, username, message):
        if (room not in self.chat_rooms) or (username not in self.chat_rooms[room]): # also here we want to check if the user in a room
            # or is the room not in the rooms dic
            return f"The user: {username} is not in any room ({room}), Please find a room to join"
        
        chat_message = f"Room: [{room}]. \n {username} say: {message}." # this is where we will store the massges and display it to teh users
        self.chat_history[room].append(chat_message)
        return chat_message


    def who_function(self, room):
        # here uf i want to know the who in my room
        return list(self.chat_rooms.get(room, {}).keys())  # so here the end goal i want to get the users in my room Right ? 
        # sp i have to go inside my room dic and then get the values and the values here i mean the key in out case is the users
        # (it will return as a dic so we need to use another function to return it as a list ) 
        

    def get_messages(self, room):
        return self.chat_history.get(room, []) # this is used to display the massges


    def clear_chat_history(self, room):
        if room in self.chat_history: # here to check if the room (key respect to the dic chat_room dic) is here ot not
            self.chat_history[room] = [f"Chat history cleared for {room}."] # why we area using a list here?
            # bc if u rememvber that the massges should be a list so i can display it (so i mean it is look like this )
            # {"Room1": {"Hassan": True, 'Abdualla": True, "Mouth": True}} This is for the chat_rooms
            # {"Room1": ["Room: [{room}]. \n {username} say: {message}."]} this si for the chat_history
            return f"The Chat has been cleared for this room ({room})."
        return f"Nah i did not find a chat history found for this room ({room}) ."

# now we are outside of chat_server class


def run_server():
    server = SimpleXMLRPCServer(("localhost", 8888)) # this is mean i will create an instance
    # that will listen tp the port 8000 and it will be run locally
    
    chat = ChatServer() 
    server.register_instance(chat) # this is mean all the functions that we dfiend above it will be available as a remote precedures (RPC) via  XMLRPC
    print("Chat server running on port 8888...")
    server.serve_forever() 


server_thread = threading.Thread(target=run_server) # (basically, concurrent tasks).
server_thread.start()
