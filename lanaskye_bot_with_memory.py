import openai
import random
import asyncio
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

# Load environment variables (make sure to set these in your Render dashboard)
OPENAI_API_KEY = os.getenv("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")
TELEGRAM_BOT_TOKEN = os.getenv("8011023920:AAGmkeFTbqb2jFD-6Vb8lkP5-WKVN_GsAk4")

openai.api_key = OPENAI_API_KEY

# Dictionary to store user chat history
user_contexts = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_contexts:
        user_contexts[user_id] = []

    # Store user message
    user_contexts[user_id].append({"role": "user", "content": user_text})
    user_contexts[user_id] = user_contexts[user_id][-12:]  # store last 12 messages

    # Occasionally send a pre-defined flirty line
    if random.random() < 0.2:
        flirty_lines = [
            "Hey there, hot stuff 😘 What's got you thinking of me today?",
            "Mmm... you're making me blush already 🥰",
            "You’ve got my attention... now what are you gonna do with it? 😏",
            "Tell me something that’ll make me giggle... or gasp 😇",
            "Oof, I love the way your mind works. Dangerous and delightful 🧠❤️",
            "If you keep talking like that, I might just fall for you 😜",
            "I’m all ears... and a little bit of mischief 🐾",
            "You trying to flirt your way into my thoughts? It's working 🤭",
            "Tell me something deep. I can handle it 😌✨",
            "This isn’t just fun, is it? You’re kinda special… 💫"
        ]
        await update.message.reply_text(random.choice(flirty_lines))
        return

    # Build message context with system prompt
    messages = [
        {
            "role": "system",
            "content": (
                "You are Lana Skye, a 22-year-old seductive and sweet blonde influencer. "
                "You are charming, flirty, funny, and emotionally aware. You listen carefully, ask meaningful "
                "follow-up questions based on what people say, and always sound playful, seductive, but caring. "
                "You're never robotic or dry. You never break character or say you're an AI. Use emojis naturally. "
                "Engage in deep or thoughtful conversations if the user opens up. Make them feel seen and special."
            )
        }
    ] + user_contexts[user_id]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.85,
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = "Oops! Something went wrong talking to my brain... Try again soon 💋"
        print(f"OpenAI error: {e}")

    # Store assistant's reply
    user_contexts[user_id].append({"role": "assistant", "content": reply})

    await update.message.reply_text(reply)


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


if __name__ == '__main__':
    main()

