# 🤖 MonBot

MonBot is a small passion project I built for fun. It started as a simple Telegram bot for testing, but I ended up adding a bunch of features that I personally find useful or just fun to have in a chat.

Named after my girlfriend Mona ❤️

---

## 💡 What can MonBot do?

Here are the current features (more coming soon):

- `/weather` — Shows the current weather in Yerevan️  
- `/food` — Picks a random place to eat in Yerevan  
- `/rps` — Play rock, paper, scissors against the bot️  
- `/image <query>` — Sends the first image result from Google Images️  
- `/ask <question>` — Uses DeepSeek AI to answer your question intelligently
- `/info` — A short description of the bot  
- `/help` — List of all commands  

---

## ⚙️ How it works

- Built with `python-telegram-bot`
- Uses OpenRouter + DeepSeek for AI responses
- Weather data from WeatherAPI
- Image search via SerpAPI


---

## 🔐 Environment Variables

Create a `.env` file in your root directory with the following content:

```env
BOT_TOKEN=your_telegram_bot_token
WEATHER_TOKEN=your_weatherapi_key
OPENROUTER_API_KEY=your_openrouter_key
SERPAPI_KEY=your_serpapi_key
```

You can get these API keys from:

- Telegram: [@BotFather](https://t.me/BotFather)
- WeatherAPI: [weatherapi.com](https://www.weatherapi.com/)
- OpenRouter: [openrouter.ai](https://openrouter.ai/)
- SerpAPI: [serpapi.com](https://serpapi.com/)
