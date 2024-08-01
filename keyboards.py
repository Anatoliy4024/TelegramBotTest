from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
import calendar

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

def generate_month_name(month, language):
    months = {
        'en': ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        'ru': ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
        'es': ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
        'fr': ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
        'uk': ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"],
        'pl': ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"]
    }
    return months.get(language, months['en'])[month - 1]

# def generate_calendar_keyboard(month_offset=0, language='en'):
#     today = datetime.today()
#     start_date = today + timedelta(days=1)  # Завтрашний день
#     end_date = start_date + timedelta(days=60)  # Два месяца вперед
#
#     calendar_buttons = []
#
#     month_name = generate_month_name(start_date.month, language)
#     calendar_buttons.append([InlineKeyboardButton(f"{month_name} {start_date.year}", callback_data='none')])
#
#     days_of_week = {
#         'en': ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
#         'ru': ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
#         'es': ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
#         'fr': ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"],
#         'uk': ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"],
#         'pl': ["Pon", "Wt", "Śr", "Czw", "Pią", "Sob", "Niedz"]
#     }
#     days_of_week_translated = days_of_week.get(language, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
#     calendar_buttons.append([InlineKeyboardButton(day, callback_data='none') for day in days_of_week_translated])
#
#     current_date = start_date
#     while current_date <= end_date:
#         week_buttons = []
#         for i in range(7):
#             if current_date > end_date:
#                 week_buttons.append(InlineKeyboardButton(" ", callback_data='none'))
#             else:
#                 date_str = current_date.strftime('%Y-%m-%d')
#                 week_buttons.append(InlineKeyboardButton(f"{current_date.day}", callback_data=f'date_{date_str}'))
#                 current_date += timedelta(days=1)
#         calendar_buttons.append(week_buttons)
#
#     # Добавление кнопок для навигации по месяцам
#     previous_month_button = InlineKeyboardButton("<", callback_data=f"prev_month_{month_offset - 1}")
#     next_month_button = InlineKeyboardButton(">", callback_data=f"next_month_{month_offset + 1}")
#     navigation_row = [previous_month_button, next_month_button]
#     calendar_buttons.append(navigation_row)
#
#     return InlineKeyboardMarkup(calendar_buttons)

def generate_calendar_keyboard(month_offset=0, language='en'):
    today = datetime.today()
    base_month = today.month + month_offset
    base_year = today.year

    if base_month > 12:
        base_month -= 12
        base_year += 1
    elif base_month < 1:
        base_month += 12
        base_year -= 1

    first_of_month = datetime(base_year, base_month, 1)
    last_day = calendar.monthrange(first_of_month.year, first_of_month.month)[1]
    last_of_month = first_of_month.replace(day=last_day)

    month_name = generate_month_name(first_of_month.month, language)
    days_of_week = {
        'en': ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        'ru': ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
        # Добавьте другие языковые опции по аналогии
    }

    calendar_buttons = [
        [InlineKeyboardButton(f"{month_name} {first_of_month.year}", callback_data='none')],
        [InlineKeyboardButton(day, callback_data='none') for day in days_of_week.get(language, days_of_week['en'])]
    ]

    # Подготовка первой строки с пустыми кнопками до первого дня месяца
    first_weekday = first_of_month.weekday()
    first_weekday = (first_weekday + 6) % 7  # понедельник как первый день недели
    week_buttons = [InlineKeyboardButton(" ", callback_data='none') for _ in range(first_weekday)]

    current_date = first_of_month
    while current_date <= last_of_month:
        if len(week_buttons) == 7:
            calendar_buttons.append(week_buttons)
            week_buttons = []

        day_button = InlineKeyboardButton(str(current_date.day), callback_data=f'date_{current_date.strftime("%Y-%m-%d")}')
        week_buttons.append(day_button)
        current_date += timedelta(days=1)

    # Добавить последнюю неделю, если она не полная
    if week_buttons:
        week_buttons.extend([InlineKeyboardButton(" ", callback_data='none') for _ in range(7 - len(week_buttons))])
        calendar_buttons.append(week_buttons)

    # Навигационные кнопки
    prev_month_button = InlineKeyboardButton("<", callback_data=f"prev_month_{month_offset - 1}") if month_offset > -1 else InlineKeyboardButton(" ", callback_data="none")
    next_month_button = InlineKeyboardButton(">", callback_data=f"next_month_{month_offset + 1}") if month_offset < 2 else InlineKeyboardButton(" ", callback_data="none")
    calendar_buttons.append([prev_month_button, next_month_button])

    return InlineKeyboardMarkup(calendar_buttons)


def generate_time_selection_keyboard(language):
    start_time = datetime.strptime('08:00', '%H:%M')
    end_time = datetime.strptime('20:00', '%H:%M')

    time_buttons = []
    current_time = start_time

    while current_time <= end_time:
        time_str = current_time.strftime('%H:%M')
        time_buttons.append(InlineKeyboardButton(time_str, callback_data=f'time_{time_str}'))
        current_time += timedelta(minutes=30)

    num_buttons_per_row = 4
    rows = [time_buttons[i:i + num_buttons_per_row] for i in range(0, len(time_buttons), num_buttons_per_row)]

    return InlineKeyboardMarkup(rows)
