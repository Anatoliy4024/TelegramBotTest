from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta

# Словарь для перевода названий месяцев
MONTHS = {
    'en': ['January', 'February', 'March', 'April', 'May', 'June',
           'July', 'August', 'September', 'October', 'November', 'December'],
    'ru': ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
           'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
    'es': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
           'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
    'fr': ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
           'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
    'uk': ['Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
           'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'],
    'pl': ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
           'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień']
}

def language_selection_keyboard():
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
         InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
        [InlineKeyboardButton("🇪🇸 Español", callback_data='lang_es'),
         InlineKeyboardButton("🇫🇷 Français", callback_data='lang_fr')],
        [InlineKeyboardButton("🇺🇦 Українська", callback_data='lang_uk'),
         InlineKeyboardButton("🇵🇱 Polski", callback_data='lang_pl')]
    ]
    return InlineKeyboardMarkup(keyboard)

def yes_no_keyboard(language):
    texts = {
        'en': ('Yes', 'No'),
        'ru': ('Да', 'Нет'),
        'es': ('Sí', 'No'),
        'fr': ('Oui', 'Non'),
        'uk': ('Так', 'Ні'),
        'pl': ('Tak', 'Nie')
    }
    yes_text, no_text = texts.get(language, ('Yes', 'No'))
    keyboard = [
        [InlineKeyboardButton(yes_text, callback_data='yes'),
         InlineKeyboardButton(no_text, callback_data='no')]
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_calendar_keyboard(month_offset=0, language='en'):
    # Получаем текущую дату и смещаем ее на месяц вперед или назад, если это указано
    today = datetime.now().date()
    first_day_of_month = today.replace(day=1) + timedelta(days=month_offset*30)

    # Получаем первый день следующего месяца
    next_month = first_day_of_month.replace(day=28) + timedelta(days=4)
    first_day_of_next_month = next_month - timedelta(days=next_month.day - 1)

    # Определяем диапазон для выбора даты
    start_date = today + timedelta(days=1)
    end_date = start_date + timedelta(days=61)  # Два месяца от завтрашнего дня

    # Получаем текущий месяц и год
    current_month = first_day_of_month.month
    current_year = first_day_of_month.year

    # Определяем, сколько дней в текущем месяце
    next_month_first_day = first_day_of_month.replace(day=28) + timedelta(days=4)
    days_in_month = (next_month_first_day - timedelta(days=next_month_first_day.day)).day

    # Создаем клавиатуру
    keyboard = []

    # Название месяца и года
    month_year = f"{MONTHS[language][current_month - 1]} {current_year}"
    keyboard.append([InlineKeyboardButton(month_year, callback_data="ignore")])

    # Заголовки дней недели
    days_of_week = {
        'en': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'ru': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
        'es': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
        'fr': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
        'uk': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'],
        'pl': ['Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob', 'Niedz']
    }
    keyboard.append([InlineKeyboardButton(day, callback_data="ignore") for day in days_of_week[language]])

    # Первое число месяца
    first_day_weekday = first_day_of_month.weekday()

    # Создаем пустые кнопки до первого дня текущего месяца
    row = [InlineKeyboardButton(" ", callback_data="ignore") for _ in range(first_day_weekday)]
    for day in range(1, days_in_month + 1):
        current_date = first_day_of_month.replace(day=day)
        if start_date <= current_date <= end_date:
            row.append(InlineKeyboardButton(str(day), callback_data=f"date_{current_date}"))
        else:
            row.append(InlineKeyboardButton(" ", callback_data="ignore"))
        if len(row) == 7:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    # Добавляем кнопки навигации
    navigation_buttons = []
    if month_offset > 0:
        navigation_buttons.append(InlineKeyboardButton("<", callback_data=f"prev_{month_offset - 1}"))
    if end_date.month != current_month:
        navigation_buttons.append(InlineKeyboardButton(">", callback_data=f"next_{month_offset + 1}"))
    if navigation_buttons:
        keyboard.append(navigation_buttons)

    return InlineKeyboardMarkup(keyboard)