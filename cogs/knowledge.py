import discord
from discord.ext import commands
from datetime import datetime
import dateutil.parser
from functions import log

class Knowledge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Knowledge is online.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author) != 'RumorMan#7258':
            info = [message.channel, message.author]
            if message.content != '':
                info.append(message.content)
            if len(message.attachments) > 0:
                for attachment in message.attachments:
                    info.append(attachment.url)
            log('MESSAGE', info)

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        log('TYPING', [user, channel])

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log('MESSAGE DELETED', [message.channel, message.author, message.content])

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if str(before.author) != 'RumorMan#7258':
            log('MESSAGE EDITED', [before.author, before.content, after.content])

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        log('REACITON ADD', [user, reaction, reaction.message.content])

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        log('REACTION REMOVE', [user, reaction, reaction.message.content])

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log('GUILD USER JOIN', [member])
        await self.client.get_channel(656594748802596867).send(f'GUILD USER JOIN: {member}')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log('GUILD USER LEAVE', [member])
        await self.client.get_channel(656594748802596867).send(f'GUILD USER LEAVE: {member}')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        '''
        if before.raw_status != after.raw_status:
            if before.status != after.status:
                if after.status:
                    log('MEMBER ONLINE', [before.name])
                else:
                    log('MEMBER OFFLINE', [before.name])

            if before.web_status != after.web_status:
                if after.web_status:
                    log('MEMBER ONLINE (WEB)', [before.name])
                else:
                    log('MEMBER OFFLINE (WEB)', [before.name])
            elif before.desktop_status != after.desktop_status:
                if after.desktop_status:
                    log('MEMBER ONLINE (DESKTOP)', [before.name])
                else:
                    log('MEMBER OFFLINE (DESKTOP)', [before.name])
            elif before.is_on_mobile != after.is_on_mobile:
                if after.is_on_mobile:
                    log('MEMBER ONLINE (MOBILE)', [before.name])
                else:
                    log('MEMBER OFFLINE (MOBILE)', [before.name])'''

        if before.avatar != after.avatar:
            log('MEMBER AVATAR CHANGE', [before.name, before.avatar_url, after.avatar_url])

        if len(before.roles) < len(after.roles): #Add Role
            for role in after.roles:
                if role not in before.roles:
                    log('MEMBER ROLE GIVEN', [before.name, role])
        else: #Remove Role
            for role in before.roles:
                if role not in after.roles:
                    log('MEMBER ROLE TAKEN', [before.name, role])

        if before.display_name != after.display_name:
            log('MEMBER NAME CHANGE', [before.display_name, after.display_name])

        if before.name != after.name:
            log('MEMBER NAME CHANGE', [before.name, after.name])

        if before.nick != after.nick:
            log('MEMBER NICK CHANGE', [before.nick, after.nick])

        if False and before.activity != after.activity:
            if str(before.activity) == 'Spotify':
                if str(after.activity) == 'Spotify':
                    if before.activity.title != after.activity.title:
                        log('SPOTIFY', [after.name, after.activity.artist, after.activity.title])
                        #print(f'{datetime.now()} | SPOTIFY {after.name} ({after.activity.artist}) {after.activity.title}') #({before.activity.artist}) {before.activity.title} ->
                        #print(before.activity._timestamps) #eg {'start': 1605484250682, 'end': 1605484483215} ????
                        #print(before.activity._created_at)
                        #print(f'{datetime.now()} | {after.activity.start} {after.activity.duration} {after.activity.end}')

                        #Does Not Work
                        #print(datetime.utcfromtimestamp(int(before.activity._created_at)))
            else:
                if before.activity != None and after.activity != None:
                    nameChange = False
                    detailsChange = False
                    if "name" in dir(before.activity) and "name" in dir(after.activity):
                        if before.activity.name != after.activity.name:
                            nameChange = True

                    if "details" in dir(before.activity) and "details" in dir(after.activity):
                        if before.activity.details != after.activity.details:
                            detailsChange = True

                    if nameChange and detailsChange:
                        log('MEMBER ACTIVITY', [before.name, '[', before.activity.name, '(', before.activity.details, ')', '->', after.activity.name, '(', after.activity.details, ')', ']'])
                        #print(f'{datetime.now()} | MEMBER ACTIVITY: {before.name} [ {before.activity.name} ({before.activity.details}) -> {after.activity.name} ({after.activity.details}) ]')
                    elif nameChange:
                        log('MEMBER ACTIVITY', [before.name, '[', before.activity.name, '->', after.activity.name, ']'])
                        #print(f'{datetime.now()} | MEMBER ACTIVITY: {before.name} [ {before.activity.name} -> {after.activity.name} ]')

                    #print(f'{datetime.now()} | MEMBER ACTIVITY: {before.name} [ {before.activity.name} ({before.activity.details}) -> {after.activity.name} ({after.activity.details}) ]')
                    #print(f'{datetime.now()} | MEMBER ACTIVITY: {before.name} {before.activity.to_dict} {after.activity.to_dict}')
                    #'created_at', 'emoji', 'name', 'state', 'to_dict', 'type']

            '''
            ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
            '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__',
            '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__',
            '_assets', '_created_at', '_details', '_party', '_session_id', '_state', '_sync_id', '_timestamps', 'album',
            'album_cover_url', 'artist', 'artists', 'color', 'colour', 'created_at', 'duration', 'end', 'name', 'party_id',
            'start', 'title', 'to_dict', 'track_id', 'type']
            '''

            #print(f'{datetime.now()} | MEMBER UPDATE activities: {before.name} {before.activities} {after.activities}')
            #print(f'{datetime.now()} | MEMBER UPDATE activity: {before.name} {before.activity} {after.activity}')
            #print(f'{datetime.now()} | MEMBER UPDATE: {before.avatar} {after.avatar}')
            #print(f'{datetime.now()} | MEMBER UPDATE: {before.desktop_status} {after.desktop_status}')
            #print(f'{datetime.now()} | MEMBER UPDATE: {before.display_name} {after.display_name}')
            #print(f'{datetime.now()} | MEMBER UPDATE: {before.is_on_mobile} {after.is_on_mobile}')
            #print(f'{datetime.now()} | MEMBER UPDATE: {before.name} {after.name}')
            #print(f'{datetime.now()} | MEMBER UPDATE: {before.nick} {after.nick}')
            #print(f'{datetime.now()} | MEMBER UPDATE: {before.raw_status} {after.raw_status}')
            #print(f'{datetime.now()} | MEMBER UPDATE: {before.roles} {after.roles}')
            #print(f'{datetime.now()} | MEMBER UPDATE: {before.status} {after.status}')
            #print(f'{datetime.now()} | MEMBER UPDATE: {before.top_role} {after.top_role}')
            #print(f'{datetime.now()} | MEMBER UPDATE: {before.web_status} {after.web_status}')

            '''
            'activities', 'activity', 'add_roles', 'avatar', 'avatar_url', 'avatar_url_as', 'ban', 'block', 'bot', 'color', 'colour',
            'create_dm', 'created_at', 'default_avatar', 'default_avatar_url', 'desktop_status', 'discriminator', 'display_name',
            'dm_channel', 'edit', 'fetch_message', 'guild', 'guild_permissions', 'history', 'id', 'is_avatar_animated', 'is_blocked',
            'is_friend', 'is_on_mobile', 'joined_at', 'kick', 'mention', 'mentioned_in', 'mobile_status', 'move_to', 'mutual_friends',
            'name', 'nick', 'permissions_in', 'pins', 'premium_since', 'profile', 'public_flags', 'raw_status', 'relationship',
            'remove_friend', 'remove_roles', 'roles', 'send', 'send_friend_request', 'status', 'system', 'top_role', 'trigger_typing',
            'typing', 'unban', 'unblock', 'voice', 'web_status']
            '''

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        log('USER UPDATE', [before, after, dir(before)])
        #print(f'{datetime.now()} | USER UPDATE: {before} {after} {dir(before)}')

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        log('GUILD UPDATE', [before, after])
        #print(f'{datetime.now()} | GUILD UPDATE: {before} {after}')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == None and after.channel != None:
            log('VOICE (Connect)', [member, after.channel.name])
            #print(f'{datetime.now()} | VOICE (Connect): {member} {after.channel.name}')
        if before.channel != None and after.channel == None:
            log('VOICE (Disconnect)', [member, before.channel.name])
            #print(f'{datetime.now()} | VOICE (Disconnect): {member} {before.channel.name}')
        if before.channel != None and after.channel != None:
            if before.channel.id != after.channel.id: #change channel
                log('VOICE (Switch)', [member, before.channel.name, '->', after.channel.name])
                #print(f'{datetime.now()} | VOICE (Switch): {member} {before.channel.name} -> {after.channel.name}')
            if before.self_stream != after.self_stream:
                if after.self_stream:
                    log('VOICE (Stream Start)', [member, dir(member)])
                    #print(f'{datetime.now()} | VOICE (Stream Start): {member}')
                else:
                    log('VOICE (Stream Stop)', [member])
                    #print(f'{datetime.now()} | VOICE (Stream Stop): {member}')

            if before.self_deaf != after.self_deaf:
                if after.self_deaf:
                    log('VOICE (Deafen)', [member])
                else:
                    log('VOICE (Un-Deafen)', [member])
            elif before.self_mute != after.self_mute:
                if after.self_mute:
                    log('VOICE (Mute)', [member])
                else:
                    log('VOICE (Un-Mute)', [member])

            if before.self_video != after.self_video:
                if after.self_video:
                    log('VOICE (Video Start)', [member])
                else:
                    log('VOICE (Video Stop)', [member])

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        pass

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        log('INVITE CREATED', [invite, invite.inviter, invite.channel])


def setup(client):
    client.add_cog(Knowledge(client))
