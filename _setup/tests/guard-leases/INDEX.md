# _setup/tests/guard-leases · INDEX
generated 2026-10-02 by build-index.py · 1 entries

- test.py · script · 2026-10-02 · quarantine-guard.py's second duty, lease enforcement (ERRORS.md #12), with hook inputs on stdin against a temp tree. An Edit, a Write and a Bash redirection (`>`, `>>`, `tee`) onto a path inside another live lease's `writes_only` are refused and logged in lease-access.log; the holder passes, both as the nerd.run session named by the lease and as a process under the lease's pid; a path outside every lease passes; a read of the leased file passes; a lease whose pid is gone refuses nothing; `--install` widens an older reads-only registration to Write and Edit.
