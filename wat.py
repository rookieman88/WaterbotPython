
#WaterBot v.1 (Python Version) code

#notice module by 메리
#some command by haveadooday


"""
Github GNU General Public License version 3.0 (GPLv3)
Copyright 헤브어 2019, All Right Reserved.
"""



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
from selenium import webdriver

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

     if message.content.startswith('~날씨'):
        try:
            meg = await client.send_message(channel,'로딩중...')
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
            embed = discord.Embed(title=location+'날씨',description=div.text+'℃'+'\n'+div2.text+'\n'+'네이버 날씨',color=0x00ff00)
            await client.send_message(meg,embed=embed)
        except:
           await client.send_message(channel,'없는 도시입니다!')
            
     if message.content.startswith('~미세먼지'):
        try:
           meg = await client.send_message(channel,'로딩중..')
           learn = message.content.split(" ")
           location = learn[1]
           enc_location = urllib.parse.quote(location+'미세먼지')
           hdr = {'User-Agent': 'Mozilla/5.0'}
           url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
           req = Request(url, headers=hdr)
           html = urllib.request.urlopen(req)
           bs_obj = bs4.BeautifulSoup(html, "html.parser")
           div = bs_obj.find("em",{"class":'main_figure'})
           div2 = bs_obj.find("span",{'class':'update'})
           learn2 = int(div.text)
           if learn2 < 16:
               a = '최고'
           elif learn2 < 31:
               a = '좋음'
           elif learn2 < 41:
               a = '양호'
           elif learn2 < 51:
               a = '보통'
           elif learn2 < 76:
               a = '나쁨'
           elif learn2 < 101:
               a = '상당히 나쁨'
           elif learn2 < 151:
               a = '매우나쁨'
           elif learn2 > 150:
               a = '최악'
           embed = discord.Embed(title=learn[1]+'미세먼지',description='**'+str(learn2)+'㎍/㎥ \n'+a+'**\n'+div2.text+'\n'+'네이버 미세먼지/미세먼지 기준 미세미세8단계',color=0x00ff00)
           await client.send_message(meg,embed=embed)
        except:
            await client.send_message(channel,'없는 도시 거나 도/시는 미세먼지 검색이 안됩니다.')

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


access_token = os.getenv('BOT_TOKEN')
client.run(access_token)
