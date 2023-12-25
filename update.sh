#!/usr/bin/env zsh

# Move to release branch
git checkout beget_master
# Pick the latest commit
git cherry-pick HEAD
# Minificate all static files
minify -r public_html/static -o public_html/
# Adding new changes 
git add .
# New commit 
git commit -m "Applying minification"
# Update branch
git push
