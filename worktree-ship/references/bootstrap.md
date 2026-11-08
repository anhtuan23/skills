# Worktree bootstrap

A worktree has only tracked files. Untracked state stays in the main checkout.
Per project, record a "Worktree" section in `AGENTS.md` listing what to link.
If absent, inspect `.gitignore` and the main checkout, propose the list, and
ask before creating anything.

## Defaults for `~/projects/equity`

| Item | Action | Why |
| --- | --- | --- |
| `.env` | tracked in git; nothing to link | the worktree has its own copy |
| `.env.local` | never link; create a new file in the worktree with `USE_PROD_DATA=false` and `USE_PROD_DNSE=false`, then copy any other non-switch lines from the main checkout's `.env.local` | it selects this checkout's data and DNSE profile; a link would share profile changes with the main checkout (production on `air-m1`) |
| `secrets/`, `secrets_dev/` | symlink | never copy secrets |
| `.venv` | do not share; `uv sync` in the worktree | per-branch dependencies |
| `data_dev/` | symlink by default; create it in the main checkout first if absent | development profile reads it; 100G, so never copy. A dangling link breaks profile loading |
| `data/` (production data) | never link | only the production checkout uses it |
| `log/`, caches | leave absent | regenerated |
| `.equity-local-runtime.lock` | do not link | a shared runtime lock would hide conflicts; run one local runtime at a time |

Rules:

- Symlinks must be ignored by git; check `git status` afterwards. If a link
  shows up untracked, add it to `.git/info/exclude`, not to `.gitignore`.
- Never run with `USE_PROD_DATA=true` or `USE_PROD_DNSE=true` from a
  worktree; both select production state (data root, or real DNSE trading
  and its secrets).
- Two worktrees must not run services against the same `data_dev` at once;
  concurrent writers can corrupt it. Linking is safe, running twice is not.
- On removal (`git worktree remove`), remove symlinks only; never follow them
  with `rm -r`. Ask before removing a worktree with uncommitted work.
