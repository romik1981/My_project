# Создадим код бота который будет хранить тексты и аккорды песен, а также ссылки на видеозаписи их исполнения
import json
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.client.session.aiohttp import AiohttpSession
import asyncio


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
TOKEN = '7611000284:AAE_2HtOV25PrJqoTNz0M46Z84kngeKT5Vw'

# Файл для хранения данных
DATA_FILE = 'songs.json'
MEDIA_DIR = 'media'
AUDIO_DIR = os.path.join(MEDIA_DIR, 'audio')
PHOTO_DIR = os.path.join(MEDIA_DIR, 'photo')

# Создаём папки при старте
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(PHOTO_DIR, exist_ok=True)

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
            # Явно приводим ключи к нижнему регистру
            data = {k.strip().lower(): v for k, v in raw.items()}
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

# Создаём сессию с увеличенным таймаутом
session = AiohttpSession(timeout=90) # 60 секунд вместо стандартных 5-10
bot = Bot(token=TOKEN, session=session)
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
                         "/add — добавить\n"
                         "/find — найти\n"
                         "/list — список\n"
                         "/delete — удалить\n"
                         "/edit — редактировать\n"
                         "/add_audio Название — привязать аудио\n"
                         "/add_photo Название — привязать фото", reply_markup=keyboard)

# Команда /add
@dp.message(Command("add"))
async def add_song(message: Message):
    await message.answer("Введите: Название; Текст; Аккорды; Ссылка")

# Команда /find — теперь ищет по части названия
@dp.message(Command("find"))
async def find_song(message: Message):
    try:
        query = message.text.split(' ', 1)[1].strip().lower()
    except IndexError:
        await message.answer("❌ Введите название после /find")
        return

    logger.info(f"🔍 Поиск через /find: запрошено '{query}'")
    logger.info(f"📂 Доступные ключи: {list(songs.keys())}")

    results = []
    for key, song in songs.items():
        if query in key or query in song["title"].lower() or song["title"].lower().startswith(query):
            results.append(song)

    if results:
        for song in results:
            logger.info(f"✅ Найдено: {song['title']}")

            if song.get("photo_file") and os.path.exists(song["photo_file"]):
                photo = FSInputFile(song["photo_file"])
                await message.answer_photo(photo=photo)
            if song.get("audio_file") and os.path.exists(song["audio_file"]):
                audio = FSInputFile(song["audio_file"])
                await message.answer_audio(audio=audio)

            response = (f"🎵 *{song['title']}*\n\n"
                        f"📝 Текст:\n{song['lyrics'][:300]}...\n\n"
                        f"🎼 Аккорды: {song['chords']}\n\n"
                        f"▶️ Видео: {song['video_url']}")
            await message.answer(response, parse_mode="Markdown")
    else:
        logger.warning(f"❌ Не найдено: '{query}'")
        await message.answer("Песня не найдена.")

# Добавление песни
@dp.message(F.text.func(lambda text: ";" in text))
async def process_song(message: Message):
    if message.text.startswith("/"):
        return

    parts = message.text.split(";", 3)
    if len(parts) != 4:
        await message.answer("❌ Ошибка: нужно 4 части: Название; Текст; Аккорды; Ссылка")
        return

    title, lyrics, chords, video_url = [part.strip() for part in parts]
    key = title.lower()

    songs[key] = {
        "title": title,
        "lyrics": lyrics,
        "chords": chords,
        "video_url": video_url,
        "audio_file": None,      # относительный путь к аудио
        "photo_file": None       # относительный путь к фото
    }
    save_data(songs)
    logger.info(f"Добавлена: '{key}' -> {title}")
    await message.answer(f"✅ Песня '{title}' добавлена!\nТеперь можно добавить аудио или фото.")

# Команда /add_audio Название
@dp.message(Command("add_audio"))
async def add_audio(message: Message):
    try:
        title = message.text.split(' ', 1)[1].strip()
        key = title.lower()
    except IndexError:
        await message.answer("❌ Укажите название песни: `/add_audio Название`", parse_mode="Markdown")
        return

    if key not in songs:
        await message.answer("Песня не найдена. Сначала добавьте её через /add.")
        return

    await message.answer(f"Отправьте аудиофайл для песни '{title}'. Я сохраню его локально.")

    # Сохраняем состояние
    user_states[message.from_user.id] = {"action": "waiting_audio", "key": key}

# Команда /add_photo Название
@dp.message(Command("add_photo"))
async def add_photo(message: Message):
    try:
        title = message.text.split(' ', 1)[1].strip()
        key = title.lower()
    except IndexError:
        await message.answer("❌ Укажите название песни: `/add_photo Название`", parse_mode="Markdown")
        return

    if key not in songs:
        await message.answer("Песня не найдена. Сначала добавьте её через /add.")
        return

    await message.answer(f"Отправьте фото для песни '{title}'. Я сохраню его локально.")

    # Сохраняем состояние
    user_states[message.from_user.id] = {"action": "waiting_photo", "key": key}

# Состояния пользователей
user_states = {}

# Получение аудио
@dp.message(F.audio)
async def handle_audio(message: Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if not state or state["action"] != "waiting_audio":
        return

    key = state["key"]
    song = songs[key]
    file_name = f"{key.replace(' ', '_')}.mp3"
    file_path = os.path.join(AUDIO_DIR, file_name)

    try:
        # Получаем file объект
        file = await bot.get_file(message.audio.file_id)

        # Скачиваем с увеличенным таймаутом (уже учтён в сессии)
        await bot.download_file(file.file_path, file_path)

        # Сохраняем путь
        songs[key]["audio_file"] = file_path
        save_data(songs)
        del user_states[user_id]

        await message.answer(f"✅ Аудио сохранено: `{file_path}`", parse_mode="Markdown")
        logger.info(f"Аудио успешно скачано: {file_path}")

    except TimeoutError:
        await message.answer("❌ Не удалось скачать аудио: превышено время ожидания.\n"
                             "Попробуйте ещё раз или отправьте файл меньшего размера.")
        logger.error("TimeoutError при скачивании аудио")
    except Exception as e:
        await message.answer(f"❌ Ошибка при скачивании аудио: {e}")
        logger.error(f"Ошибка при скачивании аудио: {e}")

# Получение фото
@dp.message(F.photo)
async def handle_photo(message: Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if not state or state["action"] != "waiting_photo":
        return

    key = state["key"]
    file_name = f"{key.replace(' ', '_')}.jpg"
    file_path = os.path.join(PHOTO_DIR, file_name)

    try:
        # Берём лучшее качество
        file = await bot.get_file(message.photo[-1].file_id)
        await bot.download_file(file.file_path, file_path)

        songs[key]["photo_file"] = file_path
        save_data(songs)
        del user_states[user_id]

        await message.answer(f"✅ Фото сохранено: `{file_path}`", parse_mode="Markdown")
        logger.info(f"Фото успешно скачано: {file_path}")

    except TimeoutError:
        await message.answer("❌ Не удалось скачать фото: превышено время ожидания.")
        logger.error("TimeoutError при скачивании фото")
    except Exception as e:
        await message.answer(f"❌ Ошибка при скачивании фото: {e}")
        logger.error(f"Ошибка при скачивании фото: {e}")

# Поиск по названию (без команды) — теперь по части названия
@dp.message(F.text & ~F.text.startswith("/") & ~F.text.func(lambda text: ";" in text))
async def search_song_by_name(message: Message):
    query = message.text.strip().lower()
    results = [song for key, song in songs.items()
               if query in key or query in song["title"].lower()]

    if results:
        for song in results[:3]:
            if song.get("photo_file") and os.path.exists(song["photo_file"]):
                photo = FSInputFile(song["photo_file"])
                await message.answer_photo(photo=photo)
            if song.get("audio_file") and os.path.exists(song["audio_file"]):
                audio = FSInputFile(song["audio_file"])
                await message.answer_audio(audio=audio)

            response = (f"🎵 *{song['title']}*\n\n"
                        f"📝 Текст:\n{song['lyrics'][:300]}...\n\n"
                        f"🎼 Аккорды: {song['chords']}\n\n"
                        f"▶️ Видео: {song['video_url']}")
            await message.answer(response, parse_mode="Markdown")
    else:
        await message.answer("Песня не найдена. Чтобы добавить — отправьте:\nНазвание; Текст; Аккорды; Ссылка")

# Команда /list
@dp.message(Command("list"))
async def list_songs(message: Message):
    if not songs:
        await message.answer("Список песен пуст.")
        return
    titles = "\n".join([f"• {s['title']}" for s in songs.values()])
    await message.answer(f"Доступные песни:\n{titles}")

# Команда /delete — удаление песни
@dp.message(Command("delete"))
async def delete_song(message: Message):
    try:
        query = message.text.split(' ', 1)[1].strip().lower()
    except IndexError:
        await message.answer("❌ Введите название песни после команды /delete")
        return

    # Ищем подходящие песни
    matches = []
    keys_to_delete = []
    for key, song in songs.items():
        if query in key or query in song["title"].lower():
            matches.append(song)
            keys_to_delete.append(key)

    if not matches:
        await message.answer("Песня не найдена.")
        return

    if len(matches) == 1:
        title = matches[0]["title"]
        del songs[keys_to_delete[0]]
        save_data(songs)
        await message.answer(f"🗑️ Песня '{title}' удалена.")
    else:
        # Если несколько — показываем список
        list_text = "\n".join([f"• {s['title']}" for s in matches])
        confirm = "\n".join([f"/confirm_delete {key}" for key in keys_to_delete])
        await message.answer(f"Найдено несколько песен:\n{list_text}\n\n"
                             f"Чтобы подтвердить удаление, введите:\n{confirm}")

# Команда /confirm_delete — подтверждение удаления (внутренняя)
@dp.message(Command("confirm_delete"))
async def confirm_delete(message: Message):
    try:
        key = message.text.split(' ', 1)[1].strip().lower()
    except IndexError:
        return

    if key in songs:
        title = songs[key]["title"]
        del songs[key]
        save_data(songs)
        await message.answer(f"🗑️ Песня '{title}' удалена.")
    else:
        await message.answer("Песня уже удалена или не существует.")

# Команда /edit — редактирование песни
@dp.message(Command("edit"))
async def edit_song(message: Message):
    try:
        args = message.text.split(' ', 1)[1].strip()
        # Формат: /edit Название; Новый текст; Новые аккорды; Новая ссылка
        edit_parts = args.split(';', 3)
        if len(edit_parts) != 4:
            raise ValueError()
        title = edit_parts[0].strip()
        new_lyrics = edit_parts[1].strip()
        new_chords = edit_parts[2].strip()
        new_video_url = edit_parts[3].strip()
    except:
        await message.answer("❌ Формат: `/edit Название; Новый текст; Новые аккорды; Новая ссылка`", parse_mode="Markdown")
        return

    key = title.lower()
    if key not in songs:
        await message.answer("Песня не найдена. Проверьте название.")
        return

    # Обновляем
    songs[key]["lyrics"] = new_lyrics
    songs[key]["chords"] = new_chords
    songs[key]["video_url"] = new_video_url
    save_data(songs)

    await message.answer(f"✅ Песня '{title}' обновлена!")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
