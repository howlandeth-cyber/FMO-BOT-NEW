from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Start Bot")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_buy_sell_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Buy")
    builder.button(text="Sell")
    builder.button("Back to Menu")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

def get_chain_selection_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Solana")
    builder.button(text="EVM")
    builder.button("Back")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

def get_wallet_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Import Solana Key")
    builder.button(text="Import EVM Key")
    builder.button("Back to Menu")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

def get_import_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Generate New Wallet", callback_data="gen_wallet")
    builder.button(text="Enter Private Key", callback_data="import_key")
    builder.adjust(2)
    return builder.as_markup()

def get_back_to_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Back to Menu")
    return builder.as_markup(resize_keyboard=True)