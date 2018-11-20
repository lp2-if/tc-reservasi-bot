from app.handler.MessageEvent.handler import MessageEventHandler
from app.handler.FollowEvent.handler import FollowEventHandler
from app.handler.JoinEvent.handler import JoinEventHandler

class Handler():
    def __init__(self):
        self.message_handler = MessageEventHandler()
        self.follow_handler = FollowEventHandler()
        self.join_handler = JoinEventHandler()

    def handle(self, event):
        print(event.type)
        
        if (event.type == 'message'):
            self.message_handler.handle(event)

        if (event.type == 'follow'):
            self.follow_handler.handle(event)

        if (event.type == 'join'):
            self.join_handler.handle(event)