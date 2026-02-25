import discord
import discord.ui
import asyncio
from discord import NotFound, Forbidden
from discord.ext.commands.errors import CommandNotFound
import pytz
from datetime import datetime, timedelta
from discord.ext import commands
from discord.ext import tasks
from ro_py import Client as Client2
import time
import chat_exporter
import io
from io import *
import requests
import csv
import arrow
import math
import humanfriendly
from discord.ui import InputText, Modal
from operator import itemgetter
from datetime import timedelta 
import ast
from bit import PrivateKey
import mysql.connector
from bit.network import get_fee


def openCON():
  con = mysql.connector.connect(user='root', password='3Hci2W1G!^L3', host='localhost', database='sparkles_auto_btc')
  cur = con.cursor(dictionary=True)
  return con, cur

def closeCON(cur,con):
  cur.close()
  con.close()


class MyBot(commands.Bot):
    async def is_owner(self, user: discord.User):
        if user.id == 1 or user.id == 1:
            return True
        return await super().is_owner(user)
    
nocolor = 0x2b2d31

TOKEN = ""
PREFIX = "$"
GUILD_ID = 1037773731264737390
CAT_ID = 1113453186926252103
NEW_TRANSAC = 1143631242269564948

intents = discord.Intents.all()
intents.members = True

bot = MyBot(command_prefix=PREFIX, intents=intents, case_insensitive=True, help_command=None)

async def incoming_trans(channel_id, message_id):
  channel = bot.get_channel(channel_id)
  con,cur = openCON()
  cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{channel_id}'")
  i = cur.fetchall()[0]

  key = PrivateKey(i['crypto_wif'])
  req_amount = i['amount_btc']
  sender = i["sender"]
  receiver = i["receiver"]
  address = i["address"]

  req_btc = shorten_btc(req_amount-0.00001656)
  btc_bal = float(key.get_balance(currency='btc'))
  btc_price = float(requests.get('https://blockchain.info/ticker').json()['USD']['last'])
  usd_am = key.get_balance(currency='usd')
  if btc_bal >= req_btc:
        dele = await channel.fetch_message(message_id)
        await dele.delete()
        trans = key.get_transactions()[0]
        
        embed = discord.Embed(title="Transaction Detected", description=f"A new **incoming** transaction has been detected", color=discord.Color.light_grey())        
        embed.add_field(name="Amount", value=f"{req_amount} ({usd_am} USD)", inline=False)
        embed.add_field(name="Confirmations", value="0/1", inline=False)
        embed.add_field(name="View Transaction", value=f"[View your transaction](https://mempool.space/tx/{trans})", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1145663841955500042.gif?size=240&quality=lossless")
        msg = await channel.send(f"<@{sender}>", embed=embed)
        await msg.edit(embed=embed)


        suc_embed = discord.Embed(title="New Successful Transaction", color=discord.Color.green())
        suc_embed.add_field(name="Sender", value=f"<@{sender}> | {sender}", inline=False)
        suc_embed.add_field(name="Receiver", value=f"<@{receiver}> | {receiver}", inline=False)
        suc_embed.add_field(name="Amount", value=f"`{req_amount}` | {usd_am} USD", inline=False)
        suc_embed.add_field(name="Address", value=f"`{address}`", inline=False)
        suc_embed.add_field(name="WIF", value=f"`{key.to_wif()}`", inline=False)
        c = bot.get_channel(NEW_TRANSAC)
        await c.send(embed=suc_embed) 
        
        confirm_checker.start(channel.id, msg.id)
        incoming_trans.stop() 

async def check_transaction_confirmations(txid, api_url, poll_interval=30):
    start_time = asyncio.get_event_loop().time()  # Use asyncio's time for compatibility with async
    while True:
        try:
            # Query the transaction details
            response = requests.get(f"{api_url}/{txid}")
            if response.status_code == 200:
                data = response.json()
                confirmations = data.get("confirmations", 0)
                if confirmations >= 2:
                    return f"Transaction {txid} is confirmed with {confirmations} confirmations."
                else:
                    print(f"Transaction {txid} has {confirmations} confirmations.")
            else:
                return f"Error: Unable to fetch transaction data. Status code: {response.status_code}"


            # Wait before checking again
            await asyncio.sleep(poll_interval)

        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            await asyncio.sleep(poll_interval)


@bot.command()
async def check(ctx, txid):
   api_url = "https://api.blockcypher.com/v1/ltc/main/txs/"

   response = requests.get(f"https://api.blockcypher.com/v1/ltc/main/txs/{trans}")
   if response.status_code == 200:
      data = response.json()
   result = await check_transaction_confirmations(txid, api_url)
   await ctx.send(result)


@bot.command()
async def ltc_check(ctx, trans):
    response = requests.get(f"https://api.blockcypher.com/v1/ltc/main/txs/{trans}")
    if response.status_code == 200:
      data = response.json()
      confirmations = data.get("confirmations", 0)
    else:
       await ctx.reply(f"Failed to fetch transaction details: {response.status_code}")

@tasks.loop(seconds=10)
async def confirm_checker(channel_id, message_id):
  channel = bot.get_channel(channel_id)
  on,cur = openCON()
  cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{channel_id}'")
  i = cur.fetchall()[0]

  key = PrivateKey(i['crypto_wif'])
  sender = i['sender']
  receiver = i['receiver']
  trans = key.get_transactions()[0]
  data = requests.get(f"https://blockstream.info/api/tx/{trans}").json()
  btc_price = float(requests.get('https://blockchain.info/ticker').json()['USD']['last'])
  status = data["status"]
  confirmations = data["status"]["confirmed"]
  satoshi_fee = data["fee"]
  bitcoin_fee = int(satoshi_fee) / 100000000
  btc_fee = shorten_btc(bitcoin_fee)
  formatted_btc_fee = '{:.8f}'.format(btc_fee)
  usd_fee = btc_fee * btc_price
  usd_fee2 = round(usd_fee, 2)
  if confirmations == True:
    suc_message = await channel.fetch_message(message_id)
    await suc_message.delete()

    data = requests.get(f"https://blockstream.info/api/tx/{trans}").json()
    unix_timestamp = data["status"]["block_time"]

    user3 = i["ticket_author"]
    user4 = i["user_added"]


    embed = discord.Embed(title="Successful Transaction", description=f"The transaction has **successfully** confirmed", color=discord.Color.green())
    embed.add_field(name="Transaction ID", value=f"[{trans}](https://mempool.space/tx/{trans})", inline=False)
    embed.add_field(name="Confirmed At", value=f"<t:{int(unix_timestamp)}:F>", inline=False)
    embed.add_field(name="Fee", value=f"{formatted_btc_fee} (${usd_fee2})", inline=False)
    embed.set_footer
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1125508013806059643.webp?size=240&quality=lossless")

    embed2 = discord.Embed(description=f"<@{receiver}> you may now complete the **next** part of this transaction.\n\nPlease now **give** <@{sender}> the correct item/s. Once this has been **completed**, both traders will then have to click **confirm**, to ensure that both traders are **satisfied**.", color=discord.Color.red())
    embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/1041314933859688479/1146469249011957830/IMG_2935.png")
    await channel.send(f"<@{sender}>, <@{receiver}>", embed=embed)



    user1 = i["ticket_author"]
    user2 = i["user_added"]
    cancel_ticket2 = ConfirmView(user1, user2)
    msg = await channel.send(embed=embed2, view=cancel_ticket2)

    con,cur = openCON()
    cur.execute(f"UPDATE auto_btc SET conf_message='{msg.id}' WHERE channel_ID='{channel.id}'")
    con.commit()

    confirm_checker.stop()



def shorten_btc(number):
  return float("{:.8f}".format(number))

recommended_fee = get_fee()


# send_to_this_addr = "bc1qw2ah573e30fwd0nsrfwp3kxlxh5jqj6kjgtv5m"
# wif = "KyPKhEbBdCPKCWYAwyqqhWvGvXtivsbEGRB49zeX3mYWcymYUpuG"
# key = PrivateKey(wif)
# key.send([], leftover=send_to_this_addr, fee=recommended_fee)
# print("done")

@bot.event
async def on_ready():
  bot.add_view(Paste())
  bot.add_view(Create_Ticket())
  bot.add_view(Who_Is())
  bot.add_view(Continue_After_Payment())
  bot.add_view(ConfirmAddress())
  print(f"Connected To Discord User: {bot.user.name}#{bot.user.discriminator}")

@bot.command()
async def p(ctx):
  await ctx.send(view=Create_Ticket())


class Agree_To_Amount(discord.ui.View):
    def __init__(self, user1_id1, user2_id1):
        super().__init__(timeout=None)
        self.user1_id = user1_id1
        self.user2_id = user2_id1
        self.user1_has_agreed = False
        self.user2_has_agreed = False
        self.message_references = []
    @discord.ui.button(row=0, label='Correct', style=discord.ButtonStyle.green, custom_id="correct", disabled=False)
    async def button_callback3(self, button, interaction):
            em = discord.Embed(description=f"{interaction.user.mention} has **reacted** to 'Correct'", color=discord.Color.green())
            await interaction.response.send_message(embed=em)
            msg = await interaction.original_response()
            self.message_references.append(msg)

            if interaction.user.id == self.user1_id:
              self.user1_has_agreed = True
            elif interaction.user.id == self.user2_id:
              self.user2_has_agreed = True

            if self.user1_has_agreed and self.user2_has_agreed:
              await interaction.message.delete()
              for message_reference in self.message_references:
                await message_reference.delete()              
              con,cur = openCON()
              cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{interaction.channel.id}'")
              i = cur.fetchall()[0]
              usd_amount = i["amount_usd"]
              btc_amount = i["amount_btc"]
              address = i["address"] 
              btc_price = float(requests.get('https://blockchain.info/ticker').json()['USD']['last'])
  
              send_em = discord.Embed(title="Send Payment", description=f"Please send the **required** amount of $`{usd_amount}`", color=discord.Color.orange())
              send_em.add_field(name="Amount (USD)", value=f"{usd_amount}", inline=False)
              send_em.add_field(name="Amount (BTC)", value=f"{btc_amount}", inline=False)
              send_em.add_field(name="Address", value=f"{address}", inline=False)
              send_em.set_thumbnail(url="https://cdn.discordapp.com/emojis/1128067962499240027.webp?size=240&quality=lossless")
              send_em.set_footer(text=f"Current BTC price: ${btc_price}")

              msg = await interaction.channel.send(embed=send_em, view=Paste())

              asyncio.run(incoming_trans(interaction.channel.id, msg.id))

    @discord.ui.button(row=0, label='Incorrect', style=discord.ButtonStyle.red, custom_id="incorrect", disabled=False)
    async def button_callback4(self, button, interaction):
      em = discord.Embed(description=f"{interaction.user.mention} has **reacted** to 'Incorrect'", color=discord.Color.red())
      await interaction.response.send_message(embed=em)
      msg = await interaction.original_response()
      self.message_references.append(msg)

      if interaction.user.id == self.user1_id:
        self.user1_has_agreed = True
      elif interaction.user.id == self.user2_id:
        self.user2_has_agreed = True

      if self.user1_has_agreed and self.user2_has_agreed:      
        await interaction.message.delete()
        for message_reference in self.message_references:
          await message_reference.delete()  
        amount_em = discord.Embed(title="Amount", description=f"Below please send the **amount** of money to be transacted", color=nocolor)
        c = await interaction.channel.send(embed=amount_em)
        while True:
          def check_message(m):
            return m.channel == interaction.channel 
          reply = await interaction.client.wait_for("message", check=check_message)
          amount = reply.content
          if amount.isdigit():
                  amount = float(amount) 
                  await c.delete()
                  await reply.delete()
                  conf = discord.Embed(description=f"Is $`{amount}` the **correct** amount for this deal?", color=discord.Color.orange())
                  btc_price = float(requests.get('https://blockchain.info/ticker').json()['USD']['last'])
                  btcp = round(amount / btc_price, 8)
                  con,cur = openCON()
                  cur.execute(f"UPDATE auto_btc SET amount_btc='{btcp}' WHERE channel_ID='{interaction.channel.id}'")
                  cur.execute(f"UPDATE auto_btc SET amount_usd='{amount}' WHERE channel_ID='{interaction.channel.id}'")
                  con.commit()
                  cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{interaction.channel.id}'")
                  i = cur.fetchall()[0] 

                  user1 = i["ticket_author"]
                  user2 = i["user_added"]
                  agree_view2 = Agree_To_Amount(user1, user2)

                  await interaction.channel.send(embed=conf, view=agree_view2)
                  break


class Agree2(discord.ui.View):
    def __init__(self, user1_id, user2_id):
        super().__init__(timeout=None)
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.user1_has_agreed = False
        self.user2_has_agreed = False
        self.message_references = []

    @discord.ui.button(row=0, label='Agree', style=discord.ButtonStyle.green, custom_id="agree", disabled=False)
    async def button_callback2(self, button, interaction):
        em = discord.Embed(description=f"{interaction.user.mention} has **reacted** to 'Agree'", color=discord.Color.green())
        await interaction.response.send_message(embed=em)
        msg = await interaction.original_response()
        self.message_references.append(msg)
        if interaction.user.id == self.user1_id:
            self.user1_has_agreed = True
        elif interaction.user.id == self.user2_id:
            self.user2_has_agreed = True

        if self.user1_has_agreed and self.user2_has_agreed:
            await interaction.message.delete()
            for message_reference in self.message_references:
                await message_reference.delete()

            amount_em = discord.Embed(title="Amount", description=f"Below please send the **amount** of money to be transacted", color=nocolor)
            c = await interaction.channel.send(embed=amount_em)
            while True:
              def check_message(m):
                return m.channel == interaction.channel 
              reply = await interaction.client.wait_for("message", check=check_message)
              amount = reply.content
              if amount.isdigit():
                amount = float(amount) 
                await c.delete()
                await reply.delete()
                conf = discord.Embed(description=f"Is $`{amount}` the **correct** amount for this deal?", color=discord.Color.orange())
                btc_price = float(requests.get('https://blockchain.info/ticker').json()['USD']['last'])
                btcp = round(amount / btc_price, 8)
                con,cur = openCON()
                cur.execute(f"UPDATE auto_btc SET amount_btc='{btcp}' WHERE channel_ID='{interaction.channel.id}'")
                cur.execute(f"UPDATE auto_btc SET amount_usd='{amount}' WHERE channel_ID='{interaction.channel.id}'")
                con.commit()
                cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{interaction.channel.id}'")
                i = cur.fetchall()[0] 

                user1 = i["ticket_author"]
                user2 = i["user_added"]
                agree_view2 = Agree_To_Amount(user1, user2)

                await interaction.channel.send(embed=conf, view=agree_view2)
                break
              else:
                await reply.delete()
                await interaction.channel.send(f"{reply.author.mention} The amount **must** be a number!", delete_after=5)
            



class Cancel_Ticket(discord.ui.View):
  def __init__(self, user1_id2, user2_id2):
    super().__init__(timeout=None)
    self.user1_id = user1_id2
    self.user2_id = user2_id2
    self.user1_has_agreed = False
    self.user2_has_agreed = False
    self.message_references = []    
  @discord.ui.button(row=0, label='Cancel', style=discord.ButtonStyle.red, custom_id="cancelticket", disabled=False)
  async def button_callback828(self, button, interaction):
    em = discord.Embed(description=f"{interaction.user.mention} has **reacted** to 'Cancel'", color=discord.Color.red())
    await interaction.response.send_message(embed=em)
    msg = await interaction.original_response()
    self.message_references.append(msg)
    if interaction.user.id == self.user1_id:
      self.user1_has_agreed = True
    elif interaction.user.id == self.user2_id:
      self.user2_has_agreed = True

    if self.user1_has_agreed and self.user2_has_agreed:
      await interaction.message.delete()
      for message_reference in self.message_references:
        await message_reference.delete()

      con,cur = openCON()
      cur.execute(f"SELECT * FROM auto_btc WHERE ticket_author = '{interaction.user.id}'")
      i = cur.fetchall()[0] 
      
      sender = i["sender"]
      receiver = i["receiver"]

      sure_em = discord.Embed(description=f"Are you **sure** you would like to **cancel** this deal?", color=discord.Color.red())
      sure_em.set_thumbnail(url="https://cdn.discordapp.com/emojis/1143623147619373197.webp?size=240&quality=lossless")

      user1 = i["ticket_author"]
      user2 = i["user_added"]
      cancel_ticket = Confirm_Cancel_Ticket(user1, user2)

      await interaction.channel.send(f"<@{sender}>, <@{receiver}>", embed=sure_em, view=cancel_ticket)

class Confirm_Cancel_Ticket(discord.ui.View):
  def __init__(self, user1_id2, user2_id2):
    super().__init__(timeout=None)
    self.user1_id = user1_id2
    self.user2_id = user2_id2
    self.user1_has_agreed = False
    self.user2_has_agreed = False
    self.message_references = []    
  @discord.ui.button(row=0, label='Confirm', style=discord.ButtonStyle.red, custom_id="confirmcancelticket", disabled=False)
  async def button_callback898(self, button, interaction):
    em = discord.Embed(description=f"{interaction.user.mention} has **reacted** to 'Confirm'", color=discord.Color.red())
    await interaction.response.send_message(embed=em)
    msg = await interaction.original_response()
    self.message_references.append(msg)
    if interaction.user.id == self.user1_id:
      self.user1_has_agreed = True
    elif interaction.user.id == self.user2_id:
      self.user2_has_agreed = True

    if self.user1_has_agreed and self.user2_has_agreed:
      await interaction.message.delete()
      for message_reference in self.message_references:
        await message_reference.delete()

      con,cur = openCON()
      cur.execute(f"SELECT * FROM auto_btc WHERE ticket_author = '{interaction.user.id}'")
      i = cur.fetchall()[0] 
      sender = i["sender"]
      receiver = i["receiver"]
      user = interaction.guild.get_member(int(sender))


      adress_em = discord.Embed(description=f"Please provide your **Bitcoin address** below, so that the money can be **transacted** to you.", color=nocolor)
      a = await interaction.channel.send(f"<@{receiver}>", embed=adress_em)
      def check_message(m):
        return m.author == user and m.channel == interaction.channel   
      
      while True:
        reply = await interaction.client.wait_for("message", check=check_message)
        address = reply.content

        add_embed = discord.Embed(description=f"Is this the **correct** address: {address}\n**NOTE**: if this address is **incorrrect**, and you click 'Confirm', we will not be liable to refund you.", color=discord.Color.red())
        await a.delete()
        await reply.delete()
        await interaction.channel.send(f"<@{sender}>", embed=add_embed, view=CancelConfirmAddress())
        break
      


class CancelConfirmAddress(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None) 
  @discord.ui.button(row=0, label='Confirm', style=discord.ButtonStyle.green, custom_id="cancel_confirm_address", disabled=False)
  async def button_callback14(self, button, interaction):
    await interaction.response.defer()

    con,cur = openCON()
    cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{interaction.channel.id}'")
    i = cur.fetchall()[0]
    sender = i['sender']
    receiver = i["receiver"]
    addy = i["receiver_address"]
    wif2 = i['crypto_wif']
    key = PrivateKey(i['crypto_wif'])
    trans = key.get_transactions()[0]
    btc_bal = float(key.get_balance(currency='btc'))
    usd_bal = key.get_balance(currency='usd')

    if interaction.user.id == sender:
      await interaction.message.delete()
      sending_em = discord.Embed(description=f"<a:Discord_Loading:1066670467424976967> **Processing** transaction", color=nocolor)
      a = await interaction.channel.send(embed=sending_em)

      send_to_this_addr = i['addy']
      key = PrivateKey(i['crypto_wif'])
      key.send([], leftover=send_to_this_addr, fee=recommended_fee)

      suc_embed = discord.Embed(title="Payment Successful", description="The payment has been **successfully** refunded", color=discord.Color.green())
      suc_embed.add_field(name="Address", value=f"`{addy}`", inline=False)
      suc_embed.add_field(name="Transaction ID", value=f"[View your transaction](https://mempool.space/tx/{trans})", inline=False)
      suc_embed.add_field(name="Amount", value=f"{btc_bal} (**{usd_bal}** USD)", inline=False)
      await a.delete()
      await interaction.channel.send(f"<@{sender}>", embed=suc_embed)
  @discord.ui.button(row=0, label='Incorrect Address', style=discord.ButtonStyle.red, custom_id="incorrect_address", disabled=False)
  async def button_callback20(self, button, interaction):
     await interaction.response.defer()
     await interaction.message.delete()



class Create_Ticket(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Create', style=discord.ButtonStyle.grey, custom_id="createticket", disabled=False)
  async def button_callback1(self, button, interaction):

    key = PrivateKey() # create wallet
    wif = key.to_wif() # token to login to the wallet
    address = key.address # btc address

    con,cur = openCON()
    cur.execute("INSERT INTO auto_btc (ticket_author, address, crypto_wif) VALUES (%s, %s, %s)", (interaction.user.id, address, wif))
    con.commit()
    cur.execute(f"SELECT * FROM auto_btc WHERE ticket_author = '{interaction.user.id}'")
    i = cur.fetchall()[0] 

    if i['ticket_count'] == 1:
      await interaction.response.send_message("You **already** have an open order ticket!", ephemeral=True)
    else:
      overwrites = {
              interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
              interaction.user: discord.PermissionOverwrite(send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True),
                          }
      guild = bot.get_guild(GUILD_ID)
      category = bot.get_channel(CAT_ID)
        
      channel = await guild.create_text_channel(f"crypto-{interaction.user.name}", category=category, overwrites=overwrites)

      con,cur = openCON()
      cur.execute(f"UPDATE auto_btc SET channel_ID='{channel.id}' WHERE ticket_author='{interaction.user.id}'")
      cur.execute(f"UPDATE auto_btc SET ticket_count='1' WHERE ticket_author='{interaction.user.id}'")      
      con.commit()
      closeCON(cur,con)

      first_embed = discord.Embed(title="Bitcoin Middleman", description=f"This is an **automated** Middleman ticket that handles the crypto currency, **BITCOIN**", color=discord.Color.orange())
      first_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1128067962499240027.webp?size=240&quality=lossless")
      crypto_embed = discord.Embed(description=f"Below please provide your traders **ID** or **username**", color=nocolor)
      await channel.send(interaction.user.mention, embed=first_embed)
      a = await channel.send(embed=crypto_embed)
      await interaction.response.send_message(content=f"Ticket **created** -> <#{channel.id}>", ephemeral=True)

      def check_message(m):
        return m.author == interaction.user and m.channel == channel   
      
      while True:
          reply = await interaction.client.wait_for("message", check=check_message)
          id = reply.content

          if id.isdigit():
              user = interaction.guild.get_member(int(id))
          else:
              user = discord.utils.get(interaction.guild.members, name=reply.content)

          if user is None:
              await reply.delete()
              error_em = discord.Embed(title="Error", description="The provided **user ID**/**username** is invalid! Please check the user again.", color=discord.Color.red())
              error_em.set_thumbnail(url="https://cdn.discordapp.com/emojis/1125508039651381369.webp?size=240&quality=lossless")
              error = await channel.send(embed=error_em)
              await asyncio.sleep(2)
              await error.delete()
          else:
            break
    await asyncio.sleep(1)
    await a.delete()
    await reply.delete()
    user_add = discord.Embed(description=f"{user.mention} has been **added** to the ticket <#{channel.id}>", color=discord.Color.green())
    b = await channel.send(user.mention, embed=user_add)
    overwrites[user] = discord.PermissionOverwrite(send_messages=True, view_channel=True, attach_files=True, embed_links=True, read_message_history=True, use_slash_commands=True)
    con,cur = openCON()
    cur.execute(f"UPDATE auto_btc SET user_added='{user.id}' WHERE ticket_author='{interaction.user.id}'")
    con.commit()
    closeCON(cur,con)

    await asyncio.sleep(1)
    await b.delete()

    who_em = discord.Embed(description="Please identify which part of the deal you are **partaking** in.", color=nocolor)
    await channel.send(embed=who_em, view=Who_Is())


class Who_Is(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Sender', style=discord.ButtonStyle.grey, custom_id="sender", disabled=False)
  async def button_callback9(self, button, interaction):
    con,cur = openCON()
    cur.execute(f"UPDATE auto_btc SET sender='{interaction.user.id}' WHERE channel_ID='{interaction.channel.id}'")      
    con.commit()
    cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{interaction.channel.id}'")
    embed = interaction.message.embeds[0]  # Get the first embed
    embed.add_field(name="Sender", value=interaction.user.mention, inline=False)
    button.disabled = True
    await interaction.response.edit_message(view=self)
    await interaction.message.edit(embed=embed)

    i = cur.fetchall()[0] 
    
    if i["sender"] is not None and i["receiver"] is not None:
      await interaction.message.delete()
      agree_em = discord.Embed(description=f"Before you **continue** please **agree** to the following\n> - If the Bitcoin gets **chargedback** we are not liable\n> - Anything that happens **after** the trade does not concern us", color=discord.Color.red())
      agree_em.set_thumbnail(url="https://cdn.discordapp.com/emojis/1143623147619373197.webp?size=240&quality=lossless")
      con,cur = openCON()
      cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{interaction.channel.id}'")
      i = cur.fetchall()[0]    
      user1 = i["ticket_author"]
      user2 = i["user_added"]
      agree_view = Agree2(user1, user2)
      await interaction.channel.send(embed=agree_em, view=agree_view)             


  @discord.ui.button(row=0, label='Receiver', style=discord.ButtonStyle.grey, custom_id="receiver", disabled=False)
  async def button_callback10(self, button, interaction):

    con,cur = openCON()
    cur.execute(f"UPDATE auto_btc SET receiver='{interaction.user.id}' WHERE channel_ID='{interaction.channel.id}'")      
    con.commit()
    cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{interaction.channel.id}'")

    embed = interaction.message.embeds[0]  # Get the first embed
    embed.add_field(name="Sender", value=interaction.user.mention, inline=False)
    button.disabled = True
    await interaction.response.edit_message(view=self)
    await interaction.message.edit(view=self)
    await interaction.message.edit(embed=embed)

    i = cur.fetchall()[0] 
    
    if i["sender"] is not None and i["receiver"] is not None:
      await interaction.message.delete()
      agree_em = discord.Embed(description=f"Before you **continue** please **agree** to the following\n> - If the Bitcoin gets **chargedback** we are not liable\n> - Anything that happens **after** the trade does not concern us", color=discord.Color.red())
      agree_em.set_thumbnail(url="https://cdn.discordapp.com/emojis/1143623147619373197.webp?size=240&quality=lossless")
      con,cur = openCON()
      cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{interaction.channel.id}'")
      i = cur.fetchall()[0]    
      user1 = i["ticket_author"]
      user2 = i["user_added"]
      agree_view = Agree2(user1, user2)
      await interaction.channel.send(embed=agree_em, view=agree_view) 

    
class Paste(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None) 
  @discord.ui.button(row=0, label='Paste', style=discord.ButtonStyle.grey, custom_id="Paste", disabled=False)
  async def button_callback15(self, button, interaction):
      await interaction.response.defer()

      embed = interaction.message.embeds[0]     
      amount = embed.fields[0].value
      btc = embed.fields[1].value
      address = embed.fields[2].value

      await interaction.channel.send(amount)
      await interaction.channel.send(btc)
      await interaction.channel.send(address)




class Continue_After_Payment(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @discord.ui.button(row=0, label='Confirm', style=discord.ButtonStyle.green, custom_id="confirm_after", disabled=False)
  async def button_callback12(self, button, interaction):
    await interaction.response.defer()
    con,cur = openCON()
    cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{interaction.channel.id}'")
    i = cur.fetchall()[0]
    sender = i['sender']
    receiver = i["receiver"]
    conf_msg = i["conf_message"]

    message = await interaction.channel.fetch_message(conf_msg)

    user = interaction.guild.get_member(int(receiver))

    if interaction.user.id == sender:
      await message.delete()
      await interaction.message.delete()
      adress_em = discord.Embed(description=f"Please provide your **Bitcoin address** below, so that the money can be **transacted** to you.", color=nocolor)
      a = await interaction.channel.send(f"<@{receiver}>", embed=adress_em)
      def check_message(m):
        return m.author == user and m.channel == interaction.channel   
      
      while True:
          reply = await interaction.client.wait_for("message", check=check_message)
          address = reply.content

          con,cur = openCON()
          cur.execute(f"UPDATE auto_btc SET receiver_address='{address}' WHERE channel_ID='{interaction.channel.id}'")      
          con.commit()


          add_embed = discord.Embed(title="Correct Address?", description=f"If this address is **incorrect**, and you click 'Confirm', we will **__NOT__** refund you.", color=discord.Color.red())
          add_embed.add_field(name="Provided Address", value=f"`{address}`")
          await a.delete()
          await reply.delete()
          await interaction.channel.send(f"<@{receiver}>", embed=add_embed, view=ConfirmAddress())
          break
  @discord.ui.button(row=0, label='Cancel', style=discord.ButtonStyle.red, custom_id="cancel_after", disabled=False)
  async def button_callback21(self, button, interaction):
    await interaction.response.defer()

    con,cur = openCON()
    cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{interaction.channel.id}'")
    i = cur.fetchall()[0]
    sender = i['sender']
    receiver = i["receiver"]

    if interaction.user.id == sender:
       await interaction.message.delete()




class ConfirmView(discord.ui.View):
  def __init__(self, user1_id2, user2_id2):
    super().__init__(timeout=None) 
    self.user1_id = user1_id2
    self.user2_id = user2_id2
    self.user1_has_agreed = False
    self.user2_has_agreed = False
    self.message_references = []    
  @discord.ui.button(row=0, label='Confirm', style=discord.ButtonStyle.green, custom_id="confirm", disabled=False)
  async def button_callback13(self, button, interaction):     
    await interaction.response.defer()
    con,cur = openCON()
    cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{interaction.channel.id}'")
    i = cur.fetchall()[0]
    sender = i['sender']
    receiver = i["receiver"]

    if interaction.user.id == sender:
      conf_embed = discord.Embed(title="Before you Continue", description=f"By **clicking** 'Confirm':\n> - You have received the **agreed** items\n> - You **allow** <@{receiver}> to **receive** the money", color=discord.Color.red())
      conf_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1143623147619373197.webp?size=240&quality=lossless")
      await interaction.followup.send(f"<@{sender}>", embed=conf_embed, view=Continue_After_Payment())

  @discord.ui.button(row=0, label='Cancel', style=discord.ButtonStyle.red, custom_id="cancelticket", disabled=False)
  async def button_callback828(self, button, interaction):
    em = discord.Embed(description=f"{interaction.user.mention} has **reacted** to 'Cancel'", color=discord.Color.red())
    await interaction.response.send_message(embed=em)
    msg = await interaction.original_response()
    self.message_references.append(msg)
    if interaction.user.id == self.user1_id:
      self.user1_has_agreed = True
    elif interaction.user.id == self.user2_id:
      self.user2_has_agreed = True

    if self.user1_has_agreed and self.user2_has_agreed:
      await interaction.message.delete()
      for message_reference in self.message_references:
        await message_reference.delete()

      con,cur = openCON()
      cur.execute(f"SELECT * FROM auto_btc WHERE ticket_author = '{interaction.user.id}'")
      i = cur.fetchall()[0] 
      
      sender = i["sender"]
      receiver = i["receiver"]

      sure_em = discord.Embed(description=f"Are you **sure** you would like to **cancel** this deal?", color=discord.Color.red())
      sure_em.set_thumbnail(url="https://cdn.discordapp.com/emojis/1143623147619373197.webp?size=240&quality=lossless")

      user1 = i["ticket_author"]
      user2 = i["user_added"]
      cancel_ticket = Confirm_Cancel_Ticket(user1, user2)

      await interaction.channel.send(f"<@{sender}>, <@{receiver}>", embed=sure_em, view=cancel_ticket)


class ConfirmAddress(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None) 
  @discord.ui.button(row=0, label='Confirm', style=discord.ButtonStyle.green, custom_id="confirm_address", disabled=False)
  async def button_callback14(self, button, interaction):
    await interaction.response.defer()

    for child in self.children:
      child.disabled = True
    await interaction.message.edit(view=self)

    con,cur = openCON()
    cur.execute(f"SELECT * FROM auto_btc WHERE channel_ID = '{interaction.channel.id}'")
    i = cur.fetchall()[0]
    sender = i['sender']
    receiver = i["receiver"]
    addy = i["receiver_address"]
    wif2 = i['crypto_wif']
    key = PrivateKey(i['crypto_wif'])
    trans = key.get_transactions()[0]
    btc_bal = float(key.get_balance(currency='btc'))
    usd_bal = key.get_balance(currency='usd')

    if interaction.user.id == receiver:
      await interaction.message.delete()
      sending_em = discord.Embed(description=f"<a:Discord_Loading:1066670467424976967> **Processing** transaction", color=nocolor)
      a = await interaction.channel.send(embed=sending_em)

      send_to_this_addr = addy
      key = PrivateKey(i['crypto_wif'])
      key.send([], leftover=send_to_this_addr, fee=recommended_fee)

      suc_embed = discord.Embed(title="Payment Successful", description="The payment has been **successfully** sent", color=discord.Color.green())
      suc_embed.add_field(name="Address", value=f"`{addy}`", inline=False)
      suc_embed.add_field(name="Transaction ID", value=f"[View your transaction](https://mempool.space/tx/{trans})", inline=False)
      suc_embed.add_field(name="Amount", value=f"{btc_bal} (**{usd_bal}** USD)", inline=False)
      await a.delete()
      await interaction.channel.send(f"<@{receiver}>", embed=suc_embed)
  @discord.ui.button(row=0, label='Incorrect Address', style=discord.ButtonStyle.red, custom_id="incorrect_address", disabled=False)
  async def button_callback20(self, button, interaction):
     await interaction.response.defer()
     await interaction.message.delete()


@bot.command()
async def d(ctx):
  await ctx.channel.delete()


@bot.event
async def on_guild_channel_delete(channel):
  if (channel.category.id == CAT_ID):
    con,cur = openCON()
    cur.execute(f"DELETE FROM auto_btc WHERE channel_ID='{channel.id}'")
    con.commit()
    closeCON(cur,con)

bot.run(TOKEN)
