"""Garrison command schema for Valheim (via ValheimPlus RCON or compatible mod).

NOTE: Vanilla Valheim does NOT support RCON. These commands require:
  - ValheimPlus with rconEnabled=true, OR
  - A BepInEx RCON mod (e.g. ValheimRcon on Thunderstore)

Commands are based on Valheim's in-game console and ValheimPlus RCON extensions.
"""


def get_commands():
    from app.plugins.base import CommandDef, CommandParam

    return [
        # ── PLAYER MANAGEMENT ─────────────────────────────────────────────────
        CommandDef(
            name="listplayers",
            description="List all connected players with their SteamIDs",
            category="Player Management",
            admin_only=False,
            example="listplayers",
        ),
        CommandDef(
            name="kick",
            description="Kick a player from the server by name or SteamID",
            category="Player Management",
            params=[
                CommandParam(
                    name="name",
                    type="string",
                    required=True,
                    description="Player name or SteamID64",
                ),
            ],
            admin_only=True,
            example="kick Viking123",
        ),
        CommandDef(
            name="banned add",
            description="Ban a player by name or SteamID",
            category="Player Management",
            params=[
                CommandParam(
                    name="name",
                    type="string",
                    required=True,
                    description="Player name or SteamID64",
                ),
            ],
            admin_only=True,
            example="banned add 76561198000000000",
        ),
        CommandDef(
            name="banned remove",
            description="Unban a player by name or SteamID",
            category="Player Management",
            params=[
                CommandParam(
                    name="name",
                    type="string",
                    required=True,
                    description="Player name or SteamID64",
                ),
            ],
            admin_only=True,
            example="banned remove 76561198000000000",
        ),
        CommandDef(
            name="banned list",
            description="Show the current ban list",
            category="Player Management",
            admin_only=True,
            example="banned list",
        ),
        CommandDef(
            name="permitted add",
            description="Add a player to the permitted list (whitelist)",
            category="Player Management",
            params=[
                CommandParam(
                    name="steamid",
                    type="string",
                    required=True,
                    description="SteamID64 of the player",
                ),
            ],
            admin_only=True,
            example="permitted add 76561198000000000",
        ),
        CommandDef(
            name="permitted remove",
            description="Remove a player from the permitted list",
            category="Player Management",
            params=[
                CommandParam(
                    name="steamid",
                    type="string",
                    required=True,
                    description="SteamID64 of the player",
                ),
            ],
            admin_only=True,
            example="permitted remove 76561198000000000",
        ),
        CommandDef(
            name="permitted list",
            description="Show the permitted (whitelist) players",
            category="Player Management",
            admin_only=True,
            example="permitted list",
        ),
        # ── COMMUNICATION ─────────────────────────────────────────────────────
        CommandDef(
            name="say",
            description="Broadcast a message to all connected players",
            category="Communication",
            params=[
                CommandParam(
                    name="message",
                    type="string",
                    required=True,
                    description="Message to broadcast to all players",
                ),
            ],
            admin_only=True,
            example="say Server restart in 5 minutes!",
        ),
        # ── SERVER MANAGEMENT ─────────────────────────────────────────────────
        CommandDef(
            name="save",
            description="Force a world save immediately",
            category="Server Management",
            admin_only=True,
            example="save",
        ),
        CommandDef(
            name="quit",
            description="Save the world and shut down the server gracefully",
            category="Server Management",
            admin_only=True,
            example="quit",
        ),
        # ── WORLD / ENVIRONMENT (ValheimPlus / cheat) ─────────────────────────
        CommandDef(
            name="sleep",
            description="Skip the current day/night cycle to morning",
            category="World",
            admin_only=True,
            example="sleep",
        ),
        CommandDef(
            name="skiptime",
            description="Skip forward by N seconds of in-game time",
            category="World",
            params=[
                CommandParam(
                    name="seconds",
                    type="integer",
                    required=True,
                    description="Number of in-game seconds to skip",
                ),
            ],
            admin_only=True,
            example="skiptime 1800",
        ),
        CommandDef(
            name="settime",
            description="Set the in-game time of day (0–86400)",
            category="World",
            params=[
                CommandParam(
                    name="time",
                    type="integer",
                    required=True,
                    description="Time in seconds (0=midnight, 43200=noon)",
                ),
            ],
            admin_only=True,
            example="settime 43200",
        ),
        CommandDef(
            name="env",
            description="Set the weather/environment preset",
            category="World",
            params=[
                CommandParam(
                    name="preset",
                    type="string",
                    required=True,
                    description="Weather preset name (e.g. Clear, Rain, Snow, ThunderStorm)",
                ),
            ],
            admin_only=True,
            example="env Clear",
        ),
        CommandDef(
            name="resetenv",
            description="Reset weather to the default biome environment",
            category="World",
            admin_only=True,
            example="resetenv",
        ),
        CommandDef(
            name="wind",
            description="Set wind direction and intensity",
            category="World",
            params=[
                CommandParam(
                    name="angle",
                    type="integer",
                    required=True,
                    description="Wind angle in degrees (0–360)",
                ),
                CommandParam(
                    name="intensity",
                    type="string",
                    required=False,
                    description="Wind intensity 0.0–1.0 (default 1.0)",
                ),
            ],
            admin_only=True,
            example="wind 90 0.5",
        ),
        # ── DEBUG / INFO ──────────────────────────────────────────────────────
        CommandDef(
            name="help",
            description="List all available RCON/console commands",
            category="Info",
            admin_only=False,
            example="help",
        ),
        CommandDef(
            name="info",
            description="Show server version and basic info",
            category="Info",
            admin_only=False,
            example="info",
        ),
        CommandDef(
            name="lodbias",
            description="Set the level-of-detail rendering distance bias",
            category="Server Management",
            params=[
                CommandParam(
                    name="value",
                    type="string",
                    required=True,
                    description="LOD bias value (e.g. 1.5)",
                ),
            ],
            admin_only=True,
            example="lodbias 1.5",
        ),
    ]
