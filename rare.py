import telegram
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from telegram.error import BadRequest
import requests
import json
import os
import asyncio
from datetime import datetime, timedelta
import pytz
import html

# Fix for Termux/existing event loop issues
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

# --- Configuration ---
BOT_TOKEN = "8437057536:AAEpTc5dwfoimGI3S4odqqGpiSo7G3QH6Kg"
API_BASE_URL = "http://fi5.bot-hosting.net:22684/like?uid={uid}&server_name={region}&key=STAR"
VISIT_API_BASE_URL = "https://kkkkkkkkkt.vercel.app"
DATA_FILE = "bot_data.json"
OWNER_IDS = [7913042391, 7913042391]

# India timezone
INDIA_TZ = pytz.timezone('Asia/Kolkata')
SCHEDULED_HOUR = 5
SCHEDULED_MINUTE = 0

print("=" * 50)
print("🤖 BOT STARTING WITH EMOJIS...")
print("=" * 50)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "users": {},
        "total_likes": {},
        "total_visits": {},
        "custom_message": "",
        "auto_like_users": {},
        "auto_visit_users": {},
        "allowed_groups": []
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def is_owner(user_id):
    return user_id in OWNER_IDS

def get_next_run_time():
    now = datetime.now(INDIA_TZ)
    next_run = now.replace(hour=SCHEDULED_HOUR, minute=SCHEDULED_MINUTE, second=0, microsecond=0)
    if now >= next_run:
        next_run += timedelta(days=1)
    return next_run

# --- START COMMAND WITH EMOJIS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        user_name = user.first_name
        user_id = user.id
        
        print(f"✅ Start command from {user_name} (ID: {user_id})")
        
        welcome_msg = (
            f"🌟✨ <b>Welcome, {html.escape(user_name)}!</b> ✨🌟\n\n"
            "─────────────────────\n\n"
            "🤖 <b>Auto-Like &amp; Auto-Visit Bot</b>\n\n"
            "🔴 <b>You Need To Purchase AutoLike!</b>\n\n"
            "💎────────────────────💎\n"
            "      <b>PRICING PLANS</b>\n"
            "💎────────────────────💎\n\n"
            "⚡ Rs.30  = 07 Days (1 UID)\n"
            "⚡ Rs.60  = 15 Days (1 UID)\n"
            "⚡ Rs.120 = 30 Days (1 UID)\n"
            "⚡ Rs.240 = 60 Days (1 UID)\n"
            "⚡ Rs.360 = 90 Days (1 UID)\n"
            "⚡ Rs.480 = 120 Days (1 UID)\n\n"
            "📱────────────────────📱\n"
            "      <b>CONTACT US</b>\n"
            "📱────────────────────📱\n\n"
            "👨‍💻 <b>Developer:</b> @PIXINGOFF\n"
            "💬 <b>Channel:</b> @STAR_METHODE\n\n"
            "─────────────────────\n\n"
            "✅ <b>Bot Features:</b>\n"
            "🔄 → Automatic Likes Every Day\n"
            "👀 → Automatic Visits Every Day\n"
            "📊 → Real-Time Statistics\n"
            f"⏰ → Scheduled At {SCHEDULED_HOUR:02d}:{SCHEDULED_MINUTE:02d} AM IST\n\n"
            "📌 <b>Quick Commands:</b>\n"
            "🆘 /help = Show All Commands\n"
            "📋 /status = Bot Status (Admin)\n\n"
            "─────────────────────\n"
            "⚡ <i>Powered By @PIXINGOFF</i> ⚡"
        )
        
        await update.message.reply_text(welcome_msg, parse_mode='HTML')
        print(f"✅ Welcome message sent to {user_name}")
        
    except Exception as e:
        print(f"❌ Error in start: {e}")
        try:
            await update.message.reply_text("Welcome! Bot is working ✅")
        except Exception:
            pass

# --- HELP COMMAND WITH EMOJIS ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_name = html.escape(update.effective_user.first_name)
        
        help_text = (
            f"📚✨ <b>Help Menu - {user_name}</b> ✨📚\n"
            "─────────────────────\n\n"
            "👑────────────────────👑\n"
            "   <b>ADMIN COMMANDS</b>\n"
            "👑────────────────────👑\n\n"
            "💫 /autolike UID REGION DAYS\n"
            "   → Setup Auto Likes 🔄\n\n"
            "💫 /autovisit UID REGION DAYS\n"
            "   → Setup Auto Visits 👀\n\n"
            "👍 /like UID REGION\n"
            "   → Send Single Like ⚡\n\n"
            "👤 /visit UID REGION\n"
            "   → Send Single Visit 🌐\n\n"
            "📊 /status\n"
            "   → Bot Status 📈\n\n"
            "✏️ /setmessage TEXT\n"
            "   → Set Custom Message 💬\n\n"
            "👥 /setgroup GROUP_ID\n"
            "   → Add Group 📢\n\n"
            "─────────────────────\n\n"
            "👤────────────────────👤\n"
            "   <b>USER COMMANDS</b>\n"
            "👤────────────────────👤\n\n"
            "📈 /mylike\n"
            "   → Your Like Stats 👍\n\n"
            "📊 /myvisit\n"
            "   → Your Visit Stats 👀\n\n"
            "─────────────────────\n\n"
            "📝 <b>Examples:</b>\n"
            "🔹 /autolike 1234567890 IND 30\n"
            "🔹 /autovisit 1234567890 IND 30\n\n"
            "💎────────────────────💎\n"
            "  <b>BUY AUTOLIKE</b>\n"
            "💎────────────────────💎\n"
            "👨‍💻 <b>Contact:</b> @PIXINGOFF\n\n"
            f"⏰ <b>Daily At:</b> {SCHEDULED_HOUR:02d}:{SCHEDULED_MINUTE:02d} AM IST\n"
            "─────────────────────\n"
            "⚡ <i>Powered By @PIXINGOFF</i> ⚡"
        )
        
        await update.message.reply_text(help_text, parse_mode='HTML')
        print(f"✅ Help sent to {user_name}")
        
    except Exception as e:
        print(f"❌ Help error: {e}")
        try:
            await update.message.reply_text("Help menu - Use /start to begin")
        except Exception:
            pass

# --- AUTO LIKE WITH EMOJIS ---
async def autolike(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_owner(user_id):
        await update.message.reply_text(
            "⛔────────────────────⛔\n"
            "    <b>ACCESS DENIED</b>\n"
            "⛔────────────────────⛔\n\n"
            "💎 <b>You Need To Purchase AutoLike!</b>\n\n"
            "👨‍💻 <b>Contact:</b> @PIXINGOFF",
            parse_mode='HTML'
        )
        return
    
    if len(context.args) != 3:
        await update.message.reply_text(
            "❌ <b>Invalid Format!</b>\n\n"
            "📌 <b>Usage:</b> /autolike UID REGION DAYS\n"
            "📝 <b>Example:</b> /autolike 1234567890 IND 30",
            parse_mode='HTML'
        )
        return
    
    uid = context.args[0]
    region = context.args[1]
    
    try:
        days = int(context.args[2])
    except ValueError:
        await update.message.reply_text("❌ <b>Days Must Be A Number!</b>", parse_mode='HTML')
        return
    
    loading = await update.message.reply_text("⏳ <b>Setting up Auto-Like...</b>", parse_mode='HTML')
    
    try:
        data = load_data()
        user_name = update.effective_user.full_name or str(user_id)
        
        if "auto_like_users" not in data:
            data["auto_like_users"] = {}
        
        data["auto_like_users"][str(user_id)] = {
            "uid": uid,
            "region": region,
            "total_days": days,
            "runs_completed": 0,
            "start_date": datetime.now(INDIA_TZ).isoformat(),
            "chat_id": update.effective_chat.id,
            "user_name": user_name,
            "last_run": datetime.now(INDIA_TZ).isoformat()
        }
        
        if "allowed_groups" not in data:
            data["allowed_groups"] = []
        if update.effective_chat.id not in data["allowed_groups"]:
            data["allowed_groups"].append(update.effective_chat.id)
        
        save_data(data)
        
        try:
            await loading.delete()
        except Exception:
            pass
        
        # Send like request
        api_url = f"{API_BASE_URL}/like?uid={uid}&server_name={region}"
        
        try:
            response = requests.get(api_url, timeout=30)
            api_data = response.json()
            
            result_msg = (
                "─────────────────────\n"
                "   🎮 <b>AUTO-LIKE RESULTS</b> 🎮\n"
                "─────────────────────\n\n"
                f"👤 <b>Nickname:</b> {api_data.get('PlayerNickname', 'N/A')}\n"
                f"🆔 <b>UID:</b> {api_data.get('UID', 'N/A')}\n"
                f"📉 <b>Before:</b> {api_data.get('LikesbeforeCommand', 'N/A')}\n"
                f"📈 <b>After:</b> {api_data.get('LikesafterCommand', 'N/A')}\n"
                f"👍 <b>Likes Given:</b> {api_data.get('LikesGivenByAPI', 'N/A')}\n"
                f"👑 <b>User:</b> {html.escape(user_name)}\n"
                "─────────────────────\n"
                "⚡ <i>Powered By @PIXINGOFF</i> ⚡"
            )
            
            await update.message.reply_text(result_msg, parse_mode='HTML')
            
        except Exception as e:
            await update.message.reply_text(f"❌ API Error: {str(e)}")
        
        next_run = get_next_run_time().strftime('%Y-%m-%d %H:%M:%S')
        await update.message.reply_text(
            f"✅ <b>Auto-Like Activated!</b>\n\n"
            f"👤 User: {html.escape(user_name)}\n"
            f"🆔 UID: {uid}\n"
            f"🌍 Region: {region}\n"
            f"📅 Days: {days}\n\n"
            f"⏰ Next Run: {next_run} IST",
            parse_mode='HTML'
        )
        
    except Exception as e:
        try:
            await loading.edit_text(f"❌ Error: {str(e)}")
        except BadRequest:
            pass
        except Exception:
            pass

# --- AUTO VISIT WITH EMOJIS ---
async def autovisit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_owner(user_id):
        await update.message.reply_text(
            "⛔────────────────────⛔\n"
            "    <b>ACCESS DENIED</b>\n"
            "⛔────────────────────⛔\n\n"
            "💎 <b>You Need To Purchase AutoLike!</b>\n\n"
            "👨‍💻 <b>Contact:</b> @PIXINGOFF",
            parse_mode='HTML'
        )
        return
    
    if len(context.args) != 3:
        await update.message.reply_text(
            "❌ <b>Invalid Format!</b>\n\n"
            "📌 <b>Usage:</b> /autovisit UID REGION DAYS\n"
            "📝 <b>Example:</b> /autovisit 1234567890 IND 30",
            parse_mode='HTML'
        )
        return
    
    uid = context.args[0]
    region = context.args[1]
    
    try:
        days = int(context.args[2])
    except ValueError:
        await update.message.reply_text("❌ <b>Days Must Be A Number!</b>", parse_mode='HTML')
        return
    
    loading = await update.message.reply_text("⏳ <b>Setting up Auto-Visit...</b>", parse_mode='HTML')
    
    try:
        data = load_data()
        user_name = update.effective_user.full_name or str(user_id)
        
        if "auto_visit_users" not in data:
            data["auto_visit_users"] = {}
        
        data["auto_visit_users"][str(user_id)] = {
            "uid": uid,
            "region": region,
            "total_days": days,
            "runs_completed": 0,
            "start_date": datetime.now(INDIA_TZ).isoformat(),
            "chat_id": update.effective_chat.id,
            "user_name": user_name,
            "last_run": datetime.now(INDIA_TZ).isoformat()
        }
        
        if "allowed_groups" not in data:
            data["allowed_groups"] = []
        if update.effective_chat.id not in data["allowed_groups"]:
            data["allowed_groups"].append(update.effective_chat.id)
        
        save_data(data)
        
        try:
            await loading.delete()
        except Exception:
            pass
        
        # Send visit request
        api_url = f"{VISIT_API_BASE_URL}/{region}/{uid}"
        
        try:
            response = requests.get(api_url, timeout=90)
            api_data = response.json()
            
            result_msg = (
                "─────────────────────\n"
                "   👤 <b>AUTO-VISIT RESULTS</b> 👤\n"
                "─────────────────────\n\n"
                f"🎮 <b>Nickname:</b> {api_data.get('nickname', 'N/A')}\n"
                f"🆔 <b>UID:</b> {api_data.get('uid', 'N/A')}\n"
                f"📊 <b>Level:</b> {api_data.get('level', 'N/A')}\n"
                f"🌍 <b>Region:</b> {api_data.get('region', 'N/A')}\n"
                f"✅ <b>Success:</b> {api_data.get('success', 'N/A')}\n"
                f"👑 <b>User:</b> {html.escape(user_name)}\n"
                "─────────────────────\n"
                "⚡ <i>Powered By @PIXINGOFF</i> ⚡"
            )
            
            await update.message.reply_text(result_msg, parse_mode='HTML')
            
        except Exception as e:
            await update.message.reply_text(f"❌ API Error: {str(e)}")
        
        next_run = get_next_run_time().strftime('%Y-%m-%d %H:%M:%S')
        await update.message.reply_text(
            f"✅ <b>Auto-Visit Activated!</b>\n\n"
            f"👤 User: {html.escape(user_name)}\n"
            f"🆔 UID: {uid}\n"
            f"🌍 Region: {region}\n"
            f"📅 Days: {days}\n\n"
            f"⏰ Next Run: {next_run} IST",
            parse_mode='HTML'
        )
        
    except Exception as e:
        try:
            await loading.edit_text(f"❌ Error: {str(e)}")
        except BadRequest:
            pass
        except Exception:
            pass

# --- LIKE COMMAND WITH EMOJIS ---
async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ <b>Access Denied!</b>", parse_mode='HTML')
        return
    
    if len(context.args) != 2:
        await update.message.reply_text(
            "📌 <b>Usage:</b> /like UID REGION\n"
            "📝 <b>Example:</b> /like 1234567890 IND",
            parse_mode='HTML'
        )
        return
    
    uid = context.args[0]
    region = context.args[1]
    
    loading = await update.message.reply_text("⏳ <b>Processing Like...</b>", parse_mode='HTML')
    
    try:
        api_url = f"{API_BASE_URL}/like?uid={uid}&server_name={region}"
        response = requests.get(api_url, timeout=30)
        api_data = response.json()
        
        result_msg = (
            "─────────────────────\n"
            "   👍 <b>LIKE RESULTS</b> 👍\n"
            "─────────────────────\n\n"
            f"👤 <b>Nickname:</b> {api_data.get('PlayerNickname', 'N/A')}\n"
            f"🆔 <b>UID:</b> {api_data.get('UID', 'N/A')}\n"
            f"📉 <b>Before:</b> {api_data.get('LikesbeforeCommand', 'N/A')}\n"
            f"📈 <b>After:</b> {api_data.get('LikesafterCommand', 'N/A')}\n"
            f"👍 <b>Likes:</b> {api_data.get('LikesGivenByAPI', 'N/A')}\n"
            "─────────────────────\n"
            "⚡ <i>Powered By @PIXINGOFF</i> ⚡"
        )
        
        try:
            await loading.delete()
        except Exception:
            pass
        await update.message.reply_text(result_msg, parse_mode='HTML')
        
    except Exception as e:
        try:
            await loading.edit_text(f"❌ Error: {str(e)}")
        except BadRequest:
            pass
        except Exception:
            pass

# --- VISIT COMMAND WITH EMOJIS ---
async def visit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ <b>Access Denied!</b>", parse_mode='HTML')
        return
    
    if len(context.args) != 2:
        await update.message.reply_text(
            "📌 <b>Usage:</b> /visit UID REGION\n"
            "📝 <b>Example:</b> /visit 1234567890 IND",
            parse_mode='HTML'
        )
        return
    
    uid = context.args[0]
    region = context.args[1]
    
    loading = await update.message.reply_text("⏳ <b>Processing Visit...</b>", parse_mode='HTML')
    
    try:
        api_url = f"{VISIT_API_BASE_URL}/{region}/{uid}"
        response = requests.get(api_url, timeout=30)
        api_data = response.json()
        
        result_msg = (
            "─────────────────────\n"
            "   👤 <b>VISIT RESULTS</b> 👤\n"
            "─────────────────────\n\n"
            f"🎮 <b>Nickname:</b> {api_data.get('nickname', 'N/A')}\n"
            f"🆔 <b>UID:</b> {api_data.get('uid', 'N/A')}\n"
            f"📊 <b>Level:</b> {api_data.get('level', 'N/A')}\n"
            f"🌍 <b>Region:</b> {api_data.get('region', 'N/A')}\n"
            f"✅ <b>Success:</b> {api_data.get('success', 'N/A')}\n"
            "─────────────────────\n"
            "⚡ <i>Powered By @PIXINGOFF</i> ⚡"
        )
        
        try:
            await loading.delete()
        except Exception:
            pass
        await update.message.reply_text(result_msg, parse_mode='HTML')
        
    except Exception as e:
        try:
            await loading.edit_text(f"❌ Error: {str(e)}")
        except BadRequest:
            pass
        except Exception:
            pass

# --- STATUS COMMAND WITH EMOJIS ---
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ <b>Access Denied!</b>", parse_mode='HTML')
        return
    
    data = load_data()
    
    like_users = data.get("auto_like_users", {})
    visit_users = data.get("auto_visit_users", {})
    groups = data.get("allowed_groups", [])
    
    status_msg = (
        "─────────────────────\n"
        "   📊 <b>BOT STATUS DASHBOARD</b> 📊\n"
        "─────────────────────\n\n"
        f"👑 <b>Total Admins:</b> {len(OWNER_IDS)}\n\n"
        f"👍 <b>Auto-Like Users:</b> {len(like_users)}\n"
        f"👀 <b>Auto-Visit Users:</b> {len(visit_users)}\n"
        f"🏢 <b>Total Groups:</b> {len(groups)}\n\n"
        f"⏰ <b>Next Run:</b> {get_next_run_time().strftime('%Y-%m-%d %H:%M:%S')} IST\n"
        "─────────────────────\n"
        "⚡ <i>Powered By @PIXINGOFF</i> ⚡"
    )
    
    await update.message.reply_text(status_msg, parse_mode='HTML')

# --- MYLIKE COMMAND ---
async def mylike(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id = str(update.effective_user.id)
    user_name = html.escape(update.effective_user.first_name)
    stats = data.get("total_likes", {}).get(user_id)
    
    if stats:
        msg = (
            f"─────────────────────\n"
            f"   📈 <b>{user_name}'s Like Stats</b> 📈\n"
            "─────────────────────\n\n"
            f"👍 <b>Total Likes:</b> {stats.get('count', 0)}\n"
            f"📅 <b>Total Days:</b> {stats.get('days', 0)}\n"
            "─────────────────────"
        )
        await update.message.reply_text(msg, parse_mode='HTML')
    else:
        await update.message.reply_text(f"ℹ️ <b>{user_name}, No like stats found!</b>", parse_mode='HTML')

# --- MYVISIT COMMAND ---
async def myvisit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user_id = str(update.effective_user.id)
    user_name = html.escape(update.effective_user.first_name)
    stats = data.get("total_visits", {}).get(user_id)
    
    if stats:
        msg = (
            f"─────────────────────\n"
            f"   📊 <b>{user_name}'s Visit Stats</b> 📊\n"
            "─────────────────────\n\n"
            f"👀 <b>Total Visits:</b> {stats.get('count', 0)}\n"
            f"📅 <b>Total Days:</b> {stats.get('days', 0)}\n"
            "─────────────────────"
        )
        await update.message.reply_text(msg, parse_mode='HTML')
    else:
        await update.message.reply_text(f"ℹ️ <b>{user_name}, No visit stats found!</b>", parse_mode='HTML')

# --- SETGROUP COMMAND ---
async def setgroup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ <b>Access Denied!</b>", parse_mode='HTML')
        return
    
    if not context.args:
        await update.message.reply_text(
            "📌 <b>Usage:</b> /setgroup GROUP_ID\n"
            "📝 <b>Example:</b> /setgroup -1001234567890",
            parse_mode='HTML'
        )
        return
    
    try:
        group_id = int(context.args[0])
        data = load_data()
        
        if "allowed_groups" not in data:
            data["allowed_groups"] = []
        
        if group_id not in data["allowed_groups"]:
            data["allowed_groups"].append(group_id)
            save_data(data)
            await update.message.reply_text(
                f"✅ <b>Group Added Successfully!</b>\n\n"
                f"🏢 <b>Group ID:</b> {group_id}",
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text("⚠️ <b>This Group Already Exists!</b>", parse_mode='HTML')
            
    except ValueError:
        await update.message.reply_text("❌ <b>Invalid Group ID!</b>", parse_mode='HTML')

# --- SETMESSAGE COMMAND ---
async def setmessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("⛔ <b>Access Denied!</b>", parse_mode='HTML')
        return
    
    if not context.args:
        await update.message.reply_text("📌 <b>Usage:</b> /setmessage YOUR_MESSAGE", parse_mode='HTML')
        return
    
    msg = ' '.join(context.args)
    data = load_data()
    data["custom_message"] = msg
    save_data(data)
    
    await update.message.reply_text(
        f"✅ <b>Custom Message Set!</b>\n\n"
        f"💬 {html.escape(msg)}",
        parse_mode='HTML'
    )

# --- SCHEDULED TASK ---
async def scheduled_worker(bot):
    while True:
        try:
            now = datetime.now(INDIA_TZ)
            next_run = get_next_run_time()
            sleep_seconds = max(1, (next_run - now).total_seconds())
            
            print(f"⏰ Next run at: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            await asyncio.sleep(sleep_seconds)
            
            print(f"🚀 Running daily tasks at {datetime.now(INDIA_TZ).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Auto Like
            data = load_data()
            all_groups = data.get("allowed_groups", [])
            like_users = data.get("auto_like_users", {})
            
            for user_id, config in list(like_users.items()):
                try:
                    remaining = config['total_days'] - config.get('runs_completed', 0)
                    if remaining <= 0:
                        del data["auto_like_users"][user_id]
                        save_data(data)
                        continue
                    
                    config['runs_completed'] = config.get('runs_completed', 0) + 1
                    config['last_run'] = datetime.now(INDIA_TZ).isoformat()
                    save_data(data)
                    
                    api_url = f"{API_BASE_URL}/like?uid={config['uid']}&server_name={config['region']}"
                    response = requests.get(api_url, timeout=30)
                    api_data = response.json()
                    
                    remaining = config['total_days'] - config.get('runs_completed', 0)
                    msg = (
                        "─────────────────────\n"
                        "   🎮 <b>AUTO-LIKE RESULTS</b> 🎮\n"
                        "─────────────────────\n\n"
                        f"👤 <b>Nickname:</b> {api_data.get('PlayerNickname', 'N/A')}\n"
                        f"🆔 <b>UID:</b> {api_data.get('UID', 'N/A')}\n"
                        f"📉 <b>Before:</b> {api_data.get('LikesbeforeCommand', 'N/A')}\n"
                        f"📈 <b>After:</b> {api_data.get('LikesafterCommand', 'N/A')}\n"
                        f"👍 <b>Likes:</b> {api_data.get('LikesGivenByAPI', 'N/A')}\n"
                        f"📅 <b>Days Left:</b> {remaining}/{config['total_days']}\n"
                        f"👑 <b>User:</b> {config.get('user_name', 'Unknown')}\n"
                        "─────────────────────\n"
                        "⚡ <i>Powered By @PIXINGOFF</i> ⚡"
                    )
                    
                    # Send to user
                    try:
                        await bot.send_message(chat_id=config['chat_id'], text=msg, parse_mode='HTML')
                    except Exception:
                        pass
                    
                    # Send to groups
                    for gid in all_groups:
                        try:
                            await bot.send_message(chat_id=gid, text=msg, parse_mode='HTML')
                        except Exception:
                            pass
                    
                    print(f"✅ Like done for {config.get('user_name', 'Unknown')}")
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    print(f"❌ Like error: {e}")
            
            # Auto Visit
            data = load_data()
            visit_users = data.get("auto_visit_users", {})
            
            for user_id, config in list(visit_users.items()):
                try:
                    remaining = config['total_days'] - config.get('runs_completed', 0)
                    if remaining <= 0:
                        del data["auto_visit_users"][user_id]
                        save_data(data)
                        continue
                    
                    config['runs_completed'] = config.get('runs_completed', 0) + 1
                    config['last_run'] = datetime.now(INDIA_TZ).isoformat()
                    save_data(data)
                    
                    api_url = f"{VISIT_API_BASE_URL}/{config['region']}/{config['uid']}"
                    response = requests.get(api_url, timeout=90)
                    api_data = response.json()
                    
                    remaining = config['total_days'] - config.get('runs_completed', 0)
                    msg = (
                        "─────────────────────\n"
                        "   👤 <b>AUTO-VISIT RESULTS</b> 👤\n"
                        "─────────────────────\n\n"
                        f"🎮 <b>Nickname:</b> {api_data.get('nickname', 'N/A')}\n"
                        f"🆔 <b>UID:</b> {api_data.get('uid', 'N/A')}\n"
                        f"📊 <b>Level:</b> {api_data.get('level', 'N/A')}\n"
                        f"🌍 <b>Region:</b> {api_data.get('region', 'N/A')}\n"
                        f"✅ <b>Success:</b> {api_data.get('success', 'N/A')}\n"
                        f"📅 <b>Days Left:</b> {remaining}/{config['total_days']}\n"
                        f"👑 <b>User:</b> {config.get('user_name', 'Unknown')}\n"
                        "─────────────────────\n"
                        "⚡ <i>Powered By @PIXINGOFF</i> ⚡"
                    )
                    
                    # Send to user
                    try:
                        await bot.send_message(chat_id=config['chat_id'], text=msg, parse_mode='HTML')
                    except Exception:
                        pass
                    
                    # Send to groups
                    for gid in all_groups:
                        try:
                            await bot.send_message(chat_id=gid, text=msg, parse_mode='HTML')
                        except Exception:
                            pass
                    
                    print(f"✅ Visit done for {config.get('user_name', 'Unknown')}")
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    print(f"❌ Visit error: {e}")
            
            print(f"✅ Daily tasks completed at {datetime.now(INDIA_TZ).strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"❌ Scheduler error: {e}")
            await asyncio.sleep(60)

# --- POST INIT ---
async def post_init(application: Application):
    print("✨ Bot initialized, starting scheduler...")
    asyncio.create_task(scheduled_worker(application.bot))

# --- MAIN ---
def main():
    print("\n" + "=" * 50)
    print("🌟 BOT IS RUNNING WITH EMOJIS 🌟")
    print("=" * 50)
    print(f"👑 Admins: {OWNER_IDS}")
    print(f"⏰ Schedule: {SCHEDULED_HOUR:02d}:{SCHEDULED_MINUTE:02d} AM IST")
    print("=" * 50 + "\n")
    
    try:
        # Create application
        application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("autolike", autolike))
        application.add_handler(CommandHandler("autovisit", autovisit))
        application.add_handler(CommandHandler("like", like))
        application.add_handler(CommandHandler("visit", visit))
        application.add_handler(CommandHandler("status", status))
        application.add_handler(CommandHandler("mylike", mylike))
        application.add_handler(CommandHandler("myvisit", myvisit))
        application.add_handler(CommandHandler("setgroup", setgroup))
        application.add_handler(CommandHandler("setmessage", setmessage))
        
        # Start bot
        print("✅ Bot configured, starting polling...\n")
        application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()