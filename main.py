from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Запрещённые слова
BAN_KEYWORDS = ['оплата соответствующая', 'пишите в лс', 'ищу сотрудника', 'ищу сотрудников', 'ищем сотрудников', 'ищем сотрудника', 'набор персонала', 'для подработки', 'есть свободные вакансии', 'требуются разнорабочие', 'требуются люди', 'за подробностями в лс', 'ищешь подработку', 'ищите подработку', 'гибкий график', 'обучим с нуля', 'обучаем с нуля', 'нужна подработка', 'есть вакансии', 'есть свободные вакансии', 'на удаленке', 'на удаленной работе', 'удаленная работа', 'зарплата от', 'свободный граффик', 'перейди по ссылке', 'хуй', 'похуй', 'похую', 'похуист', 'нахуй', 'нахуя', 'захуй', 'похую', 'хуйня', 'хуйней', 'хуево', 'хуевый', 'хуесос', 'хуесоска', 'пизда', 'пиздец', 'пиздевый', 'ебать', 'ебаный', 'ебануться', 'ебнутый', 'оплата достойная', 'требуются 2', 'требуются 2-3', 'за каждый час', 'пишите в личные сообщения', 'с оплатой не обижу', 'с оплатой не обидем', 'договорная', 'требуются несколько помощников', 'работа простая', 'оплчивается щедро', 'оплата соответствующая', 'пиши в лс', 'за подробностями', 'в час', 'требуются люди', 'на постоянную работу', 'ищу работника', 'ищу работников', 'ищем работника', 'ищем работников']

# Удаление обычных сообщений
async def handle_new_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message and message.text:
        text = message.text.lower()
        if any(word in text for word in BAN_KEYWORDS):
            try:
                await message.delete()
                print(f"Удалено сообщение от @{message.from_user.username}")
            except Exception as e:
                print(f"Ошибка удаления: {e}")

# Удаление отредактированных сообщений
async def handle_edited_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("EDITED:", update.edited_message)  # добавим отладку
    if update.edited_message and update.edited_message.text:
        text = update.edited_message.text.lower()
        if any(word in text for word in BAN_KEYWORDS):
            try:
                await update.edited_message.delete()
                print(f"Удалено ОТРЕДАКТИРОВАННОЕ сообщение от @{update.edited_message.from_user.username}")
            except Exception as e:
                print(f"Ошибка удаления редактированного: {e}")

import os
TOKEN = os.environ["BOT_TOKEN"]

# Инициализация приложения
app = ApplicationBuilder().token(TOKEN).build()

# Обработчик новых сообщений
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_message))

# Обработчик отредактированных сообщений
app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE & filters.TEXT, handle_edited_message))

# Запуск бота
app.run_polling()
