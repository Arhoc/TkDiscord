# ===================================================================
# Copyright (C) 2023 Arhoc <arhoc@darktech.tk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ===================================================================

import discum
import tkinter as tk
from tkinter import scrolledtext, Frame
from tkinter.ttk import Style, Scrollbar

class DiscordClient:
    def __init__(self, token):
        self.token = token
        self.client = discum.Client(token=self.token)

        # create the tkinter window
        self.window = tk.Tk()
        self.window.title("Discord Client")
        self.window.geometry('800x600')

        # create a frame to hold the messages box and scrollbar
        self.messages_frame = Frame(self.window)
        self.messages_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # create a scrollbar and attach it to the messages box
        self.scrollbar = Scrollbar(self.messages_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # create a text box to display messages
        self.messages_box = scrolledtext.ScrolledText(
            self.messages_frame,
            height=20,
            width=60,
            bg='#36393f',
            fg='white',
            insertbackground='white',
            wrap=tk.WORD,
            yscrollcommand=self.scrollbar.set
        )
        self.messages_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # configure the scrollbar to scroll the messages box
        self.scrollbar.config(command=self.messages_box.yview)

        # add a frame to hold the input box and send button
        self.input_frame = Frame(self.window, bg='#2f3136')
        self.input_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # add a text box for user input
        self.input_box = tk.Entry(self.input_frame, width=60, bg='#40444b', fg='white')
        self.input_box.pack(side=tk.LEFT, padx=10, pady=4)

        # add a button to send messages
        self.send_button = tk.Button(
            self.input_frame,
            text='Send',
            command=self.send_message,
            bg='#7289da',
            fg='white',
            activebackground='#677bc4',
            activeforeground='white'
        )
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=4)

    def run(self):
        # connect to the Discord API using the provided token
        self.client.gateway.fetchGateway()

        # handle incoming messages and display them in the text box
        @self.client.gateway.command
        def handle_messages(resp):
            if resp.event.message:
                message_data = resp.parsed.auto()
                message = f'[ {message_data["author"]["username"]}#{message_data["author"]["discriminator"]} ]  {message_data["content"]}'
                self.messages_box.insert(tk.END, f'{message}\n')

        # start the client
        self.client.gateway.run()

    def send_message(self):
        # get the message from the input box and send it to Discord
        message = self.input_box.get()
        if message:
            self.client.sendMessage('channel_id', message)
            self.messages_box.insert(tk.END, f'[ You ]  {message}\n')
            self.input_box.delete(0, tk.END)

if __name__ == '__main__':
    # replace 'token' with your own Discord bot token
    client = DiscordClient('token')

    # configure the style of the tkinter window to match Discord's dark theme
    style = Style()
    style.theme_use('clam')
    style.configure('.', background='#2f3136')
    style.configure('TScrollbar', background='#202225')
    style.configure('TEntry', fieldbackground='#40444b')

    # run the client
    client.run()
