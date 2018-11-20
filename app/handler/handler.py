from app.handler.MessageEvent.handler import MessageEventHandler
from app.handler.FollowEvent.handler import FollowEventHandler

class Handler():
    def __init__(self):
        self.message_handler = MessageEventHandler()
        self.follow_handler = FollowEventHandler()

    def handle(self, event):
        print(event.type)
        
        if (event.type == 'message'):
            self.message_handler.handle(event)

        if (event.type == 'follow'):
            self.follow_handler.handle(event)