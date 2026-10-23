# FOM — Future of Myanmar

Team 6 product code for the Escrow, Cross banking, and shop inquiry experience.

## Run locally

Requires Python 3.11 or newer. No package installation or frontend build is needed.

```sh
python server.py
```

Open http://127.0.0.1:8800/ for the customer app, `/mobile.html` for the phone preview, or `/admin.html` for the staff workspace. On Windows, you can also double-click `Start FOM.cmd`.

The app creates its local SQLite database automatically in `data/`.

## Vercel deployment

The GitHub Actions workflow `.github/workflows/deploy-vercel.yml` deploys `main` or `master` to Vercel and supports manual runs. Add `VERCEL_TOKEN`, `VERCEL_ORG_ID`, and `VERCEL_PROJECT_ID` under repository Settings → Secrets and variables → Actions. The workflow pulls the production environment, builds, and deploys the prebuilt output. It does not require connecting this organization repository to a paid Vercel team Git integration.

Vercel serves `public/` and runs `api/index.py` for API requests. Shared records live in a hosted libSQL database (Turso); local SQLite files are not used on Vercel. Set these production environment variables in the Vercel project:

- `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN`: credentials for a libSQL database.
- `HANDSHAKE_STAFF_PASSWORD`: a private staff password.
- `HANDSHAKE_CALLBACK_SECRET`: a private simulator callback secret.
- `HANDSHAKE_PUBLIC_URL`: the public HTTPS origin if using a custom domain. Vercel's default deployment domains are detected automatically.

The database schema initializes transactionally on the first API request. Missing database configuration returns a clear unavailable response instead of using temporary local storage. The health check is `/api/health`. Simulator jobs advance on incoming API requests; the current customer receipt flow does not depend on a background worker. Use fictional information for this prototype.

Presentation and video files stay in GitHub and are excluded from the deployed app bundle.

## Submission files

- `deck.pptx`: final 15-slide presentation.
- `video.mp4`: final pitch video (4 minutes 45 seconds).

## Included flows

- Escrow: create a deal, share its code, submit a receipt, record delivery, and confirm receipt.
- Cross banking: create a request, share its code, view receiving details, and submit a receipt.
- Shop inquiry: submit shop details for review.
- Staff workspace and the retained local provider simulator.

This is a local prototype. Receipt submission does not verify payment or move money. Bank and wallet services are not connected.

The local staff simulator uses usernames `support`, `operations`, `finance-a`, `finance-b`, and `admin`, with the demonstration password `handshake-demo-2026`. Set `HANDSHAKE_STAFF_PASSWORD` in the process environment to replace it. Other optional environment settings are listed in `.env.example`; the server does not load that file automatically.
