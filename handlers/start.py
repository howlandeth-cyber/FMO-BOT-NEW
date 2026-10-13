from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN_USER_ID

class BotStates(StatesGroup):
    waiting_for_chain = State()

async def notify_admin(text: str):
    if ADMIN_USER_ID:
        from config import dp as dp_ref
        try:
            await dp_ref.bot.send_message(ADMIN_USER_ID, text)
        except:
            pass

def register_start_handlers(dp):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "Welcome to Fomo the Trading Bot\n\n"
            "Trade on Solana and EVM chains, and mirror other wallets with copy trading.\n\n"
            "⚠️ Security note: your private key is encrypted at rest, but importing a key always carries risk. Only import keys for wallets you're comfortable dedicating to this bot.",
            reply_markup=get_main_keyboard()
        )
        
        activity_text = f"🟢 NEW USER STARTED BOT\nUser: {message.from_user.id} ({message.from_user.first_name} {message.from_user.last_name or ''})"
        await notify_admin(activity_text)

    @dp.message(F.text == "Start Bot")
    async def handle_main_menu(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer("Choose an option below to get started:", reply_markup=get_main_keyboard())

    @dp.message(F.text == "Buy")
    async def handle_buy_sell(message: types.Message, state: FSMContext):
        await message.answer("Which chain do you want to trade on?", reply_markup=get_chain_selection_keyboard())
        await state.set_state(BotStates.waiting_for_chain)

    @dp.message(F.text.in_(["Solana", "EVM"]))
    async def handle_chain_selection(message: types.Message, state: FSMContext):
        chain = message.text
        await state.update_data(chain=chain)
        
        activity_text = f"🔄 USER CHAIN SELECTION\nUser: {message.from_user.id}\nChain: {chain}"
        await notify_admin(activity_text)
        
        if chain == "Solana":
            await message.answer("Solana selected. Please connect or import your Solana wallet.", reply_markup=get_wallet_keyboard())
        elif chain == "EVM":
            await message.answer("EVM selected. Please connect or import your EVM wallet.", reply_markup=get_wallet_keyboard())
        await state.clear()

    @dp.message(F.text == "Wallet")
    async def handle_wallet(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer("Your Wallets:\n\nNo wallets imported yet.", reply_markup=get_wallet_keyboard())

    @dp.message(F.text == "Back to Menu")
    async def handle_back_to_menu(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer("Back to main menu", reply_markup=get_main_keyboard())