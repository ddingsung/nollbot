import asyncio
import discord
from discord import flags
import requests
import pymysql
import os
from discord_buttons_plugin import  *
from discord import Intents
from discord_slash import SlashCommand
from discord.ext import commands
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
from discord.utils import get
intents = discord.Intents.default() 
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)
buttons = ButtonsClient(bot)

#token = "ODc3MzUyNTg2NTYxMzM5NDcy.YRxYRQ.MKLngogbcx6ETYVCO6OY4pOGPWA"


@bot.event
async def on_ready():
    print("Logged in as ") 
    print(bot.user.name)
    print(bot.user.id)
    
@bot.event
async def on_message(msg):
    if msg.author.bot: return None
    topic = msg.channel.topic
    if topic is not None and '#인증' in topic:
        await bot.process_commands(msg)
@bot.event
async def on_member_join(member):
    await member.add_roles(bot.get_guild(877349097881874492).get_role(888770400954241065))
@bot.command(name='정보')
async def chat(ctx):
    print(ctx.author.nick)
    await ctx.message.author.add_role(get(ctx.guild.roles, name="버서커"))
@bot.command(name='인증')
#@commands.has_permissions(change_nickname=True) / - 스레기
async def information(ctx, *, nickname):
            url = "https://lostark.game.onstove.com/Profile/Character/"+ nickname
            print (url) # 로그 성 출력
            global Class
            global guild
            global nick
            global idk
            idk = ctx.author.id
            print(idk)
            nick = nickname
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            Class = soup.find("div", attrs={"class":"content content--profile"}).find("img").get('alt')
            img = soup.find("div", attrs={"class":"content content--profile"}).find("img").get('src')
            level = soup.find_all("div", {"class":"level-info2__item"})[0].find_all("span")[1].text
            guild = soup.find_all("div", {"class":"game-info__guild"})[0].find_all("span")[1].text

    
            print(Class) 
            id = ctx.author
            channel = ctx.channel
            embed = discord.Embed(title=nick + "님 환영합니다.", description="", color=0x62c1cc)
            embed.set_thumbnail(url=img)
            embed.add_field(name="직업정보", value="`" + Class + "`", inline=True)
            embed.add_field(name="길드", value="`" + guild + "`", inline=True)
            embed.add_field(name="달성 아이템 레벨", value="`" + level + "`", inline=False)
            embed.set_footer(text="")
            await ctx.send(embed=embed)
            await buttons.send(
                content = "`이 캐릭터가 맞나요?`",
                channel = ctx.channel.id,
                components = [ActionRow([
                    Button(
                        label="네",
                        style=ButtonType().Success,
                        custom_id="button_yes"
                    ),
                    Button(
                        label="아니요",
                        style=ButtonType().Danger,
                        custom_id="button_no"

                    )
                ])]
                )
@buttons.click
async def button_yes(ctx):
            if guild == 'noll':
                print(idk)
                user_id = ctx.member.id
                member = ctx.guild.get_member(user_id)
                await asyncio.sleep(1)
                await ctx.channel.purge(limit=3)
                await member.add_roles(get(ctx.guild.roles, name=Class))
                await member.remove_roles(get(ctx.guild.roles, name="손님"))
                await member.edit(nick=nick)
                await ctx.reply("`권한부여 완료. 환영합니다 :D`", flags = MessageFlags().EPHEMERAL)
            else:
                await ctx.reply("`길드원만 들어올수있는 디스코드입니다.\n관리자에게 문의 해주세요.`", flags = MessageFlags().EPHEMERAL)
                await ctx.channel.purge(limit=3)
        #member = ctx.message.author
        #await member.edit(nick=text)
        #await ctx.send(f"<"+ text +"> 님의 직업은 "+str(Class))
@buttons.click
async def button_no(ctx):
    await ctx.reply("`다시 한번 시도해보세요`", flags=MessageFlags().EPHEMERAL)
    await ctx.channel.purge(limit=3)
@information.error
async def infor_error(ctx, error):
    await ctx.send("`닉네임을 찾을수없습니다.\n다시한번 확인후 입력해주세요.\n오류가 지속되면 관리자에게 DM주세요.`")
    await asyncio.sleep(3)
    await ctx.channel.purge(limit=2)
@bot.command(name="채널")
async def 정보(ctx):
    members = [member.name for member in ctx.guild.members]
    await ctx.send(
        "{} 서버는 {} 서버이며 구성원은 {} 이고 총 {} 명입니다.".format(
            ctx.guild.name, 
            ctx.guild.region, 
            members, 
            ctx.guild.member_count
        )
    )

bot.run(os.environ['token'])
    
