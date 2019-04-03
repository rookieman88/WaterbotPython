
#WaterBot v.1 (Python Version) code

#notice module by 메리
#some command by haveadooday


"""
Github GNU General Public License version 3.0 (GPLv3)
Copyright 헤브어 2019, All Right Reserved.
"""


owner = ['417571990820618250']

import discord
import asyncio
import random
import time
from urllib.request import urlopen, Request
import urllib
import bs4
from urllib.request import Request
import openpyxl
import re
import requests
from bs4 import BeautifulSoup
import datetime
import os
import sys
import json
import setting
from selenium import webdriver

set = setting.set()
client = discord.Client()
times = int(time.time())
afk = []
warn = {}
party = 'off'
@client.event
async def on_ready():
     print('온라인(관리)')
     print(client.user.name)
     print('======')
     
@client.event
async def on_message(message):

     if '~날씨' in message.content:
        try:
            meg = await client.send_message(message.channel,'로딩중...')
            learn = message.content.split(" ")
            location = learn[1]
            enc_location = urllib.parse.quote(location+'날씨')
            hdr = {'User-Agent': 'Mozilla/5.0'}
            url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
            req = Request(url, headers=hdr)
            html = urllib.request.urlopen(req)
            bsObj = bs4.BeautifulSoup(html, "html.parser")
            todayBase = bsObj.find('div', {'class': 'main_info'})

            todayTemp1 = todayBase.find('span', {'class': 'todaytemp'})
            todayTemp = todayTemp1.text.strip()  # 온
            todayValueBase = todayBase.find('ul', {'class': 'info_list'})
            todayValue2 = todayValueBase.find('p', {'class': 'cast_txt'})
            todayValue = todayValue2.text.strip()  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌

            todayFeelingTemp1 = todayValueBase.find('span', {'class': 'sensible'})
            todayFeelingTemp = todayFeelingTemp1.text.strip()  # 체감온도

            todayMiseaMongi1 = bsObj.find('div', {'class': 'sub_info'})
            todayMiseaMongi2 = todayMiseaMongi1.find('div', {'class': 'detail_box'})
            todayMiseaMongi3 = todayMiseaMongi2.find('dd')
            todayMiseaMongi = todayMiseaMongi3.text  # 미세먼지

            tomorrowBase = bsObj.find('div', {'class': 'table_info weekly _weeklyWeather'})
            tomorrowTemp1 = tomorrowBase.find('li', {'class': 'date_info'})
            tomorrowTemp2 = tomorrowTemp1.find('dl')
            tomorrowTemp3 = tomorrowTemp2.find('dd')
            tomorrowTemp = tomorrowTemp3.text.strip()  # 오늘 오전,오후온도
          
            embed = discord.Embed(
            title=learn[1]+ ' 날씨 정보',
            description=learn[1]+ '날씨 정보입니다.',
            colour=discord.Colour.gold()
        )
            embed.add_field(name='현재온도', value=todayTemp+'˚', inline=False)  # 현재온도
            embed.add_field(name='체감온도', value=todayFeelingTemp, inline=False)  # 체감온도
            embed.add_field(name='현재상태', value=todayValue, inline=False)  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
            embed.add_field(name='현재 미세먼지 상태', value=todayMiseaMongi, inline=False)  # 오늘 미세먼지
            embed.add_field(name='오늘 오전/오후 날씨', value=tomorrowTemp, inline=False)  # 오늘날씨 # color=discord.Color.blue()

            await client.send_message(message.channel,embed=embed)
        except:
           await client.send_message(message.channel,'없는 도시입니다!')
            

     if '~번역' in message.content:
        learn = message.content.split(" ")
        client_id = "cMk952QL7RsmQsctxHYP"
        client_secret = "fvfG3a6Q_c"
        encText = learn[1]
        url = "https://openapi.naver.com/v1/papago/n2mt"

        headers = {"X-Naver-Client-Id" :client_id,
                "X-Naver-Client-Secret":client_secret}

        params = (("source", "ko"),
                ("target", "en"),
                ("text", encText))

        response = requests.post(url, data=params, headers=headers)
        if response.status_code == 200:
            response_body = response.json()
            embed = discord.Embed(
                title='한글->영어 번역결과',
                description=response_body[u'message'][u'result'][u'translatedText'],
                colour=discord.Colour.green()
            )
            await client.send_message(message.channel,embed=embed)





from itertools import cycle
        
status = ['WaterBot v1.0', '주식기능 개발중!' , '꼬우면 oAsIcS#5074로 DMㄱㄱ', 'JS + Python 버전', '~도움 입력 가즈아ㅏㅏ']
async def change_status():
	await client.wait_until_ready()
	msgelel = cycle(status)

	while not client.is_closed:
		current_status = next(msgelel)
		await client.change_presence(game=discord.Game(name=current_status))
		await asyncio.sleep(3)
		
client.loop.create_task(change_status())



import youtube_dl
from discord.ext import commands
from discord.utils import find
import requests as rq

def get_prefix(bot, msg):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""


    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['~']

    return commands.when_mentioned_or(*prefixes)(bot, msg)


bot = commands.Bot(command_prefix=get_prefix,description='A music bot fro discord Kurusaki')
YOUTUBE_API='AIzaSyD5HkfjExwmv2HFDfS0zwAHdkrNNEmJcsw'
bot.remove_command('help')

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
async def on_ready():
    bot.loop.create_task(bg())
    print(bot.user.name)


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
    """알 수 없는 오류가 발생했습니다... oAsIcS#5574 로 알려주세요"""
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**서버에서만 가능하다고! DM 은 안되..**")

    if con.message.channel.is_private == False:  # command is used in a server
        rq_channel[con.message.server.id] = con.message.channel.id
        if bot.is_voice_connected(con.message.server) == False:
            await bot.join_voice_channel(con.message.author.voice.voice_channel)

        if bot.is_voice_connected(con.message.server) == True:
            if player_status[con.message.server.id] == True:
                song_names[con.message.server.id].append(url)
                r = rq.Session().get('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={}&key={}'.format(url,YOUTUBE_API)).json()
                await bot.send_message(con.message.channel, "** `{}` 가 재생목록에 추가되었습니다!**".format(r['items'][0]['snippet']['title']))

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
                    pack.add_field(name='',value='Live!',inline=True)
                msg = await bot.send_message(con.message.channel, embed=pack)
                now_playing[con.message.server.id] = msg
                song_names[con.message.server.id].pop(0)


@bot.command(pass_context=True)
async def 스킵(con):
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**서버에서만 가능하다고! DM 은 안되...**")

    # COMMAND NOT IN DM
    if con.message.channel.is_private == False:
        if servers_songs[con.message.server.id] == None or len(song_names[con.message.server.id]) == 0 or player_status[con.message.server.id] == False:
            await bot.send_message(con.message.channel, "**스킵할 노래가 없는데요**")
        if servers_songs[con.message.server.id] != None:
            bot.loop.create_task(queue_songs(con, True, False))


@bot.command(pass_context=True)
async def 들어와(con, *, channel=None):
    """알수 없는 오류가 발생했습니다.. oAsIcS#5574 로 오류를 알려주세요"""

    # COMMAND IS IN DM
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**서버에서만 가능하다고! DM 은 안되..**")

    # COMMAND NOT IN DM
    if con.message.channel.is_private == False:
        voice_status = bot.is_voice_connected(con.message.server)

        voice = find(lambda m: m.name == channel, con.message.server.channels)

        if voice_status == False and channel == None:  # VOICE NOT CONNECTED
            if con.message.author.voice_channel == None:
                await bot.send_message(con.message.channel, "**거기에 들어갈수 있는 권한이 없어!**")
            if con.message.author.voice_channel != None:
                await bot.join_voice_channel(con.message.author.voice.voice_channel)

        if voice_status == False and channel != None:  # PICKING A VOICE CHANNEL
            await bot.join_voice_channel(voice)
            await bot.send_message(con.message.channel, "들어감!")

        if voice_status == True:  # VOICE ALREADY CONNECTED
            if voice == None:
                await bot.send_message(con.message.channel, "**이미 다른 채널에 있어..**")

            if voice != None:
                if voice.type == discord.ChannelType.voice:
                    await bot.voice_client_in(con.message.server).move_to(voice)

                    

@bot.command(pass_context=True)
async def 저리가(con):
    """모든 유저가 음성 채널을 떠났어 ㅠㅠ 음악 끌게.."""
    # COMMAND USED IN DM
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**서버에서만 가능하다고! DM 은 안되..**")

    # COMMAND NOT IN DM
    if con.message.channel.is_private == False:

        # IF VOICE IS NOT CONNECTED
        if bot.is_voice_connected(con.message.server) == False:
            await bot.send_message(con.message.channel, "음악 채널에 연결이 안되있어 ~들어와 로 초대해줘")

        # VOICE ALREADY CONNECTED
        if bot.is_voice_connected(con.message.server) == True:
            bot.loop.create_task(queue_songs(con, False, True))
            await bot.send_message(con.message.channel, "ㅠㅠ 나감..")


@bot.command(pass_context=True)
async def 일시정지(con):
    # COMMAND IS IN DM
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**서버에서만 가능하다고! DM 은 안되..**")

    # COMMAND NOT IN DM
    if con.message.channel.is_private == False:
        if servers_songs[con.message.server.id] != None:
            if paused[con.message.server.id] == True:
                await bot.send_message(con.message.channel, "**쀍 음악 일시중지;;**")
            if paused[con.message.server.id] == False:
                servers_songs[con.message.server.id].pause()
                paused[con.message.server.id] = True


@bot.command(pass_context=True)
async def 재생(con):
    # COMMAND IS IN DM
    if con.message.channel.is_private == True:
        await bot.send_message(con.message.channel, "**음악 채널에 먼저 들어가시죠...**")

    # COMMAND NOT IN DM
    if con.message.channel.is_private == False:
        if servers_songs[con.message.server.id] != None:
            if paused[con.message.server.id] == False:
                await bot.send_message(con.message.channel, "**음악이 이미 틀어져 있다고!**")
            if paused[con.message.server.id] == True:
                servers_songs[con.message.server.id].resume()
                paused[con.message.server.id] = False


@bot.command(pass_context=True)
async def 볼륨(con, vol: float):
    if player_status[con.message.server.id] == False:
        await bot.send_message(con.message.channel, "아무 음악도 안틀어져있잖아..")
    if player_status[con.message.server.id] == True:
servers_songs[con.message.server.id].volume = vol

access_token = os.getenv('BOT_TOKEN')
client.run(access_token)
