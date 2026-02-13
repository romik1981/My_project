# Создадим код бота который будет хранить тексты и аккорды песен, а также ссылки на видеозаписи их исполнения
import json
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
TOKEN = '7611000284:AAE_2HtOV25PrJqoTNz0M46Z84kngeKT5Vw'

# Файл для хранения данных
DATA_FILE = 'songs.json'

# Показываем, где мы находимся
print("Текущая рабочая директория:", os.getcwd())

# Загрузка данных из файла
def load_data():
    if not os.path.exists(DATA_FILE):
        logger.warning(f"Файл {DATA_FILE} не найден. Создаётся новый.")
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            raw = json.load(f)
            data = {k.lower(): v for k, v in raw.items()}
            logger.info(f"Загружено {len(data)} песен из {DATA_FILE}")
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON: {e}")
        return {}

# Сохранение данных в файл
def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Данные сохранены в {DATA_FILE}. Количество песен: {len(data)}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении: {e}")

# Загружаем данные
songs = load_data()

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаём кнопки
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start"), KeyboardButton(text="/list")],
        [KeyboardButton(text="/add"), KeyboardButton(text="/find")]
    ],
    resize_keyboard=True
)

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я бот для хранения песен.\n"
                         "Команды:\n"
                         "/add — добавить песню\n"
                         "/find название — найти песню\n"
                         "/list — список всех песен",
                         reply_markup=keyboard)

# Команда /add
@dp.message(Command("add"))
async def add_song(message: Message):
    await message.answer("Введите: Название; Текст; Аккорды; Ссылка")

# Команда /find
@dp.message(Command("find"))
async def find_song(message: Message):
    try:
        query = message.text.split(' ', 1)[1].strip().lower()
    except IndexError:
        await message.answer("❌ Введите название после команды: `/find название`", parse_mode="Markdown")
        return

    logger.info(f"Поиск: '{query}' среди {list(songs.keys())}")

    song = songs.get(query)
    if song:
        response = (f"🎵 *{song['title']}*\n\n"
                    f"📝 Текст:\n{song['lyrics']}\n\n"
                    f"🎼 Аккорды: {song['chords']}\n\n"
                    f"▶️ Видео: {song['video_url']}")
        await message.answer(response, parse_mode="Markdown")
    else:
        await message.answer("Песня не найдена.")

# Команда /list
@dp.message(Command("list"))
async def list_songs(message: Message):
    if not songs:
        await message.answer("Список песен пуст.")
        return
    titles = "\n".join([f"• {s['title']}" for s in songs.values()])
    await message.answer(f"Доступные песни:\n{titles}")

# Обработка текста (добавление песни)
@dp.message(F.text)
async def process_song(message: Message):
    text = message.text
    if message.text.startswith("/") or ";" not in text:
        return

    parts = text.split(";", 3)  # Разбиваем только на 4 части
    if len(parts) != 4:
        await message.answer("❌ Ошибка: нужно 4 части, разделённые точкой с запятой.")
        return

    title, lyrics, chords, video_url = [part.strip() for part in parts]
    key = title.lower()

    songs[key] = {
        "title": title,
        "lyrics": lyrics,
        "chords": chords,
        "video_url": video_url
    }
    save_data(songs)
    logger.info(f"Добавлена: '{key}' -> {title}")
    await message.answer(f"✅ Песня '{title}' добавлена!")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
