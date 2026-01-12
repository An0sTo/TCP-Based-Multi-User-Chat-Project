import customtkinter as ctk
from client_logic import ChatClientLogic


class ChatGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat Login")
        self.geometry("750x550")

        # Keep track of my name to filter the list and prevent self-messaging
        self.my_name = None

        self.logic = ChatClientLogic()
        self.logic.on_message_received = self.handle_incoming_message
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Layout settings
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar for online users (Will hide self)
        self.sidebar = ctk.CTkScrollableFrame(self, width=160, label_text="Online Users")
        self.sidebar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.chat_display = ctk.CTkTextbox(self, state="disabled")
        self.chat_display.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entry_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.entry_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Name: Message...")
        self.entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.entry.bind("<Return>", lambda e: self.send_action())

        self.send_btn = ctk.CTkButton(self.entry_frame, text="Send", command=self.send_action)
        self.send_btn.grid(row=0, column=1)

        self.disconnect_btn = ctk.CTkButton(self, text="Disconnect", fg_color="#922b21", command=self.on_closing)
        self.disconnect_btn.grid(row=1, column=0, padx=10, pady=10)

        self.after(100, self.ask_for_name)

    def handle_incoming_message(self, message):
        # Case: Name taken - Infinite Loop protection
        if message == "ERR_NAME_TAKEN":
            self.update_chat("[SYSTEM] This name is taken. Please choose another.")
            self.logic.disconnect()
            self.after(100, self.ask_for_name)
            return

        # Case: Update sidebar user list
        if message.startswith("LIST:"):
            for child in self.sidebar.winfo_children(): child.destroy()
            users = message.replace("LIST:", "").split(",")
            for user in users:
                # FIX: Don't show myself in the online users list
                if user and user != self.my_name:
                    ctk.CTkButton(self.sidebar, text=f"👤 {user}", fg_color="transparent", anchor="w",
                                  command=lambda u=user: self.set_recipient(u)).pack(fill="x", pady=2)

        elif "JOINED" in message or "LEFT" in message:
            self.update_chat(f"\n📢 {message}\n")
        else:
            self.update_chat(message)

    def set_recipient(self, name):
        # FIX: Added space after colon for easier typing
        self.entry.delete(0, 'end')
        self.entry.insert(0, f"{name}: ")
        self.entry.focus()

    def ask_for_name(self):
        # Prompt user and set Dynamic Title
        name = ctk.CTkInputDialog(text="Enter a unique name:", title="Login").get_input()
        if name:
            self.my_name = name.capitalize()  # Save for local checks
            if self.logic.connect(name):
                self.title(f"Logged in as: {self.my_name}")
        else:
            self.destroy()

    def send_action(self):
        msg = self.entry.get()
        if not msg: return

        # FIX: Local check to prevent messaging yourself
        if ":" in msg:
            target, content = msg.split(":", 1)
            if target.strip().capitalize() == self.my_name:
                self.update_chat("❌ [SYSTEM] You can't message yourself!")
                self.entry.delete(0, 'end')
                return

        self.logic.send_message(msg)
        self.update_chat(f"You: {msg}")
        self.entry.delete(0, 'end')

    def update_chat(self, text):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", text + "\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def on_closing(self):
        self.logic.disconnect()
        self.destroy()


if __name__ == "__main__":
    app = ChatGUI()
    app.mainloop()