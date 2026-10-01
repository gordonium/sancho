# _setup/pipeline · INDEX
generated 2026-10-01 by build-index.py · 4 entries

- earballs.py · script · 2026-10-01 · The recording pipeline. Plaud fetch (incremental every 5 min, full reconcile daily) → download → Groq transcription → pyannote diarization + embeddings → voiceprint match → transcript.md / speakers.md / meta.md in recordings/inbox/ → recordings/STATUS.md → watchdog push. Also backfill, reprocess, library rebuild.
- earballs.sh · sh · 2026-09-30 · NO DESCRIPTION
- install-venv.sh · sh · 2026-09-30 · NO DESCRIPTION
- requirements.txt · txt · 2026-09-30 · NO DESCRIPTION
