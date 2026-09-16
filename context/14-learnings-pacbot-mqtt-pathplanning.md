# PacBot learnings — MQTT + Path Planning (analysed 2026-09-16)

Pasted by Saurabh on 2026-09-16 from the PB portal (`theme_pb/learnings/mqtt/…`, path planning page),
with the mqtt.org diagram, `qos-levels.svg`, `topic-wildcards.svg` and planner animation stills.
**PacBot Task 1 instructions have not been received yet.**

## 1. MQTT
- A publish/subscribe protocol for IoT (IBM 1999, built for flaky satellite links, so it's tiny).
  **Every message goes through a broker**; clients never talk directly. Topics are slash strings
  (`home/livingroom/temperature`) created simply by publishing. Publisher and subscriber are
  decoupled in space, time (persistent sessions) and sync.
- **vs ROS 2 (a teaching point):** same pub/sub idea, but ROS 2 peers discover each other directly
  (DDS) with typed messages; MQTT needs a central broker and the payload is untyped bytes.
- Wildcards: `+` = exactly one level (`home/+/temperature`); `#` = everything below, last
  character only (`home/#`).
- **QoS:** 0 at most once (fire and forget); 1 at least once (PUBACK, duplicates possible);
  2 exactly once (PUBLISH→PUBREC→PUBREL→PUBCOMP). Higher = more round trips.
- Sessions: CONNECT carries client ID, keep-alive, and the clean-session flag. A persistent
  session queues QoS 1/2 messages while offline. **Retained message** = last known value handed to
  new subscribers. **Last Will (LWT)** = published by the broker if a client drops ungracefully
  (crash detection).
- Resources: HiveMQ MQTT Essentials parts 3, 5–10 (paired per concept); Steve's Internet Guide;
  OASIS specs v5.0 / v3.1.1 (reference only).
- Code: Python **paho-mqtt with `CallbackAPIVersion.VERSION2`** (paho 2.x API). C++ `paho.mqtt.cpp`
  must be built from source with `sudo cmake --install` (only if the team picks C++).
- **Security note (Saurabh's interest):** the portal's public broker `test.mosquitto.org:1883` is
  unencrypted and unauthenticated. **Anyone can read or publish `pacbot/test`.** Fine for "hello",
  never for real data; later a good hardware-security discussion (TLS, auth, ACLs).

### MQTT setup status [VERIFIED 2026-09-16]
- `mosquitto` 2.0.11 broker installed, **systemd service active**, listening on **localhost:1883
  only** (IPv4 + IPv6), so it is not exposed to the network. `mosquitto_pub` / `mosquitto_sub` are
  installed.
- `paho-mqtt` **2.1.0** (user site), `CallbackAPIVersion` import OK, which matches the portal's
  example code.
- **Local round trip passed:** `mosquitto_sub -t pacbot/setup_check` received a `mosquitto_pub`
  message.
- Not done / not needed yet: the C++ Paho build; opening the broker to the LAN (needed only when
  an ESP32 in Stage 2 must reach this laptop; would need `listener 1883 0.0.0.0` plus auth).

## 2. Path Planning page (PB) — **"Task 1A" of PacBot is a grid-maze planning problem**
- Maze → graph: open cell = node, move between neighbours without a wall = edge. Every algorithm
  keeps a **frontier**, and the only difference between them is **which frontier cell is expanded
  next**.
| Algorithm | Expands next | Costs | Cheapest path? | Goal-directed? |
|---|---|---|---|---|
| BFS | oldest (queue), even rings | no | yes, on equal-cost moves | no |
| DFS | newest (stack), one long thread + backtrack | no | **no** (wandering path) | no |
| Dijkstra | lowest cost-so-far g | yes | yes | no (BFS = Dijkstra with unit costs) |
| Greedy best-first | lowest heuristic h | ignores | no (commits into dead ends) | yes |
| **A\*** | lowest g + h | yes | **yes if h never overestimates** | yes (h = 0 → Dijkstra; ignoring g → Greedy) |
- The portal's closing hint for PB Task 1A: the maze is a grid, **fully visible from the start**,
  you need a *good* route, and **what to do about the pellets is your decision**. So Task 1A goes
  beyond shortest path: it is also **ordering pellet collection** (a travelling-salesman-like
  choice) *[INFERRED; confirm with the Task 1A brief]*. Ghosts appear in the theme (Task 2+?).
- The stills show the same 50×30 map with walls, start (blue) and goal (green); grey = explored.
  Compare how far each algorithm had spread.

## Roadmap mapping (for the rebuild)
- **P1 MQTT:** ① mqtt.org diagram + portal intro → ② HiveMQ Essentials parts 5 (topics), 6 (QoS),
  8–9 (retained, LWT) → **DO:** local broker already running; Saurabh runs `mosquitto_sub` /
  `mosquitto_pub` himself, then the portal's Python subscriber/publisher, then **experiments**:
  wildcard subscriptions; QoS 0 vs 1 while killing the subscriber; retained message → start a
  late subscriber; LWT → kill a client with Ctrl+C vs `kill -9` (predict first). TEACH: MQTT vs
  ROS 2.
- **P2 Path planning (becomes important if PB Task 1A is attempted):** portal page + its
  animations → Computerphile Dijkstra (10 min) → A* (14 min) → **DO on paper:** run BFS, DFS and A*
  on a small grid by hand (count expanded cells) → Saurabh codes BFS himself in Python (a good
  daily-Python exercise), then A* → pellet-ordering discussion.
- Both themes share A*/Dijkstra with KD (drone search in Task 2).
