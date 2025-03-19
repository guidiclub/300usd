import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import sqlite3
from datetime import datetime , timedelta
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

API_TOKEN = '7484280406:AAGm7eEK3Nf7nwJ9kUTDdJa9irc1k0q6bC0'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
ADMIN_IDS = [525127130]
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0,
    language TEXT,
    currency TEXT,
    registration_date TEXT,
    last_login TEXT,
    subscription_active INTEGER DEFAULT 0,
    subscription_expiry TEXT,
    quantity INTEGER DEFAULT 0, 
    sold_accounts INTEGER DEFAULT 0 
)
''')
conn.commit()
import sqlite3

# Подключение к базе данных (если файла нет, он будет создан)
conn = sqlite3.connect('pricing.db')
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''
CREATE TABLE IF NOT EXISTS pricing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code VARCHAR(10) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    phone_code VARCHAR(10) NOT NULL,
    price_with_delay INTEGER NOT NULL,
    price_without_delay INTEGER NOT NULL,
    category VARCHAR(50) NOT NULL
)
''')

# Вставка данных
data = [
    # Восточная Европа
    ('RU', 'Российская Федерация', '+7', 70, 45, 'стандарт'),
    ('UA', 'Украина', '+380', 70, 45, 'стандарт'),
    ('BY', 'Беларусь', '+375', 38, 20, 'стандарт'),
    ('MD', 'Республика Молдова', '+373', 38, 20, 'стандарт'),
    ('RO', 'Румыния', '+40', 38, 20, 'стандарт'),

    # Южная Америка
    ('BR', 'Бразилия', '+55', 70, 45, 'стандарт'),
    ('AR', 'Аргентина', '+54', 38, 20, 'стандарт'),
    ('VE', 'Боливарианская Республика Венесуэла', '+58', 38, 20, 'стандарт'),

    # Западная Европа
    ('DE', 'Германия', '+49', 40, 20, 'стандарт'),
    ('FR', 'Франция', '+33', 38, 20, 'стандарт'),
    ('AT', 'Австрия', '+43', 38, 20, 'стандарт'),

    # Центральная Азия
    ('KZ', 'Казахстан', '+7', 38, 20, 'стандарт'),
    ('KG', 'Киргизия', '+996', 38, 20, 'стандарт'),
    ('TJ', 'Таджикистан', '+992', 38, 20, 'стандарт'),
    ('TM', 'Туркменистан', '+993', 38, 20, 'стандарт'),
    ('UZ', 'Узбекистан', '+998', 38, 20, 'стандарт'),

    # Западная Азия
    ('AM', 'Армения', '+374', 38, 20, 'стандарт'),
    ('AZ', 'Азербайджан', '+994', 38, 20, 'стандарт'),
    ('IL', 'Израиль', '+972', 38, 20, 'стандарт'),
    ('SA', 'Саудовская Аравия', '+966', 38, 20, 'стандарт'),
    ('KW', 'Кувейт', '+965', 38, 20, 'стандарт'),
    ('IQ', 'Ирак', '+964', 38, 20, 'стандарт'),
    ('SY', 'Сирийская Арабская Республика', '+963', 38, 20, 'стандарт'),

    # Северная Европа
    ('IE', 'Ирландия', '+353', 38, 20, 'стандарт'),
    ('LV', 'Латвия', '+371', 38, 20, 'стандарт'),
    ('NO', 'Норвегия', '+47', 38, 20, 'стандарт'),
    ('GB', 'Соединённое Королевство', '+44', 38, 20, 'стандарт'),

    # Южная Европа
    ('RS', 'Сербия', '+381', 38, 20, 'стандарт'),

    # Южная Азия
    ('AF', 'Афганистан', '+93', 38, 20, 'стандарт'),
    ('BD', 'Бангладеш', '+880', 2, 2, 'стандарт'),
    ('IN', 'Индия', '+91', 2, 2, 'стандарт'),

    # Карибский бассейн
    ('CU', 'Куба', '+53', 38, 20, 'стандарт'),

    # Юго-Восточная Азия
    ('TH', 'Таиланд', '+66', 38, 20, 'стандарт'),
    ('LA', 'Лаосская Народно-Демократическая Республика', '+856', 38, 20, 'стандарт'),
    ('KH', 'Камбоджа', '+855', 38, 20, 'стандарт'),
    ('MY', 'Малайзия', '+60', 38, 20, 'стандарт'),
    ('ID', 'Индонезия', '+62', 2, 2, 'стандарт'),
    ('MM', 'Мьянма', '+95', 2, 2, 'стандарт'),
    ('PH', 'Филиппины', '+63', 2, 2, 'стандарт'),

    # Центральная Америка
    ('SV', 'Сальвадор', '+503', 38, 20, 'стандарт'),
    ('GT', 'Гватемала', '+502', 38, 20, 'стандарт'),
    ('MX', 'Мексика', '+52', 38, 20, 'стандарт'),

    # Все остальные
    ('XX', 'Любая другая страна', '', 17, 2, 'стандарт'),

    # Центральная Африка
    ('AO', 'Ангола', '+244', 2, 2, 'стандарт'),
    ('CD', 'Демократическая Республика Конго', '+243', 2, 2, 'стандарт'),
    ('CF', 'Центрально-африканская республика', '+236', 2, 2, 'стандарт'),
    ('CG', 'Конго', '+242', 2, 2, 'стандарт'),
    ('CM', 'Камерун', '+237', 2, 2, 'стандарт'),
    ('GA', 'Габон', '+241', 2, 2, 'стандарт'),
    ('GQ', 'Экваториальная Гвинея', '+240', 2, 2, 'стандарт'),
    ('ST', 'Сан-Томе и Принсипи', '+239', 2, 2, 'стандарт'),
    ('TD', 'Чад', '+235', 2, 2, 'стандарт'),

    # Западная Африка
    ('BF', 'Буркина-Фасо', '+226', 2, 2, 'стандарт'),
    ('BJ', 'Бенин', '+229', 2, 2, 'стандарт'),
    ('CI', 'Кот-д\'Ивуар', '+225', 2, 2, 'стандарт'),
    ('CV', 'Кабо-Верде', '+238', 2, 2, 'стандарт'),
    ('GH', 'Гана', '+233', 2, 2, 'стандарт'),
    ('GM', 'Гамбия', '+220', 2, 2, 'стандарт'),
    ('GN', 'Гвинея', '+224', 2, 2, 'стандарт'),
    ('GW', 'Гвинея-Бисау', '+245', 2, 2, 'стандарт'),
    ('LR', 'Либерия', '+231', 2, 2, 'стандарт'),
    ('ML', 'Мали', '+223', 2, 2, 'стандарт'),
    ('MR', 'Мавритания', '+222', 2, 2, 'стандарт'),
    ('NE', 'Нигер', '+227', 2, 2, 'стандарт'),
    ('NG', 'Нигерия', '+234', 2, 2, 'стандарт'),
    ('SH', 'Остров Святой Елены, Остров Вознесения и Тристан-да-Кунья', '+290', 2, 2, 'стандарт'),
    ('SL', 'Сьерра-Леоне', '+232', 2, 2, 'стандарт'),
    ('SN', 'Сенегал', '+221', 2, 2, 'стандарт'),
    ('TG', 'Того', '+228', 2, 2, 'стандарт'),

    # Восточная Африка
    ('BI', 'Бурунди', '+257', 2, 2, 'стандарт'),
    ('DJ', 'Джибути', '+253', 2, 2, 'стандарт'),
    ('ER', 'Эритрея', '+291', 2, 2, 'стандарт'),
    ('ET', 'Эфиопия', '+251', 2, 2, 'стандарт'),
    ('KE', 'Кения', '+254', 2, 2, 'стандарт'),
    ('KM', 'Коморы', '+269', 2, 2, 'стандарт'),
    ('MG', 'Мадагаскар', '+261', 2, 2, 'стандарт'),
    ('MU', 'Маврикий', '+230', 2, 2, 'стандарт'),
    ('MW', 'Малави', '+265', 2, 2, 'стандарт'),
    ('MZ', 'Мозамбик', '+258', 2, 2, 'стандарт'),
    ('RE', 'Реюньон', '+262', 2, 2, 'стандарт'),
    ('RW', 'Руанда', '+250', 2, 2, 'стандарт'),
    ('SC', 'Сейшелы', '+248', 2, 2, 'стандарт'),
    ('SO', 'Сомали', '+252', 2, 2, 'стандарт'),
    ('SS', 'Южный Судан', '+211', 2, 2, 'стандарт'),
    ('TZ', 'Танзания', '+255', 2, 2, 'стандарт'),
    ('UG', 'Уганда', '+256', 2, 2, 'стандарт'),
    ('YT', 'Майот', '+262', 2, 2, 'стандарт'),
    ('ZM', 'Замбия', '+260', 2, 2, 'стандарт'),
    ('ZW', 'Зимбабве', '+263', 2, 2, 'стандарт'),

    # Южная Африка
    ('BW', 'Ботсвана', '+267', 2, 2, 'стандарт'),
    ('LS', 'Лесото', '+266', 2, 2, 'стандарт'),
    ('NA', 'Намибия', '+264', 2, 2, 'стандарт'),
    ('SZ', 'Эсватини', '+268', 2, 2, 'стандарт'),
    ('ZA', 'Южная Африка', '+27', 2, 2, 'стандарт'),

    # Северная Африка
    ('DZ', 'Алжир', '+213', 2, 2, 'стандарт'),
    ('LY', 'Ливия', '+218', 2, 2, 'стандарт'),
    ('MA', 'Марокко', '+212', 2, 2, 'стандарт'),
    ('SD', 'Судан', '+249', 2, 2, 'стандарт'),
    ('TN', 'Тунис', '+216', 2, 2, 'стандарт')
]

# Вставка данных в таблицу
cursor.executemany('''
INSERT INTO pricing (country_code, country_name, phone_code, price_with_delay, price_without_delay, category)
VALUES (?, ?, ?, ?, ?, ?)
''', data)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

class AdminStates(StatesGroup):
    WAITING_FOR_USER_ID_AND_AMOUNT = State()
    WAITING_FOR_USER_ID_FOR_SUBSCRIPTION = State()
    WAITING_FOR_COUNTRY_CODE_AND_PRICE = State()
def is_admin(user_id):
    return user_id in ADMIN_IDS
def get_user(user_id):
    try:
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        if result:
            return {
                "user_id": result[0],
                "balance": result[1],
                "language": result[2],
                "currency": result[3],
                "registration_date": result[4],
                "last_login": result[5],
                "subscription_active": result[6],
                "subscription_expiry": result[7],
                "quantity": result[8],  # Количество проданных аккаунтов
                "sold_accounts": result[9]  # Общая сумма проданных аккаунтов
            }
        return None
    except sqlite3.Error as e:
        logging.error(f"Ошибка при получении пользователя: {e}")
        return None
def add_user(user_id, language=None, currency=None):
    try:
        cursor.execute('''
        INSERT INTO users (user_id, language, currency, registration_date, last_login)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, language, currency, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при добавлении пользователя: {e}")

def update_user(user_id, language=None, currency=None):
    try:
        if language:
            cursor.execute('UPDATE users SET language = ? WHERE user_id = ?', (language, user_id))
        if currency:
            cursor.execute('UPDATE users SET currency = ? WHERE user_id = ?', (currency, user_id))
        cursor.execute('UPDATE users SET last_login = ? WHERE user_id = ?', (datetime.now().isoformat(), user_id))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при обновлении пользователя: {e}")


def update_balance(user_id, amount):
    try:
        cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (amount, user_id))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при изменении баланса: {e}")

def activate_subscription(user_id, duration_days=30):
    try:
        expiry_date = (datetime.now() + timedelta(days=duration_days)).isoformat()
        cursor.execute('''
        UPDATE users
        SET subscription_active = 1, subscription_expiry = ?
        WHERE user_id = ?
        ''', (expiry_date, user_id))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при активации подписки: {e}")

def deactivate_subscription(user_id):
    try:
        cursor.execute('''
        UPDATE users
        SET subscription_active = 0, subscription_expiry = NULL
        WHERE user_id = ?
        ''', (user_id,))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при деактивации подписки: {e}")

def get_subscription_info(user_id):
    try:
        cursor.execute('SELECT subscription_active, subscription_expiry FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        if result:
            active, expiry = result
            if active == 1 and expiry:
                expiry_date = datetime.fromisoformat(expiry)
                return {
                    "active": expiry_date > datetime.now(),
                    "expiry_date": expiry_date
                }
        return {"active": False, "expiry_date": None}
    except sqlite3.Error as e:
        logging.error(f"Ошибка при получении информации о подписке: {e}")
        return {"active": False, "expiry_date": None}

def update_quantity(user_id, quantity):
    try:
        cursor.execute('UPDATE users SET quantity = ? WHERE user_id = ?', (quantity, user_id))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при обновлении количества аккаунтов: {e}")

def update_sold_accounts(user_id, amount):
    try:
        cursor.execute('UPDATE users SET sold_accounts = ? WHERE user_id = ?', (amount, user_id))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при обновлении суммы проданных аккаунтов: {e}")

def update_price(country_code: str, price_with_delay: int, price_without_delay: int):
    try:
        cursor.execute('''
        UPDATE pricing
        SET price_with_delay = ?, price_without_delay = ?
        WHERE country_code = ?
        ''', (price_with_delay, price_without_delay, country_code))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при обновлении цены: {e}")
# Клавиатуры
language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="English 🇬🇧"), KeyboardButton(text="Русский 🇷🇺")]
    ],
    resize_keyboard=True
)

currency_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="USD 🇺🇸"), KeyboardButton(text="Рубли 🇷🇺")]
    ],
    resize_keyboard=True
)

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Продать аккаунты"), KeyboardButton(text="💼 Профиль"), KeyboardButton(text="📈 Цены")],
        [KeyboardButton(text="💬 Поддержка"), KeyboardButton(text="🔌 API"),
         KeyboardButton(text="🤝 Сотрудничество и Реферальные программы")],
        [KeyboardButton(text="📖 Условия работы"), KeyboardButton(text="💞 Отзывы")]
    ],
    resize_keyboard=True
)

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Пользователи")],
        [KeyboardButton(text="💳 Изменить баланс")],
        [KeyboardButton(text="🔓 Активировать подписку")],
        [KeyboardButton(text="🔒 Деактивировать подписку")],
        [KeyboardButton(text="💵 Изменить цены")],
        [KeyboardButton(text="🔙 В главное меню")]
    ],
    resize_keyboard=True
)

@dp.message(Command('start'))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if user and user.get("currency"):  # Используем .get() для безопасного доступа
        await message.answer("👋", reply_markup=main_menu_keyboard)
    else:
        await message.answer(
            "Welcome! Please select your preferred language.\nПожалуйста, выберите язык.",
            reply_markup=language_keyboard
        )
        if not user:
            add_user(user_id)

@dp.message(Command('admin'))
async def admin_panel(message: types.Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("У вас нет доступа к этой команде.")
        return

    await message.answer("Админ-панель", reply_markup=admin_keyboard)

# Изменение баланса
@dp.message(lambda message: message.text == "💳 Изменить баланс")
async def change_balance(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("У вас нет доступа к этой команде.")
        return
    await message.answer("Админ-панель", reply_markup=admin_keyboard)

    await message.answer("Введите ID пользователя и сумму через пробел (например, `123456789 1000`):")
    await state.set_state(AdminStates.WAITING_FOR_USER_ID_AND_AMOUNT)

@dp.message(AdminStates.WAITING_FOR_USER_ID_AND_AMOUNT)
async def process_balance_input(message: types.Message, state: FSMContext):
    try:
        user_id, amount = map(int, message.text.split())
        update_balance(user_id, amount)
        await message.answer(f"Баланс пользователя {user_id} изменен на {amount}.")
    except ValueError:
        await message.answer("Некорректный ввод. Используйте формат: `ID_пользователя сумма`.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
    finally:
        await state.clear()  # Сбрасываем состояние

# Активация подписки
@dp.message(lambda message: message.text == "🔓 Активировать подписку")
async def activate_subscription_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("У вас нет доступа к этой команде.")
        return

    await message.answer("Введите ID пользователя для активации подписки:")
    await state.set_state(AdminStates.WAITING_FOR_USER_ID_FOR_SUBSCRIPTION)

# Обработка ввода ID пользователя для активации подписки
@dp.message(AdminStates.WAITING_FOR_USER_ID_FOR_SUBSCRIPTION)
async def process_activate_subscription(message: types.Message, state: FSMContext):
    try:
        target_user_id = int(message.text)
        activate_subscription(target_user_id)
        await message.answer(f"Подписка для пользователя {target_user_id} активирована.")
    except ValueError:
        await message.answer("Некорректный ввод. Введите ID пользователя.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
    finally:
        await state.clear()  # Сбрасываем состояние

# Деактивация подписки
@dp.message(lambda message: message.text == "🔒 Деактивировать подписку")
async def deactivate_subscription_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("У вас нет доступа к этой команде.")
        return

    await message.answer("Введите ID пользователя для деактивации подписки:")
    await state.set_state(AdminStates.WAITING_FOR_USER_ID_FOR_SUBSCRIPTION)

# Обработка ввода ID пользователя для деактивации подписки
@dp.message(AdminStates.WAITING_FOR_USER_ID_FOR_SUBSCRIPTION)
async def process_deactivate_subscription(message: types.Message, state: FSMContext):
    try:
        target_user_id = int(message.text)
        deactivate_subscription(target_user_id)
        await message.answer(f"Подписка для пользователя {target_user_id} деактивирована.")
    except ValueError:
        await message.answer("Некорректный ввод. Введите ID пользователя.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
    finally:
        await state.clear()  # Сбрасываем состояние

# Возврат в главное меню
@dp.message(lambda message: message.text == "🔙 В главное меню")
async def back_to_main_menu(message: types.Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("У вас нет доступа к этой команде.")
        return

    await message.answer("Возврат в главное меню.", reply_markup=main_menu_keyboard)

@dp.message(lambda message: message.text == "English 🇬🇧")
async def language_english(message: types.Message):
    user_id = message.from_user.id
    update_user(user_id, language="en")
    await message.answer("You selected English.\nChoose your currency:", reply_markup=currency_keyboard)

@dp.message(lambda message: message.text == "Русский 🇷🇺")
async def language_russian(message: types.Message):
    user_id = message.from_user.id
    update_user(user_id, language="ru")
    await message.answer("Вы выбрали русский язык.\nВыберите валюту:", reply_markup=currency_keyboard)

@dp.message(lambda message: message.text == "USD 🇺🇸")
async def currency_usd(message: types.Message):
    user_id = message.from_user.id
    update_user(user_id, currency="usd")
    await message.answer("You selected USD 🇺🇸.", reply_markup=main_menu_keyboard)

@dp.message(lambda message: message.text == "Рубли 🇷🇺")
async def currency_rub(message: types.Message):
    user_id = message.from_user.id
    update_user(user_id, currency="rub")
    await message.answer("Вы выбрали рубли 🇷🇺.", reply_markup=main_menu_keyboard)

@dp.message(lambda message: message.text == "🛒 Продать аккаунты")
async def sell_accounts(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[])
    button = InlineKeyboardButton(
        text="📦Загрузить большой архив",
        url="https://bigsize.blitzkrieg.space/big_files/upload-big-file?seller_id=5270&ref_id=FRANCHISE_APP_1"
    )
    markup.inline_keyboard.append([button])

    await message.answer(
        """<b>🛒 Загрузка архива с аккаунтами</b>

Загрузите архив в формате .ZIP или .RAR

<b>Максимальный размер:</b> 20 MB

<b>Форматы:</b> TDATA, SESSION + JSON

📦 <a href="https://bigsize.blitzkrieg.space/big_files/upload-big-file?seller_id=5270&ref_id=FRANCHISE_APP_1">Загрузить большой архив</a>

📖 <a href="https://teletype.in/@blitzkriegdev/blitzkrieg-faq#vZhK">Требования к аккаунтам</a>
""",
        parse_mode="HTML",
        reply_markup=markup
    )


@dp.message(lambda message: message.text == "💼 Профиль")
async def profile(message: types.Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if not user:
        await message.answer("Пользователь не найден.")
        return

    subscription_info = get_subscription_info(user_id)
    subscription_status = "Активна" if subscription_info["active"] else "Неактивна"
    expiry_date = subscription_info["expiry_date"].strftime("%Y-%m-%d %H:%M:%S") if subscription_info["expiry_date"] else "Нет данных"

    text = f"""<b>• ID {user_id}</b>

🏆 <b>{user['quantity']} проданных аккаунтов • {user['sold_accounts']} RUB</b>

💰 <b>Баланс:</b> {user['balance']} RUB
👑 <b>Подписка:</b> {subscription_status} (истекает: {expiry_date})

📅 <b>Зарегистрирован:</b> {user['registration_date']}
"""
    keyboard = create_stats_keyboard()
    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)

def create_stats_keyboard(active_button=None):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    buttons = [
        ("📊 За 30 дней", "30_days"),
        ("📈 За всё время", "all_time"),
        ("💸 Вывод средств", "withdraw"),
        ("📂 Мои аккаунты", "my_accounts"),
        ("⚙️ Настройки", "settings")
    ]

    for text, callback_data in buttons:
        if callback_data == active_button:
            text = f"• {text} •"
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])

    return keyboard

@dp.message(Command('activate_subscription'))
async def activate_subscription_command(message: types.Message):
    user_id = message.from_user.id
    activate_subscription(user_id, duration_days=30)
    await message.answer("Ваша подписка активирована на 30 дней.")

@dp.message(Command('check_subscription'))
async def check_subscription_command(message: types.Message):
    user_id = message.from_user.id
    subscription_info = get_subscription_info(user_id)
    if subscription_info["active"]:
        expiry_date = subscription_info["expiry_date"].strftime("%Y-%m-%d %H:%M:%S")
        await message.answer(f"Ваша подписка активна. Истекает: {expiry_date}")
    else:
        await message.answer("Ваша подписка неактивна.")
@dp.callback_query(lambda call: call.data == "30_days")
async def handle_30_days(call: types.CallbackQuery):
    await call.answer("Вы выбрали 30 дней.")
    keyboard = create_stats_keyboard(active_button="30_days")
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query(lambda call: call.data == "all_time")
async def handle_all_time(call: types.CallbackQuery):
    await call.answer("Вы выбрали всё время.")
    keyboard = create_stats_keyboard(active_button="all_time")
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query(lambda call: call.data == "withdraw")
async def handle_withdraw(call: types.CallbackQuery):
    await call.answer("Переход к выводу средств.")
    withdraw_text = """<b>Вывод средств</b>

Минимальная сумма вывода — 50.0 RUB.  
На вашем балансе сейчас — 0.0 RUB.

<b>Привязанные кошельки</b>


"""
    withdraw_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    withdraw_keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="💸 Вывести средства", callback_data="withdraw_funds")])
    withdraw_keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔄 Изменить кошельки", callback_data="change_wallets")])
    withdraw_keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔙 Назад в профиль", callback_data="back_to_profile")])

    await call.message.edit_text(withdraw_text, parse_mode="HTML", reply_markup=withdraw_keyboard)


@dp.callback_query(lambda call: call.data == "my_accounts")
async def handle_my_accounts(call: types.CallbackQuery):
    await call.answer("Вы выбрали Мои аккаунты.")
    await call.message.edit_text("Вы выбрали Мои аккаунты.")


@dp.callback_query(lambda call: call.data == "settings")
async def handle_settings(call: types.CallbackQuery):
    await call.answer("Вы выбрали Настройки.")
    settings_text = """<b>Настройки</b>

Здесь вы можете настроить параметры вашего профиля.  
"""
    settings_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    settings_keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔔 Уведомления", callback_data="notifications")])
    settings_keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🛒 Режим покупки", callback_data="purchase_mode")])
    settings_keyboard.inline_keyboard.append([InlineKeyboardButton(text="🌐 Язык", callback_data="change_language")])
    settings_keyboard.inline_keyboard.append([InlineKeyboardButton(text="💱 Валюта", callback_data="change_currency")])
    settings_keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔙 Назад в профиль", callback_data="back_to_profile")])

    await call.message.edit_text(settings_text, parse_mode="HTML", reply_markup=settings_keyboard)


def create_language_keyboard(active_button=None):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    buttons = [
        ("Русский", "set_language_ru"),
        ("English", "set_language_en")
    ]

    for text, callback_data in buttons:
        if callback_data == active_button:
            text = f"• {text} •"
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])

    return keyboard


@dp.callback_query(lambda call: call.data.startswith("set_language_"))
async def handle_set_language(call: types.CallbackQuery):
    user_id = call.from_user.id
    language = call.data.split("_")[-1]

    update_user(user_id, language=language)

    if language == "ru":
        await call.answer("Язык изменен на русский.")
    else:
        await call.answer("Language changed to English.")

    keyboard = create_language_keyboard(active_button=call.data)
    await call.message.edit_reply_markup(reply_markup=keyboard)


def create_currency_keyboard(active_button=None):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    buttons = [
        ("Рубли 🇷🇺", "set_currency_rub"),
        ("USD 🇺🇸", "set_currency_usd")
    ]

    for text, callback_data in buttons:
        if callback_data == active_button:
            text = f"• {text} •"
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])

    return keyboard


@dp.callback_query(lambda call: call.data.startswith("set_currency_"))
async def handle_set_currency(call: types.CallbackQuery):
    user_id = call.from_user.id
    currency = call.data.split("_")[-1]

    update_user(user_id, currency=currency)

    if currency == "rub":
        await call.answer("Валюта изменена на рубли.")
    else:
        await call.answer("Currency changed to USD.")

    keyboard = create_currency_keyboard(active_button=call.data)
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query(lambda call: call.data == "change_language")
async def handle_change_language(call: types.CallbackQuery):
    await call.answer("Изменение языка.")
    change_language_text = """<b>Изменение языка</b>

Выберите язык интерфейса.  
"""
    change_language_keyboard = create_language_keyboard()
    await call.message.edit_text(change_language_text, parse_mode="HTML", reply_markup=change_language_keyboard)


@dp.callback_query(lambda call: call.data == "change_currency")
async def handle_change_currency(call: types.CallbackQuery):
    await call.answer("Изменение валюты.")
    change_currency_text = """<b>Изменение валюты</b>

Выберите валюту для отображения цен.  
"""
    change_currency_keyboard = create_currency_keyboard()
    await call.message.edit_text(change_currency_text, parse_mode="HTML", reply_markup=change_currency_keyboard)


@dp.callback_query(lambda call: call.data == "notifications")
async def handle_notifications(call: types.CallbackQuery):
    await call.answer("Настройка уведомлений.")
    notifications_text = """<b>Настройка уведомлений</b>

Выберите типы уведомлений, которые вы хотите получать.

В этом режиме вы получаете все уведомления: отчеты по архивам, вывод средств, прогресс обработки архивов, реферальные отчисления и другие.

- [ ] Все *
- [x] Только важные
"""
    notifications_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    notifications_keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔙 Назад в настройки", callback_data="settings")])

    await call.message.edit_text(notifications_text, parse_mode="HTML", reply_markup=notifications_keyboard)


@dp.callback_query(lambda call: call.data == "purchase_mode")
async def handle_purchase_mode(call: types.CallbackQuery):
    await call.answer("Настройка режима покупки.")
    purchase_mode_text = """<b>Настройка режима покупки</b>

Выберите режим покупки для аккаунтов без отлежки 24 часа. Рекомендуем ознакомиться с различиями в ценах для аккаунтов с отлежкой и без (см. раздел Цены) перед тем, как менять настройки в этом разделе.

В текущем режиме аккаунты без отлежки 24 часа будут покупаться сервисом только после ее наступления автоматически.


"""
    purchase_mode_keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    purchase_mode_keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔙 Назад в настройки", callback_data="settings")])

    await call.message.edit_text(purchase_mode_text, parse_mode="HTML", reply_markup=purchase_mode_keyboard)


@dp.callback_query(lambda call: call.data == "set_language_ru")
async def handle_set_language_ru(call: types.CallbackQuery):
    user_id = call.from_user.id

    update_user(user_id, language="ru")

    await call.answer("Язык изменен на русский.")
    await call.message.edit_text("Язык изменен на русский.")


@dp.callback_query(lambda call: call.data == "set_language_en")
async def handle_set_language_en(call: types.CallbackQuery):
    user_id = call.from_user.id

    update_user(user_id, language="en")

    await call.answer("Language changed to English.")
    await call.message.edit_text("Language changed to English.")


@dp.callback_query(lambda call: call.data == "set_currency_rub")
async def handle_set_currency_rub(call: types.CallbackQuery):
    user_id = call.from_user.id

    update_user(user_id, currency="rub")

    await call.answer("Валюта изменена на рубли.")
    await call.message.edit_text("Валюта изменена на рубли.")


@dp.callback_query(lambda call: call.data == "set_currency_usd")
async def handle_set_currency_usd(call: types.CallbackQuery):
    user_id = call.from_user.id
    update_user(user_id, currency="usd")

    await call.answer("Currency changed to USD.")
    await call.message.edit_text("Currency changed to USD.")


@dp.callback_query(lambda call: call.data == "back_to_profile")
async def handle_back_to_profile(call: types.CallbackQuery):
    await call.answer("Возврат в профиль.")
    (await profile(call.message)


@dp.message(lambda message: message.text == "📈 Цены"))
async def prices(message: types.Message):
    await message.answer("📈 Цены на аккаунты доступны на сайте.")


@dp.message(lambda message: message.text == "💬 Поддержка")
async def support(message: types.Message):
    await message.answer("📩 Официальная поддержка: [связаться](https://t.me/Blitzkrieg_sup)", parse_mode="Markdown")


@dp.message(lambda message: message.text == "🔌 API")
async def api_info(message: types.Message):
    await message.answer("🔌 API документация доступна на сайте.")


@dp.message(lambda message: message.text == "🤝 Сотрудничество и Реферальные программы")
async def partnership(message: types.Message):
    await message.answer("🤝 Информация о сотрудничестве доступна на сайте.")


@dp.message(lambda message: message.text == "📖 Условия работы")
async def terms(message: types.Message):
    await message.answer("📖 Условия работы: [прочитать](https://teletype.in/@cjsdkncvkjdsnkvcds/4O_vM0eBTAK).",
                         parse_mode="Markdown")


@dp.message(lambda message: message.text == "💞 Отзывы")
async def reviews(message: types.Message):
    await message.answer("💞 Оставьте отзыв: [форум](https://lolz.live/threads/7661091/).", parse_mode="Markdown")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())