# Contributing to DE Learning

Thanks for helping. Even small fixes, like a wrong default value or a confusing sentence, make this better for everyone using it to prepare.

## Ways to contribute

| You want to… | Do this |
| --- | --- |
| Report a mistake or unclear explanation | Open an issue using the **Content correction** template |
| Suggest a topic or a new learning path | Open an issue using the **Topic request** template |
| Fix or improve content yourself | Open a pull request (steps below) |

## Pull request workflow

1. **Fork** the repo (or create a branch if you have write access). Name it after the change, for example `fix/aqe-skew-threshold` or `add/streaming-watermarks`.
2. Make your change. Read [AGENTS.md](AGENTS.md) first; it explains the page structure, design tokens and the topic-tracker rules.
3. Run the checks:
   ```bash
   python3 scripts/check.py
   ```
4. Open the pages you changed in a browser, in light and dark mode and at phone width.
5. Open a pull request into `main` and fill in the template.
6. The maintainer reviews it. Expect questions on technical claims; please include a source link for new facts.

## Ground rules

- **One change per PR.** Easier to review and easier to revert.
- **Don't reorder or delete tracker topics** in `index.html`. Append only; see AGENTS.md for why.
- **Keep it dependency-free.** No frameworks, build tools, CDNs or trackers.
- **Credit sources** for numbers and defaults.
- AI-assisted contributions are welcome. You're responsible for checking that the content is correct, and please say in the PR that an AI agent helped.

## Undoing a bad change

Every merged change can be reverted with one click from its pull request page (**Revert**), or by the maintainer with `git revert <commit>`. Nothing is lost.
