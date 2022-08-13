from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from habr_parser import get_last_articles


def get_paginator(articles, per_page):
    items_per_page = per_page
    max_page = len(articles) // items_per_page

    start = 0
    end = items_per_page

    paginated_articles = []

    for _ in range(max_page):
        paginated_articles.append(articles[start:end])
        start = end
        end += items_per_page

    return paginated_articles


def get_main_menu(last_articles, page=0):
    articles = get_paginator(list(last_articles.keys()), 5)

    inline_keyboard = [
        [InlineKeyboardButton(article, callback_data=last_articles[article])]
        for article in articles[page]
    ]

    if page == len(articles) - 1:
        inline_keyboard.append(
            [InlineKeyboardButton("Назад", callback_data=f"pag, {page - 1}")]
        )
    elif page == 0:
        inline_keyboard.append(
            [InlineKeyboardButton("Вперед", callback_data=f"pag, {page + 1}")]
        )
    else:
        inline_keyboard.append(
            [
                InlineKeyboardButton("Назад", callback_data=f"pag, {page - 1}"),
                InlineKeyboardButton("Вперед", callback_data=f"pag, {page + 1}"),
            ]
        )

    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup
