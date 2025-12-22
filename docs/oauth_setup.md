# OAuth Setup (Yahoo Fantasy API)

This project supports both OAuth 2.0 (recommended) and OAuth 1.0a (fallback).

## Create the Yahoo app
1) Visit the Yahoo Developer portal.
2) Create a new app and enable **Fantasy Sports (Read)** permissions.
3) Choose **Confidential Client**.
4) Add a Redirect URI that you control (must match exactly).

Common Redirect URI examples:
- Local dev: `https://localhost/callback`
- GitHub Pages: `https://<username>.github.io/<repo>/callback`

## Configure `.env`
Copy the example and fill in values:
```
YAHOO_CONSUMER_KEY=your_client_id
YAHOO_CONSUMER_SECRET=your_client_secret
YAHOO_OAUTH_REDIRECT_URI=https://localhost/callback
YAHOO_OAUTH_SCOPE=fspt-r
```

## Bootstrap (OAuth 2.0 recommended)
1) Run:
   - `python scripts/oauth2_bootstrap.py`
2) Approve the app in the browser.
3) Paste the full redirect URL (or the `code`) when prompted.
4) Tokens are stored in `config/oauth_tokens.json`.

## Bootstrap (OAuth 1.0a fallback)
If your app is configured for OAuth 1.0a and OAuth 2.0 fails:
1) Run:
   - `python scripts/oauth_bootstrap.py`
2) Approve the app in the browser.
3) If redirect fails to load, copy `oauth_verifier` from the URL.
4) Tokens are stored in `config/oauth_tokens.json`.

## Notes
- The Redirect URI must match the Yahoo app settings exactly.
- `config/oauth_tokens.json` is ignored by git. Do not commit tokens.
