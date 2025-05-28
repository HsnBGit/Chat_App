from customtkinter import *
import xmlrpc.client
import threading
import time


app = CTk()
app.geometry("575x750")
set_default_color_theme("blue")
set_appearance_mode("dark")

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatting Application (Grp 2)")

        self.server = xmlrpc.client.ServerProxy("http://localhost:8888") # as u see teh port is like in the server 

        # ---------- Center Panel: Chat Room ----------
        tabview = CTkTabview(master=root)
        tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        tabview.add("Chat Room")
        tabview.add("User Login")
        

        # --- Chat Room Tab ---
        chat_frame = tabview.tab("Chat Room")
        CTkLabel(master=chat_frame, text="Creators: Hassan, Abdullah, Mouth", font=("Arial Bold", 15)).pack(pady=(5, 5))
        CTkLabel(master=chat_frame, text="Chat Room", font=("Arial Bold", 20)).pack(pady=(10, 15))
        self.chat_display = CTkTextbox(chat_frame, height=200, width=500, state='disabled', wrap="word")
        self.chat_display.pack(pady=10, padx=10)
        self.message_entry = CTkEntry(chat_frame, width=400, placeholder_text="Type your message...")
        self.message_entry.pack(pady=5, padx=10)
        self.send_button = CTkButton(chat_frame, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)


        # --- Display Users in the Room ---
        self.user_list_label = CTkLabel(chat_frame, text="Online Users: None", font=("Arial", 14))
        self.user_list_label.pack(pady=10)
        self.who_button = CTkButton(chat_frame, text="Who is Online???! ", command=self.get_users)
        self.who_button.pack(pady=5)


        # --- User Login Tab ---
        login_frame = tabview.tab("User Login")
        CTkLabel(master=login_frame, text="Login", font=("Arial Bold", 20)).pack(pady=(10, 15))
        self.username_entry = CTkEntry(login_frame, placeholder_text="Username")
        self.username_entry.pack(expand=True, pady=10, padx=20)
        self.room_entry = CTkEntry(login_frame, placeholder_text="Chat Room")
        self.room_entry.pack(expand=True, pady=10, padx=20)
        self.connect_button = CTkButton(login_frame, text="Join Chat", command=self.connect)
        self.connect_button.pack(pady=10)


        # ---------- Settings ----------
        frame_right = CTkFrame(master=root, fg_color="gray", border_width=2)
        frame_right.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        CTkLabel(master=frame_right, text="Settings", font=("Arial Bold", 20)).pack(pady=15)
        self.clear_chat_button = CTkButton(frame_right, text="Clear Chat", fg_color="red", command=self.clear_chat_history)
        self.clear_chat_button.pack(pady=5)
        self.leave_button = CTkButton(frame_right, text="Leave Chat", fg_color="red", command=self.leave_chat)
        self.leave_button.pack(pady=5)

        self.running = False 
        self.chat_room = ""
        self.username = ""
        self.lock = threading.Lock()


    # ---------- Chat Functions ----------
    def connect(self):
        self.username = self.username_entry.get()
        self.chat_room = self.room_entry.get()
        if not self.username or not self.chat_room:
            CTkMessagebox(title="Error", message="Username and Room cannot be empty", icon="cancel")
            return
        response = self.server.connect_function(self.chat_room, self.username)
        self.update_chat(response)
        self.running = True
        threading.Thread(target=self.poll_messages, daemon=True).start()


    def send_message(self):
        message = self.message_entry.get()
        if message:
            with self.lock:
                response = self.server.say_function(self.chat_room, self.username, message)
            self.message_entry.delete(0, END)
            


    def get_users(self):
        with self.lock:
            users = self.server.who_function(self.chat_room)
        if users:
            self.user_list_label.configure(text=f"Online Users: {', '.join(users)}")
        else:
            self.user_list_label.configure(text="Online Users: None")


    def clear_chat_history(self):
        with self.lock:
            response = self.server.clear_chat_history(self.chat_room)
        self.update_chat(response)


    def leave_chat(self):
        with self.lock:
            response = self.server.leave_function(self.chat_room, self.username)
        self.running = False
        self.update_chat(response)



    def update_chat(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert("end", message + "\n")
        self.chat_display.configure(state='disabled')


    def poll_messages(self):
        while self.running:
            with self.lock:
                messages = self.server.get_messages(self.chat_room)
            self.chat_display.configure(state='normal')
            self.chat_display.delete("1.0", END)  # Clear chat box
            for msg in messages:
                self.chat_display.insert("end", msg + "\n")
            self.chat_display.configure(state='disabled')
        time.sleep(2)  


client = ChatClient(app)
app.mainloop()
