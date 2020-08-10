#! /bin/bash
# Update web page
cd scripts
python setup_page.py
cd ..

# Commit to GitHub
git add .
git commit -m "$1"
git push