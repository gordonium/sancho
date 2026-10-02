# recordings · STATUS
generated 2026-10-02 17:52 CEST by earballs.py · pipeline AMBER

**AMBER**: 4 recording(s) failed 5 times; see recordings/STATUS.md.

- waiting for ingest (recordings/inbox/): 1; oldest rec_920d1a79bf recorded 2026-10-02 15:12
- fresh in the pipeline: 0 to download, 0 to transcribe, 21 ready in total, 1 junk
- last Plaud list: 2026-10-02T15:52 · last full reconcile: 2026-10-02T00:01 · token: ok · network: online
- Groq today: 0.1 audio-hours in 1 requests (0.0 h backfill of 6 h cap)
- voiceprint library: 23 people · diarization: pyannote/speaker-diarization-3.1
- Zoom: not configured (what to create at Zoom is in _setup/MAC-SETUP.md)
- ledger backup: 2026-10-02T00:01
- data today: 1 MB audio downloaded, 1 MB sent to Groq (sync.com backs the audio up again)

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
