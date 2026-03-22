"""Garrison command schema for Valheim (via ValheimPlus RCON)."""


def get_commands():
    from app.plugins.base import CommandDef, CommandParam

    return [
        # ── PLAYER MANAGEMENT ─────────────────────────────────────────
        CommandDef(
            name="listplayers",
            description="List all connected players",
            category="PLAYER_MGMT",
            example="listplayers",
        ),
        CommandDef(
            name="kick",
            description="Kick a player from the server",
            category="PLAYER_MGMT",
            params=[
                CommandParam(name="name", type="string", description="Player name or SteamID"),
            ],
            example="kick PlayerName",
        ),
        CommandDef(
            name="ban",
            description="Ban a player (add to banlist)",
            category="MODERATION",
            params=[
                CommandParam(name="name", type="string", description="Player name or SteamID"),
            ],
            example="banned add PlayerName",
        ),
        CommandDef(
            name="unban",
            description="Unban a player (remove from banlist)",
            category="MODERATION",
            params=[
                CommandParam(name="name", type="string", description="Player name or SteamID"),
            ],
            example="banned remove PlayerName",
        ),
        CommandDef(
            name="banned",
            description="Show the banlist",
            category="MODERATION",
            params=[
                CommandParam(
                    name="action",
                    type="choice",
                    description="Action to perform",
                    choices=["list", "add", "remove"],
                ),
                CommandParam(name="name", type="string", required=False, description="Player name or SteamID"),
            ],
            example="banned list",
        ),

        # ── SERVER ────────────────────────────────────────────────────
        CommandDef(
            name="say",
            description="Broadcast a message to all players",
            category="SERVER",
            params=[
                CommandParam(name="message", type="string", description="Message to broadcast"),
            ],
            example="say Hello world",
        ),
        CommandDef(
            name="save",
            description="Force save the world",
            category="SERVER",
            example="save",
        ),
        CommandDef(
            name="quit",
            description="Save and shut down the server",
            category="SERVER",
            example="quit",
        ),
        CommandDef(
            name="help",
            description="List available RCON commands",
            category="ADMIN",
            example="help",
        ),
    ]
