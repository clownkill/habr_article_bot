import logging
import os
from textwrap import dedent

from environs import Env
from telegram import ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

from habr_parser import parse_habr_article, save_article, get_article_filename


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def error(error):
    logger.warning(f"Bot caused error {error}")


def start_command(update, context):
    user = update.effective_user
    message_text = f"""Привет, <b>{user.mention_html()}</b>!
Можешь прислать мне ссылку на статью с <a>habr.com</a>
и я попробую прочитать ее для тебя"""

    update.message.reply_html(
        dedent(message_text),
        reply_markup=ForceReply(selective=True),
    )


def help_command(update, context):
    message_text = """Я умею читать статьи с <i><b>habr.com</b></i>,
и озвучивать их содержимое для тебя.
Чтобы получить аудиофайл статьи, пришли мне ссылку на нее
    """
    update.message.reply_html(
        dedent(message_text),
        reply_markup=ForceReply(selective=True),
    )


def get_send_audio_article(update, context):
    url = update.message.text
    article_title, article_body = parse_habr_article(url)
    filename = get_article_filename(article_title)

    update.message.reply_text("Я уже начал читать статью придется подождать немного")
    save_article(article_title, article_body)

    with open(filename, "rb") as f:
        context.bot.send_audio(
            chat_id=update.effective_chat.id,
            audio=f,
        )

    os.remove(filename)


def wrong_message(update, context):
    user = update.effective_user
    message_text = f"""<b>{user.mention_html()}</b>!
    Я пока могу читать только статьи с  <a>habr.com</a>
    пришли мне ссылку оттуда"""

    update.message.reply_html(
        dedent(message_text),
        reply_markup=ForceReply(selective=True),
    )


def main():
    env = Env()
    env.read_env()

    tg_token = env.str("TELEGRAM_TOKEN")

    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(
        MessageHandler(
            Filters.entity("url") & Filters.regex(r"https:\/\/habr\.com.*"),
            get_send_audio_article,
        )
    )
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, wrong_message)
    )

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
