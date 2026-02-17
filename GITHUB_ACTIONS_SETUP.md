# GitHub Actions Setup Instructions

## ✅ Workflow Created Successfully!

Your GitHub Actions workflow has been created at:
`.github/workflows/update-papers.yml`

## 🔧 Required Setup Steps

### Step 1: Enable Workflow Permissions

To allow the workflow to commit and push changes, you need to enable write permissions:

1. Go to your repository on GitHub: https://github.com/aalice-z/bst236-coding-blog
2. Click **Settings** (top right)
3. In the left sidebar, click **Actions** → **General**
4. Scroll down to **Workflow permissions**
5. Select **"Read and write permissions"**
6. Check ✅ **"Allow GitHub Actions to create and approve pull requests"** (optional but recommended)
7. Click **Save**

### Step 2: Test the Workflow

#### Option A: Manual Trigger
1. Go to the **Actions** tab in your repository
2. Click on **"Update arXiv Papers"** workflow in the left sidebar
3. Click **"Run workflow"** button (top right)
4. Select the `main` branch
5. Click **"Run workflow"**

#### Option B: Wait for Scheduled Run
The workflow will automatically run daily at midnight UTC (00:00 UTC).

### Step 3: Monitor Workflow Runs

1. Go to the **Actions** tab in your repository
2. You'll see all workflow runs listed
3. Click on any run to see detailed logs
4. Green ✅ means success, Red ❌ means failure

## 📋 What the Workflow Does

Every day at midnight UTC (or when manually triggered):

1. ✅ Checks out your repository
2. ✅ Sets up Python 3.11
3. ✅ Installs dependencies (`requests`)
4. ✅ Fetches latest 20 papers from arXiv matching "machine learning" and "deep learning"
5. ✅ Generates updated `papers.html` with the new data
6. ✅ Commits changes if papers were updated
7. ✅ Pushes to your repository
8. ✅ GitHub Pages automatically deploys the updated site

## 🎯 Expected Behavior

- **If new papers found**: The workflow commits with message "🤖 Auto-update arXiv papers - [date]"
- **If no changes**: The workflow completes without committing
- **Commit author**: `github-actions[bot]`

## 🔍 Troubleshooting

### Workflow fails with "Permission denied"
- Make sure you've enabled "Read and write permissions" in Settings → Actions

### No changes detected every time
- arXiv API might return the same papers
- The papers are sorted by submission date, so changes only happen when new papers are submitted

### Python errors
- Check the Actions logs for detailed error messages
- Dependencies might need updating

## 📝 Customization

To change the search keywords, edit `.github/workflows/update-papers.yml`:

```yaml
- name: Fetch papers from arXiv
  run: |
    python fetch_papers.py "your keywords" "here"
```

To change the schedule, edit the cron expression:

```yaml
schedule:
  - cron: '0 0 * * *'  # Daily at midnight UTC
  # Examples:
  # - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 12 * * *'   # Daily at noon UTC
```

## ✨ Success!

Once set up, your arXiv papers page will automatically stay up-to-date with the latest research!

Visit: https://aalice-z.github.io/bst236-coding-blog/papers.html
