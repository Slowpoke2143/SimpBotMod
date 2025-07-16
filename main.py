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
    'захуй', 'хуйня', 'хуйней', 'хуево', 'хуевый', 'хуесос', 'хуесоска',
    'пизда', 'пиздец', 'пиздевый', 'ебать', 'ебаный', 'ебануться', 'ебнутый',
    'оплата достойная', 'требуются 2', 'требуются 2-3', 'за каждый час',
    'пишите в личные сообщения', 'с оплатой не обижу', 'с оплатой не обидем',
    'договорная', 'требуются несколько помощников', 'работа простая',
    'оплчивается щедро', 'пиши в лс', 'за подробностями',
    'в час', 'требуются люди', 'на постоянную работу', 'пиши в личку',
    'пишите в личку', '2-3 человека нужны', 'нужны срочно', 'дела легкие',
    'наличкой', 'справится любой', 'на пару часов', 'требуются сотрудники',
    'требуются работники', 'требуется работник', 'требуется сотрудник',
    'подработка', 'нужны люди', 'нужны на сегодня', 'на сегодня',
    'выходить будет прилично', 'выходит прилично',
    'буквально за', 'места ограничены', 'присоединяйся к нашей команде',
    'личку', 'личка', 'личке', 'тыс', 'тыс.', 'лс', '₽', 'руб', 'рублей',
    'рубли', 'рублем', 'рублём', 'халтурка', 'халтура', 'зарабатывать',
    'зарабатывай', 'заработок', 'работа', 'заработать',
    'заработал', 'заработай'
]

# 2) Сборка единого паттерна: для каждого ключевика убираем пробелы,
#    а буквы соединяем через \s* (0 или более любых пробельных),
#    и оборачиваем в \b...\b, чтобы не захватывать вложенные куски.
spaced_patterns = []
for kw in BAN_KEYWORDS:
    chars = list(kw.replace(' ', ''))        # ['п','о','д','р','а','б','о','т','к','а']
    # экранируем каждый символ и склеиваем через \s*
    p = r'\b' + r'\s*'.join(re.escape(c) for c in chars) + r'\b'
    spaced_patterns.append(p)

SPACED_KEYWORDS_PATTERN = re.compile(
    '|'.join(spaced_patterns),
    flags=re.IGNORECASE
)

# 3) Аналогично улучшаем паттерн для цен, чтобы ловить "2 0 0 0 ₽", "3 0 0 0р" и т.п.
PRICE_PATTERN = re.compile(
    r'\b(?:\d\s*){2,}(?:₽|[Рр])\b',
    flags=re.IGNORECASE
)

async def handle_new_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return

    text = msg.text
    # теперь проверяем строго по одной регулярке:
    if SPACED_KEYWORDS_PATTERN.search(text) or PRICE_PATTERN.search(text):
        try:
            await msg.delete()
            print(f"Удалено сообщение от @{msg.from_user.username}")
        except Exception as e:
            print(f"Ошибка удаления: {e}")

async def handle_edited_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.edited_message
    if not msg or not msg.text:
        return

    text = msg.text
    if SPACED_KEYWORDS_PATTERN.search(text) or PRICE_PATTERN.search(text):
        try:
            await msg.delete()
            print(f"Удалено ОТРЕДАКТИРОВАННОЕ сообщение от @{msg.from_user.username}")
        except Exception as e:
            print(f"Ошибка удаления редактированного: {e}")

if __name__ == "__main__":
    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_message))
    app.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE & filters.TEXT, handle_edited_message))
    app.run_polling()
