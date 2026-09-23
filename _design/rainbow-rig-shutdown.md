# Rainbow Rig: what to shut down when it comes back online

Written 2026-09-22. Status: **waiting for Gordon to say the Rig is online.** Then do this before Sync.com finishes anything.

## Why
v2's daemons ran on the Rig from `E:\Sync\Gordonium Enterprises Sync\gordon-os-v2\` (Windows venv at `E:\...\gordon-os-v2\.venv`, user `Owner`), scheduled by Windows Task Scheduler. Evidence: `tools/logs/orchestrator-desktop.log` (identity `desktop-nerd`), `logs/jarvis-listener.log`, `logs/nerd-dispatch.log`, `logs/file-watcher.log`, git commits "GordonOS Desktop Nerd auto-sync". Last write 18:56 MDT 2026-09-21, when the Rig was retired. The E: drive was swapped out, so the scripts are gone from that path, but **if Sync.com on the Rig recreates `E:\Sync\` on the new drive, the scripts come back and the scheduled tasks resume.**

## What to stop (names are unknown; discover, don't guess)
Known processes from the logs: orchestrator (`jarvis-orchestrator.py` or similar), mesh listener (`jarvis-listener.py`, HTTP on port 18790), `nerd-dispatch`, file watcher / git-flush, `periodic-sync.py` (deprecated March 2026 but still scheduled), file server (`gordon-file-server.py`, port 8765, retired), plaud-sync (already retired June 2026, marker files exist). Also any Tailscale mesh token use and the ntfy topic.

## PowerShell, run as the Owner user (or hand this file to Claude on that machine)
```powershell
# 1. See what is scheduled that looks like ours
Get-ScheduledTask | Where-Object { $_.TaskName -match 'jarvis|gordon|nerd|orchestr|plaud|earballs|mesh|listener|dispatch|sync|watcher|file-server' } |
  Select-Object TaskName, State, TaskPath | Format-Table -AutoSize

# 2. Also catch tasks by what they run, since names may be generic
Get-ScheduledTask | ForEach-Object {
  $a = ($_.Actions | ForEach-Object { "$($_.Execute) $($_.Arguments)" }) -join ' '
  if ($a -match 'gordon-os-v2|E:\\Sync|jarvis|python') { [pscustomobject]@{Task=$_.TaskName; State=$_.State; Runs=$a} }
} | Format-Table -AutoSize -Wrap

# 3. Disable them (review the list from 1 and 2 first; replace the -match pattern with the confirmed names if you prefer)
Get-ScheduledTask | Where-Object { $_.TaskName -match 'jarvis|gordon|nerd|orchestr|plaud|earballs|mesh|listener|dispatch|watcher|file-server' } | Disable-ScheduledTask

# 4. Kill anything already running from the old tree
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'gordon-os-v2|jarvis' } |
  Select-Object ProcessId, Name, CommandLine | Format-Table -AutoSize -Wrap
# then, once reviewed:
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'gordon-os-v2|jarvis' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

# 5. Confirm nothing listens on the mesh or file-server ports
Get-NetTCPConnection -State Listen | Where-Object { $_.LocalPort -in 18790, 8765 }

# 6. Startup-folder and Run-key leftovers
Get-ChildItem "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run'
```

## Sync.com on the Rig
Either sign Sync.com out on that machine, or exclude `Gordonium Enterprises Sync` from syncing there. Do this **before** step 3 is undone by a re-download. The Rig's only remaining job is cold storage, so it needs no live Sync.

## After
- Re-run step 1 and 4 to confirm empty. Note the task names found here, in this file, for the record.
- Check from the Mac that v2 stays inert: no files under `~/Sync/Gordonium Enterprises Sync/gordon-os-v2/comms/spawn-logs/` newer than 2026-09-21 18:56 MDT.
- Then log "Rig tidied" in `decisions.md` and delete the "waiting" line at the top of this file.
