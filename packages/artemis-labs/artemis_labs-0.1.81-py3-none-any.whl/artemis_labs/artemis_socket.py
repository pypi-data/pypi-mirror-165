'''
This serves the local websocket on 127.0.0.1:5678 and manages communications
with this websocket
'''

# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=broad-except
# pylint: disable=consider-using-with
# pylint: disable=too-many-branches

import asyncio
import queue
import threading
import json
import os
from collections.abc import Callable
import websockets

class ArtemisSocket:
    '''
    This class creates a websocket and serves it on 127.0.0.1. This websocket class
    can be used to create the websocket, check if this websocket is active,
    send messages, set callbacks for messages
    '''

    # Heartbeat
    heartbeat = json.dumps(({ "type" : "heartbeat", "attribute" : "", "name" : "" }))

    # Connected status
    connected = False

    def __init__(self, callback_message_received : Callable[[str], None], ip_addr : str = '127.0.0.1', port:int = 5678):
        '''
        Stores websocket information and sets up queues for callbacks. This does not
        actually start the websocket
        :param callback_message_received: Callback to call when a message is received
        :param ip_addr: Ip address of websocket
        :param port: Port for websocket
        '''
        self.ip_addr = ip_addr
        self.port = port
        self.messages = queue.Queue(maxsize=0)
        self.callback_message_received = callback_message_received
        self.connected = False

    def is_connected(self) -> bool:
        '''
        Checks if a client is connected to the websocket
        :return: Whether a client is connected to the websocket
        '''
        return self.connected

    def send(self, message : str) -> None:
        '''
        Send a message out the websocket
        :param message: S
        :return:
        '''
        self.messages.put(message)

    async def server(self, web_socket) -> None:
        '''
        This in an infinite loop which waits for websocket messages
        and calls the callback when it gets one, and sends websocket messages
        when ones are added to its queue
        :param web_socket: web_sockets websocket
        :param path: Extra param
        :return: None
        '''
        while True:

            # Wait for message
            try:
                message = await web_socket.recv()
            except websockets.exceptions.ConnectionClosed as exception:
                print("[Artemis] Connection closed")
                print('[Artemis] Exception: ')
                print(exception)
                os._exit(1) #pylint: disable=protected-access
                break

            # Set connected
            self.connected = True

            # Notify callbacks
            self.callback_message_received(message)

            # Send messages in queue
            while not self.messages.empty():
                message = self.messages.get()
                await web_socket.send(message)

            # Send message
            await web_socket.send(self.heartbeat)

    def launch_main_loop(self) -> None:
        '''
        Main loop which calls server to serve websocket
        :return: None
        '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server = websockets.serve(self.server, self.ip_addr, self.port) #pylint: disable=no-member
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()

    def run(self) -> None:
        '''
        Launch server on a new daemon thread
        :return: None
        '''
        thread = threading.Thread(target=self.launch_main_loop, daemon=True)
        thread.start()
