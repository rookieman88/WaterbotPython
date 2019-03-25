import asyncio
import discord 
import setting
import os
import youtube_dl
from discord.ext import commands
from discord.utils import find
import requests as rq

thetoken = os.getenv("BOT_TOKEN")


#music 

def get_prefix(bot, msg):
    """이 봇의 접두사는 '~' 입니다."""


    prefixes = ['~']

    return commands.when_mentioned_or(*prefixes)(bot, msg)


bot = commands.Bot(command_prefix=get_prefix,description='Waterbot Music')
app = discord.Client()
YOUTUBE_API='AIzaSyD5HkfjExwmv2HFDfS0zwAHdkrNNEmJcsw'

set = setting.set()

client = discord.Client()

@app.event
async def on_ready():
    print("." , app.user.name, " (%s)" % app.user.id)
    bot.loop.create_task(bg())
    print(bot.user.name)
    owner.append(set.owner)


from discord import opus
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll','libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
            try:
                opus.load_opus(opus_lib)
                return
            except OSError:
                pass

    raise RuntimeError('Could not load an opus lib. Tried %s' %(', '.join(opus_libs)))


load_opus_lib()
opts = {
    'default_search': 'auto',
    'quiet': True,
    "no_warnings":True,
    "simulate":True, #do not keep the video files
    "nooverwrites":True,
    "keepvideo":False,
    "noplaylist":True,
    "skip_download":True,
    "prefer_ffmpeg":True
}  # youtube_dl options



servers_songs = {}
player_status = {}
now_playing = {}
song_names = {}
paused = {}
rq_channel = {}


async def set_player_status():
    for i in bot.servers:
        player_status[i.id] = False
        servers_songs[i.id] = None
        paused[i.id] = False
        song_names[i.id] = []
    print(200)


async def bg():
    bot.loop.create_task(set_player_status())



@bot.event
async def on_command_error(con, error):
    pass



async def queue_songs(con, skip, clear):
    if clear == True:
        # servers_songs[con.message.server.id].stop()
        await bot.voice_client_in(con.message.server).disconnect()
        player_status[con.message.server.id] = False
        song_names[con.message.server.id].clear()

    if clear == False:
        if skip == True:
            servers_songs[con.message.server.id].pause()
            # servers_songs[con.message.server.id].stop()

        if len(song_names[con.message.server.id]) == 0:
            servers_songs[con.message.server.id] = None

        if len(song_names[con.message.server.id]) != 0:
            r = rq.Session().get('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={}&key={}'.format(song_names[con.message.server.id][0],YOUTUBE_API)).json()
            pack = discord.Embed(title=r['items'][0]['snippet']['title'],url="https://www.youtube.com/watch?v={}".format(r['items'][0]['id']['videoId']))
            pack.set_thumbnail(url=r['items'][0]['snippet']['thumbnails']['default']['url'])
            pack.add_field(name="신청한 사람:", value=con.message.author.name)
            servers_songs[con.message.server.id] = await bot.voice_client_in(con.message.server).create_ytdl_player(song_names[con.message.server.id][0], ytdl_options=opts, after=lambda: bot.loop.create_task(after_song(con, False, False)))
            servers_songs[con.message.server.id].start()
            if servers_songs[con.message.server.id].duration != 0.0:
                pack.add_field(name='길이 (초)', value=servers_songs[con.message.server.id].duration, inline=True)
            if servers_songs[con.message.server.id].duration == 0.0:
                pack.add_field(name='길이 (초)', value='Live!',inline=True)
            await bot.delete_message(now_playing[con.message.server.id])
            msg = await bot.send_message(con.message.channel, embed=pack)
            now_playing[con.message.server.id] = msg

            if len(song_names[con.message.server.id]) >= 1:
                song_names[con.message.server.id].pop(0)

        if len(song_names[con.message.server.id]) == 0 and servers_songs[con.message.server.id] == None:
            player_status[con.message.server.id] = False


async def after_song(con, skip, clear):
    bot.loop.create_task(queue_songs(con, skip, clear))

    

    
@bot.command(pass_context=True)
async def 플레이(con, *, url):
    """음악을 플레이하는 커맨드 입니다"""
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**뮤직 기능은 DM 에서 사용하실수 없습니다**")

    if con.message.channel.is_private == False:  # DM 무시
        rq_channel[con.message.server.id] = con.message.channel.id
        if bot.is_voice_connected(con.message.server) == False:
            await bot.join_voice_channel(con.message.author.voice.voice_channel)

        if bot.is_voice_connected(con.message.server) == True:
            if player_status[con.message.server.id] == True:
                song_names[con.message.server.id].append(url)
                r = rq.Session().get('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={}&key={}'.format(url,YOUTUBE_API)).json()
                await bot.send_message(con.message.channel, "** `{}` 가 재생목록에 추가되었습니다. **".format(r['items'][0]['snippet']['title']))

            if player_status[con.message.server.id] == False:
                player_status[con.message.server.id] = True
                song_names[con.message.server.id].append(url)
                song = await bot.voice_client_in(con.message.server).create_ytdl_player(song_names[con.message.server.id][0], ytdl_options=opts, after=lambda: bot.loop.create_task(after_song(con, False, False)))
                servers_songs[con.message.server.id] = song
                servers_songs[con.message.server.id].start()
                r = rq.Session().get('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={}&key={}'.format(url,YOUTUBE_API)).json()
                pack = discord.Embed(title=r['items'][0]['snippet']['title'],url="https://www.youtube.com/watch?v={}".format(r['items'][0]['id']['videoId']))
                pack.set_thumbnail(
                    url=r['items'][0]['snippet']['thumbnails']['default']['url'])
                pack.add_field(name="신청한 사람:",value=con.message.author.name)
                if servers_songs[con.message.server.id].duration != 0.0:
                    pack.add_field(name='길이 (초)',value=servers_songs[con.message.server.id].duration,inline=True)
                if servers_songs[con.message.server.id].duration == 0.0:
                    pack.add_field(name='길이 (초)',value='Live!',inline=True)
                msg = await bot.send_message(con.message.channel, embed=pack)
                now_playing[con.message.server.id] = msg
                song_names[con.message.server.id].pop(0)


@bot.command(pass_context=True)
async def 스킵(con):
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**뮤직 기능은 DM 에서 사용하실수 없습니다**")

    # DM 무시
    if con.message.channel.is_private == False:
        if servers_songs[con.message.server.id] == None or len(song_names[con.message.server.id]) == 0 or player_status[con.message.server.id] == False:
            await bot.send_message(con.message.channel, "**스킵할 노래가 없습니다**")
        if servers_songs[con.message.server.id] != None:
            bot.loop.create_task(queue_songs(con, True, False))


@bot.command(pass_context=True)
async def 들어와(con, *, channel=None):
    """음성 채널에 들어가게 해주는 커맨드 입니다."""

    # DM 무시
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**뮤직 기능은 DM 에서 사용하실수 없습니다**")

    if con.message.channel.is_private == False:
        voice_status = bot.is_voice_connected(con.message.server)

        voice = find(lambda m: m.name == channel, con.message.server.channels)

        if voice_status == False and channel == None:  # 못들어갈때
            if con.message.author.voice_channel == None:
                await bot.send_message(con.message.channel, "**권한이 없거나 채널을 찾을수 없습니다**")
            if con.message.author.voice_channel != None:
                await bot.join_voice_channel(con.message.author.voice.voice_channel)

        if voice_status == False and channel != None:  # 채널 선택
            await bot.join_voice_channel(voice)

        if voice_status == True:  # 이미 있을때
            if voice == None:
                await bot.send_message(con.message.channel, "**이미 다른 채널에 들어가있습니다.**")

            if voice != None:
                if voice.type == discord.ChannelType.voice:
                    await bot.voice_client_in(con.message.server).move_to(voice)


@bot.command(pass_context=True)
async def 저리가(con):
    """채널 나가기"""
    # DM 무시
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**뮤직 기능은 DM 에서 사용하실수 없습니다**")

   
    if con.message.channel.is_private == False:

        # 들어간 채널이 없을때
        if bot.is_voice_connected(con.message.server) == False:
            await bot.send_message(con.message.channel, "**들어간 채널이 없음**")

        # 나가기
        if bot.is_voice_connected(con.message.server) == True:
            bot.loop.create_task(queue_songs(con, False, True))
            await bot.send_message(con.message.channel, "쳇..")
            


@bot.command(pass_context=True)
async def 일시정지(con):
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**DM 에서 사용 불가**")

  
    if con.message.channel.is_private == False:
        if servers_songs[con.message.server.id] != None:
            if paused[con.message.server.id] == True:
                await bot.send_message(con.message.channel, "**이미 일시정지 됨**")
            if paused[con.message.server.id] == False:
                servers_songs[con.message.server.id].pause()
                paused[con.message.server.id] = True


@bot.command(pass_context=True)
async def 재생(con):
    # COMMAND IS IN DM
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**DM 에서 사용 불가**")

    # COMMAND NOT IN DM
    if con.message.channel.is_private == False:
        if servers_songs[con.message.server.id] != None:
            if paused[con.message.server.id] == False:
                await bot.send_message(con.message.channel, "**이미 플레이중**")
            if paused[con.message.server.id] == True:
                servers_songs[con.message.server.id].resume()
                paused[con.message.server.id] = False


@bot.command(pass_context=True)
async def 볼륨(con, vol: float):
    if player_status[con.message.server.id] == False:
        await bot.send_message(con.message.channel, "아무 음악도 안틀어져 있음")
    if player_status[con.message.server.id] == True:
        servers_songs[con.message.server.id].volume = vol
        

bot.run(thetoken)