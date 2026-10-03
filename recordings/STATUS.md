# recordings · STATUS
generated 2026-10-03 21:55 CEST by earballs.py · pipeline AMBER

**AMBER**: 6 recording(s) failed 5 times; see recordings/STATUS.md.

- waiting for ingest (recordings/inbox/): 4; oldest rec_c080609f7c recorded 2026-10-02 09:39
- fresh in the pipeline: 0 to download, 0 to transcribe, 26 ready in total, 1 junk
- last Plaud list: 2026-10-03T19:55 · last full reconcile: 2026-10-03T00:02 · token: ok · network: online
- Groq today: 0.0 audio-hours in 0 requests (0.0 h backfill of 6 h cap)
- voiceprint library: 23 people · diarization: pyannote/speaker-diarization-3.1
- Zoom: not configured (what to create at Zoom is in _setup/MAC-SETUP.md)
- ledger backup: 2026-10-03T00:02
- data today: 21 MB audio downloaded, 0 MB sent to Groq (sync.com backs the audio up again)

## Backlog

| era | status | recordings | audio hours |
|---|---|---|---|
| era1 | listed | 257 | 289 |
| era2 | listed | 396 | 265 |
| era3 | listed | 372 | 293 |

## Needs attention

- rec_ebe92ab8e4 (failed): transcribe: RuntimeError: Groq refused: HTTP 403: {"error":{"message":"Access denied. Please check your network settings."}}
- rec_1b58db42a1 (failed): transcribe: RuntimeError: Groq refused: HTTP 403: {"error":{"message":"Access denied. Please check your network settings."}}
- rec_2834a09615 (failed): transcribe: RuntimeError: Groq refused: HTTP 403: {"error":{"message":"Access denied. Please check your network settings."}}
- rec_938ff416ac (failed): transcribe: RuntimeError: Groq refused: HTTP 403: {"error":{"message":"Access denied. Please check your network settings."}}
- rec_9382c74738 (failed): transcribe: RuntimeError: Groq refused: HTTP 403: {"error":{"message":"Access denied. Please check your network settings."}}
- rec_1716cb70ff (failed): transcribe: CalledProcessError: Command '['ffmpeg', '-y', '-loglevel', 'error', '-ss', '0.000', '-t', '1080', '-i', '/Users/gordonium/Sync/Sancho-Audio/processe
