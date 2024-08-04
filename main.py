import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters
import logging
import os
from datetime import datetime, timedelta
import sqlite3

from keyboards import language_selection_keyboard, yes_no_keyboard, generate_calendar_keyboard, \
    generate_time_selection_keyboard, generate_person_selection_keyboard, generate_party_styles_keyboard

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Пути к видеофайлам
VIDEO_PATHS = [
    'media/IMG_5981 (online-video-cutter.com).mp4',
    'media/IMG_6156 (online-video-cutter.com).mp4',
    'media/IMG_4077_1 (online-video-cutter.com).mp4',
    'media/IMG_6412 (online-video-cutter.com).mp4'
]

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = 'YOUR_BOT_TOKEN'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_data['step'] = 'start'
    if update.message:
        await update.message.reply_text(
            "Choose your language / Выберите язык / Elige tu idioma",
            reply_markup=language_selection_keyboard()
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            "Choose your language / Выберите язык / Elige tu idioma",
            reply_markup=language_selection_keyboard()
        )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_data = context.user_data

    time_set_texts = {
        'start_time': {
            'en': 'Start time set to {}. Now select end time.',
            'ru': 'Время начала установлено на {}. Теперь выберите время окончания.',
            'es': 'La hora de inicio se ha establecido en {}. Ahora selecciona la hora de finalización.',
            'fr': 'L\'heure de début est fixée à {}. Maintenant, sélectionnez l\'heure de fin.',
            'uk': 'Час початку встановлено на {}. Тепер виберіть час закінчення.',
            'pl': 'Czas rozpoczęcia ustawiono na {}. Teraz wybierz czas zakończenia.',
            'de': 'Startzeit auf {} gesetzt. Wählen Sie nun die Endzeit.',
            'it': 'L\'ora di inizio è stata impostata su {}. Ora seleziona l\'ora di fine.'
        },
        'end_time': {
            'en': 'End time set to {}. Confirm your selection.',
            'ru': 'Время окончания установлено на {}. Подтвердите свой выбор.',
            'es': 'La hora de finalización se ha establecido en {}. Confirma tu selección.',
            'fr': 'L\'heure de fin est fixée à {}. Confirmez votre sélection.',
            'uk': 'Час закінчення встановлено на {}. Підтвердіть свій вибір.',
            'pl': 'Czas zakończenia ustawiono na {}. Potwierdź swój wybór.',
            'de': 'Endzeit auf {} gesetzt. Bestätigen Sie Ihre Auswahl.',
            'it': 'L\'ora di fine è stata impostata su {}. Conferma la tua selezione.'
        }
    }

    time_selection_headers = {
        'start': {
            'en': 'Select start and end time (minimum duration 2 hours)',
            'ru': 'Выберите время начала и окончания (минимальная продолжительность 2 часа)',
            'es': 'Selecciona la hora de inicio y fin (duración mínima 2 horas)',
            'fr': 'Sélectionnez l\'heure de début et de fin (durée minimale 2 heures)',
            'uk': 'Виберіть час початку та закінчення (мінімальна тривалість 2 години)',
            'pl': 'Wybierz czas rozpoczęcia i zakończenia (minimalny czas trwania 2 godziny)',
            'de': 'Wählen Sie Start- und Endzeit (Mindestdauer 2 Stunden)',
            'it': 'Seleziona l\'ora di inizio e fine (durata minima 2 ore)'
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

    people_selection_headers = {
        'en': 'How many people are attending?',
        'ru': 'На сколько персон твоя встреча?',
        'es': '¿Cuántas personas asistirán?',
        'fr': 'Combien de personnes participent?',
        'uk': 'На скільки персон твоя зустріч?',
        'pl': 'Ile osób będzie uczestniczyć?',
        'de': 'Wie viele Personen nehmen teil?',
        'it': 'Quante persone parteciperanno?'
    }

    party_styles_headers = {
        'en': 'What style do you choose?',
        'ru': 'Какой стиль ты выбираешь?',
        'es': '¿Qué estilo eliges?',
        'fr': 'Quel style choisis-tu?',
        'uk': 'Який стиль ти обираєш?',
        'pl': 'Jaki styl wybierasz?',
        'de': 'Welchen Stil wählst du?',
        'it': 'Che stile scegli?'
    }

    if query.data.startswith('lang_'):
        language_code = query.data.split('_')[1]
        user_data['language'] = language_code
        user_data['step'] = 'greeting'

        # Отправляем сообщение с "ожиданием" на выбранном языке
        loading_texts = {
            'en': 'Loading...',
            'ru': 'Ожидай...',
            'es': 'Cargando...',
            'fr': 'Chargement...',
            'uk': 'Завантаження...',
            'pl': 'Ładowanie...',
            'de': 'Laden...',
            'it': 'Caricamento...'
        }
        loading_message = await query.message.reply_text(
            loading_texts.get(language_code, 'Loading...'),
        )

        # Выбор случайного видео
        video_path = random.choice(VIDEO_PATHS)

        # Загрузка видео и обновление сообщения
        if os.path.exists(video_path):
            # Отправляем видео как документ
            with open(video_path, 'rb') as video_file:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=video_file,
                    disable_notification=True
                )
                # Удаляем сообщение с "ожиданием"
                await loading_message.delete()
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Video file not found.")
            await loading_message.delete()

        greeting_texts = {
            'en': 'Hello! What is your name?',
            'ru': 'Привет! Как вас зовут?',
            'es': '¡Hola! ¿Cómo te llamas?',
            'fr': 'Salut! Quel est votre nom ?',
            'uk': 'Привіт! Як вас звати?',
            'pl': 'Cześć! Jak masz na imię?',
            'de': 'Hallo! Wie heißt du?',
            'it': 'Ciao! Come ti chiami?'
        }
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=greeting_texts.get(language_code, 'Hello! What is your name?')
        )

    elif query.data == 'yes':
        if user_data['step'] == 'name_received':
            user_data['step'] = 'calendar'
            await show_calendar(query, user_data.get('month_offset', 0), user_data.get('language', 'en'))
        elif user_data['step'] == 'date_confirmation':
            user_data['step'] = 'time_selection'
            await query.message.reply_text(
                time_selection_headers['start'].get(user_data['language'],
                                                    "Select start and end time (minimum duration 2 hours)"),
                reply_markup=generate
            )

            ### 1. Создание скрипта `init_db.py` для инициализации базы данных

#            python
            import sqlite3


def create_db():
    conn = sqlite3.connect('preferences.db')
    cursor = conn.cursor()

    # Создание таблицы для хранения предпочтений пользователя
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS preferences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_db()
