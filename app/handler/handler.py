from app.handler.MessageEvent.handler import MessageEventHandler
from app.handler.FollowEvent.handler import FollowEventHandler

class Handler():
    def __init__(self):
        self.messageHandler = MessageEventHandler()
        self.followHandler = FollowEventHandler()

    def handle(self, event):
        if (event.type == 'message'):
            self.messageHandler.handle(event)
        elif (event.type == 'follow'):
            self.followHandler.handle(event)