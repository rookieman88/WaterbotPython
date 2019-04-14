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

        client_id = ""
        client_secret = ""

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


    if message.content.startswith('~플레이'):
        Text = ""
        learn = message.content.split(" ")
        vrsize = len(learn)  # 배열크기
        vrsize = int(vrsize)
        for i in range(1, vrsize):  # 띄어쓰기 한 텍스트들 인식함
            Text = Text + " " + learn[i]
        encText = Text

        chromedriver_dir = r'C:\selum\chromedriver_win32\chromedriver.exe' #크롬드라이버 경로
        driver = webdriver.Chrome(chromedriver_dir)
        driver.get('https://www.youtube.com/results?search_query='+encText) #유튜브 검색링크
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'}) # a태그에서 video title 이라는 id를 찾음

        embed = discord.Embed(
            title="영상들!",
            description="검색한 영상 결과",
            colour=discord.Color.blue())

        for i in range(0, 5):
            entireNum = entire[i]
            entireText = entireNum.text.strip()  # 영상제목
            print(entireText)
            test1 = entireNum.get('href')  # 하이퍼링크
            print(test1)
            rink = 'https://www.youtube.com'+test1
           # embed.add_field(name=str(i+1)+'번째 영상',value=entireText + '\n링크 : '+rink)
            embed.add_field(name=str(i + 1) + '번째 영상', value='\n' + '[%s](<%s>)' % (entireText, rink),
                            inline=False)  # [텍스트](<링크>) 형식으로 적으면 텍스트 하이퍼링크 만들어집니다
            searchYoutubeHref[i] = rink
        await client.send_message(message.channel,embed=embed)

    if message.content.startswith('1'):

        if not searchYoutubeHref: #저장된 하이퍼링크가 없다면
            print('searchYoutubeHref 안에 값이 존재하지 않습니다.')
            await client.send_message(message.channel, embed=discord.Embed(description="검색한 영상이 없습니다."))
        else:
            print(searchYoutubeHref[0])
            server = message.server
            voice_client = client.voice_client_in(server)
            url = searchYoutubeHref[0]
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
            print(player.is_playing())
            players[server.id] = player
            await client.send_message(message.channel, embed=discord.Embed(description="재생한다!!!!"))
            print(player.is_playing())
            player.start()

            for i in range(0,5):
                del searchYoutubeHref[i]

    if message.content.startswith('2'):

        if not searchYoutubeHref:
            print('searchYoutubeHref 안에 값이 존재하지 않습니다.')
            await client.send_message(message.channel, embed=discord.Embed(description="검색한 영상이 없습니다."))
        else:
            print(searchYoutubeHref[1])
            server = message.server
            voice_client = client.voice_client_in(server)
            url = searchYoutubeHref[1]
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
            print(player.is_playing())
            players[server.id] = player
            await client.send_message(message.channel, embed=discord.Embed(description="재생한다!!!!"))
            print(player.is_playing())
            player.start()

            for i in range(0,5):
                del searchYoutubeHref[i]

    if message.content.startswith('3'):

        if not searchYoutubeHref:
            print('searchYoutubeHref 안에 값이 존재하지 않습니다.')
            await client.send_message(message.channel, embed=discord.Embed(description="검색한 영상이 없습니다."))
        else:
            print(searchYoutubeHref[2])
            server = message.server
            voice_client = client.voice_client_in(server)
            url = searchYoutubeHref[2]
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
            print(player.is_playing())
            players[server.id] = player
            await client.send_message(message.channel, embed=discord.Embed(description="재생한다!!!!"))
            print(player.is_playing())
            player.start()

            for i in range(0,5):
                del searchYoutubeHref[i]

    if message.content.startswith('4'):

        if not searchYoutubeHref:
            print('searchYoutubeHref 안에 값이 존재하지 않습니다.')
            await client.send_message(message.channel, embed=discord.Embed(description="검색한 영상이 없습니다."))
        else:
            print(searchYoutubeHref[3])
            server = message.server
            voice_client = client.voice_client_in(server)
            url = searchYoutubeHref[3]
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
            print(player.is_playing())
            players[server.id] = player
            await client.send_message(message.channel, embed=discord.Embed(description="재생한다!!!!"))
            print(player.is_playing())
            player.start()

            for i in range(0,5):
                del searchYoutubeHref[i]

    if message.content.startswith('5'):

        if not searchYoutubeHref:
            print('searchYoutubeHref 안에 값이 존재하지 않습니다.')
            await client.send_message(message.channel, embed=discord.Embed(description="검색한 영상이 없습니다."))
        else:
            print(searchYoutubeHref[4])
            server = message.server
            voice_client = client.voice_client_in(server)
            url = searchYoutubeHref[4]
            player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
            print(player.is_playing())
            players[server.id] = player
            await client.send_message(message.channel, embed=discord.Embed(description="재생한다!!!!"))
            print(player.is_playing())
            player.start()

            for i in range(0,5):
                del searchYoutubeHref[i]



    if message.content.startswith('!타이머'):

        Text = ""
        learn = message.content.split(" ")
        vrsize = len(learn)  # 배열크기
        vrsize = int(vrsize)
        for i in range(1, vrsize):  # 띄어쓰기 한 텍스트들 인식함
            Text = Text + " " + learn[i]

        secint = int(Text)
        sec = secint

        for i in range(sec, 0, -1):
            print(i)
            await client.send_message(message.channel, embed=discord.Embed(description='타이머 작동중 : '+str(i)+'초'))
            time.sleep(1)

        else:
            print("땡")
            await client.send_message(message.channel, embed=discord.Embed(description='타이머 종료'))





thetokeen = os.getenv('BOT_TOKEN')

client.run(thetokeen)
