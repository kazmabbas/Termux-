from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config



ask_ques = "** انشـاء جلـسة سيـشن **"
buttons_ques = [
    [
        InlineKeyboardButton("بايࢪوجـرام", callback_data="pyrogram"),
        InlineKeyboardButton("تيـليثـون", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("بايروجـرام بـوت", callback_data="pyrogram_bot"),
        InlineKeyboardButton("تليثـون بـوت", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="انشـاء جلـسة سيـشن", callback_data="generate")
    ]
]




@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if telethon:
        ty = "** تيـليثـون **"
    else:
        ty = "** بايࢪوجـرام **"
    if is_bot:
        ty += "** بـوت **"
    await msg.reply(f"** جـاࢪ عمـل كـود سيـشن **{ty}** ... **")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "** ارسـل ايبـي ايـدي \n للـتخطي اࢪسـل /skip **", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("⎆ **هنـاك مشـكلـة! يࢪجـى تأكـد مـن الايبـي ايـدي /start**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "**اࢪسـل ايبـي هـاش**", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "**اࢪسـل رقـم الهاتـف الخـاص بـك مـع كـتابـة رمـز الـدولة \nمثـال : +9640000000000**"
    else:
        t = " ** يرجـى اࢪسال تـوكن الـبوت **"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("** يـتم اࢪسـال الكـود **")
    else:
        await msg.reply("** يـتم تسجيـل دخـول الـى توكـن البـوت **")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply("** يوجـد خطـأ فـي الايـبيات **", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("** رقـم الهاتـف خطـأ اࢪسـال رقـم الهاتـف مـع رمـز الـدولـة الخـاصـة بـك **", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "** تـم اࢪسـال كـود تـسجيـل الـدخـول من شـركـة Telegram \n\n اࢪسـل كـود الدخـول بهـذا الـتࢪتيـب \n اذا كان كـود تسـجيـل بـهذا الشـكـل 29915 \n اࢪسل الكـود بهـذا الـتࢪتيـب 5 1 9 9 2 \n مـع وجـود مسـافـات بـين كـل الاࢪقـام **", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("** لقـد تجـاوزت الحـد الزمـني 10 دقائـق **", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("** رقـم الهـاتف خطـأ رجـاءً ارسـال رقـم الهاتـف مـع رمز الدولـة الخـاصة بـك **", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("** كـود التـحقـق خـطأ الࢪجـاء الأسـتخـراج مـره اخـرى والتأكـد من وضـع فـࢪاغ بيـن الأرقام **", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await bot.ask(user_id, "** اࢪسـل رمـز التـحقـق **", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("** انتـهت مهلـة استـخراج الجلسـة يࢪجـى اعـادة مـن جديـد /start **", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await two_step_msg.reply("** خطـأ؟ يࢪجـى اعـادة استـخراج مـن جديـد وتأكـد مـن اࢪسـال رمـز التـحقـق **", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"** كـود سيـشن {ty} ** \n\n ** `{string_session}` ** \n\n** تم الاستخـراج بواسطـة @BThonTBoT **"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "** تم استخـراج كـود سيـشن {} \n  تم اࢪسـال الكـود الـى الرسـائـل المـحفوظـة **".format("** تيـليثـون **" if telethon else "** بايࢪوجـرام **"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("**تم الغـاء عمـلية الاسـتخراج**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("**تم ترسيـت البـوت**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("**تم إلغـاء الجلسـة**", quote=True)
        return True
    else:
        return False
