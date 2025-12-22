# Deployment (GitHub Pages)

This repo publishes the static site in `site/` to a `gh-pages` branch using `git subtree`.

## One-time setup
1) Create a GitHub repo (no README).
2) Initialize git and commit (already done for this project).
3) Create the `gh-pages` branch from `site/`:
```
git subtree split --prefix site -b gh-pages
git push -u origin gh-pages
```
4) In GitHub: Settings -> Pages -> Source: `gh-pages` / `(root)`.

## Deploy updates
Whenever you regenerate data or update the site:
```
git add .
git commit -m "Update site data"
git push
git subtree push --prefix site origin gh-pages
```

## Live URL
GitHub Pages will be:
```
https://<username>.github.io/<repo>/
```

## Notes
- Only files in `site/` are published to the live site.
- `.env`, SQLite files, and OAuth tokens are excluded by `.gitignore`.
