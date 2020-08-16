#! /bin/bash
# Update web page
echo "Updating page..."
cd scripts
python setup_page.py
cd ..
echo "Page updated"

# Commit to GitHub
echo "Pushing to GitHub..."
git add .
git commit -m "$1"
git push