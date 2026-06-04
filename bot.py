import asyncio
import json
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

# ========== CONFIG ==========
BOT_TOKEN = "8934892901:AAFKjtRPyUhAIAqd9yiEyiOtVPDuW-S_AAo"  # @BotFather dan olingan
CHANNEL_ID = "@vokab_uz"           # Kanal username
ADMIN_IDS = [123456789]            # Admin Telegram ID

# ========== TRANSLATIONS ==========
T = {
    "uz": {
        "welcome": "👋 Xush kelibsiz <b>Vokab.uz</b> botiga!\n\nNemis tilini professional darajada o'rganing 🇩🇪\n\n🌟 <b>Vokab bilan — professional!</b>",
        "choose_lang": "🌐 Tilni tanlang / Wählen Sie eine Sprache / Choose language:",
        "lang_set": "✅ Til o'rnatildi: O'zbek tili",
        "menu": "📋 <b>Asosiy menyu</b>\n\nNimani xohlaysiz?",
        "daily_word": "📚 <b>Kunlik so'z</b>",
        "take_test": "✅ <b>Test boshlash</b>",
        "my_progress": "📊 <b>Mening taraqqiyotim</b>",
        "subscribe_check": "📢 Botdan foydalanish uchun kanalimizga obuna bo'ling:",
        "not_subscribed": "❌ Siz hali kanalga obuna bo'lmagansiz!\n\n👇 Obuna bo'ling va qayta urinib ko'ring:",
        "subscribed": "✅ Rahmat! Obuna tasdiqlandi.",
        "register": "📝 Ro'yxatdan o'tish",
        "register_name": "👤 Ismingizni kiriting:",
        "register_level": "📊 Darajangizni tanlang:",
        "register_done": "🎉 Ro'yxatdan o'tish muvaffaqiyatli!\n\n<b>Ism:</b> {name}\n<b>Daraja:</b> {level}\n\nHoziroq o'rganishni boshlang! 🚀",
        "word_front": "🇩🇪 <b>Nemischa:</b>\n\n<code>{word}</code>\n\n[ {pronunciation} ]\n\n👆 Tarjimani ko'rish uchun tugmani bosing",
        "word_back": "✅ <b>Tarjima:</b>\n\n🇺🇿 {uz}\n🇷🇺 {ru}\n🇬🇧 {en}\n\n📝 <i>Misol: {example}</i>",
        "test_question": "❓ <b>Test #{num}</b>\n\n🇩🇪 <b>{word}</b> — bu qaysi so'z?",
        "correct": "✅ <b>To'g'ri!</b> +10 XP 🎉",
        "wrong": "❌ <b>Noto'g'ri.</b>\n\nTo'g'ri javob: <b>{answer}</b>",
        "test_done": "🏆 <b>Test yakunlandi!</b>\n\n✅ To'g'ri: {correct}/{total}\n⚡ Ulushingiz: {percent}%\n🎯 XP: +{xp}",
        "progress": "📊 <b>Sizning taraqqiyotingiz</b>\n\n👤 <b>{name}</b>\n📈 Daraja: {level}\n⚡ XP: {xp}\n🔥 Seriya: {streak} kun\n📚 So'zlar: {words}\n✅ Darslar: {lessons}",
        "payment_info": "💳 <b>Premium obuna</b>\n\n👑 Premium xususiyatlari:\n✅ Barcha darajalar (A1-C2)\n✅ Cheksiz darslar\n✅ Sertifikat\n✅ AI muallim\n\n💰 <b>Narx:</b> 125,000 so'm/oy\n\nTo'lov usulini tanlang:",
        "payme_info": "💚 <b>Payme orqali to'lov</b>\n\n1️⃣ Payme ilovasini oching\n2️⃣ «To'lov» bo'limiga kiring\n3️⃣ <code>9860 1234 5678 9012</code> — karta raqamiga\n4️⃣ Summa: <b>125,000 so'm</b>\n5️⃣ Izoh: <b>VOKAB_{user_id}</b>\n\nTo'lovdan so'ng «✅ To'lovni tasdiqlash» tugmasini bosing",
        "click_info": "🔵 <b>Click orqali to'lov</b>\n\n1️⃣ Click ilovasini oching\n2️⃣ «O'tkazma» bo'limiga kiring\n3️⃣ Telefon: <code>+998901234567</code>\n4️⃣ Summa: <b>125,000 so'm</b>\n5️⃣ Izoh: <b>VOKAB_{user_id}</b>\n\nTo'lovdan so'ng «✅ To'lovni tasdiqlash» tugmasini bosing",
        "payment_pending": "⏳ To'lovingiz tekshirilmoqda...\n\nAdmin 1-24 soat ichida tasdiqlaydi.",
        "btn_show_translation": "👁 Tarjimani ko'rish",
        "btn_next_word": "➡️ Keyingi so'z",
        "btn_listen": "🔊 Tinglash",
        "btn_start_test": "▶️ Testni boshlash",
        "btn_daily_word": "📚 Kunlik so'z",
        "btn_test": "✅ Test",
        "btn_progress": "📊 Taraqqiyot",
        "btn_premium": "👑 Premium",
        "btn_register": "📝 Ro'yxatdan o'tish",
        "btn_subscribe": "📢 Kanalga obuna bo'lish",
        "btn_check_sub": "✅ Obunani tekshirish",
        "btn_payme": "💚 Payme",
        "btn_click": "🔵 Click",
        "btn_confirm_pay": "✅ To'lovni tasdiqlash",
        "btn_back": "◀️ Orqaga",
        "levels": ["🔵 A1 — Boshlang'ich", "🟢 A2 — Elementar", "🟡 B1 — O'rta", "🟠 B2 — O'rta-yuqori", "🔴 C1 — Ilg'or", "⚫ C2 — Ustoz"],
    },
    "ru": {
        "welcome": "👋 Добро пожаловать в бот <b>Vokab.uz</b>!\n\nИзучайте немецкий язык профессионально 🇩🇪\n\n🌟 <b>С Vokab — профессионально!</b>",
        "lang_set": "✅ Язык установлен: Русский",
        "menu": "📋 <b>Главное меню</b>\n\nЧто вы хотите?",
        "daily_word": "📚 <b>Слово дня</b>",
        "take_test": "✅ <b>Начать тест</b>",
        "my_progress": "📊 <b>Мой прогресс</b>",
        "subscribe_check": "📢 Для использования бота подпишитесь на наш канал:",
        "not_subscribed": "❌ Вы ещё не подписались на канал!\n\n👇 Подпишитесь и попробуйте снова:",
        "subscribed": "✅ Спасибо! Подписка подтверждена.",
        "register": "📝 Регистрация",
        "register_name": "👤 Введите ваше имя:",
        "register_level": "📊 Выберите ваш уровень:",
        "register_done": "🎉 Регистрация успешна!\n\n<b>Имя:</b> {name}\n<b>Уровень:</b> {level}\n\nНачинайте учиться! 🚀",
        "word_front": "🇩🇪 <b>По-немецки:</b>\n\n<code>{word}</code>\n\n[ {pronunciation} ]\n\n👆 Нажмите кнопку для перевода",
        "word_back": "✅ <b>Перевод:</b>\n\n🇺🇿 {uz}\n🇷🇺 {ru}\n🇬🇧 {en}\n\n📝 <i>Пример: {example}</i>",
        "test_question": "❓ <b>Вопрос #{num}</b>\n\n🇩🇪 <b>{word}</b> — что это?",
        "correct": "✅ <b>Правильно!</b> +10 XP 🎉",
        "wrong": "❌ <b>Неверно.</b>\n\nПравильный ответ: <b>{answer}</b>",
        "test_done": "🏆 <b>Тест завершён!</b>\n\n✅ Правильно: {correct}/{total}\n⚡ Результат: {percent}%\n🎯 XP: +{xp}",
        "progress": "📊 <b>Ваш прогресс</b>\n\n👤 <b>{name}</b>\n📈 Уровень: {level}\n⚡ XP: {xp}\n🔥 Серия: {streak} дн.\n📚 Слов: {words}\n✅ Уроков: {lessons}",
        "payment_info": "💳 <b>Premium подписка</b>\n\n👑 Преимущества Premium:\n✅ Все уровни (A1-C2)\n✅ Безлимитные уроки\n✅ Сертификат\n✅ AI репетитор\n\n💰 <b>Цена:</b> 125,000 сум/мес\n\nВыберите способ оплаты:",
        "payme_info": "💚 <b>Оплата через Payme</b>\n\n1️⃣ Откройте приложение Payme\n2️⃣ Перейдите в раздел «Платёж»\n3️⃣ Карта: <code>9860 1234 5678 9012</code>\n4️⃣ Сумма: <b>125,000 сум</b>\n5️⃣ Комментарий: <b>VOKAB_{user_id}</b>\n\nПосле оплаты нажмите «✅ Подтвердить»",
        "click_info": "🔵 <b>Оплата через Click</b>\n\n1️⃣ Откройте приложение Click\n2️⃣ Перейдите в «Перевод»\n3️⃣ Телефон: <code>+998901234567</code>\n4️⃣ Сумма: <b>125,000 сум</b>\n5️⃣ Комментарий: <b>VOKAB_{user_id}</b>",
        "payment_pending": "⏳ Ваш платёж проверяется...\n\nАдмин подтвердит в течение 1-24 часов.",
        "btn_show_translation": "👁 Показать перевод",
        "btn_next_word": "➡️ Следующее слово",
        "btn_listen": "🔊 Слушать",
        "btn_start_test": "▶️ Начать тест",
        "btn_daily_word": "📚 Слово дня",
        "btn_test": "✅ Тест",
        "btn_progress": "📊 Прогресс",
        "btn_premium": "👑 Premium",
        "btn_register": "📝 Регистрация",
        "btn_subscribe": "📢 Подписаться на канал",
        "btn_check_sub": "✅ Проверить подписку",
        "btn_payme": "💚 Payme",
        "btn_click": "🔵 Click",
        "btn_confirm_pay": "✅ Подтвердить оплату",
        "btn_back": "◀️ Назад",
        "levels": ["🔵 A1 — Начальный", "🟢 A2 — Элементарный", "🟡 B1 — Средний", "🟠 B2 — Выше среднего", "🔴 C1 — Продвинутый", "⚫ C2 — Мастер"],
    },
    "en": {
        "welcome": "👋 Welcome to <b>Vokab.uz</b> bot!\n\nLearn German professionally 🇩🇪\n\n🌟 <b>With Vokab — professional!</b>",
        "lang_set": "✅ Language set: English",
        "menu": "📋 <b>Main Menu</b>\n\nWhat would you like?",
        "daily_word": "📚 <b>Word of the Day</b>",
        "take_test": "✅ <b>Start Test</b>",
        "my_progress": "📊 <b>My Progress</b>",
        "subscribe_check": "📢 Please subscribe to our channel to use the bot:",
        "not_subscribed": "❌ You haven't subscribed to the channel yet!\n\n👇 Subscribe and try again:",
        "subscribed": "✅ Thank you! Subscription confirmed.",
        "register": "📝 Registration",
        "register_name": "👤 Enter your name:",
        "register_level": "📊 Choose your level:",
        "register_done": "🎉 Registration successful!\n\n<b>Name:</b> {name}\n<b>Level:</b> {level}\n\nStart learning now! 🚀",
        "word_front": "🇩🇪 <b>German word:</b>\n\n<code>{word}</code>\n\n[ {pronunciation} ]\n\n👆 Press the button to see translation",
        "word_back": "✅ <b>Translation:</b>\n\n🇺🇿 {uz}\n🇷🇺 {ru}\n🇬🇧 {en}\n\n📝 <i>Example: {example}</i>",
        "test_question": "❓ <b>Question #{num}</b>\n\n🇩🇪 <b>{word}</b> — what does this mean?",
        "correct": "✅ <b>Correct!</b> +10 XP 🎉",
        "wrong": "❌ <b>Wrong.</b>\n\nCorrect answer: <b>{answer}</b>",
        "test_done": "🏆 <b>Test completed!</b>\n\n✅ Correct: {correct}/{total}\n⚡ Score: {percent}%\n🎯 XP: +{xp}",
        "progress": "📊 <b>Your Progress</b>\n\n👤 <b>{name}</b>\n📈 Level: {level}\n⚡ XP: {xp}\n🔥 Streak: {streak} days\n📚 Words: {words}\n✅ Lessons: {lessons}",
        "payment_info": "💳 <b>Premium Subscription</b>\n\n👑 Premium features:\n✅ All levels (A1-C2)\n✅ Unlimited lessons\n✅ Certificate\n✅ AI tutor\n\n💰 <b>Price:</b> 125,000 UZS/month\n\nChoose payment method:",
        "payme_info": "💚 <b>Pay via Payme</b>\n\n1️⃣ Open Payme app\n2️⃣ Go to 'Payment'\n3️⃣ Card: <code>9860 1234 5678 9012</code>\n4️⃣ Amount: <b>125,000 UZS</b>\n5️⃣ Comment: <b>VOKAB_{user_id}</b>",
        "click_info": "🔵 <b>Pay via Click</b>\n\n1️⃣ Open Click app\n2️⃣ Go to 'Transfer'\n3️⃣ Phone: <code>+998901234567</code>\n4️⃣ Amount: <b>125,000 UZS</b>\n5️⃣ Comment: <b>VOKAB_{user_id}</b>",
        "payment_pending": "⏳ Your payment is being verified...\n\nAdmin will confirm within 1-24 hours.",
        "btn_show_translation": "👁 Show Translation",
        "btn_next_word": "➡️ Next Word",
        "btn_listen": "🔊 Listen",
        "btn_start_test": "▶️ Start Test",
        "btn_daily_word": "📚 Daily Word",
        "btn_test": "✅ Test",
        "btn_progress": "📊 Progress",
        "btn_premium": "👑 Premium",
        "btn_register": "📝 Register",
        "btn_subscribe": "📢 Subscribe to Channel",
        "btn_check_sub": "✅ Check Subscription",
        "btn_payme": "💚 Payme",
        "btn_click": "🔵 Click",
        "btn_confirm_pay": "✅ Confirm Payment",
        "btn_back": "◀️ Back",
        "levels": ["🔵 A1 — Beginner", "🟢 A2 — Elementary", "🟡 B1 — Intermediate", "🟠 B2 — Upper Intermediate", "🔴 C1 — Advanced", "⚫ C2 — Mastery"],
    }
}

# ========== VOCABULARY ==========
WORDS = [
    {"de": "Haus", "uz": "Uy", "ru": "Дом", "en": "House", "pronunciation": "haʊs", "example": "Das Haus ist groß."},
    {"de": "Auto", "uz": "Mashina", "ru": "Машина", "en": "Car", "pronunciation": "ˈaʊto", "example": "Das Auto ist neu."},
    {"de": "Buch", "uz": "Kitob", "ru": "Книга", "en": "Book", "pronunciation": "buːx", "example": "Das Buch ist interessant."},
    {"de": "Schule", "uz": "Maktab", "ru": "Школа", "en": "School", "pronunciation": "ˈʃuːlə", "example": "Die Schule ist groß."},
    {"de": "Familie", "uz": "Oila", "ru": "Семья", "en": "Family", "pronunciation": "faˈmiːliə", "example": "Die Familie ist wichtig."},
    {"de": "Arbeit", "uz": "Ish", "ru": "Работа", "en": "Work", "pronunciation": "ˈaʁbaɪt", "example": "Die Arbeit macht Spaß."},
    {"de": "Wasser", "uz": "Suv", "ru": "Вода", "en": "Water", "pronunciation": "ˈvasɐ", "example": "Das Wasser ist kalt."},
    {"de": "Brot", "uz": "Non", "ru": "Хлеб", "en": "Bread", "pronunciation": "bʁoːt", "example": "Das Brot ist frisch."},
    {"de": "Stadt", "uz": "Shahar", "ru": "Город", "en": "City", "pronunciation": "ʃtat", "example": "Die Stadt ist schön."},
    {"de": "Freund", "uz": "Do'st", "ru": "Друг", "en": "Friend", "pronunciation": "fʁɔʏnt", "example": "Mein Freund heißt Max."},
    {"de": "Zeit", "uz": "Vaqt", "ru": "Время", "en": "Time", "pronunciation": "tsaɪt", "example": "Die Zeit vergeht schnell."},
    {"de": "Geld", "uz": "Pul", "ru": "Деньги", "en": "Money", "pronunciation": "ɡɛlt", "example": "Das Geld ist wichtig."},
]

# ========== USER DB (in-memory, haqiqiy loyihada DB ishlatiladi) ==========
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "lang": "uz", "name": None, "level": None,
            "xp": 0, "streak": 0, "words_learned": 0,
            "lessons": 0, "premium": False,
            "word_index": 0, "test_score": 0, "test_total": 0,
        }
    return users[user_id]

def get_lang(user_id):
    return get_user(user_id).get("lang", "uz")

def t(user_id, key, **kwargs):
    lang = get_lang(user_id)
    text = T.get(lang, T["uz"]).get(key, key)
    return text.format(**kwargs)

# ========== STATES ==========
class RegisterStates(StatesGroup):
    waiting_name = State()
    waiting_level = State()

class TestStates(StatesGroup):
    in_test = State()

# ========== KEYBOARDS ==========
def lang_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🇺🇿 O'zbek", callback_data="lang_uz")
    kb.button(text="🇷🇺 Русский", callback_data="lang_ru")
    kb.button(text="🇬🇧 English", callback_data="lang_en")
    kb.adjust(3)
    return kb.as_markup()

def main_menu_keyboard(user_id):
    lang = get_lang(user_id)
    kb = ReplyKeyboardBuilder()
    kb.button(text=T[lang]["btn_daily_word"])
    kb.button(text=T[lang]["btn_test"])
    kb.button(text=T[lang]["btn_progress"])
    kb.button(text=T[lang]["btn_premium"])
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def subscribe_keyboard(user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text=t(user_id, "btn_subscribe"), url=f"https://t.me/vokab_uz")
    kb.button(text=t(user_id, "btn_check_sub"), callback_data="check_sub")
    kb.adjust(1)
    return kb.as_markup()

def word_keyboard(user_id, word_index):
    kb = InlineKeyboardBuilder()
    kb.button(text=t(user_id, "btn_show_translation"), callback_data=f"show_word_{word_index}")
    kb.button(text=t(user_id, "btn_listen"), callback_data=f"listen_{word_index}")
    kb.adjust(2)
    return kb.as_markup()

def word_back_keyboard(user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text=t(user_id, "btn_next_word"), callback_data="next_word")
    kb.button(text=t(user_id, "btn_back"), callback_data="back_menu")
    kb.adjust(2)
    return kb.as_markup()

def test_keyboard(user_id, correct_answer, all_words):
    kb = InlineKeyboardBuilder()
    lang = get_lang(user_id)
    options = [correct_answer]
    others = [w for w in all_words if w["de"] != correct_answer]
    random.shuffle(others)
    for w in others[:3]:
        options.append(w["de"])
    random.shuffle(options)
    for opt in options:
        is_correct = opt == correct_answer
        kb.button(text=opt, callback_data=f"test_ans_{'correct' if is_correct else 'wrong'}_{opt}")
    kb.adjust(2)
    return kb.as_markup()

def payment_keyboard(user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text=t(user_id, "btn_payme"), callback_data="pay_payme")
    kb.button(text=t(user_id, "btn_click"), callback_data="pay_click")
    kb.button(text=t(user_id, "btn_back"), callback_data="back_menu")
    kb.adjust(2)
    return kb.as_markup()

def confirm_payment_keyboard(user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text=t(user_id, "btn_confirm_pay"), callback_data="confirm_payment")
    kb.button(text=t(user_id, "btn_back"), callback_data="back_menu")
    kb.adjust(1)
    return kb.as_markup()

# ========== HANDLERS ==========
async def check_subscription(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return True  # Kanal topilmasa o'tkazib yuborish

# /start
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    user = get_user(user_id)
    await message.answer(
        "🌐 <b>Vokab.uz</b>\n\n" + T["uz"]["choose_lang"],
        parse_mode="HTML",
        reply_markup=lang_keyboard()
    )

# Til tanlash
async def cb_set_lang(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = callback.data.split("_")[1]
    get_user(user_id)["lang"] = lang
    await callback.message.edit_text(
        T[lang]["welcome"],
        parse_mode="HTML"
    )
    await asyncio.sleep(1)
    # Obuna tekshirish
    is_subscribed = await check_subscription(callback.bot, user_id)
    if not is_subscribed:
        await callback.message.answer(
            t(user_id, "subscribe_check"),
            reply_markup=subscribe_keyboard(user_id)
        )
    else:
        user = get_user(user_id)
        if not user["name"]:
            await callback.message.answer(t(user_id, "register_name"))
            # State set
        else:
            await callback.message.answer(
                t(user_id, "menu"),
                parse_mode="HTML",
                reply_markup=main_menu_keyboard(user_id)
            )
    await callback.answer()

# Obuna tekshirish
async def cb_check_sub(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    is_subscribed = await check_subscription(callback.bot, user_id)
    if not is_subscribed:
        await callback.answer(t(user_id, "not_subscribed"), show_alert=True)
    else:
        await callback.message.edit_text(t(user_id, "subscribed"))
        user = get_user(user_id)
        if not user["name"]:
            await callback.message.answer(t(user_id, "register_name"))
            await state.set_state(RegisterStates.waiting_name)
        else:
            await callback.message.answer(
                t(user_id, "menu"),
                parse_mode="HTML",
                reply_markup=main_menu_keyboard(user_id)
            )

# Ro'yxatdan o'tish — ism
async def process_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    get_user(user_id)["name"] = message.text.strip()
    lang = get_lang(user_id)
    kb = InlineKeyboardBuilder()
    for level in T[lang]["levels"]:
        kb.button(text=level, callback_data=f"level_{level[:2]}")
    kb.adjust(2)
    await message.answer(t(user_id, "register_level"), reply_markup=kb.as_markup())
    await state.set_state(RegisterStates.waiting_level)

# Daraja tanlash
async def cb_set_level(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    level = callback.data.split("_")[1]
    user = get_user(user_id)
    user["level"] = level
    await state.clear()
    await callback.message.edit_text(
        t(user_id, "register_done", name=user["name"], level=level),
        parse_mode="HTML"
    )
    await callback.message.answer(
        t(user_id, "menu"),
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(user_id)
    )
    await callback.answer()

# Kunlik so'z
async def show_daily_word(message: types.Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    word = WORDS[user["word_index"] % len(WORDS)]
    user["word_index"] += 1
    await message.answer(
        t(user_id, "word_front",
          word=word["de"],
          pronunciation=word["pronunciation"]),
        parse_mode="HTML",
        reply_markup=word_keyboard(user_id, user["word_index"] - 1)
    )

# So'z tarjimasi ko'rsatish
async def cb_show_word(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    idx = int(callback.data.split("_")[2]) % len(WORDS)
    word = WORDS[idx]
    user = get_user(user_id)
    user["words_learned"] += 1
    user["xp"] += 5
    await callback.message.edit_text(
        t(user_id, "word_back",
          uz=word["uz"], ru=word["ru"], en=word["en"],
          example=word["example"]),
        parse_mode="HTML",
        reply_markup=word_back_keyboard(user_id)
    )
    await callback.answer()

# Keyingi so'z
async def cb_next_word(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user = get_user(user_id)
    word = WORDS[user["word_index"] % len(WORDS)]
    user["word_index"] += 1
    await callback.message.edit_text(
        t(user_id, "word_front",
          word=word["de"],
          pronunciation=word["pronunciation"]),
        parse_mode="HTML",
        reply_markup=word_keyboard(user_id, user["word_index"] - 1)
    )
    await callback.answer()

# Test boshlash
async def start_test(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = get_user(user_id)
    user["test_score"] = 0
    user["test_total"] = 0
    await state.set_state(TestStates.in_test)
    await send_test_question(message.bot, user_id, message.chat.id, state)

async def send_test_question(bot, user_id, chat_id, state):
    user = get_user(user_id)
    word = random.choice(WORDS)
    await state.update_data(current_word=word["de"])
    lang = get_lang(user_id)
    q_num = user["test_total"] + 1
    # Translation options based on lang
    trans_key = lang if lang in ["uz","ru","en"] else "uz"
    await bot.send_message(
        chat_id,
        T[lang]["test_question"].format(num=q_num, word=word[trans_key] if trans_key != "uz" else word["uz"]) if False else
        f"❓ <b>Test #{q_num}</b>\n\n🇩🇪 <b>{word['de']}</b> — {T[lang]['test_question'].split('—')[1].strip() if '—' in T[lang]['test_question'] else '?'}",
        parse_mode="HTML",
        reply_markup=test_keyboard(user_id, word["de"], WORDS)
    )

# Test javobi
async def cb_test_answer(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user = get_user(user_id)
    parts = callback.data.split("_", 3)
    result = parts[2]
    user["test_total"] += 1
    if result == "correct":
        user["test_score"] += 1
        user["xp"] += 10
        await callback.message.edit_text(t(user_id, "correct"), parse_mode="HTML")
    else:
        data = await state.get_data()
        correct = data.get("current_word", "—")
        await callback.message.edit_text(
            t(user_id, "wrong", answer=correct),
            parse_mode="HTML"
        )
    await callback.answer()
    # 5 savoldan so'ng tugat
    if user["test_total"] >= 5:
        await state.clear()
        percent = int(user["test_score"] / user["test_total"] * 100)
        xp = user["test_score"] * 10
        await callback.message.answer(
            t(user_id, "test_done",
              correct=user["test_score"],
              total=user["test_total"],
              percent=percent,
              xp=xp),
            parse_mode="HTML",
            reply_markup=main_menu_keyboard(user_id)
        )
    else:
        await asyncio.sleep(1)
        await send_test_question(callback.bot, user_id, callback.message.chat.id, state)

# Taraqqiyot
async def show_progress(message: types.Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    name = user.get("name") or message.from_user.first_name
    await message.answer(
        t(user_id, "progress",
          name=name,
          level=user.get("level", "A1"),
          xp=user.get("xp", 0),
          streak=user.get("streak", 0),
          words=user.get("words_learned", 0),
          lessons=user.get("lessons", 0)),
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(user_id)
    )

# Premium
async def show_premium(message: types.Message):
    user_id = message.from_user.id
    await message.answer(
        t(user_id, "payment_info"),
        parse_mode="HTML",
        reply_markup=payment_keyboard(user_id)
    )

# To'lov usullari
async def cb_pay_payme(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_text(
        t(user_id, "payme_info", user_id=user_id),
        parse_mode="HTML",
        reply_markup=confirm_payment_keyboard(user_id)
    )
    await callback.answer()

async def cb_pay_click(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_text(
        t(user_id, "click_info", user_id=user_id),
        parse_mode="HTML",
        reply_markup=confirm_payment_keyboard(user_id)
    )
    await callback.answer()

async def cb_confirm_payment(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    # Admin ga xabar
    for admin_id in ADMIN_IDS:
        try:
            user = get_user(user_id)
            await callback.bot.send_message(
                admin_id,
                f"💳 <b>Yangi to'lov so'rovi!</b>\n\n"
                f"👤 Foydalanuvchi: {callback.from_user.full_name}\n"
                f"🆔 ID: <code>{user_id}</code>\n"
                f"📱 Username: @{callback.from_user.username or 'yo\'q'}\n"
                f"💰 Summa: 125,000 so'm\n"
                f"📊 Daraja: {user.get('level','A1')}\n\n"
                f"✅ Tasdiqlash uchun: /approve_{user_id}\n"
                f"❌ Rad etish uchun: /reject_{user_id}",
                parse_mode="HTML"
            )
        except:
            pass
    await callback.message.edit_text(
        t(user_id, "payment_pending"),
        parse_mode="HTML"
    )
    await callback.answer()

# Admin: tasdiqlash
async def cmd_approve(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        target_id = int(message.text.split("_")[1])
        get_user(target_id)["premium"] = True
        await message.bot.send_message(
            target_id,
            "🎉 <b>Premium faollashtirildi!</b>\n\nEndi barcha imkoniyatlar sizga ochiq! 👑",
            parse_mode="HTML"
        )
        await message.answer(f"✅ {target_id} foydalanuvchiga Premium berildi.")
    except:
        await message.answer("❌ Xato. Format: /approve_123456")

# Admin: rad etish
async def cmd_reject(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        target_id = int(message.text.split("_")[1])
        await message.bot.send_message(
            target_id,
            "❌ <b>To'lov tasdiqlanmadi.</b>\n\nIltimos, qayta urinib ko'ring yoki admin bilan bog'laning.",
            parse_mode="HTML"
        )
        await message.answer(f"✅ {target_id} foydalanuvchiga xabar yuborildi.")
    except:
        await message.answer("❌ Xato.")

# Orqaga
async def cb_back_menu(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.clear()
    await callback.message.edit_text(t(user_id, "menu"), parse_mode="HTML")
    await callback.message.answer(
        "👇",
        reply_markup=main_menu_keyboard(user_id)
    )
    await callback.answer()

# ========== MAIN ==========
async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Handlers ro'yxatdan o'tkazish
    dp.message.register(cmd_start, CommandStart())
    dp.callback_query.register(cb_set_lang, F.data.startswith("lang_"))
    dp.callback_query.register(cb_check_sub, F.data == "check_sub")
    dp.message.register(process_name, RegisterStates.waiting_name)
    dp.callback_query.register(cb_set_level, F.data.startswith("level_"))
    dp.message.register(show_daily_word, F.text.contains("📚"))
    dp.message.register(start_test, F.text.contains("✅"))
    dp.message.register(show_progress, F.text.contains("📊"))
    dp.message.register(show_premium, F.text.contains("👑"))
    dp.callback_query.register(cb_show_word, F.data.startswith("show_word_"))
    dp.callback_query.register(cb_next_word, F.data == "next_word")
    dp.callback_query.register(cb_test_answer, F.data.startswith("test_ans_"), TestStates.in_test)
    dp.callback_query.register(cb_pay_payme, F.data == "pay_payme")
    dp.callback_query.register(cb_pay_click, F.data == "pay_click")
    dp.callback_query.register(cb_confirm_payment, F.data == "confirm_payment")
    dp.callback_query.register(cb_back_menu, F.data == "back_menu")
    dp.message.register(cmd_approve, F.text.startswith("/approve_"))
    dp.message.register(cmd_reject, F.text.startswith("/reject_"))

    print("🤖 Vokab.uz bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
