# _setup/tests/notify · INDEX
generated 2026-10-02 by build-index.py · 1 entries

- test.py · script · 2026-10-01 · notify.py against a sink file (and, where localhost can be bound, a local fake Pushover endpoint): sends with the right fields and priority, skips a repeat within a day, sends again when the message for the key changes, fails cleanly without keys; levels are info -1, warn 0, alert 0 with its own title and sound (nothing breaks quiet hours); the sender's session is echoed and does not defeat dedupe; a warn with an unregistered reason is sent but tagged; every warn or alert in a script or skill carries a reason registered at that level in _setup/notify-reasons.md.
