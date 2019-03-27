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

thetoken = os.getenv("BOT_TOKEN")




@app.event
async def on_message(message):
	
     if message.content.startswith('~날씨'):
        try:
            meg = await app.send_message(channel,'로딩중... 1분정도 소요됩니다')
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
            await app.send_message(meg,embed=embed)
        except:
          await app.send_message(channel,'없는 도시입니다!')





			    
app.run(thetoken)
