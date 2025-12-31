# Operations and Publishing

## GitHub Pages (gh-pages)
The static site is published from `site/` to the `gh-pages` branch using git subtree.

Publish updates:
```
git add .
git commit -m "Refresh data"
git push
git subtree push --prefix site origin gh-pages
```

If gh-pages rejects with non-fast-forward, re-split and force push:
```
git subtree split --prefix site -b gh-pages-temp
git push -f origin gh-pages-temp:gh-pages
git branch -D gh-pages-temp
```

## Custom domain
GitHub Pages uses `site/CNAME`. Keep this file in sync with the live domain.

## Cloudflare proxy
If Cloudflare is in front of GitHub Pages, caching can delay updates.
Troubleshooting:
- Purge cache for `index.html`, `app.js`, and `/data/*` after deploy.
- Confirm latest `app.js` via:
  https://raw.githubusercontent.com/AdamZ-8113/Fantasy-Football-Awards-Publisher/gh-pages/app.js

## Verification checklist
- Season picker includes latest season.
- Team picker works and hides League Overview on team view.
- "The Schedule Screwed Me" description matches latest copy.
