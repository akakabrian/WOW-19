# Lean 4.27 kernel-check unblock

The proof build has not failed. GitHub has not started any workflow in this new repository.

Tested event paths:

- ordinary pushes to `main`;
- branch creation;
- scheduled full build;
- repeated scheduled one-step smoke build.

No run, status check, smoke branch, `ci-results` branch, or compiler log was created.

## GitHub route

1. Open the repository's **Actions** tab.
2. Enable workflows if GitHub displays an enablement prompt.
3. Select **Lean kernel check**.
4. Choose **Run workflow** on `main`.

The job will publish:

```text
branch: ci-results
file: CI_RESULT.md
```

A valid completion requires:

```text
failed_phase: none
exit_code: 0
```

## Local route

```bash
git clone https://github.com/akakabrian/WOW-19.git
cd WOW-19
bash scripts/run_port_ci.sh
cat ci-output/CI_RESULT.md
```

The script fetches exact pinned source commits, generates the definition-preserving port, rejects proof placeholders, downloads the pinned Mathlib cache, and runs `lake env lean` on the exact final theorem.
