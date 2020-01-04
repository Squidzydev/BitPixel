
import datetime

import requests

import os



from bs4 import BeautifulSoup
import discord, asyncio
from discord.ext import commands
from discord import Embed





_timeanddata = datetime.datetime.now()
client = commands.Bot(command_prefix='!')


@client.command(pass_context = True)
async def toptoday(ctx):
    await ctx.message.delete()
    r = requests.get('https://minecraft-statistic.net/ru/server/95.217.40.80_25565/top/today/')
    b = BeautifulSoup(r.text, 'html.parser')
    trs = b.find_all('tr')
    tops = ''
    em = Embed(color=0xffff00, title='Топ игроков за сегодня')
    for x in range(1 ,6):
        tops = tops + '```css'+ trs[x].text + '```'
    em.description = tops
    await ctx.send(embed =em)

@client.command(pass_context = True)
async def topall(ctx):
    await ctx.message.delete()
    r = requests.get('https://minecraft-statistic.net/ru/server/95.217.40.80_25565/top/')
    b = BeautifulSoup(r.text, 'html.parser')
    trs = b.find_all('tr')
    tops = ''
    em = Embed(color=0xffff00, title='Топ игроков за все время')
    for x in range(1 ,6):
        tops = tops + '```css'+ trs[x].text + '```'
    em.description = tops
    await ctx.send(embed =em)


@client.command(pass_context = True)
async def info(ctx, player = None):
    await ctx.message.delete()
    try:
        name_url = 'https://ru.namemc.com/profile/{0}'.format(player)
        r = requests.get(url=name_url)
        print(r.text)
        b = BeautifulSoup(r.text, 'html.parser')
        v = b.find('div', attrs={'class':"card-body text-center"})
        print(v)
        n = v.find('a')['href']
        em = Embed()
        print(n)
        n = n.replace('/skin/', '')
        print(n)
        vb = b.find_all('div', attrs={'class':'card-body py-1'})
        mnn = ''
        numer = 0
        for x in vb:

            try:

                f = x.find_all('div', attrs = {'class':'row no-gutters'})
                for nd in f:
                    nbnb = nd.find_all('a', attrs={'translate': "no"})
                    print(nbnb)
                    for vnm in nbnb:
                        numer = numer + 1
                        mnn = mnn + str(numer) + ': ' +vnm.text + '\n'


            except:
                pass


        mn = b.find('div', attrs={'class':"row no-gutters align-items-center"})
        mn = mn.find('samp').text

        vb = vb[1].text
        bnm = f'https://render.namemc.com/skin/3d/body.png?skin=' + n+ '&modelslim&width=320&height=320&bg1=ffffff&bg2=f4f4f4'
        print(bnm)
        em.set_thumbnail(url=bnm)
        em.description = '**История НИКОВ:**' + '```css' + '\n'  + '\n'+mnn +'```' + '\n' + '**Ссылка на профиль игрока**' + '\n'+ name_url +'\n'+'\n' + '**UUID**:' +'\n'+ mn
        em.set_footer(text='Спасибо проекту namemc.com', icon_url='https://static.namemc.com/i/favicon-30.png')

        em.title = 'История и информация об игроке ' + player
        awaite = await ctx.send(embed = em)
        await asyncio.sleep(30)
        await awaite.delete()
    except:
        em = Embed(title='Something wrong...')
        awaited = await ctx.send(embed =em)
        await asyncio.sleep(3)
        await awaited.delete()




@client.command(pass_context = True)
async def user(ctx, player : discord.Member):
   await ctx.message.delete()
   pn = player.nick
   pav = player.avatar_url
   pca = player.created_at
   ps = player.status
   if player.activity != None:
        pac = player.activity
        pac = pac.name
   else:
        pac = 'Пользователь ни во что не играет'

   pja = player.joined_at
   ds = 'Настоящий ник пользователя: ' +str(pn) + '\n' + 'Время создания аккаунта: ' +str(pca) + '\n' +'Статус:' +str(ps) + '\n'+ 'Пользователь занят: ' + str(pac) + '\n' + str(pja.year)+ '.' + str(pja.month)+ '.' + str(pja.day)
   em = Embed(title='Информация о пользователе '+ player.display_name, description=ds, color=0xffff00)
   em.set_footer(icon_url=pav, text='Buzzy Bees')
   await ctx.send(embed = em)




@client.command(pass_context = True)
async def minewiki(ctx, *kwargs):
    await ctx.message.delete()
    nd = ''
    for x in kwargs:
        nd = nd + ' ' + x
    nd = nd[1:len(nd)]

    s = requests.Session()
    s.get('https://minecraft-ru.gamepedia.com')
    data = {
        'search': nd,
        'title': 'Служебная:Поиск',
        'go': 'Перейти'
    }
    r = s.post('https://minecraft-ru.gamepedia.com', data=data)
    b = BeautifulSoup(r.text, 'html.parser')
    f = b.find('div', attrs={'class':"mw-parser-output"})
    bd = ''
    try:
        v = f.find_all('p')

        for x in v:
            if x.text.startswith(nd):
                bd = bd + x.text
    except:
        pass

    if bd == '':
        print('k')
        f = b.find_all('li')
        print(f)
        for x in f:

            try:
                if len(bd) < 1500:
                    if x.find('a')['href'].startswith('/'):
                        if 'index.php' in x.find('a')['href']:
                            pass
                        else:
                            bd = bd +'\n' +x.find('a').text+ '\n' +'https://minecraft-ru.gamepedia.com' + x.find('a')['href']
            except:
                pass


    print(bd)
    tit = 'Результаты по запросу {}'.format(nd)




    em = Embed(title=tit, description=bd, color=0xffff00)
    await ctx.send(embed = em)

token = os.environ.get('BOT_TOKEN')
client.run(token, bot = True)