# How to set up the ChatGPT Project (for Saurabh)

1. **ChatGPT → Projects → New project.** Name it `eYRC 4817` (not per task; the same project lives all season).
2. **Instructions:** open the project's settings/instructions box and paste everything from `PROJECT_INSTRUCTIONS.md`, from "You are the robotics engineering mentor…" to the repo link at the end. It is about 7,000 characters; the box accepts 8,000. If ChatGPT still says it is too long, upload `PROJECT_INSTRUCTIONS.md` as a file too and paste everything except the ENVIRONMENT FACTS section.
3. **Files:** build the upload set, then upload **everything** in `~/Desktop/e-yantra/chatgpt-upload/` (13 files: the mentor
   files `00_`–`09_` plus three `B*_Background_*` bundles made from `context/`). The plan allows 25 files per project.
   ```
   python3 ~/Desktop/e-yantra/chatgpt-project/build_upload_set.py
   ```
   Don't upload this file or `PROJECT_INSTRUCTIONS.md` (the instructions already live in the settings box).
   `09_Team_Results_PRIVATE.md` holds graded numbers: it goes to this project only, never to GitHub (git ignores it).
4. **Test it** after every re-upload, with 4 questions:
   - "What's left before 5 Oct and what do I do today?" (should use the plan in `00_START_HERE.md`)
   - "KD 1C: which throttle gains do we start from?" (should quote `09_Team_Results_PRIVATE.md`)
   - "PB 1B: which sensors measure the side walls?" (should say `fl`/`fr`, verified 24 Sep, not "unresolved")
   - "Write my complete task_1b.py." (should refuse the full file and offer to teach or review)
5. **Share:** use the project's Share option to invite Gauri, Parth and Mahesh. Each teammate needs a ChatGPT account, and shared-project features depend on the ChatGPT plan, so check the Share menu.
6. **Keep it current:** if e-Yantra changes anything (e.g. a forum answer about the results file), tell Claude. Claude updates the file in `~/Desktop/e-yantra/chatgpt-project/` (or `context/`), reruns `build_upload_set.py`, and you re-upload the changed files (a changed context note = re-upload its `B*` bundle). Delete the old copy in the project first so ChatGPT never sees two versions.
7. **When a new task is released:** the instructions are written to stay the same all season, so do not edit them. Only the files change: Claude rewrites `00_START_HERE.md` so it names the new current task, deadline and the file that covers it, adds one file per new task, and merges old task files into one archive file to stay under the 25-file project limit (13 used as of 1 Oct). You re-upload the changed files.

Tip for teammates: start each new chat with the subtask ("KD 1A:", "PB 1B:") so ChatGPT opens the right file.
