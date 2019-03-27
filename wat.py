
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

     if message.content.startswith('~날씨'):
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
            

     if message.content.startswith('~번역'):
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
   
        s = set.first + set.no
        if "~공지" in message.content:
            if message.author.id in owner:
                notice = message.content.replace(s, "")
                embed=discord.Embed(title="공지 시스템", color=0x80ff80)
                embed.add_field(name="공지 발신 준비중!", value="<@" + message.author.id + ">", inline=True)
                mssg = await client.send_message(message.channel, embed=embed)
                a = []
                b = []
                e = []
                ec = {}
                embed=discord.Embed(title="공지 시스템", color=0x80ff80)
                embed.add_field(name="공지 발신중!", value="<@" + message.author.id + ">", inline=True)
                await client.edit_message(mssg, embed=embed)
                for server in client.servers:
                    for channel in server.channels:
                        for tag in set.allowprefix:
                            if tag in channel.name:
                                dtat = True
                                for distag in set.disallowprefix:
                                    if distag in channel.name:
                                        dtat = False
                                if dtat:
                                    if not server.id in a:
                                        try:
                                            await client.send_message(channel, notice)
                                        except discord.HTTPException:
                                            e.append(str(channel.id))
                                            ec[channel.id] = "HTTPException"
                                        except discord.Forbidden:
                                            e.append(str(channel.id))
                                            ec[channel.id] = "Forbidden"
                                        except discord.NotFound:
                                            e.append(str(channel.id))
                                            ec[channel.id] = "NotFound"
                                        except discord.InvalidArgument:
                                            e.append(str(channel.id))
                                            ec[channel.id] = "InvalidArgument"
                                        else:
                                            a.append(str(server.id))
                                            b.append(str(channel.id))
                asdf = "```\n"
                for server in client.servers:
                    if not server.id in a:
                        if set.nfct:
                            try:
                                ch = await client.create_channel(server, set.nfctname)
                                await client.send_message(ch, notice)
                            except:
                                asdf = asdf + str(server.name) + "[채널 생성 실패]\n"
                            else:
                                asdf = asdf + str(server.name) + "[채널 생성 및 재발송 성공]\n"
                        else:
                            asdf = asdf + str(server.name) + "\n"
                asdf = asdf + "```"
                embed=discord.Embed(title="공지 시스템", color=0x80ff80)
                embed.add_field(name="공지 발신완료!", value="<@" + message.author.id + ">", inline=True)
                bs = "```\n"
                es = "```\n"
                for bf in b:
                    bn = client.get_channel(bf).name
                    bs = bs + str(bn) + "\n"
                for ef in e:
                    en = client.get_channel(ef).name
                    es = es + str(client.get_channel(ef).server.name) + "(#" + str(en) + ") : " + ec[ef] + "\n"
                bs = bs + "```"
                es = es + "```"
                if bs == "``````":
                    bs = "``` ```"
                if es == "``````":
                    es = "``` ```"
                if asdf == "``````":
                    asdf = "``` ```"
                sucess = bs
                missing = es
                notfound = asdf
                embed.add_field(name="공지 발신 성공 채널:", value=sucess, inline=True)
                embed.add_field(name="공지 발신 실패 채널:", value=missing, inline=True)
                embed.add_field(name="공지 채널 없는 서버:", value=notfound, inline=True)
                await client.edit_message(mssg, embed=embed)
            else:
               await client.send_message(message.channel, "봇 제작자만 사용할수 있는 커맨드입니다!")    



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


access_token = os.getenv('BOT_TOKEN')
client.run(access_token)
