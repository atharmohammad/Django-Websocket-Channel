import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] #Extractig the room_name
        self.room_group_name = 'chats_%s' % self.room_name   #Giving a Group name

        await self.channel_layer.group_add( #Adding the group in user
            self.room_group_name,
            self.channel_name
        )

        await self.accept() #accept to connect

        await self.channel_layer.group_send(    #To send message in group
            self.room_group_name,
            {
                'type':'tester_message',    #This type is will be the name of function calls
                'tester':'Hello Group'
            }
        )

    async def tester_message(self,event):
        tester = event['tester']

        await self.send(text_data=json.dumps({
            'tester': tester
        }))

    async  def disconnect(self,close_code):
        #Leave room group
        await self.channel_layer.group_discard( #discarding the group by giving it the group and channel name
            self.room_group_name,
            self.channel_name
        )
