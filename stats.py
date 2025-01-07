import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class UserStats(loader.Module):
    """Модуль для подсчёта сообщение пользователя а виде столбчатой диаграммы"""

    strings = {
        "name": "UserStats",
        "no_data": "Нет данных для отображения.",
        "calculating": "Считаю статистику...",
        "done": "Готово, вот статистика ",
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def stats(self, message: Message):
        """
        Подсчёт статистики сообщений пользователя.
        .stats <@юзернейм или ID>
        """
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Укажите пользователя (ID или юзернейм).")
            return

        target = await self.client.get_entity(args)
        chat = message.chat_id

        await utils.answer(message, self.strings["calculating"])

        # сбор
        now = datetime.now()
        stats = {
            "today": 0,
            "yesterday": 0,
            "week": 0,
            "month": 0,
            "year": 0,
            "all_time": 0,
        }

        async for msg in self.client.iter_messages(chat, from_user=target.id):
            stats["all_time"] += 1
            msg_date = msg.date.replace(tzinfo=None)

            if msg_date.date() == now.date():
                stats["today"] += 1
            elif msg_date.date() == (now - timedelta(days=1)).date():
                stats["yesterday"] += 1
            if now - timedelta(weeks=1) <= msg_date:
                stats["week"] += 1
            if now - timedelta(days=30) <= msg_date:
                stats["month"] += 1
            if now - timedelta(days=365) <= msg_date:
                stats["year"] += 1

        if stats["all_time"] == 0:
            await utils.answer(message, self.strings["no_data"])
            return

        # График
        labels = ["Сегодня", "Вчера", "Неделя", "Месяц", "Год", "Все время"]
        values = [
            stats["today"],
            stats["yesterday"],
            stats["week"],
            stats["month"],
            stats["year"],
            stats["all_time"],
        ]

        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color="skyblue")
        plt.title(f"Статистика сообщений {target.first_name}")
        plt.xlabel("Период")
        plt.ylabel("Количество сообщений")
        plt.grid(axis="y")

        file_path = f"/tmp/stats_{target.id}.png"
        plt.savefig(file_path)
        plt.close()

        await self.client.send_file(chat, file_path, caption=self.strings["done"])
        os.remove(file_path)
