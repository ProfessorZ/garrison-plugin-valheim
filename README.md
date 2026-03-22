# garrison-plugin-valheim

Garrison plugin for [Valheim](https://www.valheimgame.com/) dedicated servers.

## ⚠️ RCON mod required

Vanilla Valheim dedicated servers do **not** include RCON support. You need one of:

| Mod | Notes |
|-----|-------|
| **[ValheimPlus](https://github.com/valheimplus/ValheimPlus)** | Most popular; enables Source RCON |
| **BepInEx + RCON mod** | Several options on Thunderstore/Nexus |

### ValheimPlus setup

1. Install ValheimPlus on the server (BepInEx mod).
2. Edit `BepInEx/config/valheim_plus.cfg`:

```ini
[Server]
rconEnabled = true
rconPort = 2461
rconPassword = yoursecretpassword
```

3. Restart the server.
4. Configure Garrison with `host`, `rcon_port=2461`, and the password above.

## Commands supported

| Command | Description |
|---------|-------------|
| `listplayers` | List connected players |
| `kick <name>` | Kick a player |
| `banned add <name>` | Ban a player |
| `banned remove <name>` | Unban a player |
| `banned list` | Show ban list |
| `say <message>` | Broadcast chat message |
| `save` | Force world save |
| `quit` | Save and stop server |

## Protocol

Uses standard **Source RCON** (Valve protocol, TCP) — the same as CS:GO, ARK, etc.

## Tested with

- ValheimPlus 0.9.x
- Valheim dedicated server (vanilla — RCON not available)
