# Worktree bootstrap

A worktree has only tracked files. Untracked state stays in the main checkout.
The project's "Worktree" section in `AGENTS.md`, or the doc it links to, lists
what to link and create. If there is none, inspect `.gitignore` and the main
checkout, propose the list, and ask before creating anything.

Rules:

- Never copy secrets. Link development secrets, and never link production ones.
- Do not share a virtual environment. Create one per worktree.
- Never give a worktree a link to production data or a production profile.
- Symlinks must be ignored by git; check `git status` afterwards. If a link
  shows up untracked, add it to `.git/info/exclude`, not to `.gitignore`.
- Two worktrees must not run services against the same data at once; concurrent
  writers can corrupt it. Linking is safe, running twice is not.
- On removal (`git worktree remove`), remove symlinks only; never follow them
  with `rm -r`. Ask before removing a worktree with uncommitted work.
