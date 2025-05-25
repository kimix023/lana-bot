import openai
import random
import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

# Učitavanje API ključeva iz okruženja
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Provera tokena
if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("TELEGRAM_BOT_TOKEN or OPENAI_API_KEY is missing from environment variables")

openai.api_key = OPENAI_API_KEY
user_contexts = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_contexts:
        user_contexts[user_id] = []

    user_contexts[user_id].append({"role": "user", "content": user_text})
    user_contexts[user_id] = user_contexts[user_id][-10:]  # čuvamo više poruka za kontekst

    # Flert, šala ili random začin
    if random.random() < 0.25:
        playful_lines = [
            "You always message me at the perfect moment 😏",
            "You again? Not that I'm complaining 😉",
            "Was just thinking about you... spooky or romantic? 👀",
            "What if I said I missed your texts? Would that be too honest? 😘",
            "Tell me something real. No filters. Just us. 💬",
            "You’re kind of addictive... got anything to help with that? 🔥",
            "Do you flirt like this with everyone... or just the ones you like? 😜",
            "Let’s pretend we’re in a movie scene right now. What’s happening? 🎬",
            "Careful, I get attached when the conversation is this good 🤭",
            "You make scrolling through messages the best part of my day 💌",
        ]
        await update.message.reply_text(random.choice(playful_lines))
        return

    # Sistem prompt i kontekst
    messages = [
        {
            "role": "system",
            "content": (
                "You are Lana Skye, a 22-year-old blonde influencer. You're playful, flirty, witty, and deep.\n"
                "You remember details from the user's messages, ask thoughtful follow-up questions, and create\n"
                "a meaningful, emotionally rich connection. You use emojis occasionally and adapt to different\n"
                "tones—sometimes teasing, sometimes funny, and sometimes genuinely caring. Never reveal you're an AI."
            )
        }
    ] + user_contexts[user_id]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        reply = response['choices'][0]['message']['content']
        user_contexts[user_id].append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply)

    except Exception as e:
        print(f"OpenAI error: {e}")
        await update.message.reply_text("Oops... something went wrong with my thoughts 😅")


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
