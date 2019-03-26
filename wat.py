"""
WaterBot v.1 (Python Version) code

notice module by 메리
some command by haveadooday
"""

owner = ['417571990820618250']

import asyncio
import discord 
import setting
import os
from discord.ext import commands
from discord.utils import find
import requests as rq
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
import sys
import json
from selenium import webdriver


set = setting.set()


app = discord.Client()
client = discord.Client()

thetoken = os.getenv("BOT_TOKEN")







@app.event
async def on_message(message):
	
     if message.content.startswith('~날씨'):
        try:
            meg = await client.send_message(channel,'로딩중... 1분정도 소요됩니다')
            learn = message.content.split(" ")
            location = learn[1]
            enc_location = urllib.parse.quote(location+'날씨')
            hdr = {'User-Agent': 'Mozilla/5.0'}
            url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
            req = Request(url, headers=hdr)
            html = urllib.request.urlopen(req)
            bs_obj = bs4.BeautifulSoup(html, "html.parser")
            div = bs_obj.find("span",{"class":'todaytemp'})
            div2 = bs_obj.find("p",{"class":"cast_txt"})
            embed = discord.Embed(title=location+'날씨',description=div.text+'℃'+'\n'+div2.text+'\n'+'Powerd by 네이버 날씨',color=0x00ff00)
            await client.send_message(meg,embed=embed)
        except:
await client.send_message(channel,'없는 도시입니다!')


    s = set.first + set.no
    if "~공지" in message.content:
        if message.author.id in owner:
            notice = message.content.replace(s, "")
            embed=discord.Embed(title="공지 시스템", color=0x80ff80)
            embed.add_field(name="공지 발신 준비중!", value="<@" + message.author.id + ">", inline=True)
            embed.set_author(name="by 매리(#4633)", icon_url="https://cdn.discordapp.com/avatars/351613953769603073/b4805197b14b4366c3aaebaf79109fa8.webp")
            embed.set_footer(text="Notice Module by Mary")
            mssg = await app.send_message(message.channel, embed=embed)
            a = []
            b = []
            e = []
            ec = {}
            embed=discord.Embed(title="공지 시스템", color=0x80ff80)
            embed.add_field(name="공지 발신중!", value="<@" + message.author.id + ">", inline=True)
            await app.edit_message(mssg, embed=embed)
            for server in app.servers:
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
                                        await app.send_message(channel, notice)
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
            for server in app.servers:
                if not server.id in a:
                    if set.nfct:
                        try:
                            ch = await app.create_channel(server, set.nfctname)
                            await app.send_message(ch, notice)
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
                bn = app.get_channel(bf).name
                bs = bs + str(bn) + "\n"
            for ef in e:
                en = app.get_channel(ef).name
                es = es + str(app.get_channel(ef).server.name) + "(#" + str(en) + ") : " + ec[ef] + "\n"
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
            await app.edit_message(mssg, embed=embed)
        else:
           await app.send_message(message.channel, "봇 제작자만 사용할수 있는 커맨드입니다!")    



from itertools import cycle
        
status = ['WaterBot v1.0', '주식기능 개발중!' , '꼬우면 oAsIcS#5074로 DMㄱㄱ', 'JS + Python 버전', '~도움 입력 가즈아ㅏㅏ']
async def change_status():
	await app.wait_until_ready()
	msgelel = cycle(status)

	while not app.is_closed:
		current_status = next(msgelel)
		await app.change_presence(game=discord.Game(name=current_status))
		await asyncio.sleep(3)
		
app.loop.create_task(change_status())








			    
app.run(thetoken)
