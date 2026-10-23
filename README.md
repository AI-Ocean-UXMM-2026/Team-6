# FOM — Future of Myanmar

Team 6 product code for the Escrow, Cross banking, and shop inquiry experience.

## Run locally

Requires Python 3.11 or newer. No package installation or frontend build is needed.

```sh
python server.py
```

Open http://127.0.0.1:8800/ for the customer app, `/mobile.html` for the phone preview, or `/admin.html` for the staff workspace. On Windows, you can also double-click `Start FOM.cmd`.

The app creates its local SQLite database automatically in `data/`.

## Live demo hosting

Use the included `render.yaml` Blueprint on Render to deploy branch `main` as a free Python web service. No package installation is required. The configuration binds the server to the hosting port, supports the service's HTTPS origin, and generates private staff and callback secrets. The health check is `/api/health`.

Free hosting is for the submission demo: records and uploaded receipts reset when the service restarts, redeploys, or sleeps. The first visit after inactivity may take about a minute to load. Use fictional information. Persistent storage requires a paid service and disk; set `HANDSHAKE_DB` to a location on that disk if upgrading.

For another host, set `HANDSHAKE_HOST=0.0.0.0`, `PORT`, `HANDSHAKE_PUBLIC_URL` to the public HTTPS origin, and a private `HANDSHAKE_STAFF_PASSWORD`. Run `python server.py`.

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
