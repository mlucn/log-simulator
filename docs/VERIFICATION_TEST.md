# Branch Protection Verification Test

This file is used to verify that branch protection rules are correctly configured.

## Expected Behavior

When this file is pushed in a PR to `main`, the following checks should run:

### Test Checks (4 checks)
- ✅ test (3.9)
- ✅ test (3.10)
- ✅ test (3.11)
- ✅ test (3.12)

### Lint Check (1 check)
- ✅ lint / Linting and Type Checking

## Verification Steps

1. All 5 checks should appear in the PR
2. All checks should pass (green)
3. PR should be mergeable only after all checks pass
4. "Merge pull request" button should be enabled only when:
   - All required checks pass
   - Branch is up to date with main
   - Any required approvals are met

## Current Configuration

- **Total Required Checks**: 5
- **Python Versions Tested**: 3.9, 3.10, 3.11, 3.12
- **Security Scanning**: Bandit, Safety
- **Code Quality**: Black, Ruff, Mypy
- **Test Coverage**: 64%

---

**Test Date**: 2025-11-17
**Purpose**: Verify branch protection configuration
**Status**: This file will be deleted after verification
