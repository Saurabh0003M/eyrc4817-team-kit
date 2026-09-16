# Portal learnings — Control Systems (analysed 2026-09-16)

Source: KD portal → Learnings → Control Systems (Map of Control Theory, Intro, System Modelling,
Model Examples, Stability, Pendulum, PID, LQR), pasted by Saurabh on 2026-09-16. Analysed from the
page text and figures plus video **metadata only** (titles and lengths; no transcripts were read,
to save tokens). For roadmap use.

## Signals that change the plan
1. **"For this competition, focus on classical PID and modern LQR/LQI control. These are the ones
   you'll actually be implementing on the drone."** Task 1B/1C only *tunes* PID, so a later task
   will probably have Saurabh **write** PID and/or **LQR/LQI** code. *[INFERRED: which task is not
   stated.]* → The roadmap needs an **LQR module after Task 1**, and M3's "toy drone in Python"
   stays valuable.
2. The portal's **"P, PD & PID for Drones"** section is the Task 1B/1C tuning story in miniature.
   It uses real plots from an older eYRC Pluto drone: **P** oscillates and overshoots forever;
   **PD** damps the oscillation but leaves a **steady-state error**; **PID** has no overshoot and no
   steady-state error. That matches e-Yantra's ball-and-beam demo. → **M3 core reading, just before
   M6.**
3. LQR on the portal says "use the inbuilt `lqr` command in **Octave**". *Possible future setup
   item: GNU Octave + control package, only when a task needs it.* Not installed now.

## Mistakes and oddities in the portal pages [checked by hand]
- **PID I-term formula is wrong as written:** `Iterm = (Iterm + error) · Ki` multiplies the whole
  running sum by Ki on every step, so it leaks when Ki < 1 and blows up when Ki > 1. Standard form:
  `Iterm = Iterm + Ki · error` (or sum the errors, then multiply by Ki). → A good **"spot the bug"
  exercise** for Saurabh in M3.
- "Ki / Kd are calculated keeping the sampling time in consideration" means the time step dt is
  folded into the gains (`Kd·(e − e_prev)` stands for `Kd'·(e − e_prev)/dt`). Explains why raw gain
  numbers depend on loop rate.
- Linearization example: the eigenvalue −2√2 is written as "−2.824"; it is −2.828 (typo only).
  Stability and pendulum worked examples check out (equilibria (0,0), (±1,∓1); s = 2 ± 2√2;
  pendulum ±i√(g/l) marginally stable, ±√(g/l) unstable).
- "Map of Control Theory" (Brian Douglas, 2020) is an orientation poster. Only the **PID**,
  **LQR**, **linearization**, **state space**, **stability** and **step response** regions matter
  for Stage 1.

## Video ladders (ordered by metadata; Brian Douglas = the MATLAB presenter, so a consistent style)
**PID ladder (M3, feeds Tasks 1B/1C):**
① `UR0hOmjaHp0` *PID Control – A brief introduction* (B. Douglas, 7:44)
→ ② `wkfEZmsQqiA` *What Is PID Control?* MATLAB Part 1
→ ③ `XfAt6hNV8XM` *Simple Examples of PID Control* (13:10)
→ ④ Parts 2 anti-windup `NVLXCwc8HzM`, 3 noise filtering `7dUVdrs1e18`, **4 tuning guide
`sFOEsA0Irjs` (12:05, the most useful before tuning)**
→ portal "P/PD/PID for drones" page
→ ⑤ Part 6 manual/automatic tuning `qj8vTO1eIHo` (13:31), Part 7 important concepts `tbgV6caAVcs`
(12:29). Part 5 *3 ways to build a model* `qhIjIu-Zk10` (13:45) belongs to the modelling ladder.

**Big picture (M3 start or M0):** `lBC1nEq0_nk` *Everything You Need to Know About Control
Theory* (MATLAB, 16:07; already in the roadmap as M3 rung ④, so move it earlier) + the Map poster.

**Stability ladder (after Task 1 or alongside M3, understand-level):** `uqjKG32AkC4` *Intro to
System Stability and Control* (11:32) → `yf09OrHa520` *Stability of Closed Loop Control Systems*
(11:36) → portal Stability + Pendulum pages (the **Tip** exercise: Jacobian of an upright vs
hanging pendulum; do it on paper with Gauri).

**Modelling → LQR ladder (new module after Task 1):** portal System Modelling page (F = ma →
Euler–Lagrange → state space) + Model Examples (point mass, spring-mass-damper, projectile, 2-D
rotation) → `hpeKrMG-WP0` *Intro to State-Space Equations* (14:12) → linearization + eigenvalues
→ `qhIjIu-Zk10` 3 ways to build a model → `E_RDCFOlJx4` *What Is LQR?* (17:24) → `ZktL3YjTbB4`
*Why the Riccati Equation…* (14:30) → Murray LQR notes → MuJoCo **LQR Colab** (from the MuJoCo
pages).

**Design mindset (optional):** `Mbx5IMICS_Y` *A real control system – how to start designing*
(B. Douglas, 26:58).

**Reference, not a to-do:** playlist *Classical Control Theory* (B. Douglas) is **46 videos, ≈10
h**, and includes Fourier/frequency-domain topics that Stage 1 doesn't need. Pick single videos
only when a concept is stuck.

## Reading behind the portal login (Claude cannot fetch these)
- `fundamentals_of_control_r1_6.pdf`: Brian Douglas's *Fundamentals of Control Theory* book. The
  portal says "everyone is expected to go through" it but "focus on PID and LQR/LQI". If
  downloaded, Claude reads **only its table of contents** to pick chapters. It has **not** been read.
- `StateSpace.pdf` (state-space notes) and `lqr.pdf` (R. M. Murray LQR lecture notes): for the
  LQR module.
- Suggested location: `eYRC 2026-27/Media/Learnings/`.

## Depth for Saurabh (Cyber Security; maths background not yet assessed)
- **Must feel (Task 1):** open vs closed loop, error, P/I/D effects, overshoot, steady-state error,
  windup, tuning order.
- **Understand (later tasks):** state space x′ = Ax + Bu, equilibrium, linearization, "eigenvalue
  real part > 0 means unstable", u = −Kx.
- **Pair with Gauri (EE):** Euler–Lagrange derivations, Jacobians, the Riccati equation. These are
  her coursework, and a TEACH opportunity in both directions.
