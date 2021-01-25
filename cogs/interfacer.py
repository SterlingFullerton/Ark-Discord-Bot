import discord
from discord.ext import commands, tasks
from discord.abc import Messageable
from functions import read_json, write_json, append_json
from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Interfacer(commands.Cog):
    def __init__(self, client):
        self.USERNAME = getenv("USERNAME")
        self.PASSWORD = getenv("PASSWORD")
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Interfacer is online.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rcon(self, ctx, *, command):
        rcon_client = SSHClient()
        rcon_client.set_missing_host_key_policy(AutoAddPolicy())
        rcon_client.connect('158.69.23.49', username=self.USERNAME, password=self.PASSWORD)

        msg = await ctx.send("Started")
        stdin, stdout, stderr = rcon_client.exec_command(command, get_pty=True)

        for line in iter(stdout.readline, ""):
            if len(msg.content) > 2000 or len(msg.content)+len(line) > 2000:
                msg = await ctx.send("Hit Message Limit")
            await msg.edit(content=f'{msg.content}\n{line}')

        await msg.edit(content=f'{msg.content}\nFinished | Return code: {stdout.channel.recv_exit_status()}')

        stdin.close()
        stdout.close()
        stderr.close()

        rcon_client.close()

def setup(client):
    client.add_cog(Interfacer(client))
