# Chat Ap

This is a Python-based chat application that supports real-time messaging via XML-RPC. The project includes both a command-line interface and a modern graphical interface built using `customtkinter`.

## Features

* Join multiple chat rooms
* Send and receive messages in real time
* View online users in the current chat room
* Clear chat history
* Leave chat room gracefully
* GUI version with separate tabs for chat and login
* Multithreaded server to support concurrent clients

---

## Screenshots

### GUI - Chat Room

![Chat Room Screenshot](v![image](https://github.com/user-attachments/assets/1043ffe3-ad83-46d0-b80d-362c3bd30f5e))

### GUI - User Login

![User Login Screenshot](![image](https://github.com/user-attachments/assets/2ed33525-95de-471d-a9c4-17a8610f8a68))

### CLI  - Options

![Settings Screenshot](v![image](https://github.com/user-attachments/assets/3aff5fe9-33f0-497b-a78d-c2c88216eb6d))

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/chat_app.git
cd chat_app
```

### 2. Install Dependencies

```bash
pip install customtkinter
```

No external server frameworks are needed; the project uses Python’s built-in `xmlrpc`.

### 3. Start the Server

```bash
python server.py
```

### 4. Start the Client

For the **Command Line Interface**:

```bash
python client_cli.py
```

For the **Graphical Interface**:

```bash
python client_gui.py
```

---

## Project Structure

```
chat_app/
├── client_cli.py      # Command-line interface for chat
├── client_gui.py      # GUI interface using customtkinter
├── server.py          # XML-RPC chat server
├── README.md          # Project documentation
└── *.png              # GUI screenshots
```

---

## Technologies Used

* Python 3
* `xmlrpc.server` and `xmlrpc.client`
* `customtkinter` for GUI
* Threading for concurrent message polling

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
