from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import get_main_keyboard

from config import ADMIN_USER_ID

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
        "Settings Menu:\n\n"
        "1. /notifications - Notification settings\n"
        "2. /trading_prefs - Trading preferences\n"
        "3. /security - Account security\n\n"
        "Use /start to return to main menu.",
        reply_markup=get_main_keyboard()
    )

async def admin_broadcast(message: types.Message, state: FSMContext):
    """Admin broadcast feature - only admin can use this"""
    if message.from_user.id != ADMIN_USER_ID:
        await message.answer("You are not authorized to use this command.")
        return
    
    await message.answer(
        "Admin Broadcast Mode:\n\n"
        "Send your message to broadcast to all users, or specify User ID:\n\n"
        "Example: `all Hello everyone!` or `123456789 Your message`",
        reply_markup=get_main_keyboard()
    )
    await state.set_state(BroadcastStates.waiting_for_broadcast)

async def process_broadcast(message: types.Message, state: FSMContext):
    data = await state.get_data()
    target = data.get("target", "single")
    
    if target == "all":
        # Simple broadcast - in production would iterate over stored user IDs
        await message.answer("Broadcast to all feature - under construction", reply_markup=get_main_keyboard())
    else:
        try:
            user_id = int(target)
            await message.bot.send_message(user_id, message.text)
            await message.answer(f"Message sent to user {user_id}", reply_markup=get_main_keyboard())
        except ValueError:
            await message.answer("Invalid User ID format", reply_markup=get_main_keyboard())
    
    await state.clear()

class BroadcastStates(StatesGroup):
    waiting_for_broadcast = State()
    waiting_for_target = State()

def register_settings_handlers(dp):
    @dp.message(Command("settings"))
    async def settings_cmd(message: types.Message, state: FSMContext):
        await cmd_settings(message, state)

    @dp.message(Command("broadcast"))
    async def broadcast_cmd(message: types.Message, state: FSMContext):
        await admin_broadcast(message, state)

    @dp.message(F.text == "/broadcast")
    async def broadcast_text_handler(message: types.Message, state: FSMContext):
        await admin_broadcast(message, state)

    @dp.message()  # Target User ID or "all"
    async def broadcast_target_handler(message: types.Message, state: FSMContext):
        if (await state.get_state()) == BroadcastStates.waiting_for_target:
            await process_broadcast(message, state)

    @dp.message()  # Broadcast message text
    async def broadcast_message_handler(message: types.Message, state: FSMContext):
        if (await state.get_state()) == BroadcastStates.waiting_for_broadcast:
            await process_broadcast(message, state)