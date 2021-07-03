import logging
import asyncio
import os

from pyrogram import Client, filters


logging.basicConfig(
    format='%(levelname)5s - %(name)s - %(message)s',
    level=0
)
LOGGER = logging.getLogger("root")
LOGGER.setLevel(logging._nameToLevel[os.environ.get("log_level", "NOTSET").upper()])


string_session = os.environ.get("string_session")
api_id = os.environ.get("api_id")
api_hash = os.environ.get("api_hash")

group_a = int(os.environ.get("group_a"))
group_b = int(os.environ.get("group_b"))

password = os.environ.get("password", None)

client = Client(
    string_session,
    int(api_id),
    api_hash,
    password=password
)
basic_filters = filters.group & ~filters.edited & ~filters.service


@client.on_message(filters.chat(group_a) & basic_filters)
async def group_a_to_group_b(client, event):
    await client.forward_messages(group_b, event.chat.id, event.message_id, as_copy=True)


@client.on_message(filters.chat(group_b) & basic_filters)
async def group_b_to_group_a(client, event):
    await client.forward_messages(group_a, event.chat.id, event.message_id, as_copy=True)


if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()
    loop.run_until_complete(client.run())
