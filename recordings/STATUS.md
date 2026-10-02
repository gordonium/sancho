# recordings · STATUS
generated 2026-10-02 13:51 CEST by earballs.py · pipeline AMBER

**AMBER**: 4 recording(s) failed 5 times; see recordings/STATUS.md.

- waiting for ingest (recordings/inbox/): 4; oldest rec_564c0541a8 recorded 2026-09-10 13:01
- fresh in the pipeline: 0 to download, 0 to transcribe, 20 ready in total, 1 junk
- last Plaud list: 2026-10-02T11:51 · last full reconcile: 2026-10-02T00:01 · token: ok · network: online
- Groq today: 0.0 audio-hours in 0 requests (0.0 h backfill of 6 h cap)
- voiceprint library: 20 people · diarization: pyannote/speaker-diarization-3.1
- Zoom: not configured (what to create at Zoom is in _setup/MAC-SETUP.md)
- ledger backup: 2026-10-02T00:01
- data today: 0 MB audio downloaded, 0 MB sent to Groq (sync.com backs the audio up again)

## Backlog

| era | status | recordings | audio hours |
|---|---|---|---|
| era1 | listed | 257 | 289 |
| era2 | listed | 396 | 265 |
| era3 | listed | 372 | 293 |

## Needs attention

- rec_2834a09615 (failed): transcribe: RuntimeError: Groq refused: HTTP 403: {"error":{"message":"Access denied. Please check your network settings."}}
- rec_938ff416ac (failed): transcribe: RuntimeError: Groq refused: HTTP 403: {"error":{"message":"Access denied. Please check your network settings."}}
- rec_9382c74738 (failed): transcribe: RuntimeError: Groq refused: HTTP 403: {"error":{"message":"Access denied. Please check your network settings."}}
- rec_1716cb70ff (failed): transcribe: CalledProcessError: Command '['ffmpeg', '-y', '-loglevel', 'error', '-ss', '0.000', '-t', '1080', '-i', '/Users/gordonium/Sync/Sancho-Audio/processe
