import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

# --- ТВОИ ДАННЫЕ ---
TOKEN = "8224789333:AAFV0RN_FEBa9TU-4I2cTTS1No7d2wpR_mk"
ADMINS = [6083938306, 8522107566]
# --------------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Приветствие
@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "**сап!**\n"
        "можешь писать свое сообщение, и через некоторое время я отвечу!\n"
    )


# ======= ПЕРЕСЫЛКА ЮЗЕРА АДМИНАМ (все типы сообщений) =======
@dp.message()
async def user_message(message: Message):
    user = message.from_user

    # Формируем шапку
    header = (
        f"📩 соо от @{user.username} (ID: {user.id})\n"
        f"тип: {message.content_type}\n\n"
    )

    # Отсылаем ВСЕМ админам
    for admin_id in ADMINS:
        try:
            # Текст
            if message.text:
                await bot.send_message(admin_id, header + message.text)

            # Фото
            elif message.photo:
                await bot.send_photo(admin_id, message.photo[-1].file_id, caption=header)

            # Видео
            elif message.video:
                await bot.send_video(admin_id, message.video.file_id, caption=header)

            # Голосовые
            elif message.voice:
                await bot.send_voice(admin_id, message.voice.file_id, caption=header)

            # Аудио
            elif message.audio:
                await bot.send_audio(admin_id, message.audio.file_id, caption=header)

            # Документы (файлы)
            elif message.document:
                await bot.send_document(admin_id, message.document.file_id, caption=header)

            # Стикеры
            elif message.sticker:
                await bot.send_sticker(admin_id, message.sticker.file_id)
                await bot.send_message(admin_id, header)

            # Видео-заметки (кружочки)
            elif message.video_note:
                await bot.send_video_note(admin_id, message.video_note.file_id)
                await bot.send_message(admin_id, header)

        except:
            pass

    # Сообщение пользователю
    await message.answer("**Успешно✅ ждите ответа!**")



# ======= ОТВЕТ АДМИНА ЮЗЕРУ =======
@dp.message(F.reply_to_message, F.from_user.id.in_(ADMINS))
async def admin_reply(message: Message):
    original = message.reply_to_message.text

    # Парсим ID юзера
    try:
        user_id = int(original.split("ID: ")[1].split(")")[0])
    except:
        await message.answer("не удалось определить пользователя.")
        return

    # Отправляем ответ пользователю
    if message.text:
        await bot.send_message(user_id, f"ответ администратора:\n\n{message.text}")

    elif message.photo:
        await bot.send_photo(user_id, message.photo[-1].file_id,
                             caption="ответ администратора")

    elif message.video:
        await bot.send_video(user_id, message.video.file_id,
                             caption="ответ администратора")

    elif message.voice:
        await bot.send_voice(user_id, message.voice.file_id,
                             caption="ответ администратора")

    elif message.audio:
        await bot.send_audio(user_id, message.audio.file_id,
                             caption="ответ администратора")

    elif message.document:
        await bot.send_document(user_id, message.document.file_id,
                                caption="ответ администратора")

    elif message.sticker:
        await bot.send_sticker(user_id, message.sticker.file_id)

    elif message.video_note:
        await bot.send_video_note(user_id, message.video_note.file_id)

    await message.answer("ответ отправлен йоу")



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
