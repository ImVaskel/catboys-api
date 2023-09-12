from __future__ import annotations

import re
from typing import TYPE_CHECKING
import uuid
import discord
from sqlalchemy import select


from catboys.db import async_session, models

if TYPE_CHECKING:
    from catboys.bot.utils.bot import Bot
    from sqlalchemy.ext.asyncio import AsyncSession

UUID_REGEX = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


class DynamicSubmissionButton(
    discord.ui.DynamicItem[discord.ui.Button], template=rf"confirm:user:({UUID_REGEX})"
):
    def __init__(self, uid: uuid.UUID):
        super().__init__(
            discord.ui.Button(
                label="Approve",
                style=discord.ButtonStyle.green,
                custom_id=f"confirm:user:{uid}",
                emoji="\N{THUMBS UP SIGN}",
            )
        )
        self.uid: uuid.uuid4 = uid

    @classmethod
    async def from_custom_id(
        cls,
        interaction: discord.Interaction,
        item: discord.ui.Button,
        match: re.Match[str],
        /,
    ):
        uid = match.group(1)
        return cls(uid)

    async def interaction_check(self, interaction: discord.Interaction[Bot]) -> bool:
        return await interaction.client.is_owner(interaction.user)

    async def callback(self, interaction: discord.Interaction) -> None:
        async with async_session() as session:
            async with session.begin():
                session: AsyncSession
                submissions = await session.execute(
                    select(models.Submission).where(
                        models.Submission.id == str(self.uid)
                    )
                )
                submission = submissions.scalars().first()
                if submission:
                    new_media = models.Media(
                        url=str(submission.url),
                        artist_url=str(submission.artist_url),
                        artist_name=str(submission.artist_name),
                        source_url=str(submission.source_url),
                        anime=str(submission.anime),
                        id=submission.id,
                    )
                    session.add(new_media)
                    await session.commit()
                    await interaction.response.send_message(
                        "Picture approved.", ephemeral=True
                    )
                    await interaction.message.delete()
                    try:
                        user = interaction.client.get_user(submission.submitter)
                        await user.send("Congrats! Your submission was approved!")
                    except:
                        pass
                else:
                    await interaction.response.send_message(
                        "Could not find the submission in the database. Was it already approved?",
                        ephemeral=True,
                    )


class DynamicRejectionButton(
    discord.ui.DynamicItem[discord.ui.Button], template=rf"reject:user:({UUID_REGEX})"
):
    def __init__(self, uid: uuid.UUID):
        super().__init__(
            discord.ui.Button(
                label="Reject",
                style=discord.ButtonStyle.red,
                custom_id=f"reject:user:{uid}",
                emoji="\N{THUMBS DOWN SIGN}",
            )
        )
        self.uid: int = uid

    @classmethod
    async def from_custom_id(
        cls,
        interaction: discord.Interaction,
        item: discord.ui.Button,
        match: re.Match[str],
        /,
    ):
        uid = match.group(1)
        return cls(uid)

    async def interaction_check(self, interaction: discord.Interaction[Bot]) -> bool:
        return await interaction.client.is_owner(interaction.user)

    async def callback(self, interaction: discord.Interaction) -> None:
        async with async_session() as session:
            async with session.begin():
                session: AsyncSession
                submissions = await session.execute(
                    select(models.Submission).where(
                        models.Submission.id == str(self.uid)
                    )
                )
                submission = submissions.scalars().first()
                if submission:
                    session.delete(submission)
                    await session.commit()
                    await interaction.response.send_message(
                        "Picture denied.", ephemeral=True
                    )
                    await interaction.message.delete()
                    try:
                        user = interaction.client.get_user(submission.submitter)
                        await user.send(
                            "Hello, unfortunately your submission was rejected."
                        )
                    except:
                        pass
                else:
                    await interaction.response.send_message(
                        "Could not find the submission in the database. Was it already rejected?",
                        ephemeral=True,
                    )
