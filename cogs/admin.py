import discord
from discord.ext import commands, tasks
from discord.abc import Messageable
from functions import read_json, write_json, append_json, log
from random import randint
import time, os, subprocess, sys

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Admin is online.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        await self.client.guilds[0].get_channel(656594748802596867).send("Bot Exiting...")
        sys.exit(0)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=2, hidden=True):
        if amount < 31:
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.channel.purge(limit=1)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def edit(self, ctx, channel_id, message_id, *, new_message):
        channel = self.client.guilds[0].get_channel(int(channel_id))
        message = await channel.fetch_message(int(message_id))
        await message.edit(content=new_message)
        await ctx.send('The Message has been edited')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, *, msg):
        person = ''
        find_one_hash = True
        for i, char in enumerate(msg):
            if char == '#' and find_one_hash:
                person = msg[:i+5]
                msg = msg[i+6:]
                find_one_hash = False
                break

        #Find User DM Channel
        for member in self.client.guilds[0].members:
            if str(member.name)+'#'+str(member.discriminator) == person:
                requested_member = member
                break

        await ctx.channel.purge(limit=1)
        await ctx.send(f'Admin {ctx.message.author} ---> {ctx.message.content}')
        await requested_member.send(msg)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def whorumor(self, ctx, *, requested_rumor):
        history = read_json('rumor_log')
        times = list(history.keys())

        for i in history:
            for name in history[i]:
                if history[i][name] == requested_rumor:
                    await ctx.send(f'The Person you are looking for is ||{name:^50}||')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def postthething(self, ctx, *, other):
        await self.client.guilds[0].get_channel(701116605769318541).send(other)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ShowJoinMessage(self, ctx):
        with open('Newbie_Message.txt', 'r') as fp:
            txt = fp.read()
        await ctx.send(txt)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ChangeJoinMessage(self, ctx, *, txt):
        with open('Newbie_Message.txt', 'w') as fp:
            txt = fp.write(txt)
        await ctx.send('Message Changed!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def testing(self, ctx):
        for member in self.client.guilds[0].members:
            if member.name == ctx.author.name:
                #log('', [member.name, member.discriminator, member.id, member.nick])
                with open('Newbie_Message.txt', 'r') as fp:
                    txt = fp.read()
                await member.send(txt)

def setup(client):
    client.add_cog(Admin(client))
