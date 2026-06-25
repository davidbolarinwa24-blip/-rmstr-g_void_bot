import telebot
import requests

# Put your NEW token here after you revoke old one in BotFather
API_TOKEN = '8303316737:AAGptofHkHLlhvx6Q-18WSsx9fyoWVOx-Xs'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔥 **Like Bot Online** 🔥\n\nUsage: `/like [region] [uid]`\nExample: `/like ind 811094988`", parse_mode='Markdown')

@bot.message_handler(commands=['like'])
def handle_like(message):
    args = message.text.split()

    if len(args) < 3:
        bot.reply_to(message, "❌ **Usage:** `/like {region} {uid}`\nExample: `/like ind 5513136279`", parse_mode='Markdown')
        return

    region = args[1].lower()
    uid = args[2]

    sent_msg = bot.reply_to(message, "⏳ *Processing your request...*", parse_mode='Markdown')

    api_url = f"https://najmi-ob53-like-api-vvkb.vercel.app/like?uid={uid}&server_name={region}&key=NJM"

    try:
        response = requests.get(api_url, timeout=15)

        if response.status_code!= 200:
            bot.edit_message_text(f"❌ API Error: {response.status_code}",
                chat_id=message.chat.id, message_id=sent_msg.message_id)
            return

        data = response.json()
        name = data.get('PlayerNickname', 'N/A')
        likes_before = data.get('LikesbeforeCommand', '0')
        likes_given = data.get('LikesGivenByAPI', '0')
        likes_after = data.get('LikesafterCommand', '0')
        remaining = data.get('remains', 'N/A')

        # REMY STYLE GREEN FRAME - copy this exact block
        template = (
            f"┏━━━━━━━━━━━━━━┓\n"
            f"┃ 🎉 LIKE SUCCESSFULLY ┃\n"
            f"┗━━━━━━━━━━━━━━┛\n\n"
            f"👑 Name: {name}\n"
            f"🆔 UID: {uid}\n"
            f"🌍 Region: {region.upper()}\n\n"
            f"❤️ Likes Before: {likes_before}\n"
            f"📤 Likes Given: {likes_given}\n"
            f"💚 Likes After: {likes_after}\n\n"
            f"📊 Remaining Requests: {remaining}\n\n"
            f"┏━━━━━━━━━━━━━━┓\n"
            f"┃ Powered by Bot ┃\n"
            f"┗━━━━━━━━━━━━━━┛"
        )

        bot.edit_message_text(template, chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode='Markdown')

    except Exception as e:
        bot.edit_message_text(f"❌ **Error:** `{str(e)}`",
            chat_id=message.chat.id, message_id=sent_msg.message_id, parse_mode='Markdown')

print("Bot is now online...")
bot.infinity_polling()
