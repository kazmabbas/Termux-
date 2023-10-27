from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)

@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = (await bot.get_me()).mention
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""** مـࢪحبـاً ** {msg.from_user.mention},
اهـلاً بـك فـي {me2},
بوت استخراج كـود تيرمكـس بـوت أمـن متخطـي البانـد
المطـور : [ƊαᎡᴋ](tg://user?id={OWNER_ID}) !""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=" انشـاء جلسـة ", callback_data="generate")
                ],
                [
                    InlineKeyboardButton("- قنـاة السـورس .", url="https://t.me/BThon"),
                    InlineKeyboardButton("- المطـور .", user_id=OWNER_ID)
                ]
            ]
        ),
        disable_web_page_preview=True,
    )
