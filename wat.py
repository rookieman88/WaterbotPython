
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
        learn = message.content.replace('~번역', "")
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
                title='한글 -> 영어 번역결과',
                description=response_body[u'message'][u'result'][u'translatedText'],
                colour=discord.Colour.green()
            )
            await client.send_message(message.channel,embed=embed)
     if message.content.startswith('~문의'):
         learn = message.content.replace('~문의', "")
         embed = discord.Embed(title='문의전송안내',description='문의내용:'+learn+'\n 혹시 잘못전송되었으면 "취소합니다."라고 다시 문의를 보내주세요.',color=0x00ff00)
         await client.send_message(channel,embed=embed)
         embed = discord.Embed(title='문의 수신',description='문의전송안내'+'아이디:'+id+'이름:'+message.author.name+'\n 내용:'+learn,color=0x00ff00)
	 channel1 = discord.utils.get(client.get_all_members(),id='417571990820618250')
         await client.send_message(channel1,embed=embed)
	
     if message.content.startswith('~답변'):
        learn = message.content.replace('~답변', "")
        embed = discord.Embed(title='문의답변',description='답변이 왔습니다. \n 내용:'+learn[2],color=0x00ff00)
        member = discord.utils.get(client.get_all_members(),id=learn[1])
        await client.send_message(member,embed=embed)
        await client.send_message(channel,':white_check_mark:')

     if message.content.startswith('~궁합'):
          try:
             learn = message.content.split(' ')
             learn.remove('~궁합')
             a = str(random.randint(1,100))
             a = learn[0]+'님과'+learn[1]+'님의 궁합은'+a+ '%입니다!'
             embed = discord.Embed(title="재미로 보는 궁합!",description=a,color=0x00ff00)
             await client.send_message(channel,embed=embed)
          except:
               await client.send_message(channel,'~궁합 <멘션> <멘션> 이렇게 해주세요!')





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
