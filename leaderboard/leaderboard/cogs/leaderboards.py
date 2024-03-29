import logging
import uuid
from typing import Any, List, Optional

import discord
from discord import app_commands
from discord.ext import commands

from .. import actions, data
from ..settings import MOONSTREAM_URL

logger = logging.getLogger(__name__)


class LeaderboardsView(actions.PaginationView):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class LeaderboardsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self._slash_command_data = data.SlashCommandData(
            name="leaderboards",
            description="Check list of all leaderboards in the Discord server",
        )

    @property
    def slash_command_data(self) -> data.SlashCommandData:
        return self._slash_command_data

    async def slash_command_handler(self, interaction: discord.Interaction):
        logger.info(
            actions.prepare_log_message(
                "/leaderboards",
                "SLASH COMMAND",
                interaction.user,
                interaction.guild,
                interaction.channel,
            )
        )

        if interaction.guild is None:
            await interaction.response.send_message(
                embed=discord.Embed(description=data.MESSAGE_GUILD_NOT_FOUND)
            )
            return

        server_config: Optional[data.ResourceConfig] = self.bot.server_configs.get(
            interaction.guild.id
        )
        if server_config is None:
            await interaction.response.send_message(
                embed=discord.Embed(description="Guild not configured")
            )
            return

        if len(server_config.resource_data.leaderboards) == 0:
            await interaction.response.send_message(
                embed=discord.Embed(description="Guild has no linked leaderboards")
            )
            return

        leaderboard_fields = [
            [
                {
                    "field_name": "Short name",
                    "field_value": l.short_name,
                },
                {
                    "field_name": "Title",
                    "field_value": f"[{l.leaderboard_info.title if l.leaderboard_info is not None else '-'}]({MOONSTREAM_URL}/leaderboards/?leaderboard_id={l.leaderboard_id})",
                },
                {
                    "field_name": "Description",
                    "field_value": (
                        l.leaderboard_info.description
                        if l.leaderboard_info is not None
                        else "-"
                    ),
                },
            ]
            for l in server_config.resource_data.leaderboards
        ]

        leaderboards_view = LeaderboardsView(
            title="Linked leaderboards",
            description="",
            wrapped_fields=leaderboard_fields,
        )

        await leaderboards_view.send(interaction)
