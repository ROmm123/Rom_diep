from socket import *
from threading import *
from tkinter import *
from Network_chat import *
import pygame
from pynput.keyboard import Key, Listener

class ChatClient:
    def __init__(self, host_chat, client_chat):

        self.chat = Client_chat(host_chat, client_chat)
        self.chat.connect()

        self.window = Tk()
        self.window.title("chat")
        self.window_state = True  # Track window state

        self.txtMessages = Text(self.window, width=50)
        self.txtMessages.grid(row=0, column=0, padx=10, pady=10)

        self.txtYourMessage = Entry(self.window, width=50)
        self.txtYourMessage.insert(0, "Your message")
        self.txtYourMessage.grid(row=1, column=0, padx=10, pady=10)

        self.btnSendMessage = Button(self.window, text="Send", width=20, command=self.sendMessage)
        self.btnSendMessage.grid(row=2, column=0, padx=10, pady=10)

        self.recvThread = Thread(target=self.recvMessage)
        self.recvThread.daemon = True
        self.recvThread.start()

        # הוספת תהליך רקידה לקליטת מקשים
        self.keyboard_listener = Listener(on_press=self.on_key_press)
        self.keyboard_listener.daemon = True
        self.keyboard_listener.start()


        self.hide_chat()
        self.window.mainloop()

    def open_chat(self):
        self.window.deiconify()  # Show the window

    def hide_chat(self):
        self.window.withdraw()  # Hide the window

    def sendMessage(self):
        clientMessage = self.txtYourMessage.get()
        self.txtMessages.insert(END, "\n" + "You: " + clientMessage)
        self.chat.send_data(clientMessage)

    def recvMessage(self):
        while True:
            serverMessage = self.chat.recevie_data()
            print(serverMessage)
            self.txtMessages.insert(END, "\n" + serverMessage)

    # פונקציה לטיפול בלחיצות מקלדת
    def on_key_press(self, key):
        try:
            if key.char == 'c':
                self.open_chat()
            elif key.char == 'e':
                self.hide_chat()
        except AttributeError:
            print("eroror")