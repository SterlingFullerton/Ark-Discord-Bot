import discord
from discord.ext import commands, tasks
from discord.abc import Messageable
from datetime import datetime, timedelta

class Vcmove(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.vcmoveinformation = []

    @commands.Cog.listener()
    async def on_ready(self):
        print('Vcmove is online.')

    @commands.command()
    async def vc(self, ctx, *, person):
        print('vcmoverequest')
        await ctx.message.delete()
        #get_voice_channels of discord
        tribelist = []
        tribevclist = []
        for guild in self.client.guilds:
            for channel in guild.channels:
                if str(channel.type) == 'voice':
                    if str(channel.category) == 'Tribes':
                        tribelist.append(channel.name)
                        tribevclist.append(channel.id)

        #Get asking user and tribe
        asking_user = await self.client.guilds[0].query_members(ctx.author.name)
        asking_user = asking_user[0]

        for role in asking_user.roles:
            if role.name in tribelist:
                asking_user_tribe = role
                asking_user_tribe_vc = self.client.guilds[0].get_channel(tribevclist[tribelist.index(role.name)])

        #get asking discord
        requested_user_id = await self.client.guilds[0].query_members(person.split('#')[0])
        requested_user = requested_user_id[0]

        request_message = await ctx.send(f'vc request sent!\nAsking User: {asking_user}\nRequested User: {requested_user.mention}\nVoice Channel: {asking_user_tribe}')

        random = "be magically transported on a rainbow bridge"

        request_message2 = await ctx.send(f"""```Voice Chat Move Request From {asking_user.name} Would you like to enter {asking_user_tribe}'s VC?\n\nUse the .join command to {random}```""")
        #or requested_user.send

        self.vcmoveinformation.append((datetime.now(), requested_user, asking_user, asking_user_tribe_vc, request_message, request_message2))

    @commands.command()
    async def join(self, ctx):
        print('vcmoverequest accepted')
        await ctx.message.delete()
        for i in self.vcmoveinformation:
            oldtime = i[0]

            if ((datetime.now() - timedelta(minutes=15)) > oldtime):
                self.vcmoveinformation.pop(self.vcmoveinformation.index(i))
                await request_message.delete()
                await request_message2.delete()
            else:
                requested_user = i[1]
                if ctx.author == requested_user:
                    asking_user = i[2]
                    asking_user_tribe_vc = i[3]
                    request_message = i[4]
                    request_message2 = i[5]

                    await requested_user.move_to(asking_user_tribe_vc)

                    self.vcmoveinformation.pop(self.vcmoveinformation.index(i))

                    await request_message.delete()
                    await request_message2.delete()


def setup(client):
    client.add_cog(Vcmove(client))
