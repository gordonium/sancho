---
name: Metered networks
type: registry
lobe: both
description: Which networks count as metered (heavy commands wait); hand-set by Gordon or via `net.mark`; read by netstate.py every watcher tick
sources: ["[gordon 2026-09-30]"]
---
# Metered networks

Networks are identified by the Wi-Fi router's hardware address (macOS hides network names without Location permission). While a network is metered, commands marked `heavy` in `commands.md` wait in `_queue/deferred/` and run on their own when the Mac is on an unmetered network; the fresh pipeline keeps running but skips single downloads over 50 MB.

Unknown networks: unmetered (only networks listed below as metered are). A policy line "Unknown networks: metered until YYYY-MM-DD" turns the cautious default back on.

To add the network the Mac is on now: say "this network is the hotel / my phone" and a session queues `net.mark` with a label.

| router | label | treat as | added |
|---|---|---|---|
| 66:de:f3:0c:e8:4e | phone-hotspot | metered | 2026-09-30 |
| 64:d1:54:09:cc:4f | hotel-wifi | unmetered | 2026-09-30 |
