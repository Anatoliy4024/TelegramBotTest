from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters
import logging
import os
import asyncio

from keyboards import language_selection_keyboard, yes_no_keyboard, generate_calendar_keyboard, generate_time_selection_keyboard

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Добавьте путь к вашему видеофайлу
VIDEO_PATH = 'media/IMG_4077_1 (online-video-cutter.com).mp4'  # Укажите здесь путь к вашему видеофайлу

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
BOT_TOKEN = '7407529729:AAErOT5NBpMSO-V-HPAW-MDu_1WQt0TtXng'

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
    user_id = query.from_user.id

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

        # Загрузка видео и обновление сообщения
        if os.path.exists(VIDEO_PATH):
            # Отправляем видео после загрузки
            with open(VIDEO_PATH, 'rb') as video_file:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=video_file)
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
        await query.message.reply_text(greeting_texts.get(language_code, 'Hello! What is your name?'))

    elif query.data == 'yes':
        if user_data['step'] == 'name_received':
            user_data['step'] = 'calendar'
            await show_calendar(query, user_data.get('month_offset', 0), user_data.get('language', 'en'))
        elif user_data['step'] == 'date_confirmation':
            user_data['step'] = 'time_selection'
            time_selection_texts = {
                'en': "Select start and end time (minimum duration 2 hours)",
                'ru': "Выберите время начала и окончания (минимальная продолжительность 2 часа)",
                'es': "Selecciona la hora de inicio y fin (duración mínima 2 horas)",
                'fr': "Sélectionnez l'heure de début et de fin (durée minimale 2 heures)",
                'uk': "Виберіть час початку та закінчення (мінімальна тривалість 2 години)",
                'pl': "Wybierz czas rozpoczęcia i zakończenia (minimalny czas trwania 2 godziny)",
                'de': "Wählen Sie Start- und Endzeit (Mindestdauer 2 Stunden)",
                'it': "Seleziona l'ora di inizio e fine (durata minima 2 ore)"
            }
            await query.message.reply_text(
                time_selection_texts.get(user_data['language'], "Select start and end time (minimum duration 2 hours)"),
                reply_markup=generate_time_selection_keyboard(user_data['language'])  # Передаем язык в клавиатуру
            )

    elif query.data == 'no':
        if user_data['step'] == 'calendar':
            user_data['step'] = 'name_received'
            await handle_name(query, context)
        elif user_data['step'] == 'date_confirmation':
            user_data['step'] = 'calendar'
            await show_calendar(query, user_data.get('month_offset', 0), user_data.get('language', 'en'))
        elif user_data['step'] == 'name_received':
            user_data['step'] = 'greeting'
            await start(update, context)

    elif query.data.startswith('date_'):
        selected_date = query.data.split('_')[1]
        user_data['step'] = 'date_confirmation'
        user_data['selected_date'] = selected_date

        # Меняем цвет кнопки на красный и делаем ее неактивной
        await query.edit_message_reply_markup(reply_markup=update_calendar_markup(query.message.reply_markup, selected_date))

        confirmation_texts = {
            'en': f'You selected {selected_date}, correct?',
            'ru': f'Вы выбрали {selected_date}, правильно?',
            'es': f'Seleccionaste {selected_date}, ¿correcto?',
            'fr': f'Vous avez sélectionné {selected_date}, correct ?',
            'uk': f'Ви вибрали {selected_date}, правильно?',
            'pl': f'Wybrałeś {selected_date}, poprawne?',
            'de': f'Sie haben {selected_date} gewählt, richtig?',
            'it': f'Hai selezionato {selected_date}, corretto?'
        }
        await query.message.reply_text(
            confirmation_texts.get(user_data['language'], f'You selected {selected_date}, correct?'),
            reply_markup=yes_no_keyboard(user_data['language'])
        )

    elif query.data.startswith('time_'):
        selected_time = query.data.split('_')[1]
        if 'start_time' not in user_data:
            user_data['start_time'] = selected_time
            await query.message.reply_text(f'Start time set to {selected_time}. Now select end time.',
                                          reply_markup=generate_time_selection_keyboard(user_data['language']))  # Передаем язык в клавиатуру
        else:
            user_data['end_time'] = selected_time
            user_data['step'] = 'confirm'
            await query.message.reply_text(f'End time set to {selected_time}. Confirm your selection.',
                                          reply_markup=yes_no_keyboard(user_data.get('language', 'en')))

    elif query.data.startswith('prev_month_') or query.data.startswith('next_month_'):
        month_offset = int(query.data.split('_')[2])
        user_data['month_offset'] = month_offset
        await show_calendar(query, month_offset, user_data.get('language', 'en'))

async def show_calendar(query, month_offset, language):
    # Ограничиваем смещение месяцев: один месяц назад и два месяца вперед
    if month_offset < -1:
        month_offset = -1
    elif month_offset > 2:
        month_offset = 2

    calendar_keyboard = generate_calendar_keyboard(month_offset, language)  # Передаем язык в календарь

    select_date_text = {
        'en': "Select a date:",
        'ru': "Выберите дату:",
        'es': "Seleccione una fecha:",
        'fr': "Sélectionnez une date:",
        'uk': "Виберіть дату:",
        'pl': "Wybierz datę:",
        'de': "Wählen Sie ein Datum:",
        'it': "Seleziona una data:"
    }

    await query.message.reply_text(
        select_date_text.get(language, 'Select a date:'),
        reply_markup=calendar_keyboard
    )

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    if update.callback_query:
        user_data['name'] = "Имя пользователя"
    else:
        user_data['name'] = update.message.text

    user_data['step'] = 'name_received'

    language_code = user_data.get('language', 'en')

    greeting_texts = {
        'en': f'Hello {user_data["name"]}! Do you want to see available dates?',
        'ru': f'Привет {user_data["name"]}! Хочешь увидеть доступные даты?',
        'es': f'Hola {user_data["name"]}! ¿Quieres ver las fechas disponibles?',
        'fr': f'Bonjour {user_data["name"]}! Voulez-vous voir les dates disponibles?',
        'uk': f'Привіт, {user_data["name"]}! Хочеш подивитися які дати доступні?',
        'pl': f'Cześć {user_data["name"]}! Chcesz zobaczyć dostępne daty?',
        'de': f'Hallo {user_data["name"]}! Möchten Sie verfügbare Daten sehen?',
        'it': f'Ciao {user_data["name"]}! Vuoi vedere le date disponibili?'
    }

    if update.message:
        await update.message.reply_text(
            greeting_texts.get(language_code, f'Hello {user_data["name"]}! Do you want to see available dates?'),
            reply_markup=yes_no_keyboard(language_code)
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            greeting_texts.get(language_code, f'Hello {user_data["name"]}! Do you want to see available dates?'),
            reply_markup=yes_no_keyboard(language_code)
        )

def update_calendar_markup(reply_markup, selected_date):
    new_keyboard = []
    for row in reply_markup.inline_keyboard:
        new_row = []
        for button in row:
            if button.callback_data and button.callback_data.endswith(selected_date):
                new_row.append(InlineKeyboardButton(f"🔴 {selected_date.split('-')[2]}", callback_data='none'))
            else:
                new_row.append(button)
        new_keyboard.append(new_row)
    return InlineKeyboardMarkup(new_keyboard)

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))

    application.run_polling()
