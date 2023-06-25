import discord
from discord.ext import commands
import openai

class ChatGPT(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.file = "1"
        
        # Update this part based on your desired logic
        match self.file:
            case "1":
                self.file = "chat1.txt"
            case "2":
                self.file = "chat2.txt"
            case "3": 
                self.file = "chat3.txt"
            case _:
                print("Invalid choice.")
                exit()

        with open(self.file, "r") as f:
            self.chat = f.read() 

        openai.api_key = "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"

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author != self.client.user:
                self.chat += f"{message.author}: {message.content}\n"
                print(f'Message from {message.author}: {message.content}')
                if self.client.user in message.mentions:
                    response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=f"{self.chat}\nHarryGPT: ",
                        temperature=1,
                        max_tokens=256,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )
                    channel = message.channel
                    messageToSend = response.choices[0].text
                    await channel.send(messageToSend)    
        except Exception as e:
            print(e)
            self.chat = ""

async def setup(client):
    await client.add_cog(ChatGPT(client))
