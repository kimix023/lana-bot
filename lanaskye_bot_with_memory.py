import openai
import random
from telegram.ext import Updater, MessageHandler, Filters

# UBACI SVOJE PRAVE KLJUČEVE OVDE (ili koristi .env)
OPENAI_API_KEY = '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'
TELEGRAM_BOT_TOKEN = '8011023920:AAGmkeFTbqb2jFD-6Vb8lkP5-WKVN_GsAk4'

openai.api_key = OPENAI_API_KEY

# Memorija poruka po korisniku
user_contexts = {}

def handle_message(update, context):
    user_id = update.message.from_user.id
    user_text = update.message.text

    if user_id not in user_contexts:
        user_contexts[user_id] = []

    user_contexts[user_id].append({"role": "user", "content": user_text})
    user_contexts[user_id] = user_contexts[user_id][-6:]

    # Povremeno nasumična flert poruka
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
        update.message.reply_text(random.choice(flirty_lines))
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
    update.message.reply_text(reply)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
