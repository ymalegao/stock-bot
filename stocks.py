import discord
from discord.ext import commands
import os 
import asyncio
import requests, json, random, datetime
from dotenv import load_dotenv
import collections
collections.Callable = collections.abc.Callable
import yfinance as yf
import schedule
import time
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.environ["DISCORD_TOKEN"]
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)
stocklist = {}
report={}
@client.event
async def on_ready():
    print(f"logged in as {client.user.name}")
    await morningstocks()
    await nightstocks()

@client.command(help="Adds item to list")
async def addstock(ctx,item,quantity):
    global stocklist
    if len(item+quantity) > 6:
        raise commands.BadArgument()
    for x in stocklist:
        if x == item:
            quantity =int(quantity) +int(stocklist[x])
    else:
        stocklist[item]=quantity
    for x in stocklist:
        st = yf.Ticker(x)
        last = st.fast_info['last_price']
       
        # quant = int(stocklist[x])
        lastprice = (float(f'{last:.2f}'))
        report[x]=lastprice
        print(report)
    
    print(stocklist)
    await ctx.send(f'Stock successfully added,\nYour stocks are now {stocklist}')



async def morningstocks():
    
    while True:
        now = datetime.datetime.now()
        # then = now+datetime.timedelta(days=1)

        then= now.replace(hour=8,minute=24)
        if then < now:
            then+=datetime.timedelta(days=1)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)

        channel = client.get_channel(1071297075830075405)
        await channel.send(f"Here is your stock morning summary: {report}  ")
        await asyncio.sleep(2400)

async def nightstocks():
    


    while True:
        now = datetime.datetime.now()
        # then = now+datetime.timedelta(days=1)

        then= now.replace(hour=13,minute=00)
        if then < now:
            then+=datetime.timedelta(days=1)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)

        channel = client.get_channel(1071297075830075405)
        await channel.send(f"Here is your evening stock summary: {report}  ")
        await asyncio.sleep(2400)

    

    


    



@client.command(help="shows list")
async def showstocks(ctx):
    totalval = 0
    global stocklist
    
    for x in stocklist:
        st = yf.Ticker(x)
        last = st.fast_info['last_price']
       
        quant = int(stocklist[x])
        lastprice= last * quant
        lastprice = (float(f'{lastprice:.2f}'))
        totalval +=lastprice
        portfolio = ', '.join(stocklist)

    await ctx.send(f'Your stocks are {portfolio}, the total value of your stocks is ${totalval}')



@client.command(help="search stock up based on ticker, help = Here are list of options: 'currency', 'exchange', 'timezone', 'shares', 'market_cap', 'last_price', 'previous_close' 'open', 'day_high', 'day_low', 'regular_market_previous_close', 'last_volume', 'fifty_day_average', 'two_hundred_day_average', 'ten_day_average_volume', 'three_month_average_volume', 'year_high', 'year_low', 'year_change' ")
async def stock(ctx, ticker):
   if len(ticker) >4:
        raise commands.BadArgument()
   tstock = yf.Ticker(ticker)
   name = tstock.info['shortName']
   if name == None:
    raise commands.BadArgument()      
   low = tstock.fast_info['day_low']
   high = tstock.fast_info['day_high']
   lastprice= tstock.fast_info['last_price']
   await ctx.send(f"What information do you want on {name}")
   @client.command(name="performance",help = 'tells you how stock is doing')
   async def performance(ctx):
        await ctx.send(f"The low in the market today for {name} was {low}, the high was {high}, and the last price was {lastprice} ")
   @client.command(name="info" ,help = "Here are list of options: 'currency', 'exchange', 'timezone', 'shares', 'market_cap', 'last_price', 'previous_close' 'open', 'day_high', 'day_low', 'regular_market_previous_close', 'last_volume', 'fifty_day_average', 'two_hundred_day_average', 'ten_day_average_volume', 'three_month_average_volume', 'year_high', 'year_low', 'year_change' ")
   async def info(ctx, type):
    await ctx.send(tstock.fast_info[type])




@stock.error
async def stocking_error(ctx, error ):
    if isinstance(error,commands.BadArgument):
        await ctx.send("Incorrect Format. Use Command this way: !stock GOOG")

@client.command()
async def hello(ctx):
    channel = client.get_channel(1071297075830075405)

    await channel.send(f'hello there {ctx.author.mention}')

msft = yf.Ticker("MSFT")
print(msft)
"""
returns
<yfinance.Ticker object at 0x1a1715e898>
"""

# get stock info
print(msft.fast_info['day_high'])

print("Here are list of options: 'currency', 'exchange', 'timezone', 'shares', 'market_cap', 'last_price', 'previous_close'")
print("'open', 'day_high', 'day_low', 'regular_market_previous_close', 'last_volume', 'fifty_day_average', 'two_hundred_day_average', 'ten_day_average_volume', 'three_month_average_volume', 'year_high', 'year_low', 'year_change']")


keep_alive()



client.run(TOKEN)


