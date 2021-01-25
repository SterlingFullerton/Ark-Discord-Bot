import discord
from discord.ext import commands
import os
from random import randint, choice
from functions import read_json, write_json, append_json, log
from datetime import datetime, timedelta
import asyncio


class Ispy(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.author = ''
        self.image = ''
        self.image_index = ''
        self.image_channel_message_ids = []
        self.giveup_counter = {}
        self.no_more_posting_categories = ['Archived S2', 'Archived S3', 'Archived S4', 'Archived AWR S1']
        self.no_category_entry = ['Admin', 'Tribes', 'Guilds', 'Offerings']
        self.no_channel_entry = ['sheogorath-ooc', 'ashurah-ooc', 'tarquin-ooc', 'ispy', 'cute-animals', 'ispy-history']
        self.valid_formats = ['png', 'jpeg', 'mp3', 'PNG', 'gif', 'jpg', 'JPG', 'mp4', 'webp', 'mov', 'webm']
        #self.ispy_channel = self.client.guilds[0].get_channel(744413372987998328)

    @commands.Cog.listener()
    async def on_ready(self):
        print('Ispy is online.')
        info = read_json('ispy_image')
        self.author = info['author']
        self.image = info['image']
        self.image_index = info['message'].split('_')[1]
        self.image_channel_message_ids = [info['channel'], info['message']]

    @commands.Cog.listener()
    async def on_message(self, message):
        attachments = message.attachments
        if (len(attachments) > 0) and (message.author != 'RumorMan#7258') and (str(message.channel.category) not in self.no_category_entry) and (str(message.channel.name) not in self.no_channel_entry) and (message.channel.nsfw == False):
            image_locations = read_json('image_urls')
            for attachment in attachments:
                log("ISPY Image Tracker - Adding", [message.channel.id, f'{message.id}_{attachments.index(attachment)}', 'Author:', message.author, 'Channel:', message.channel])
                #print(f'{datetime.now()} | ISpy Image Tracker - Adding: {message.channel.id} {message.id}_{attachments.index(attachment)} Author: {message.author} Channel: {message.channel}')
                image_locations['unused'][str(message.channel.id)].append(f'{message.id}_{attachments.index(attachment)}')
            write_json('image_urls', image_locations)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message.channel.id == 744413372987998328:
            channel = self.client.guilds[0].get_channel(776678349245644820)
            await channel.set_permissions(user, read_messages=True, read_message_history=True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def update(self, ctx, override=''):
        start_time = datetime.now()

        #Notify Users and Disallow Sending Messages
        log('ISpy Update Started', [])
        await ctx.send('Update started!')
        #await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

        image_locations = read_json('image_urls')

        if 'unused' not in image_locations.keys():
            image_locations['unused'] = {}
        if 'used' not in image_locations.keys():
            image_locations['used'] = {}

        for channel in self.client.guilds[0].channels:
            if (str(channel.type) == 'text') and (str(channel.category) not in self.no_category_entry) and (str(channel.name) not in self.no_channel_entry) and (channel.nsfw == False):
                if str(channel.category) in self.no_more_posting_categories and override == '':
                    print(f'{"":27}| Remembering {channel.category} -> {channel.name}')
                else:
                    messages = await channel.history(limit=100000).flatten() #Retrieve all messages within current text channel
                    print(f'{"":27}| {channel.category} -> {channel.name} -> {len(messages)}')

                    #Go through every message 0_o or Maybe not
                    for message in messages:
                        #print(type(message.created_at), message.created_at)
                        if message.attachments != []:
                            if str(message.id) in image_locations['unused'].keys() and str(message.id) in image_locations['used'].leys():
                                break
                            for i, attachment in enumerate(message.attachments):
                                if attachment.url.split('.')[-1] in self.valid_formats:
                                    if str(channel.id) in image_locations['unused'].keys():
                                        image_locations['unused'][str(channel.id)].append(f'{message.id}_{i}')
                                    else:
                                        image_locations['unused'][str(channel.id)] = [f'{message.id}_{i}']

        write_json('image_urls', image_locations)

        file = os.getcwd() + '\\image_urls.json'
        filesize = os.stat(file).st_size

        end_time = datetime.now()
        time_taken = end_time-start_time

        log('Update Done!', ['FileSize', '=', filesize])
        await ctx.send(f'Update Done!\nSize of File = {filesize}bytes\nTook{time_taken}')
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await asyncio.sleep(10)
        await ctx.invoke(self.client.get_command('picpls'))

    @commands.command()
    async def picpls(self, ctx):
        if ctx.channel.id != 744413372987998328:
            return

        if self.author != '':
            return

        await ctx.channel.purge(limit=1000)

        image_locations = read_json('image_urls')
        if 'unused' not in image_locations.keys():
            await ctx.invoke(self.client.get_command('update'), 'override')
        channels = image_locations['unused']

        #Get total # of images
        sum_of_weights = 0
        for messages in channels:
            sum_of_weights += int(len(channels[messages]))

        #Pick random Number based on total # of images
        random_int = randint(0, sum_of_weights)
        sum_of_weights_2 = 0

        #Finds The Picture Channel
        for messages in channels:
            if sum_of_weights_2 < random_int:
                sum_of_weights_2 += int(len(channels[messages]))
                picture_channel = messages
            else:
                break

        #Subtracks from the total # of images till it finds the picture channel
        for messages in channels:
            if messages != picture_channel:
                sum_of_weights -= len(channels[messages])
                random_int -= len(channels[messages])
            else:
                break



        channel_id = int(picture_channel)
        message_id_i = channels[picture_channel][random_int]
        message_id = message_id_i.split('_')[0]

        channel = self.client.guilds[0].get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        self.image_channel_message_ids = [picture_channel, message_id_i]
        self.author = message.author
        self.image_index = message_id_i.split('_')[1]
        self.image = message.attachments[int(self.image_index)].url

        info = {"author":str(self.author), "channel":str(picture_channel), "image":str(self.image), "message":str(message_id_i)}
        write_json('ispy_image', info)

        log('ISPY', [self.author, self.image])
        await ctx.send(f'Channel: {channel.name}')
        await ctx.send(self.image)

    @commands.command(aliases=['Guess', 'g', 'G'])
    async def guess(self, ctx, *, person):
        #nobody be allowed to guess outside the ispy channel
        if ctx.channel.id != 744413372987998328:
            return

        #if no image loaded, load one
        if self.author == '':
            info = read_json('ispy_image')
            if 'author' in info.keys():
                self.author = info['author']
                self.image = info['image']
                self.image_index = info['message'].split('_')[1]
                self.image_channel_message_ids = [info['channel'], info['message']]
            else:
                await ctx.invoke(self.client.get_command('picpls'))
                return

        #Check if user that guesses is in the leaderboard file, if not add them
        leaderboard = read_json('ispy_leaderboard')
        if str(ctx.author) not in leaderboard:
            leaderboard[str(ctx.author)] = {}
            leaderboard[str(ctx.author)]['Correct_Guesses'] = 0
            leaderboard[str(ctx.author)]['Wrong_Guesses'] = 0
            leaderboard[str(ctx.author)]['Points_Lost'] = 0
            leaderboard[str(ctx.author)]['Give_Ups'] = 0



        #Correct
        if person.lower() == str(self.author).lower() or (person.lower() in str(self.author).lower() and len(person) > 3):
            #Post to Ispy History
            ispy_history = self.client.guilds[0].get_channel(776678349245644820)
            color = int(f'{hex(randint(0,256))[2:]}{hex(randint(0,256))[2:]}{hex(randint(0,256))[2:]}', 16)
            embed = discord.Embed(title=str(self.author), color=color)
            embed.set_image(url=str(self.image))
            await ispy_history.send(embed=embed)
            #await ispy_history.send(f'_ _\n||{self.author}||')
            #await ispy_history.send(self.image)

            #Update Score
            leaderboard[str(ctx.author)]['Correct_Guesses'] += 1
            points = leaderboard[str(ctx.author)]['Correct_Guesses']-leaderboard[str(ctx.author)]['Points_Lost']
            await ctx.send(f'Yay! You got it right! You got 1 point! Your total is {points}')
            write_json('ispy_leaderboard', leaderboard)

            #Remove Image From Images
            image_locations = read_json('image_urls')

            if self.image_channel_message_ids[1] not in image_locations['used'].keys():
                image_locations['used'][self.image_channel_message_ids[0]] = []

            image_locations['unused'][self.image_channel_message_ids[0]].remove(self.image_channel_message_ids[1])
            image_locations['used'][self.image_channel_message_ids[0]].append(self.image_channel_message_ids[1])

            write_json('image_urls', image_locations)

            #Reset
            self.author = ''
            self.image = ''
            self.image_index = ''
            self.image_channel_message_ids = []
            self.giveup_counter = {}
            write_json('ispy_image', {})

            await asyncio.sleep(10)

            await ctx.invoke(self.client.get_command('picpls'))
            return

        if str(ctx.author) not in self.giveup_counter:
            self.giveup_counter[str(ctx.author)] = 0

        #Wrong
        leaderboard[str(ctx.author)]['Wrong_Guesses'] += 1

        if self.giveup_counter[str(ctx.author)] == 2:
            self.giveup_counter[str(ctx.author)] = 0

            leaderboard[str(ctx.author)]['Points_Lost'] += 1

            points = leaderboard[str(ctx.author)]['Correct_Guesses']-leaderboard[str(ctx.author)]['Points_Lost']
            await ctx.send(f'Oh no! You got three wrong! You lost 1 point! {points+1}->{points}')
        else:
            self.giveup_counter[str(ctx.author)] += 1

            n=3-self.giveup_counter[str(ctx.author)]
            await ctx.send(f'Careful {str(ctx.author.name)}! {n} more wrongs and you lose a point!')

        write_json('ispy_leaderboard', leaderboard)

    @commands.command()
    async def giveup(self, ctx):
        if self.author != '':
            await ctx.send(f'Oh no! The person you were looking for was: {self.author}')

            leaderboard = read_json('ispy_leaderboard')
            leaderboard[str(ctx.author)]['Give_Ups'] += 1
            write_json('ispy_leaderboard', leaderboard)

            self.author = ''
            self.image = ''
            self.image_index = ''
            self.image_channel_message_ids = []
            self.giveup_counter = {}
            write_json('ispy_image', {})

            await asyncio.sleep(10)

            await ctx.invoke(self.client.get_command('picpls'))

    @commands.command()
    async def leaderboard(self, ctx):
        if ctx.channel.id != 744413372987998328:
            return

        leaderboard = read_json('ispy_leaderboard')

        leaderboard_alt = {}

        for person in leaderboard:
            name = person.split('#')[0]

            Guessing_Ratio = round(leaderboard[person]['Correct_Guesses']/(leaderboard[person]['Wrong_Guesses']+leaderboard[person]['Correct_Guesses'])*100)
            Give_Ups = leaderboard[person]['Give_Ups']
            points = leaderboard[person]['Correct_Guesses']-leaderboard[person]['Points_Lost']

            leaderboard_alt[f'{name}: {points} Points | {Guessing_Ratio}% Right | {Give_Ups} Giveups\n'] = points

        leaderboard_alt = {k: v for k, v in sorted(leaderboard_alt.items(), key=lambda item: item[1], reverse=True)}

        leaderboard_str = '```Markdown\nLeaderboard: \n#'


        for key in leaderboard_alt:
            leaderboard_str += key

        leaderboard_str += '```'

        await ctx.send(leaderboard_str)

def setup(client):
    client.add_cog(Ispy(client))
