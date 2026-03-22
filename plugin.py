"""Garrison plugin for Valheim dedicated servers.

Valheim does NOT ship with RCON support out of the box. To use this plugin
you need one of:
  - ValheimPlus mod (enables Source RCON on a configurable port)
  - BepInEx + RCON mod (e.g. "Valheim RCON" on Nexus Mods / Thunderstore)

Without a mod the plugin will raise ConnectionError on connect().

ValheimPlus RCON config (valheim_plus.cfg):
  [Server]
  rconEnabled = true
  rconPort = 2461        # default; configure as needed
  rconPassword = secret

The plugin speaks standard Source RCON (Valve protocol) on that port.
"""

from __future__ import annotations

import asyncio
import re
import struct
import socket
from datetime import datetime
from typing import Optional

from app.plugins.base import GamePlugin, PlayerInfo, ServerStatus, CommandDef


# ── Source RCON constants ────────────────────────────────────────────────────
_SERVERDATA_AUTH = 3
_SERVERDATA_AUTH_RESPONSE = 2
_SERVERDATA_EXECCOMMAND = 2
_SERVERDATA_RESPONSE_VALUE = 0


def _pack_packet(request_id: int, packet_type: int, body: str) -> bytes:
    body_bytes = body.encode("utf-8") + b"\x00\x00"
    size = 4 + 4 + len(body_bytes)
    return struct.pack("<iii", size, request_id, packet_type) + body_bytes


def _read_packet(sock: socket.socket) -> tuple[int, int, str]:
    raw_size = _recv_all(sock, 4)
    size = struct.unpack("<i", raw_size)[0]
    data = _recv_all(sock, size)
    request_id = struct.unpack("<i", data[:4])[0]
    packet_type = struct.unpack("<i", data[4:8])[0]
    body = data[8:-2].decode("utf-8", errors="replace")
    return request_id, packet_type, body


def _recv_all(sock: socket.socket, length: int) -> bytes:
    data = b""
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Socket closed prematurely")
        data += chunk
    return data


class ValheimPlugin(GamePlugin):
    """Valheim dedicated server plugin (Source RCON via ValheimPlus or similar mod)."""

    def __init__(self):
        self._sock: Optional[socket.socket] = None
        self._request_id = 1

    @property
    def game_type(self) -> str:
        return "valheim"

    @property
    def display_name(self) -> str:
        return "Valheim"

    # ── Connection ───────────────────────────────────────────────────────────

    async def connect(self, host: str, port: int, password: str) -> None:
        """Connect and authenticate via Source RCON."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._blocking_connect, host, port, password)

    def _blocking_connect(self, host: str, port: int, password: str) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        try:
            sock.connect((host, port))
        except OSError as exc:
            raise ConnectionError(
                f"Cannot connect to Valheim RCON at {host}:{port}. "
                "Ensure ValheimPlus (or equivalent RCON mod) is installed and rconEnabled=true. "
                f"Error: {exc}"
            ) from exc

        rid = self._next_id()
        sock.sendall(_pack_packet(rid, _SERVERDATA_AUTH, password))
        resp_id, resp_type, _ = _read_packet(sock)
        if resp_id == -1:
            sock.close()
            raise PermissionError("RCON authentication failed — wrong password?")

        self._sock = sock

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    async def disconnect(self) -> None:
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None

    async def send_command(self, command: str) -> str:
        """Send a raw RCON command and return the response."""
        if not self._sock:
            raise ConnectionError("Not connected to Valheim RCON")
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._blocking_send, command)

    def _blocking_send(self, command: str) -> str:
        rid = self._next_id()
        self._sock.sendall(_pack_packet(rid, _SERVERDATA_EXECCOMMAND, command))
        _, _, body = _read_packet(self._sock)
        return body

    # ── Player info ──────────────────────────────────────────────────────────


    async def parse_players(self, raw_response: str) -> list[PlayerInfo]:
        import re
        players = []
        for line in raw_response.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^#?\d+\s+(.+?)\s+(\d{17})$', line)
            if m:
                players.append(PlayerInfo(name=m.group(1), steam_id=m.group(2)))
                continue
            m = re.match(r'^(.+?)\s+-\s+(\d+)$', line)
            if m:
                players.append(PlayerInfo(name=m.group(1), steam_id=m.group(2)))
        return players

    async def get_players(self, send_command) -> list[PlayerInfo]:
        """Return connected players. Valheim's list output varies by mod."""
        try:
            raw = await send_command("listplayers")
        except Exception:
            return []

        players: list[PlayerInfo] = []
        # ValheimPlus: "Name - SteamID"  or  "#N Name SteamID"
        for line in raw.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            # Try "#N Name SteamID" format
            m = re.match(r"^#?\d+\s+(.+?)\s+(\d{17})$", line)
            if m:
                players.append(PlayerInfo(name=m.group(1), player_id=m.group(2)))
                continue
            # Try "Name - SteamID"
            m = re.match(r"^(.+?)\s+-\s+(\d+)$", line)
            if m:
                players.append(PlayerInfo(name=m.group(1), player_id=m.group(2)))
                continue
            # Fallback: name only
            if not any(kw in line.lower() for kw in ["player", "connected", "total"]):
                players.append(PlayerInfo(name=line))

        return players

    async def kick_player(self, send_command, name: str, reason: str = "") -> str:
        return await send_command(f"kick {name}")

    async def ban_player(self, send_command, name: str, reason: str = "") -> str:
        return await send_command(f"banned add {name}")

    async def unban_player(self, send_command, name: str) -> str:
        return await send_command(f"banned remove {name}")

    async def get_status(self, send_command) -> ServerStatus:
        try:
            players = await self.get_players(send_command)
            return ServerStatus(online=True, player_count=len(players))
        except Exception:
            return ServerStatus(online=False, player_count=0)

    async def get_player_roles(self) -> list[str]:
        return []  # Valheim has no role system

    async def poll_events(self, send_command, since: datetime) -> list[dict]:
        return []  # Not supported without log streaming

    def get_commands(self) -> list[CommandDef]:
        from schema import get_commands
        return get_commands()
