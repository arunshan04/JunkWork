import telepot

TELEGRAM_BOT_TOKEN = '1235059181:AAHunHnqLTM890i1qzEkAstD_EsPrLnC4xI'

bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
print(bot.getMe())

print(bot.getUpdates())


