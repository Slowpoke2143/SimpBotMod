import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Запрещённые слова
BAN_KEYWORDS = [
    'оплата соответствующая', 'пишите в лс', 'ищу сотрудника', 'ищу сотрудников',
    'ищем сотрудников', 'ищем сотрудника', 'набор персонала', 'для подработки',
    'есть свободные вакансии', 'требуются разнорабочие', 'требуются люди',
    'за подробностями в лс', 'ищешь подработку', 'ищите подработку',
    'гибкий график', 'обучим с нуля', 'обучаем с нуля', 'нужна подработка',
    'есть вакансии', 'есть свободные вакансии', 'на удаленке',
    'на удаленной работе', 'удаленная работа', 'зарплата от', 'свободный граффик',
    'перейди по ссылке', 'хуй', 'похуй', 'похую', 'похуист', 'нахуй', 'нахуя',
    'захуй', 'похую', 'хуйня', 'хуйней', 'хуево', 'хуевый', 'хуесос', 'хуесоска',
    'пизда', 'пиздец', 'пиздевый', 'ебать', 'ебаный', 'ебануться', 'ебнутый',
    'оплата достойная', 'требуются 2', 'требуются 2-3', 'за каждый час',
    'пишите в личные сообщения', 'с оплатой не обижу', 'с оплатой не обидем',
    'договорная', 'требуются несколько помощников', 'работа простая',
    'оплчивается щедро', 'оплата соответствующая', 'пиши в лс', 'за подробностями',
    'в час', 'требуются люди', 'на постоянную работу', 'пиши в личку',
    'пишите в личку', '2-3 человека нужны', 'нужны срочно', 'дела легкие',
    'наличкой', 'справится любой', 'на пару часов', 'требуются сотрудники',
    'требуются работники', 'на постоянную работу', 'требуется работник',
    'требуется сотрудник', 'подработка', 'нужны люди', 'нужны на сегодня',
    'на сегодня', 'выходить будет прилично', 'выходит прилично',
    'буквально за', 'места ограничены', 'присоединяйся к нашей команде', 'личку', 
    'личка', 'личке', 'тыс', 'тыс.', 'лс', '₽', 'руб', 'рублей', 'рубли', 'рублем', 
    'рублём' 'халтурка', 'халтура', 'зарабатывать', зарабатывай', 'заработок', 
    'работа', 'П', 'Р', 'заработать', 'заработал', 'заработай'
]

# Паттерн для цен: три и более цифр, опциональный пробел, затем ₽ или Р/р
PRICE_PATTERN = re.compile(r"\b\d{2,}\s?(?:₽|[Рр])\b")

# Удаление обычных сообщений
async def handle_new_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message and message.text:
        text_lower = message.text.lower()
        # проверяем по списку ключевых слов или по паттерну цены
        if any(keyword in text_lower for keyword in BAN_KEYWORDS) or PRICE_PATTERN.search(message.text):
            try:
                await message.delete()
                print(f"Удалено сообщение от @{message.from_user.username}")
            except Exception as e:
                print(f"Ошибка удаления: {e}")

# Удаление отредактированных сообщений
async def handle_edited_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.edited_message
    if msg and msg.text:
        text_lower = msg.text.lower()
        if any(keyword in text_lower for keyword in BAN_KEYWORDS) or PRICE_PATTERN.search(msg.text):
            try:
                await msg.delete()
                print(f"Удалено ОТРЕДАКТИРОВАННОЕ сообщение от @{msg.from_user.username}")
            except Exception as e:
                print(f"Ошибка удаления редактированного: {e}")

# Токен бота из переменных окружения
TOKEN = os.environ["BOT_TOKEN"]

# Инициализация и запуск приложения
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_message))
app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE & filters.TEXT, handle_edited_message))

if __name__ == "__main__":
    app.run_polling()
