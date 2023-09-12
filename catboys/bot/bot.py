#!/usr/bin/env python3

import discord
from catboys.bot.utils.bot import Bot
from catboys.core import settings


intents = discord.Intents.default()
intents.message_content = True
bot = Bot(intents=intents)

bot.run(settings.token)
