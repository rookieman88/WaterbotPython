# -*- coding:utf-8 -*- 

##########################################################
#                Rutap Bot 2019 Main Module              #
# 모든 저작권은 팀 화공이 소유합니다. 모든 권리를 보유합니다. #
#                   BSD 3-Clause License                 #
##########################################################

import asyncio, discord, os, requests, random, datetime, re, json, sys, parser, time, psutil, ctypes, setting
from warn import *
from server_setting import *
from admin import *
from activity_log import *
from search import *
from msg_log import *
from hangul_clock import *
from preta import *
from upload import *
from normal import *

token = os.getenv("BOT_TOKEN")

app = discord.Client()
Setting = setting.Settings()
Copyright = Setting.copy
a = 0

async def unknown_error(message, e):
    now = datetime.datetime.now()
    randcode = "ERR :: %s%s%s%s" % (now.month, random.randint(1,10000000), now.day, random.randint(1,10000))
    embed = discord.Embed(title="죄송합니다. 원인을 알 수 없는 애러가 발생했습니다.", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주시기 바랍니다.", color=Setting.error_embed_color)
    embed.set_footer(text = randcode)
    await app.send_message(message.channel, embed=embed)
    await app.send_message(app.get_channel(Setting.err_log_channel), "```Markdown\n# Unknown error\n* info : %s(%s) | %s(%s) | %s(%s)\n* Code : %s\n* errinfo : %s```" % (message.server, message.server.id, message.channel, message.channel.id, message.author, message.author.id, randcode, e))

async def http_error(message, e):
    now = datetime.datetime.now()
    randcode = "ERR :: %s%s%s%s" % (now.month, random.randint(1,10000000), now.day, random.randint(1,10000))
    embed = discord.Embed(title="죄송합니다. 예기치 못한 애러가 발생했습니다.", description="봇이 메시지에 관련된 충분한 권한을 가지고 있는지 다시 한 번 확인 해 주시기 바랍니다.", color=0xff0000)
    embed.set_footer(text = randcode)
    await app.send_message(message.author, embed=embed)
    log_actvity("Discord HTTPException has occured in %s(%s) | %s(%s) : %s" % (message.server.id, message.server.name, message.channel.id, message.channel, e))
    await app.send_message(app.get_channel(Setting.err_log_channel), "```Markdown\n# Unknown error\n* info : %s(%s) | %s(%s) | %s(%s)\n* Code : %s\n* errinfo : %s```" % (message.server, message.server.id, message.channel, message.channel.id, message.author, message.author.id, randcode, e))


@app.event
async def on_message(message):
    try:
        try:
            if message.author.bot or os.path.isfile("%s_Banned.rts" % (message.author.id)):
                return None

            if message.channel.is_private:
                await app.send_message(message.channel, "<@%s>, DM에서는 명령어를 사용 할 수 없습니다!" % (message.author.id))
                return None

            try:
                log_msg(message.server, message.server.id, message.channel, message.channel.id, message.author.name, "#"+message.author.discriminator, message.author.id, message.content)
                ping(message)
            except Exception as e:
                print("msg log error : %s" % (e))
                
            if os.path.isfile("Server_%s/%s_Server_prefix.rts" % (message.server.id, message.server.id)):
                prefix = open("Server_%s/%s_Server_prefix.rts" % (message.server.id, message.server.id), 'r').read()

                

                if "워터봇 개발 봇종료" == message.content:
                    if message.author.id == Setting.owner_id:
                        await app.send_message(message.channel, "<@%s>, 봇의 가동을 중지합니다. 5분 이내로 오프라인으로 전환됩니다(디스코드 API 딜레이)." % (message.author.id))
                        await app.change_presence(game=discord.Game(name="Offline", type=0))
                        log_actvity("Change status to offline (Request by. %s)." % (message.author.id))
                        exit()
                    else:
                        await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. ~~오아시스는 같이 일할 노동자가 필요합니다~~." % (message.author.id))

                if message.content.startswith('워터봇 개발 상태메시지'):
                    if message.author.id == Setting.owner_id:
                        result = change_presence(message)
                        if result == False:
                            await app.send_message(message.channel, "<@%s>, 상태메시지는 비워둘 수 없습니다. 다시 시도 해 주세요." % (message.author.id))
                        else:
                            open("rpc.rts", 'w').write(str(message.content[17:]))
                            await app.send_message(message.channel, "<@%s>, 봇이 `%s`을(를) 플레이 하게 됩니다." % (message.author.id, message.content[17:]))
                            await app.change_presence(game=discord.Game(name=result, type=0))
                    else:
                        await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. ~~오아시스는 같이 일할 사람이 필요합니다~~" % (message.author.id))

            

                if message.content.startswith('워터봇 개발 블랙리스트'):
                    if message.author.id == Setting.owner_id:
                        result = user_ban(message)
                        if result == False:
                            await app.send_message(message.channel, "<@%s>, 자기 자신을 밴 시킬 수 없습니다!" % (message.author.id))
                        else:
                            await app.send_message(message.channel, "<@%s>, 앞으로 `%s`님의 모든 메시지를 무시합니다." % (message.author.id, result))
                    else:
                        await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. ~~오아시스는 같이 일할 사람이 필요합니다~~." % (message.author.id))

                if message.content.startswith('워터봇 개발 블랙리스트 풀기'):
                    if message.author.id == Setting.owner_id:
                        result = user_unban(message)
                        if result == False:
                            await app.send_message(message.channel, "<@%s>, 해당 유저는 밴 되지 않았습니다!" % (message.author.id))
                        else:
                            await app.send_message(message.channel, "<@%s>, 앞으로 `%s`님의 모든 메시지를 무시하지 않습니다." % (message.author.id, result))
                    else:
                        await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. ~~오아시스는 같이 일할 사람이 필요합니다~~." % (message.author.id))


                if "워터봇 개발 전체공지" in message.content:
                    if message.author.id == Setting.owner_id:
                        # DPNK 사용 구문 시점
                        embed=discord.Embed(title="워터봇 전체공지", color=Setting.embed_color)
                        embed.add_field(name="공지 발신을 준비하고 있습니다!", value="요청자 : <@" + message.author.id + ">", inline=True)
                        mssg = await app.send_message(message.channel, embed=embed)
                        a = []
                        b = []
                        e = []
                        ec = {}
                        embed=discord.Embed(title="워터봇 전체공지", color=Setting.embed_color)
                        embed.add_field(name="공지 발신중 입니다!", value="요청자 : <@" + message.author.id + ">", inline=True)
                        await app.edit_message(mssg, embed=embed)
                        for server in app.servers:
                            for channel in server.channels:
                                for tag in ["notice", "공지", "알림", "Alarm", "워터봇-공지"]:
                                    if tag in channel.name:
                                        dtat = True
                                        for distag in ["밴", "경고", "제재", "길드", "ban", "worry", "warn", "guild"]:
                                            if distag in channel.name:
                                                dtat = False
                                        if dtat:
                                            if not server.id in a:
                                                try:
                                                    await app.send_message(channel, message.content)
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
                                try:
                                    ch = await app.create_channel(server, "워터봇-공지")
                                    await app.send_message(ch, "**__공지 채널을 발견하지 못하여 자동적으로 해당 채널을 생성하였습니다.__")
                                    await app.send_message(ch, message.content)
                                except:
                                    asdf = asdf + str(server.name) + "[채널 생성에 실패하였습니다. (서버 관리자와 연락 요망)]\n"
                                else:
                                    asdf = asdf + str(server.name) + "[채널 생성 및 재발송에 성공하였습니다.]\n"
                        asdf = asdf + "```"
                        embed=discord.Embed(title="워터봇 전체공지", color=Setting.embed_color)
                        embed.add_field(name="공지 발신이 완료되었습니다!", value="요청자 : <@" + message.author.id + ">", inline=True)
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
                        embed.add_field(name="공지 발신에 성공한 채널은 다음과 같습니다 :", value=sucess, inline=False)
                        embed.add_field(name="공지 발신에 실패한 채널은 다음과 같습니다 :", value=missing, inline=False)
                        embed.add_field(name="키워드가 발견되지 않은 서버는 다음과 같습니다 :", value=notfound, inline=False)
                        await app.edit_message(mssg, embed=embed)
                        # DPNK 사용 구문 종점
                
                    else:
                        await app.send_message(message.channel, "<@%s>, 봇 관리자로 등록되어 있지 않습니다. ~~오아시스는 같이 일할 사람이 필요합니다~~." % (message.author.id))



app.run(token)
