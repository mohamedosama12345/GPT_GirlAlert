import discord
from discord import Intents
from discord.ext import commands
import asyncio
import aiohttp
from pydub import AudioSegment
from io import BytesIO
import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import socket
import threading

#---------------------------STAY ALIVE------------------------------
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'hello world'

def ping():
    try:
        hello_world()
    except Exception as e:
        print(f'Ping failed: {str(e)}')

scheduler = BackgroundScheduler()
scheduler.add_job(func=ping, trigger='interval', minutes=1)
scheduler.start()

def start_flask_app():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.start()
    

#---------------------------DISCORD------------------------------

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

async def play_sound(voice_client, file_path, duration):
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_channels(2).set_frame_rate(48000)
    byte_data = BytesIO()
    audio.export(byte_data, format="s16le")
    byte_data.seek(0)
    voice_client.stop()
    voice_client.play(discord.PCMVolumeTransformer(
        discord.PCMAudio(byte_data)))
    await asyncio.sleep(duration)
    voice_client.stop()
    await voice_client.disconnect()

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel and after.channel is not None:
        #girl alert
        girl_role = discord.utils.get(member.guild.roles, name="girls")
        if girl_role in member.roles:
            voice_channel = after.channel
            if voice_channel is not None:
                if voice_channel.guild.voice_client is None:
                    voice_client = await voice_channel.connect()
                else:
                    voice_client = voice_channel.guild.voice_client
                await play_sound(voice_client, "audio.mp3", 6)   #play o5taaaaaaaaaaaaah e7zary
                
        #jan alert
        #jan_role = discord.utils.get(member.guild.roles, name="المبرمج الجامد")
        if jan_role in member.roles:
            voice_channel = after.channel
            if voice_channel is not None:
                if voice_channel.guild.voice_client is None:
                    voice_client = await voice_channel.connect()
                else:
                    voice_client = voice_channel.guild.voice_client
                await play_sound(voice_client, "b7b_elbnat.mp3", 6)   #play alo ahmed


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
my_secret = os.environ['TOKEN']
bot.run(my_secret)



