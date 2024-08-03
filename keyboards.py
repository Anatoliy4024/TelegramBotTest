from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
import calendar

def generate_month_name(month, language):
    months = {
        'en': ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        'ru': ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
        'es': ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
        'fr': ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
        'uk': ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"],
        'pl': ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopад", "Grudzień"],
        'de': ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
        'it': ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]
    }
    return months[language][month - 1]

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
        'es': ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
        'fr': ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"],
        'uk': ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"],
        'pl': ["Pon", "Wt", "Śr", "Czw", "Pią", "Sob", "Niedz"],
        'de': ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
        'it': ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
    }

    calendar_buttons = [
        [InlineKeyboardButton(f"{month_name} {first_of_month.year}", callback_data='none')],
        [InlineKeyboardButton(day, callback_data='none') for day in days_of_week[language]]
    ]

    start_weekday = first_of_month.weekday()
    week_row = [InlineKeyboardButton(" ", callback_data='none') for _ in range(start_weekday)]

    current_date = first_of_month
    while current_date <= last_of_month:
        if len(week_row) == 7:
            calendar_buttons.append(week_row)
            week_row = []

        if current_date <= today:
            day_button = InlineKeyboardButton(f"🔴 {current_date.day}", callback_data='none')
        else:
            day_button = InlineKeyboardButton(f"🟢 {current_date.day}",
                                              callback_data=f'date_{current_date.strftime("%Y-%m-%d")}')

        week_row.append(day_button)
        current_date += timedelta(days=1)

    if week_row:
        week_row.extend([InlineKeyboardButton(" ", callback_data='none') for _ in range(7 - len(week_row))])
        calendar_buttons.append(week_row)

    prev_month_button = InlineKeyboardButton("<",
                                             callback_data=f"prev_month_{month_offset - 1}") if month_offset > -1 else InlineKeyboardButton(
        " ", callback_data="none")
    next_month_button = InlineKeyboardButton(">",
                                             callback_data=f"next_month_{month_offset + 1}") if month_offset < 2 else InlineKeyboardButton(
        " ", callback_data="none")
    calendar_buttons.append([prev_month_button, next_month_button])

    return InlineKeyboardMarkup(calendar_buttons)

def generate_time_selection_keyboard(language, stage='start', start_time=None):
    start_time_dt = datetime.strptime('08:00', '%H:%M')
    end_time_dt = datetime.strptime('22:00', '%H:%M')

    time_buttons = []
    current_time = start_time_dt

    while current_time <= end_time_dt:
        time_str = current_time.strftime('%H:%M')
        if stage == 'end' and start_time:
            start_time_dt = datetime.strptime(start_time, '%H:%M')
            if current_time < start_time_dt + timedelta(hours=2):
                time_buttons.append(InlineKeyboardButton(f"🔴 {time_str}", callback_data='none'))
            else:
                time_buttons.append(InlineKeyboardButton(f"🟢 {time_str}", callback_data=f'time_{time_str}'))
        else:
            if current_time >= datetime.strptime('20:30', '%H:%M'):
                time_buttons.append(InlineKeyboardButton(f"🔴 {time_str}", callback_data='none'))
            else:
                time_buttons.append(InlineKeyboardButton(f"🟢 {time_str}", callback_data=f'time_{time_str}'))
        current_time += timedelta(minutes=30)

    num_buttons_per_row = 5
    rows = [time_buttons[i:i + num_buttons_per_row] for i in range(0, len(time_buttons), num_buttons_per_row)]

    time_selection_headers = {
        'start': {
            'en': 'Planning to start around...',
            'ru': 'Планирую начать в...',
            'es': 'Planeo comenzar alrededor de...',
            'fr': 'Je prévois de commencer vers...',
            'uk': 'Планую почати о...',
            'pl': 'Planuję rozpocząć około...',
            'de': 'Ich plane zu beginnen um...',
            'it': 'Prevedo di iniziare intorno alle...'
        },
        'end': {
            'en': 'Planning to end around...',
            'ru': 'Планирую окончание около...',
            'es': 'Planeo terminar alrededor de...',
            'fr': 'Je prévois de terminer vers...',
            'uk': 'Планую закінчити приблизно о...',
            'pl': 'Planuję zakończyć około...',
            'de': 'Ich plane zu beenden um...',
            'it': 'Prevedo di finire intorno alle...'
        }
    }
    selection_text = time_selection_headers[stage].get(language, "Select start and end time (minimum duration 2 hours)")

    keyboard = [
        [InlineKeyboardButton(selection_text, callback_data='none')]
    ] + rows

    return InlineKeyboardMarkup(keyboard)

def language_selection_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 EN", callback_data='lang_en'),
            InlineKeyboardButton("🇷🇺 RU", callback_data='lang_ru'),
            InlineKeyboardButton("🇪🇸 ES", callback_data='lang_es'),
            InlineKeyboardButton("🇫🇷 FR", callback_data='lang_fr')
        ],
        [
            InlineKeyboardButton("🇺🇦 UA", callback_data='lang_uk'),
            InlineKeyboardButton("🇵🇱 PL", callback_data='lang_pl'),
            InlineKeyboardButton("🇩🇪 DE", callback_data='lang_de'),
            InlineKeyboardButton("🇮🇹 IT", callback_data='lang_it')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def yes_no_keyboard(language):
    texts = {
        'en': {'yes': 'Yes', 'no': 'No'},
        'ru': {'yes': 'Да', 'no': 'Назад'},
        'es': {'yes': 'Sí', 'no': 'No'},
        'fr': {'yes': 'Oui', 'no': 'Non'},
        'uk': {'yes': 'Так', 'no': 'Назад'},
        'pl': {'yes': 'Tak', 'no': 'Nie'},
        'de': {'yes': 'Ja', 'no': 'Nein'},
        'it': {'yes': 'Sì', 'no': 'No'}
    }

    keyboard = [
        [
            InlineKeyboardButton(texts[language]['yes'], callback_data='yes'),
            InlineKeyboardButton(texts[language]['no'], callback_data='no')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_person_selection_keyboard(language):
    person_buttons = [InlineKeyboardButton(f"🟢 {i}", callback_data=f'person_{i}') for i in range(2, 22)]
    num_buttons_per_row = 7
    rows = [person_buttons[i:i + num_buttons_per_row] for i in range(0, len(person_buttons), num_buttons_per_row)]
    return InlineKeyboardMarkup(rows)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def generate_party_styles_keyboard(language):
    styles = {
        'en': [
            ("🟢 Classic", "🟢 Child's Birthday"),
            ("🟢 Jubilee", "🟢 Adult's Birthday"),
            ("🟢 Romantic", "🟢 Starry Evening"),
            ("🟢 Picnic in the Park", "🟢 Seminars"),
            ("🟢 Team Building", "🟢 Masterclasses")
        ],
        'ru': [
            ("🟢 Классика", "🟢 Детский ДР"),
            ("🟢 Юбилей", "🟢 Взрослый ДР"),
            ("🟢 Романтик", "🟢 Звездный вечер"),
            ("🟢 Пикник в парке", "🟢 Семинар"),
            ("🟢 Тимбилдинг", "🟢 Мастер-классы")
        ],
        'es': [
            ("🟢 Desayuno en el mar", "🟢 Chicha"),
            ("🟢 Cena romántica", "🟢 Seminario"),
            ("🟢 Cena con velas", "🟢 Team building"),
            ("🟢 Aniversario", "🟢 Reunión familiar"),
            ("🟢 Cumpleaños adulto", "🟢 Clásico")
        ],
        'fr': [
            ("🟢 Chicha", "🟢 Dîner en bord de mer"),
            ("🟢 Romantique", "🟢 Conférences"),
            ("🟢 Classique", "🟢 Annivers. enfant"),
            ("🟢 Team building", "🟢 Picnic au parc"),
            ("🟢 Anniv. adulte", "🟢 Soirée étoiles")
        ],
        'uk': [
            ("🟢 Класичний", "🟢 ДР дитини"),
            ("🟢 Романтичний", "🟢 Тімбілдінг"),
            ("🟢 Морський сніданок", "🟢 Ювілей"),
            ("🟢 Вечеря під зорями", "🟢 Кальян"),
            ("🟢 Пікнік у парку", "🟢 Семінари")
        ],
        'pl': [
            ("🟢 Romantyczny", "🟢 Wieczór gwiazd"),
            ("🟢 Urodziny dorosłego", "🟢 Shisha"),
            ("🟢 Klasyczny", "🟢 Urodziny dziecka"),
            ("🟢 Morski śniadanie", "🟢 Jubileusz"),
            ("🟢 Piknik w parku", "🟢 Integracja")
        ],
        'de': [
            ("🟢 Klassik", "🟢 Sternenabend"),
            ("🟢 Erwachsenen Geburtstag", "🟢 Shisha"),
            ("🟢 Romantik", "🟢 Geburtstag Kind"),
            ("🟢 Frühstück am Meer", "🟢 Jubiläum"),
            ("🟢 Picknick im Park", "🟢 Teambildung")
        ],
        'it': [
            ("🟢 Colazione sul mare", "🟢 Shisha"),
            ("🟢 Romantico", "🟢 Seminari"),
            ("🟢 Classico", "🟢 Compleanno bambino"),
            ("🟢 Colazione al mare", "🟢 Anniversario"),
            ("🟢 Picnic nel parco", "🟢 Team building")
        ]
    }

    keyboard = []
    for left_text, right_text in styles[language]:
        # Используем пробелы для растяжения кнопок
        button_text = f"{left_text} {' ' * 10} {right_text}"
        keyboard.append([
            InlineKeyboardButton(button_text, callback_data=f'style_{left_text.strip("🟢 ")}')
        ])

    return InlineKeyboardMarkup(keyboard)
