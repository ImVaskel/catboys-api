import uuid
from discord import ui
import discord
from discord.ext import commands
from discord.interactions import Interaction
from sqlalchemy.ext.asyncio import AsyncSession

from catboys.bot.utils.bot import Bot
from catboys.bot.utils.views import DynamicRejectionButton, DynamicSubmissionButton
from catboys.core import settings
from catboys.db import models, async_session


class PromptView(ui.View):
    def __init__(self, modal: ui.Modal, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.modal = modal

    async def interaction_check(self, interaction: Interaction[Bot]) -> bool:
        return interaction.user.id == self.modal.ctx.author.id

    @ui.button(label="Click me!")
    async def prompt(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(self.modal)


class SubmitModal(ui.Modal):
    def __init__(self, ctx: commands.Context):
        super().__init__(title="Submit Picture")
        self.ctx = ctx

    url: str = ui.TextInput(label="URL")
    artist_url: str = ui.TextInput(label="Artist URL", required=False)
    artist_name: str = ui.TextInput(label="Artist Name", required=False)
    source_url: str = ui.TextInput(label="Source URL", required=False)
    anime: str = ui.TextInput(label="Anime", required=False)

    async def on_submit(self, interaction: Interaction[Bot]) -> None:
        channel = interaction.client.get_channel(settings.submission_channel_id)
        if not channel:
            await interaction.response.send_message(
                "An error occurred when submitting, please try again later.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            "Thanks for your submission! It will be forwarded for review. If you're approved you'll hear back in a DM!",
            ephemeral=True,
        )

        submission = models.Submission(
            url=str(self.url),
            artist_url=str(self.artist_url),
            artist_name=str(self.artist_name),
            source_url=str(self.source_url),
            anime=str(self.anime),
            submitter=interaction.user.id,
            id=uuid.uuid4(),
        )

        async with async_session() as session:
            async with session.begin():
                session: AsyncSession
                session.add(submission)
                await session.flush()

        embed = discord.Embed(
            title=f"Submission by {interaction.user}",
        )
        embed.set_footer(text=str(submission.id))
        embed.set_image(url=self.url)

        view = discord.ui.View()
        view.add_item(DynamicSubmissionButton(submission.id))
        view.add_item(DynamicRejectionButton(submission.id))

        await channel.send("New Submission!", embed=embed, view=view)


class Submit(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def submit(self, ctx: commands.Context):
        """Starts the process to submit a catboy picture for review."""
        # We're in an application command.
        modal = SubmitModal(ctx)

        if ctx.interaction:
            await ctx.interaction.response.send_modal(modal)
        else:
            await ctx.send(
                "Click on this to open the submit page!", view=PromptView(modal)
            )


async def setup(bot: Bot):
    await bot.add_cog(Submit(bot))
