Installation:

* Before running the application, you must install the required UI library. Open your Terminal or Command Prompt and run: pip install customtkinter
Launch the Server.

* Launch the Server:

The server must be running before any users can connect.
  
Run the file: “Server.py”
Once active, you should see the following confirmation message in your terminal: Server is running on 127.0.0.1:55555.

* Launch the Client:
  
 To join the chat, run the client application.
 You can run this file multiple times to simulate different users.
 Run the file: “client_gui.py”
 important: Ensure that “client_gui.py” and “client_logic.py” are located in the same folder for the program to function.
 User Login & Username Rules
 Upon launching the client, a login window will appear. Please note the following rules:
 
 1. Uniqueness: Every user must have a unique name.

 2. Case Sensitivity: The system treats names as unique regardless of capitalization. For example, if "Avi" is already logged in, you cannot log in as      "avi" or "AVI." The system will reject the name and display an error.
 3. Identification: Your active username will be displayed in the top-left corner of the chat window for easy reference.


* Messaging and Communication:
  
 Once connected, you can start chatting:
 1. Direct Messaging: Click a name in the Online Users column to select them.
 
 2. Manual Format: Type the recipient's name followed by a colon and a space in the message box: RecipientName: {your message}
 Disconnecting.
 
 * To leave the chat and notify the server:
 
 Click the red Disconnect button.
 OR close the window using the X in the top-right corner.
 Note: When a user disconnects, a status message will automatically appear in the Server Terminal and the chat logs of all other active users.
