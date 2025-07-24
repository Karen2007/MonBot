import requests
import random
import time
import os
import asyncio
from dotenv import load_dotenv
from serpapi import GoogleSearch
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

assert BOT_TOKEN, "BOT_TOKEN is missing in .env"
assert WEATHER_TOKEN, "WEATHER_TOKEN is missing in .env"
assert OPENROUTER_API_KEY, "OPENROUTER_API_KEY is missing in .env"
assert SERPAPI_KEY, "SERPAPI_KEY is missing in .env"

API_URL = "https://openrouter.ai/api/v1/chat/completions"
start_time = time.time()

INFO_MESSAGE = (
    "This bot was developed as a passion project and named after my girlfriend Mona. "
    "It has various useful features.\nType /help to see all the commands.\nDeveloped by @thekarenhimself"
)

HELP_MESSAGE = (
    "Here are all the commands for MonBot:\n\n"
    "/info - Displays an info message\n"
    "/food - Chooses a random place to eat\n"
    "/weather - Shows the weather in Yerevan\n"
    "/rps - Play rock, paper, scissors\n"
    "/image <text> - Search an image on Google\n"
    "/askdeepseek <text> - Ask DeepSeek anything"
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Started")


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(INFO_MESSAGE)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.date.timestamp() < start_time:
        return
    await update.message.reply_text(HELP_MESSAGE)


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.date.timestamp() < start_time:
        return

    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_TOKEN}&q=Yerevan"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp_c = data["current"]["temp_c"]
        await update.message.reply_text(f"Weather in Yerevan:\nTemperature: {temp_c}°C")
    else:
        await update.message.reply_text("Could not retrieve weather data.")


async def food_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.date.timestamp() < start_time:
        return

    PLACES = [
        "Tumanyan Shawarma", "Mr. Gyros", "Artashi Mot", "Pit Stop", "Abu Hagop", "Yerevanyan Shawarma",
        "Classic Burger", "Black Angus", "Mic Mac", "Master Class", "Tashir Pizza", "Dodo Pizza",
        "Tun Lahmajo", "Ponchikanoc", "Yum‑yum Donuts", "Karas", "KFC", "Made in China", "Lucha Tacos",
        "Shaurmyan", "The Bull", "Bar B.Q.", "Ost", "Lebanon Shawarma", "Qarvansara", "Gourmet 38", "Hot Wings"
    ]
    await update.message.reply_text(f"Esor arji gnal {random.choice(PLACES)}")

async def rock_paper_scissors_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Rock")],
        [KeyboardButton("Paper")],
        [KeyboardButton("Scissors")]
    ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Choose an option:", reply_markup=markup)

async def rps_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    CHOICES = ["Rock", "Paper", "Scissors"]
    user = update.message.text
    if user not in CHOICES:
        return

    bot = random.choice(CHOICES)
    await update.message.reply_text(f"I choose {bot}")

    if user == bot:
        await update.message.reply_text("Draw!")
    elif (user == "Rock" and bot == "Scissors") or (user == "Paper" and bot == "Rock") or (user == "Scissors" and bot == "Paper"):
        await update.message.reply_text("You win :(")
    else:
        await update.message.reply_text("I win :)")


async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        query = " ".join(context.args)
        params = {
            "engine": "google",
            "q": query,
            "tbm": "isch",
            "api_key": SERPAPI_KEY
        }

        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        if "error" in data:
            await update.message.reply_text(f"Error from SerpAPI: {data['error']}")
            return

        images = data.get("images_results", [])
        if images:
            first = images[0]
            url = first.get("original") or first.get("thumbnail") or first.get("image")
            if url:
                await update.message.reply_photo(photo=url, caption=f"Image for: {query}")
                return
        await update.message.reply_text("Could not find any images.")
    else:
        await update.message.reply_text("Tell me what to search! For example: `/image cat`", parse_mode="Markdown")


def query_deepseek(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "TelegramBot"
    }

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"DeepSeek API Error: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"Request failed: {e}"


async def ask_deepseek_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: `/askdeepseek your question`", parse_mode="Markdown")
        return

    user_prompt = " ".join(context.args)
    await update.message.reply_text("Thinking...")

    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, query_deepseek, user_prompt)
    await update.message.reply_text(response)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("info", info_command))
app.add_handler(CommandHandler("weather", weather_command))
app.add_handler(CommandHandler("food", food_command))
app.add_handler(CommandHandler("rps", rock_paper_scissors_command))
app.add_handler(CommandHandler("image", image_command))
app.add_handler(CommandHandler("askdeepseek", ask_deepseek_command))

app.add_handler(MessageHandler(~filters.COMMAND & filters.TEXT, rps_callback_handler))

print("Bot is running...")
app.run_polling()
