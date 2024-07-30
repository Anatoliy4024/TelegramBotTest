from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
import calendar  # Импортируем модуль calendar

def language_selection_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🇪🇸\nES", callback_data='lang_es'),
            InlineKeyboardButton("🇺🇦\nUA", callback_data='lang_uk'),
            InlineKeyboardButton("🇬🇧\nEN", callback_data='lang_en'),
            InlineKeyboardButton("🇫🇷\nFR", callback_data='lang_fr')
        ],
        [
            InlineKeyboardButton("🇩🇪\nDE", callback_data='lang_de'),
            InlineKeyboardButton("🇵🇱\nPL", callback_data='lang_pl'),
            InlineKeyboardButton("🇮🇹\nIT", callback_data='lang_it'),
            InlineKeyboardButton("🇷🇺\nRU", callback_data='lang_ru')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def yes_no_keyboard(language):
    texts = {
        'en': ('Yes', 'No'),
        'ru': ('Да', 'Назад'),
        'es': ('Sí', 'No'),
        'fr': ('Oui', 'Non'),
        'uk': ('Так', 'Назад'),
        'pl': ('Tak', 'Nie')
    }
    yes_text, no_text = texts.get(language, ('Yes', 'No'))
    keyboard = [
        [
            InlineKeyboardButton(yes_text, callback_data='yes'),
            InlineKeyboardButton(no_text, callback_data='no')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_calendar_keyboard(month_offset=0, language='en'):
    today = datetime.today()
    target_month = today.month + month_offset
    year = today.year
    if target_month > 12:
        target_month -= 12
        year += 1
    elif target_month < 1:
        target_month += 12
        year -= 1

    # Генерация кнопок дней месяца
    calendar_buttons = []

    # Заголовок с месяцем и годом
    month_name = calendar.month_name[target_month]  # Получаем название месяца
    calendar_buttons.append([InlineKeyboardButton(f"{month_name} {year}", callback_data='none')])

    first_day = datetime(year, target_month, 1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Дни недели (заголовки)
    days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    calendar_buttons.append([InlineKeyboardButton(day, callback_data='none') for day in days_of_week])

    for week in calendar.monthcalendar(year, target_month):
        week_buttons = []
        for day in week:
            if day == 0:
                week_buttons.append(InlineKeyboardButton(" ", callback_data='none'))
            else:
                date_str = f"{year}-{target_month:02}-{day:02}"
                if target_month == today.month and day <= today.day:
                    week_buttons.append(InlineKeyboardButton(f"🔴{day}", callback_data='none'))
                else:
                    week_buttons.append(InlineKeyboardButton(f"🟢{day}", callback_data=f'date_{date_str}'))
        calendar_buttons.append(week_buttons)

    # Определяем предыдущий и следующий месяц
    prev_month = datetime(year, target_month, 1) - timedelta(days=1)
    next_month = datetime(year, target_month, 1) + timedelta(days=31)
    prev_month_name = calendar.month_name[prev_month.month]
    next_month_name = calendar.month_name[next_month.month]

    # Кнопки для навигации по месяцам с названиями месяцев
    navigation = [
        InlineKeyboardButton(f"◀️ {prev_month_name}", callback_data=f'prev_month_{month_offset - 1}') if month_offset > -1 else InlineKeyboardButton(" ", callback_data='none'),
        InlineKeyboardButton(f"{next_month_name} ▶️", callback_data=f'next_month_{month_offset + 1}') if month_offset < 2 else InlineKeyboardButton(" ", callback_data='none')
    ]
    calendar_buttons.append(navigation)

    return InlineKeyboardMarkup(calendar_buttons)

def generate_time_selection_keyboard():
    # Начальное и конечное время
    start_time = datetime.strptime('08:00', '%H:%M')
    end_time = datetime.strptime('20:00', '%H:%M')

    # Генерация кнопок времени с шагом в 30 минут
    time_buttons = []
    current_time = start_time

    while current_time <= end_time:
        time_str = current_time.strftime('%H:%M')
        time_buttons.append(InlineKeyboardButton(time_str, callback_data=f'time_{time_str}'))
        current_time += timedelta(minutes=30)

    # Разбиение кнопок на несколько строк
    num_buttons_per_row = 4  # Количество кнопок в строке
    rows = [time_buttons[i:i + num_buttons_per_row] for i in range(0, len(time_buttons), num_buttons_per_row)]

    # Надпись на клавиатуре
    keyboard = [
        [InlineKeyboardButton("Выберите время начала", callback_data='none')]
    ] + rows

    return InlineKeyboardMarkup(keyboard)
