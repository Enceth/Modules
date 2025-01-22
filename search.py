from .. import loader, utils

class Search(loader.Module):
    """Модуль для генерации ссылки поиска"""
    strings = {"name": "Search for U"}

    async def ssearchcmd(self, message):
        """Генерация поисковой ссылки.
        Использование: .ssearch <текст для поиска>
        """
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("❌ Укажите текст для поиска!")
            return

        query = "+".join(args.split())
        link = f"https://track24.ru/google/?q={query}"

        await message.edit(f"Давай я поищу за тебя: {link}", link_preview=False)