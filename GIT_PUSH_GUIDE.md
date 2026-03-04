# 📤 Git Push Guide - VAPT Scanner to GitHub

## One-Time GitHub Setup

### 1. Create Repository on GitHub
```bash
# Go to https://github.com/new
# Repository name: VAPT_Scanner
# Description: Vulnerability Assessment and Penetration Testing Scanner
# Public or Private: Choose based on preference
# DO NOT initialize with README (we have one)
# DO NOT add .gitignore (we have one)
# DO NOT add license (optional)

# Copy the repository URL from GitHub
# Examples:
# HTTPS: https://github.com/yourusername/VAPT_Scanner.git
# SSH: git@github.com:yourusername/VAPT_Scanner.git
```

---

## Push to GitHub (First Time)

### Option 1: HTTPS (Simpler, Password Protected)

```bash
# 1. Navigate to project
cd /path/to/VAPT_Scanner

# 2. Initialize git (if not already done)
git init

# 3. Add GitHub repository as remote
git remote add origin https://github.com/yourusername/VAPT_Scanner.git

# 4. Create initial commit
git add .
git commit -m "feat: Initial VAPT Scanner - Consolidated architecture with 9 scanners

- Create consolidated scanner modules for web, network, static, tools
- Fix URL namespace routing (vaptapi, arachniscanner)
- Add background threading for non-blocking scan execution
- Integrate result display with scan interface
- Add comprehensive documentation (QUICK_START, ARCHITECTURE, etc)
- Support Kali Linux deployment
- JWT auth and organization isolation"

# 5. Set branch name to main (GitHub default)
git branch -M main

# 6. Push to GitHub
git push -u origin main

# Your code is now on GitHub!
```

### Option 2: SSH (More Secure, Key-Based)

```bash
# 1. Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your.email@example.com"

# 2. Add SSH key to GitHub
# Settings → SSH and GPG keys → New SSH key
# Paste contents of ~/.ssh/id_ed25519.pub

# 3. Navigate to project
cd /path/to/VAPT_Scanner

# 4. Initialize and set remote
git init
git remote add origin git@github.com:yourusername/VAPT_Scanner.git

# 5. Commit
git add .
git commit -m "Initial commit: Consolidated VAPT Scanner architecture"

# 6. Push
git branch -M main
git push -u origin main
```

---

## Commit Message Template

Use this format for clear commit history:

```
feat: Add new feature
fix: Fix bug
docs: Documentation changes
refactor: Code restructuring
chore: Maintenance tasks
perf: Performance improvements

Example:
feat: Add scan scheduling with Celery

- Implement background task queue integration
- Add scan_id to task tracking
- Create scheduler views and forms
- Update documentation
```

---

## Common Git Commands (After First Push)

### Make Changes and Push

```bash
# 1. Check status
git status

# 2. View changes
git diff filename.py

# 3. Stage changes
git add filename.py           # Single file
git add .                     # All changes

# 4. Commit
git commit -m "fix: Resolve ZAP scan timeout issue"

# 5. Push
git push

# All changes now on GitHub!
```

### Update from Remote

```bash
# Pull latest changes from GitHub
git pull origin main

# Useful if working with others
```

### Create Feature Branch

```bash
# Create and switch to new branch
git checkout -b feature/add-celery-tasks

# Make changes, commit
git add .
git commit -m "feat: Add Celery task queue for scan scheduling"

# Push new branch
git push -u origin feature/add-celery-tasks

# Create Pull Request on GitHub
```

---

## Pre-Push Checklist

Before pushing to GitHub:

```bash
✅ All tests pass
python manage.py test

✅ No debug prints left in code
grep -r "print(" . --include="*.py" | grep -v "# print"

✅ No hardcoded secrets
grep -r "password\|secret\|api_key" . --include="*.py"

✅ .env file in .gitignore
cat .gitignore | grep ".env"

✅ All documentation files present
ls -la QUICK_START.md SCANNER_ARCHITECTURE.md IMPLEMENTATION_SUMMARY.md

✅ Git status clean
git status
# Should show "working tree clean" after commit

✅ Commit message descriptive
git log -1
# Should have clear, detailed message
```

---

## Post-Push Verification

### Verify on GitHub

```bash
# 1. Visit your GitHub repo
https://github.com/yourusername/VAPT_Scanner

# 2. Check files are there
# - README_GITHUB.md should display as main page
# - All .py files visible
# - Documentation files visible

# 3. View commit history
# Click "X commits" to see history

# 4. Verify .gitignore is working
# Should NOT see: db.sqlite3, venv/, .env, __pycache__
```

---

## If Something Goes Wrong

### Undo Last Commit (Not Yet Pushed)

```bash
# Undo last commit but keep changes
git reset --soft HEAD~1

# Undo last commit and discard changes
git reset --hard HEAD~1
```

### Undo Already Pushed Commit

```bash
# Create new commit that undoes changes
git revert HEAD

# Or reset and force push (use carefully!)
git reset --hard HEAD~1
git push -f origin main
```

### Fix Commit Message

```bash
# Amend the last commit message
git commit --amend -m "Corrected commit message"

# If already pushed:
git push -f origin main  # Force push (use carefully!)
```

---

## File Structure for GitHub

Your GitHub repo will have:

```
VAPT_Scanner/
├── README_GITHUB.md              ← Main page, shown on GitHub
├── QUICK_START.md
├── SCANNER_ARCHITECTURE.md
├── IMPLEMENTATION_SUMMARY.md
├── KALI_SETUP_GUIDE.md
├── FIX_SUMMARY.md
├── setup_kali.sh
├── requirements.txt
├── manage.py
├── vapt/
├── webscanners/
├── networkscanners/
├── staticscanners/
├── tools/
├── authentication/
├── dashboard/
├── ... (all other Django apps)
├── .gitignore
└── .git/                         ← Hidden, created by git
```

---

## GitHub Pages (Optional)

To create documentation site:

```bash
# 1. Create gh-pages branch
git checkout --orphan gh-pages

# 2. Add documentation files
cp README_GITHUB.md index.md
cp QUICK_START.md quick-start.md
cp SCANNER_ARCHITECTURE.md architecture.md

# 3. Commit and push
git add .
git commit -m "docs: Add GitHub Pages documentation"
git push -u origin gh-pages

# 4. Enable in GitHub Settings
# Settings → Pages → Branch: gh-pages → / (root) → Save

# Your docs at: https://yourusername.github.io/VAPT_Scanner/
```

---

## GitHub Actions (Optional - CI/CD)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: 3.10
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test
    
    - name: Check code style
      run: |
        pip install flake8
        flake8 .
```

Push this file to GitHub and tests run automatically!

---

## Collaborators (Optional)

To allow others to contribute:

```
GitHub Settings → Collaborators → Add people
Invite users to collaborate on the project
```

---

## Quick Reference

```bash
# First time setup
git init
git remote add origin https://github.com/YOU/VAPT_Scanner.git
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main

# After first setup
git add .
git commit -m "Your message"
git push

# That's it!
```

---

## Helpful Links

- [GitHub Quickstart](https://docs.github.com/en/get-started/quickstart)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Actions](https://docs.github.com/en/actions)
- [GitHub Pages](https://pages.github.com/)

---

## Success Indicators

✅ You've successfully pushed when:
- [ ] Repository appears on your GitHub profile
- [ ] All files visible in GitHub web interface
- [ ] Python files show syntax highlighting
- [ ] Documentation renders as Markdown
- [ ] Commit history visible ("X commits")
- [ ] Branch shows as "main"
- [ ] README_GITHUB.md displays as main page

---

## Next Steps After Push

1. **Share Repository**
   - Send link to team: `https://github.com/yourusername/VAPT_Scanner`

2. **Create Releases**
   - Tag versions: `git tag -a v2.0 -m "Release 2.0"`
   - Create GitHub Release for version history

3. **Setup CI/CD**
   - Add GitHub Actions for automated testing

4. **Enable Discussions**
   - Settings → Features → Enable Discussions

5. **Add Issues**
   - Use GitHub Issues for tracking bugs/features

---

**Status**: 🟢 Ready to Push  
**Next**: Run the commands above to push your code!
