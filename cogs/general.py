import discord
from discord.ext import commands, tasks
from discord.abc import Messageable
from functions import read_json, write_json, append_json
from datetime import datetime
from pytz import timezone
import a2s

class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('General is online.')
        self.player_log.start()

    @tasks.loop(seconds=300)
    async def player_log(self):
        time = str(datetime.time(datetime.now())).split('.')[0]
        date = str(datetime.date(datetime.now()))

        SERVERS = {
            "Ragnarok": {
                "ADDRESS": ("158.69.23.49", 27015),
                "MESSAGE_ID": 747115005408837694},
            "Aberration": {
                "ADDRESS": ("158.69.23.49", 27016),
                "MESSAGE_ID": 764249524511572019}
        }
        RULES_AND_SERVER_INFO = 701142199772905472

        for server in SERVERS:
            try:
                #Get Current Players on Server
                players = a2s.players(SERVERS[server]["ADDRESS"])

                #Get Version
                info = a2s.info(SERVERS[server]["ADDRESS"])
                server_name = info.server_name
                version = server_name.split(' - ')[2][1:-1]

                #Formatting output
                output = f'```A World Reforged S2 - {server} - {version}\nLast Check: {date} {time} EST\n\n'
                output += f'Players:              Current Session:\n'


                #Player(index=0, name='', score=0, duration=169782.90625)
                for player in players:
                    if player.name != '':
                        output += f'{player.name:<20}  {player.duration/3600:>8.2f}hrs\n'

                output += '```'

            except Exception as e:
                output = f'```A World Reforged S2 - {server} - ERROR\nLast Check: {date} {time} EST\n\nError: {e}```'

            message = await self.client.get_channel(RULES_AND_SERVER_INFO).fetch_message(SERVERS[server]["MESSAGE_ID"])
            await message.edit(content=output)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            title = 'How to: RumorMan',
            colour=discord.Colour(0xE5E242),
            description = '.rumor : Post an anonymous rumor (DM)\n.report : Report anonymously to Admin (DM)\n.vc request a user to join your private tribe vc'
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def pfp(self, ctx, *, person):
        user = await self.client.guilds[0].query_members(person)
        user = user[0]
        await ctx.send(f'{user.avatar_url}')

    @commands.command(aliases=['Rumor'])
    async def rumor(self, ctx, *, rumormsg=''):
        if ctx.message.channel.type.name != 'private':
            await ctx.send('Try using this command in a DM :smile:')
            return

        rumor_channel = self.client.get_channel(703630291931234375)

        if rumormsg != '':
            await rumor_channel.send('```' + rumormsg + '```')
        if 'attachments' in dir(ctx.message):
            if len(ctx.message.attachments) > 0:
                rumormsg += f'|||{ctx.message.attachments[0].url}'
                await rumor_channel.send(ctx.message.attachments[0].url)

        if rumormsg == '' and 'attachments' not in dir(ctx.message):
            await ctx.send('What rumor?')
            return

        time = str(ctx.message.created_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('US/Eastern')))[:19]
        try:
            append_json('rumor_log', [(time,{str(ctx.message.author): rumormsg})])
        except:
            write_json('rumor_log', {time, {str(ctx.message.author): rumormsg}})

        await ctx.send('Rumor Sent!')

    @commands.command()
    async def suggestion(self, ctx, s, *, sugg):
        s = ' '.join(s.split('_'))
        embed = discord.Embed(
            title = f'{s}',
            colour=discord.Colour(0x00ffff),
            description = f'{sugg}'
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('OH')

    @commands.command(aliases=['whisper', 'gods'])
    async def w(self, ctx, *, msg):
        if ctx.message.channel.type.name != 'private':
            await ctx.send('Try using this command in a DM :smile:')
            return

        await self.client.get_channel(742964294408470537).send(f'{ctx.message.author}: {msg}')

    @commands.command(aliases=['Report'])
    async def report(self, ctx, *, reportmsg=''):
        if ctx.message.channel.type.name != 'private':
            await ctx.send('Try using this command in a DM :smile:')
            return

        author = str(ctx.message.author)
        reports = read_json('reports')
        if author not in reports: reports[author] = []
        reports[author].append(reportmsg)
        write_json('reports', reports)

        await self.client.get_channel(743254371843702804).send('```' + reportmsg + '```')




def setup(client):
    #client.remove_command('help')
    client.add_cog(General(client))
