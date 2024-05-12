from socket import *
from threading import *
from tkinter import *
from Network_chat import *
import pygame
import sys

class ChatClient:
    def __init__(self, host_chat, client_chat, player):
        self.flag = False
        self.chat = Client_chat(host_chat, client_chat)
        self.chat.connect()
        self.player = player
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
        self.checkThread = Thread(target=self.check_sit)
        self.recvThread.daemon = True
        self.recvThread.start()
        self.checkThread.start()

        self.window.protocol("WM_DELETE_WINDOW", self.close_window)  # Handle window close event

        self.window.mainloop()

    def close_window(self):
        # Set player chat flag to False and destroy the window
        self.player.chat_flag = False
        self.window.destroy()

    def sendMessage(self):
        clientMessage = self.txtYourMessage.get()
        self.txtMessages.insert(END, "\n" + "You: " + clientMessage)
        self.chat.send_data(clientMessage)

    def recvMessage(self):
        while self.player.chat_flag:
            serverMessage = self.chat.recevie_data()
            print(serverMessage)
            self.txtMessages.insert(END, "\n" + serverMessage)

    def check_sit(self):
        while self.player.chat_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.player.chat_flag = False
                    self.window.after(0, self.window.destroy)  # Schedule window destruction
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.player.chat_flag = False
                        self.window.after(0, self.window.destroy)  # Schedule window destruction
                        break

