import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8190263080:AAGAVgo59U1eIV3vqQqzFlBKORSyzyHSLyE"
ADMIN_ID = 6606638731
CHANNEL_ID = "@referandearnbotchannel"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchi ma'lumotlarini saqlash
users = {}

# Tugmali menyu
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Statistikani ko'rish")],
        [KeyboardButton(text="🔗 Referal havolam")],
        [KeyboardButton(text="💰 Pul yechish")],
        [KeyboardButton(text="🏆 Eng ko‘p referral yig‘ganlar")],
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"balance": 500, "referrals": []}
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}! 👋\n\nSizning hisobingiz: {users[user_id]['balance']} so‘m", reply_markup=menu)

@dp.message(lambda msg: msg.text == "📊 Statistikani ko'rish")
async def stats_cmd(message: types.Message):
    total_users = len(users)
    await message.answer(f"👥 Botdagi umumiy foydalanuvchilar soni: {total_users}")

@dp.message(lambda msg: msg.text == "🔗 Referal havolam")
async def referral_link(message: types.Message):
    user_id = message.from_user.id
    link = f"https://https://t.me/referearnmbot?start={user_id}"
    await message.answer(f"🔗 Sizning referal havolangiz: {link}\n\nDo‘stlaringizni taklif qiling va 1000 so‘m bonusga ega bo‘ling!")

@dp.message(lambda msg: msg.text == "💰 Pul yechish")
async def withdraw_cmd(message: types.Message):
    user_id = message.from_user.id
    if users[user_id]["balance"] < 10000:
        await message.answer("❌ Pul yechish uchun kamida 10 000 so‘m bo‘lishi kerak!")
        return
    await message.answer("💳 Pul yechish uchun kartangizni yuboring:")

@dp.message(lambda msg: msg.text.startswith("8600"))  # Kartani qabul qilish
async def receive_card(message: types.Message):
    user_id = message.from_user.id
    amount = users[user_id]["balance"]
    if amount < 10000:
        await message.answer("❌ Pul yechish uchun kamida 10 000 so‘m bo‘lishi kerak!")
        return
    users[user_id]["balance"] = 0
    await bot.send_message(ADMIN_ID, f"✅ Yangi pul yechish so‘rovi!\n\n💳 Karta: {message.text}\n💰 Miktor: {amount} so‘m\n👤 Foydalanuvchi: {message.from_user.full_name} ({user_id})")
    await message.answer("✅ Pul yechish so‘rovi adminga yuborildi. Tez orada tasdiqlanadi!")

@dp.message(lambda msg: msg.text == "🏆 Eng ko‘p referral yig‘ganlar")
async def top_referrals(message: types.Message):
    top_users = sorted(users.items(), key=lambda x: len(x[1]['referrals']), reverse=True)[:20]
    result = "🏆 Eng ko‘p referral qilganlar:\n\n"
    for idx, (user_id, data) in enumerate(top_users, start=1):
        result += f"{idx}. {user_id} - {len(data['referrals'])} ta referral, {data['balance']} so‘m\n"
    await message.answer(result)

@dp.message(lambda msg: msg.text.startswith("/tasdiq"))
async def confirm_withdrawal(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        user_id = int(message.text.split()[1])
        await bot.send_message(user_id, "✅ Pul yechish so‘rovingiz tasdiqlandi! Pulingiz kartangizga o‘tkazildi!")
        await bot.send_message(CHANNEL_ID, f"💸 {user_id} foydalanuvchining pul yechish so‘rovi tasdiqlandi!")
    except Exception as e:
        await message.answer(f"Xatolik: {e}")

@dp.message(lambda msg: msg.text.startswith("/xabar"))
async def send_message_to_all(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    text = message.text[7:]
    for user_id in users.keys():
        try:
            await bot.send_message(user_id, text)
        except:
            pass
    await message.answer("✅ Xabar barcha foydalanuvchilarga yuborildi!")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
