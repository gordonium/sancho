---
job: 
lobe: 
entity: 
created: 
by: 
stages:
  - {name: , skill: , status: pending}          # no gate: runs back to back with the next ungated stage, no check-in
  - {name: , skill: , status: pending, gate: human}   # gate: human = Gordon's input is needed; the only place a stage waits
  - {name: approve, gate: human, status: pending}
current: 
advance: manual         # auto: the watcher queues job.run --auto whenever a nerd.run result for this job lands (the Mac is the engine)
hops: 0                 # check-back hops taken; the checkback skill increments
hop_cap: 24             # chain stops here with a warn [gordon 2026-09-30]
waiting_on: []          # {what, evidence (a file test), status: waiting|done, since, done_at}
next_when_done:         # optional mechanical step Cowork does when every item is done
---
