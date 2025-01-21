from telethon.tl.functions.messages import ImportChatInviteRequest
import random
from .. import loader, utils

@loader.tds
class Lolicom(loader.Module):
    """
    Рандомные лоли комиксы (даже внутри)
    """

    strings = {
        "name": "Lolicom",
        "forwarding": "Ща все будет",
        "done": "✅ Ну вот",
        "error": "❌ Ошибка: {}",
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.command(
        ru_doc="да",
        en_doc="yea",
    )
    async def lolicom(self, message):
        """
        Лоли комиксы (nsfw)
        """
        chat_invite_link = "https://t.me/+lyeUtv7ExmBlZDYy"

        try:
            entity = await self.client.get_entity(chat_invite_link)
        except Exception:
            try:
                await self.client(ImportChatInviteRequest(chat_invite_link.split("+")[1]))
            except Exception as e:
                await utils.answer(message, self.strings["error"].format(e))
                return

        await utils.answer(message, self.strings["forwarding"])
        try:
            messages = await self.client.get_messages(entity, limit=300)
            random_msg = random.choice(messages)

            if random_msg:
                await self.client.send_message(message.to_id, random_msg.message, file=random_msg.media)
                await utils.answer(message, self.strings["done"])
            else:
                await utils.answer(message, "❌ Сообщения не найдены (скорее всегда пезда)")
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(e))