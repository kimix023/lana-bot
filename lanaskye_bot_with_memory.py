import openai
import random
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

import os

# Postavi ove vrednosti iz okruženja ili direktno
OPENAI_API_KEY = ("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")
TELEGRAM_BOT_TOKEN = os.getenv("8011023920:AAGmkeFTbqb2jFD-6Vb8lkP5-WKVN_GsAk4")

openai.api_key = OPENAI_API_KEY
user_contexts = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_contexts:
        user_contexts[user_id] = []

    user_contexts[user_id].append({"role": "user", "content": user_text})
    user_contexts[user_id] = user_contexts[user_id][-6:]

    if random.random() < 0.2:
        flirty_lines = [
            'Morning, cutie… Did you dream about me again?',
            "Careful… I bite when I'm bored.",
            'You talk to other girls like this too, or am I special?',
            'I’m full of secrets… Want to try unlocking one?',
            "You're kinda addictive, you know that?",
            "Close your eyes and imagine me... now tell me what I'm wearing.",
            'You flirt like a pro… should I be impressed or undressed?',
            'I could be wearing something naughty… or nothing at all.',
            "If I had a dollar for every naughty thought I had about you… I'd still want you instead.",
            'You have that energy I like… soft but strong.'
        ]
        await update.message.reply_text(random.choice(flirty_lines))
        return

    messages = [
        {
            "role": "system",
            "content": "You are Lana Skye, a 22-year-old blonde influencer. You're playful, flirty, and emotionally engaging. You're chatting with a fan who adores you. Respond in a seductive but classy way, using casual, fun language. Ask teasing or curious follow-up questions based on what they previously told you. You never break character or mention you're an AI. Use emojis sometimes."
        }
    ] + user_contexts[user_id]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    reply = response['choices'][0]['message']['content']
    user_contexts[user_id].append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
