---
job: jobrun-smoke
lobe: work
created: 2026-09-30
by: claude-code
stages:
  - {name: lint-check, status: done, task: "Run python3 _setup/lint-layers.py and report its last line. Write nothing. Do not run test-all for this stage."}
  - {name: tests, status: done, task: "Run python3 _setup/test-all.py and report its last line and any FAIL lines verbatim. Write nothing else."}
current: tests
---
# job.run smoke test
One trivial stage, run once live on 2026-09-30 to prove job.run end to end (watcher → detached runner → nerd.run → job file → push). Archive after.
- 2026-09-30T23:46:52+02:00 job.run: stage `lint-check` started
- 2026-09-30T23:47:07+02:00 job.run: stage `lint-check` failed once (Stage: blocked: lint-layers.py crashed with PermissionError at line 198 (check_secrets stats ~/.config/sancho/env, which the Nerd sandbox blocks) and never prod); retrying
- 2026-09-30T23:47:23+02:00 job.run: stage `lint-check` failed twice; stopped (Stage: blocked: lint-layers.py crashes with PermissionError on ~/.config/sancho/env under the Nerd sandbox (check_secrets, line 198); no result line produced)
- 2026-09-30T23:47:52+02:00 job.run: stage `lint-check` started
- 2026-09-30T23:48:02+02:00 job.run: stage `tests` started
- 2026-09-30T23:48:44+02:00 job.run: stage `tests` failed once (Stage: blocked: 14 of 19 suites are failing, and the run wrote files into the tree, including four stray root files that need a decision before the hourly autoc); retrying
- 2026-09-30T23:49:27+02:00 job.run: all stages done
- 2026-09-30T23:54:10+02:00 job.run: stage `tests` started
- 2026-09-30T23:56:36+02:00 job.run: all stages done
