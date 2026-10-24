# Upstream skill copies

Five skills in this repository are adapted from Matt Pocock's skills repository:

| Local skill | Upstream path |
|-------------|---------------|
| `ask-matt` | `skills/engineering/ask-matt` |
| `domain-modeling` | `skills/engineering/domain-modeling` |
| `grill-me` | `skills/productivity/grill-me` |
| `grill-with-docs` | `skills/engineering/grill-with-docs` |
| `grilling` | `skills/productivity/grilling` |

The upstream repository is <https://github.com/mattpocock/skills>. The copied
content is based on upstream commit
`5beb35b040e3de97e54fa9e386d7e42d15c295c2`. The upstream MIT license and its
copyright notice are preserved in [LICENSE-mattpocock-skills](LICENSE-mattpocock-skills).

## Updating these copies

Update these skills manually so upstream improvements do not erase local
invocation policy, routing, metadata, or license changes:

1. Fetch the upstream repository and choose the new commit to review. Keep the
   current base SHA unchanged until the update is merged and reviewed.
2. Review upstream changes since the recorded base for each mapped source path.
   Replace `NEW_SHA` below with the commit SHA being reviewed:

   ```sh
   git -C /path/to/mattpocock-skills diff \
     5beb35b040e3de97e54fa9e386d7e42d15c295c2 NEW_SHA -- \
     skills/engineering/ask-matt \
     skills/engineering/domain-modeling \
     skills/productivity/grill-me \
     skills/engineering/grill-with-docs \
     skills/productivity/grilling
   ```

3. From the personal skills repository root, compare each local copy with the
   upstream version at the recorded base to identify existing local adaptations.
   For example:

   ```sh
   UPSTREAM_DIR=/path/to/mattpocock-skills
   SOURCE_PATH=skills/productivity/grill-me
   LOCAL_SKILL=./grill-me
   BASE_DIR=/tmp/grill-me-upstream-base
   mkdir -p "$BASE_DIR"
   git -C "$UPSTREAM_DIR" archive \
     5beb35b040e3de97e54fa9e386d7e42d15c295c2 "$SOURCE_PATH" \
     | tar -x -C "$BASE_DIR"
   diff -ru "$BASE_DIR/$SOURCE_PATH" "$LOCAL_SKILL"
   ```

   `diff` exits with status 1 when it finds differences; those are the local
   adaptations to preserve or reconsider. Merge the reviewed upstream changes
   into the local copy; do not replace the whole skill directory blindly.
4. Preserve the local behavior: `grill-me` and `grill-with-docs` are eligible
   for implicit invocation, their existing Codex interface labels remain,
   and `ask-matt` routes temporary alignment to `grill-me` and durable project
   decisions to `grill-with-docs`.
5. Validate the changed skill directories, inspect the complete diff, and
   confirm the upstream license and copyright notice remain present. Only then
   replace the recorded base SHA with `NEW_SHA`.
6. Commit and publish this personal skills repository. In consuming
   repositories, update only the affected installed skills, for example:

   ```sh
   npx skills update grill-me
   npx skills update grill-with-docs
   npx skills update grilling
   npx skills update domain-modeling
   npx skills update ask-matt
   ```

   Review the resulting lockfile and installed skill copies in each consumer.
