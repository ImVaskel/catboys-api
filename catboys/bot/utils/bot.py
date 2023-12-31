from __future__ import annotations

from discord.ext import commands
import discord
from catboys.bot.utils.views import DynamicRejectionButton, DynamicSubmissionButton

COGS = ["cogs.submit", "jishaku"]


class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or("$"), intents=intents, **kwargs
        )

    async def setup_hook(self):
        for cog in COGS:
            try:
                await self.load_extension(cog)
            except Exception as exc:
                print(
                    f"Could not load extension {cog} due to {exc.__class__.__name__}: {exc}"
                )

        self.add_dynamic_items(DynamicRejectionButton, DynamicSubmissionButton)

    async def on_ready(self):
        print(f"Logged on as {self.user} (ID: {self.user.id})")
