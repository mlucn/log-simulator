# GitHub Branch Protection Configuration

This document outlines the recommended branch protection rules for the `main` branch after adding comprehensive testing and security scanning.

## Required Status Checks

With the updated CI/CD pipeline, you should require the following checks to pass before merging:

### Test Job Checks
- `test (3.9)` - Tests on Python 3.9
- `test (3.10)` - Tests on Python 3.10
- `test (3.11)` - Tests on Python 3.11
- `test (3.12)` - Tests on Python 3.12

### Lint Job Checks
- `lint / Linting and Type Checking` - All linting and security scans

## How to Update Branch Protection Rules

### Via GitHub Web Interface

1. Go to your repository: https://github.com/mlucn/log-simulator
2. Click on **Settings** tab
3. In the left sidebar, click **Branches**
4. Under "Branch protection rules", click **Edit** on the `main` branch rule (or **Add rule** if none exists)
5. Configure the following settings:

#### Require a pull request before merging
- ✅ Enable "Require a pull request before merging"
- ✅ Enable "Require approvals" (set to 1 if you want self-approval, or 2+ for team review)
- ✅ Enable "Dismiss stale pull request approvals when new commits are pushed"

#### Require status checks to pass before merging
- ✅ Enable "Require status checks to pass before merging"
- ✅ Enable "Require branches to be up to date before merging"
- Search for and add these status checks:
  - `test (3.9)`
  - `test (3.10)`
  - `test (3.11)`
  - `test (3.12)`
  - `lint / Linting and Type Checking`

#### Additional Recommended Settings
- ✅ Enable "Require conversation resolution before merging"
- ✅ Enable "Do not allow bypassing the above settings"
- ✅ Enable "Restrict who can push to matching branches" (optional - for team repos)

6. Click **Save changes** at the bottom

### Via GitHub CLI

```bash
# Install gh CLI if not already installed
# https://cli.github.com/

# Update branch protection for main
gh api repos/mlucn/log-simulator/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["test (3.9)","test (3.10)","test (3.11)","test (3.12)","lint / Linting and Type Checking"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"dismiss_stale_reviews":true,"require_code_owner_reviews":false,"required_approving_review_count":1}' \
  --field restrictions=null
```

## What Each Check Does

### Test Checks (`test (3.X)`)
These run on every Python version we support:
- Install dependencies (including API dependencies)
- Run all unit and integration tests with pytest
- Generate coverage reports
- Upload coverage to Codecov (Python 3.12 only)

**Pass Criteria**: All tests must pass with no failures

### Lint Check (`lint / Linting and Type Checking`)
This runs all code quality and security checks:
1. **Ruff** - Fast Python linter (checks code style, errors)
2. **Black** - Code formatter verification (ensures consistent formatting)
3. **Mypy** - Static type checker (catches type errors)
4. **Bandit** - Security linter (scans for security issues)
5. **Safety** - Dependency vulnerability scanner (checks for known CVEs)

**Pass Criteria**:
- Ruff: No linting errors
- Black: Code is formatted correctly
- Mypy: No type errors
- Bandit: No security issues found
- Safety: No critical vulnerabilities (informational only, continue-on-error)

## Verifying Branch Protection

After setting up, verify it works:

1. Create a test branch with intentional issues:
   ```bash
   git checkout -b test-branch-protection
   echo "print('bad formatting')" >> test.py
   git add test.py
   git commit -m "test: verify branch protection"
   git push -u origin test-branch-protection
   ```

2. Create a PR for this branch
3. Verify that:
   - PR cannot be merged until checks pass
   - Black check fails due to formatting
   - You can see all required checks in the PR

4. Clean up:
   ```bash
   git checkout main
   git branch -D test-branch-protection
   git push origin --delete test-branch-protection
   ```

## Troubleshooting

### Status check not appearing in list
- Make sure you've created at least one PR after updating `.github/workflows/test.yml`
- The status check names must match exactly (case-sensitive)
- Wait a few minutes after a PR run for GitHub to register the check

### Checks always failing
- Check the Actions tab for error details
- Ensure all dependencies are properly installed in the workflow
- Verify pyproject.toml configuration is correct

### Can't merge even when checks pass
- Ensure "Require branches to be up to date before merging" is properly configured
- Rebase or merge main into your PR branch
- Check if there are conversation threads that need resolution

## Current CI/CD Workflow Details

**Workflow File**: [.github/workflows/test.yml](.github/workflows/test.yml)

**Triggers**: Pull requests to `main` branch

**Jobs**:
1. **test** (matrix: Python 3.9, 3.10, 3.11, 3.12)
   - Checkout code
   - Setup Python
   - Install dependencies
   - Run pytest with coverage
   - Upload coverage to Codecov

2. **lint** (Python 3.12)
   - Checkout code
   - Setup Python
   - Install dependencies
   - Run ruff
   - Run black
   - Run mypy
   - Run bandit security scan
   - Run safety dependency scan

**Coverage Requirements**:
- Current: 64%
- Target: 70%+ for API module, 85%+ overall (future goal)

## Additional Resources

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Required Status Checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks)
- [Pre-commit Hooks Configuration](.pre-commit-config.yaml)
- [pytest Configuration](../pyproject.toml#L121)
- [Bandit Configuration](../pyproject.toml#L131)
- [Coverage Configuration](../pyproject.toml#L147)
