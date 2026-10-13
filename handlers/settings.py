from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import ADMIN_USER_ID
from keyboards import get_main_keyboard

async def notify_admin(text: str):
    if ADMIN_USER_ID:
        from config import dp as dp_ref
        try:
            await dp_ref.bot.send_message(ADMIN_USER_ID, text)
        except:
            pass

async def cmd_settings(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Settings:\n\n"
        "1. Notification Settings\n"
        "2. Trading Preferences\n"
        "3. Account Security\n\n"
        "Use /start to return to main menu.",
        reply_markup=get_main_keyboard()
    )

async def handle_setting_option(message: types.Message):
    options = {
        "Notification Settings": "Notification settings menu", 
        "Trading Preferences": "Trading preferences menu", 
        "Account Security": "Account security settings"
    }
    
    if message.text in options:
        await message.answer(options[message.text], reply_markup=get_main_keyboard())

async def admin_broadcast(message: types.Message, state: FSMContext):
    """Admin broadcast feature"""
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("You are not authorized to use this command.")
        return
    
    await message.answer(
        "📤 Send Message to User:\n\n"
        "Enter User ID to message directly, or type 'all' for broadcast:\n"
        "Then send your message text.\n\n"
        "Example:\n"
        "User ID: 123456789\n"
        "Message: Hello! Here's an important update about the bot.",
        reply_markup=get_main_keyboard()
    )
    await state.set_state(BroadcastStates.waiting_for_target)

async def process_broadcast_target(message: types.Message, state: FSMContext):
    target = message.text.strip()
    await state.update_data(target=target)
    
    await message.answer(
        "Now enter your message text that will be sent to the target user(s):",
        reply_markup=get_main_keyboard()
    )
    await state.set_state(BroadcastStates.waiting_for_message)

async def process_broadcast_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    target = data.get("target")
    
    if target == "all":
        await message.answer("Broadcast to all feature - please specify user IDs manually", reply_markup=get_main_keyboard())
    else:
        try:
            user_id = int(target)
            await message.bot.send_message(user_id, message.text)
            await message.answer(f"✅ Message sent to user {user_id}", reply_markup=get_main_keyboard())
        except ValueError:
            await message.answer("Invalid User ID", reply_markup=get_main_keyboard())
    
    await state.clear()

class BroadcastStates(StatesGroup):
    waiting_for_target = State()
    waiting_for_message = State()

def register_settings_handlers(dp):
    @dp.message(Command("settings"))
    async def settings_cmd(message: types.Message, state: FSMContext):
        await cmd_settings(message, state)

    @dp.message(F.text.in_(["Notification Settings", "Trading Preferences", "Account Security"]))
    async def setting_option_handler(message: types.Message):
        await handle_setting_option(message)
    
    @dp.message(Command("broadcast"))
    async def broadcast_cmd(message: types.Message, state: FSMContext):
        await admin_broadcast(message, state)
    
    @dp.message(F.text == "Broadcast")
    async def broadcast_text_handler(message: types.Message, state: FSMContext):
        await admin_broadcast(message, state)
    
    @dp.message()  # Target user ID
    async def target_user_handler(message: types.Message, state: FSMContext):
        if (await state.get_state()) == BroadcastStates.waiting_for_target:
            await process_broadcast_target(message, state)
    
    @dp.message()  # Message text
    async def message_handler(message: types.Message, state: FSMContext):
        if (await state.get_state()) == BroadcastStates.waiting_for_message:
            await process_broadcast_message(message, state)