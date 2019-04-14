import discord
import asyncio
import random
import openpyxl
from discord import Member
from discord.ext import commands
import youtube_dl
from urllib.request import urlopen, Request
import urllib
import urllib.request
import bs4
import os
import sys
import json
from selenium import webdriver
import time
import datetime
import requests

countG = 0
client = discord.Client()
players = {}
queues= {}
musiclist=[]
mCount=1
searchYoutube={}
searchYoutubeHref={}

def check_queue(id):
    if queues[id]!=[]:
        player = queues[id].pop(0)
        players[id] = player
        del musiclist[0]
        player.start()

@client.event
async def on_ready():
    print("login")
    print(client.user.name)
    print(client.user.id)
    print("------------------")
    



@client.event
async def on_message(message):

    if message.content.startswith("~날씨"):
        learn = message.content.split(" ")
        location = learn[1]
        enc_location = urllib.parse.quote(location+'날씨')
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
        print(url)
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        todayBase = bsObj.find('div', {'class': 'main_info'})

        todayTemp1 = todayBase.find('span', {'class': 'todaytemp'})
        todayTemp = todayTemp1.text.strip()  # 온도
        print(todayTemp)

        todayValueBase = todayBase.find('ul', {'class': 'info_list'})
        todayValue2 = todayValueBase.find('p', {'class': 'cast_txt'})
        todayValue = todayValue2.text.strip()  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
        print(todayValue)

        todayFeelingTemp1 = todayValueBase.find('span', {'class': 'sensible'})
        todayFeelingTemp = todayFeelingTemp1.text.strip()  # 체감온도
        print(todayFeelingTemp)

        todayMiseaMongi1 = bsObj.find('div', {'class': 'sub_info'})
        todayMiseaMongi2 = todayMiseaMongi1.find('div', {'class': 'detail_box'})
        todayMiseaMongi3 = todayMiseaMongi2.find('dd')
        todayMiseaMongi = todayMiseaMongi3.text  # 미세먼지
        print(todayMiseaMongi)

        tomorrowBase = bsObj.find('div', {'class': 'table_info weekly _weeklyWeather'})
        tomorrowTemp1 = tomorrowBase.find('li', {'class': 'date_info'})
        tomorrowTemp2 = tomorrowTemp1.find('dl')
        tomorrowTemp3 = tomorrowTemp2.find('dd')
        tomorrowTemp = tomorrowTemp3.text.strip()  # 오늘 오전,오후온도
        print(tomorrowTemp)

        tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
        tomorrowMoring1 = tomorrowAreaBase.find('div', {'class': 'main_info morning_box'})
        tomorrowMoring2 = tomorrowMoring1.find('span', {'class': 'todaytemp'})
        tomorrowMoring = tomorrowMoring2.text.strip()  # 내일 오전 온도
        print(tomorrowMoring)

        tomorrowValue1 = tomorrowMoring1.find('div', {'class': 'info_data'})
        tomorrowValue = tomorrowValue1.text.strip()  # 내일 오전 날씨상태, 미세먼지 상태
        print(tomorrowValue)

        tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
        tomorrowAllFind = tomorrowAreaBase.find_all('div', {'class': 'main_info morning_box'})
        tomorrowAfter1 = tomorrowAllFind[1]
        tomorrowAfter2 = tomorrowAfter1.find('p', {'class': 'info_temperature'})
        tomorrowAfter3 = tomorrowAfter2.find('span', {'class': 'todaytemp'})
        tomorrowAfterTemp = tomorrowAfter3.text.strip()  # 내일 오후 온도
        print(tomorrowAfterTemp)

        tomorrowAfterValue1 = tomorrowAfter1.find('div', {'class': 'info_data'})
        tomorrowAfterValue = tomorrowAfterValue1.text.strip()

        print(tomorrowAfterValue)  # 내일 오후 날씨상태,미세먼지

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

    if message.content.startswith('~영어로'):
        learn = message.content.split(" ")
        Text = ""

        client_id = "cMk952QL7RsmQsctxHYP"
        client_secret = "fvfG3a6Q_c"

        url = "https://openapi.naver.com/v1/papago/n2mt"
        print(len(learn))
        vrsize = len(learn)  # 배열크기
        vrsize = int(vrsize)
        for i in range(1, vrsize): #띄어쓰기 한 텍스트들 인식함
            Text = Text+" "+learn[i]
        encText = urllib.parse.quote(Text)
        data = "source=ko&target=en&text=" + encText

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)

        response = urllib.request.urlopen(request, data=data.encode("utf-8"))

        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            data = response_body.decode('utf-8')
            data = json.loads(data)
            tranText = data['message']['result']['translatedText']
        else:
            print("Error Code:" + rescode)

        print('번역된 내용 :', tranText)

        embed = discord.Embed(
            title='번역기 (영어)',
            description=tranText,
            colour=discord.Colour.green()
        )
        await client.send_message(message.channel,embed=embed)


    if message.content.startswith('~한국어로'):
        learn = message.content.split(" ")
        Text = ""

        client_id = "cMk952QL7RsmQsctxHYP"
        client_secret = "fvfG3a6Q_c"

        url = "https://openapi.naver.com/v1/papago/n2mt"
        print(len(learn))
        vrsize = len(learn)  # 배열크기
        vrsize = int(vrsize)
        for i in range(1, vrsize): #띄어쓰기 한 텍스트들 인식함
            Text = Text+" "+learn[i]
        encText = urllib.parse.quote(Text)
        data = "source=en&target=ko&text=" + encText

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)

        response = urllib.request.urlopen(request, data=data.encode("utf-8"))

        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            data = response_body.decode('utf-8')
            data = json.loads(data)
            tranText = data['message']['result']['translatedText']
        else:
            print("Error Code:" + rescode)

        print('번역된 내용 :', tranText)

        embed = discord.Embed(
            title='번역기 (한국어)',
            description=tranText,
            colour=discord.Colour.green()
        )
        await client.send_message(message.channel,embed=embed)





    if message.content.startswith('~타이머'):

        Text = ""
        learn = message.content.split(" ")
        vrsize = len(learn)  # 배열크기
        vrsize = int(vrsize)
        for i in range(1, vrsize):  # 띄어쓰기 한 텍스트들 인식함
            Text = Text + " " + learn[i]

        secint = int(Text)
        sec = secint
        timer = await client.send_message(message.channel, embed=discord.Embed(description='타이머 작동중 : 타이머 시작'))

        for i in range(sec, 0, -1):
            await client.edit_message(timer, embed=discord.Embed(description='타이머 작동중 : '+str(i)+'초'))
            time.sleep(1)

        else:
            print("땡")
            await client.edit_message(timer, embed=discord.Embed(description='타이머 종료'))

    if "워터봇 공지" in message.content:
       if message.author.id == '417571990820618250':
           notice = message.content.replace("워터봇 공지", "")
           embed=discord.Embed(title="워터봇 전체공지 시스템")
           embed.add_field(name="공지 발신을 준비하고 있습니다!", value="요청자 : <@" + message.author.id + ">", inline=True)
           mssg = await client.send_message(message.channel, embed=embed)
           a = []
           b = []
           e = []
           ec = {}
           embed=discord.Embed(title="워터봇 전체공지 시스템")
           embed.add_field(name="공지 발신중 입니다!", value="요청자 : <@" + message.author.id + ">", inline=True)
           await client.edit_message(mssg, embed=embed)
           for server in client.servers:
               for channel in server.channels:
                   for tag in ["워터봇-공지","notice", "공지", "알림", "Alarm"]:
                       if tag in channel.name:
                           dtat = True
                           for distag in ["밴", "경고", "제재", "길드", "ban", "worry", "warn", "guild"]:
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
                   try:
                       ch = await client.create_channel(server, "워터봇-공지")
                       await client.send_message(ch, notice)
                   except:
                       asdf = asdf + str(server.name) + "[채널 생성에 실패하였습니다. (서버 관리자와 연락 요망)]\n"
                   else:
                       asdf = asdf + str(server.name) + "[채널 생성 및 재발송에 성공하였습니다.]\n"
           asdf = asdf + "```"
           embed=discord.Embed(title="워터봇 전체공지 시스템")
           embed.add_field(name="공지 발신이 완료되었습니다!", value="요청자 : <@" + message.author.id + ">", inline=True)
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
           embed.add_field(name="공지 발신에 성공한 채널은 다음과 같습니다 :", value=sucess, inline=False)
           embed.add_field(name="공지 발신에 실패한 채널은 다음과 같습니다 :", value=missing, inline=False)
           embed.add_field(name="키워드가 발견되지 않은 서버는 다음과 같습니다 :", value=notfound, inline=False)
           await client.edit_message(mssg, embed=embed)
                    # DPNK 사용 구문 종점
           log_actvity("I send Notice for all Server. (content : %s\nSuccess : %s\nFail : %s\nNotfound : %s)." % (message.content, sucess, missing, notfound))
       else:
           await client.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다.")




thetokeen = os.getenv('BOT_TOKEN')

client.run(thetokeen)
