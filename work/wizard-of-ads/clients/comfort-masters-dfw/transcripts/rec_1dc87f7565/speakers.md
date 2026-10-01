---
name: Speakers · rec_1dc87f7565
type: doc
lobe: both
description: Who spoke in rec_1dc87f7565 (Comfort Masters DFW monthly, 2026-09-23), transcript.v2 clusters; luis-castaneda, gordon, jack-heald, amanda-moore human-confirmed 2026-10-02; SPEAKER_03 is Peter Nevland and Stephen Moore merged (reprocess at 6 did not split them), not enrolled
sources: ["[rec_1dc87f7565 2026-09-23]"]
rec_id: rec_1dc87f7565
---
# speakers · rec_1dc87f7565

`confirmed` by `machine: …` is machine-confirmed (used for filing, never enrolled). Only a row confirmed by a person (`gordon`, date) enrolls a voiceprint.

Diarization: re-run with 6 speakers (2026-10-02). Result: Peter Nevland and Stephen Moore still share one cluster (SPEAKER_03); SPEAKER_02 is 10 s of noise. Gordon confirmed the four distinct voices on v1 (2026-10-02); the mapping below carries that to the v2 clusters by content.

Over-split suspected: 5 of 6 clusters have ≥ 133 s of speech; likely 5 speakers. Reprocess with that count if confirmed.

| cluster | talk time | candidate (machine) | confirmed | by | when | note |
|---|---|---|---|---|---|---|
| SPEAKER_00 | 00:03:16 | none | luis-castaneda | gordon | 2026-10-02 | v1 SPEAKER_00, confirmed by Gordon on v1 [confirmed gordon 2026-10-02]; enrollable |
| SPEAKER_01 | 00:02:25 | gordon sim=0.93 refs=16 | gordon | gordon | 2026-10-02 | library sim 0.93 (auto-tag paused); v1 SPEAKER_01 confirmed by Gordon [confirmed gordon 2026-10-02]; enrollable |
| SPEAKER_02 | 00:00:10 | none |  |  |  | noise (10 s); not enrolled |
| SPEAKER_03 | 00:11:50 | peter-nevland sim=0.82 refs=2 |  |  |  | MERGED: Peter Nevland (library sim 0.82) and Stephen Moore in one cluster [gordon 2026-10-02 on v1]; lines attributed by content only in the summary; not confirmed as one person, not enrolled |
| SPEAKER_04 | 00:08:39 | jack-heald sim=0.72 refs=1 | jack-heald | gordon | 2026-10-02 | library sim 0.72; v1 SPEAKER_03 confirmed by Gordon [confirmed gordon 2026-10-02]; enrollable |
| SPEAKER_05 | 00:03:22 | none | amanda-moore | gordon | 2026-10-02 | v1 SPEAKER_04 confirmed by Gordon [confirmed gordon 2026-10-02]; enrollable |
