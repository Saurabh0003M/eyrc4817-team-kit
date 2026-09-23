# How to set up the ChatGPT Project (for Saurabh)

1. **ChatGPT → Projects → New project.** Name it `eYRC 4817` (not per task; the same project lives all season).
2. **Instructions:** open the project's settings/instructions box and paste everything from `PROJECT_INSTRUCTIONS.md`, from "You are the robotics engineering mentor…" to the repo link at the end. It is about 7,000 characters; the box accepts 8,000. If ChatGPT still says it is too long, upload `PROJECT_INSTRUCTIONS.md` as a file too and paste everything except the ENVIRONMENT FACTS section.
3. **Files:** upload these 9 files (they're self-contained):
   - `00_START_HERE.md`
   - `01_KD_Task1A_Survivor_Detection.md`
   - `02_KD_Task1B_1C_PID_Tuning.md`
   - `03_PB_Task1A_Maze_Path_Planning.md`
   - `04_PB_Task1B_Wall_Following.md`
   - `05_Setup_Run_Submit.md`
   - `06_Concepts_Explained.md`
   - `07_Learning_Resources.md`
   - `08_Portal_Learnings_Summary.md`

   Don't upload this file.
4. **Test it** before sharing, with 4 questions:
   - "What is my subtask if I'm Mahesh, and what do I do today?" (should use the 6-day plan)
   - "Write my complete task1a.py." (should refuse the full file and offer to teach or review)
   - "How do I detect ArUco markers?" (should use the old API: `detectMarkers`, not `ArucoDetector`)
   - "What does valid: false mean in PacBot 1A?" (should answer from file 03)
5. **Share:** use the project's Share option to invite Gauri, Parth and Mahesh. Each teammate needs a ChatGPT account, and shared-project features depend on the ChatGPT plan, so check the Share menu.
6. **Keep it current:** if e-Yantra changes anything (e.g. a forum answer about the results file), tell Claude. Claude updates the file in `~/Desktop/e-yantra/chatgpt-project/`, and you re-upload that one file.
7. **When a new task is released:** the instructions are written to stay the same all season, so do not edit them. Only the files change: Claude rewrites `00_START_HERE.md` so it names the new current task, deadline and the file that covers it, adds one file per new task, and merges old task files into one archive file to stay under the 25-file project limit. You re-upload the changed files.

Tip for teammates: start each new chat with the subtask ("KD 1A:", "PB 1B:") so ChatGPT opens the right file.
