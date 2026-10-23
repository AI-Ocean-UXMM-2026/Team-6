# FOM — Future of Myanmar

Team 6 product code for the Escrow, Cross banking, and shop inquiry experience.

## Run locally

Requires Python 3.11 or newer. No package installation or frontend build is needed.

```sh
python server.py
```

Open http://127.0.0.1:8800/ for the customer app, `/mobile.html` for the phone preview, or `/admin.html` for the staff workspace. On Windows, you can also double-click `Start FOM.cmd`.

The app creates its local SQLite database automatically in `data/`.

## Included flows

- Escrow: create a deal, share its code, submit a receipt, record delivery, and confirm receipt.
- Cross banking: create a request, share its code, view receiving details, and submit a receipt.
- Shop inquiry: submit shop details for review.
- Staff workspace and the retained local provider simulator.

This is a local prototype. Receipt submission does not verify payment or move money. Bank and wallet services are not connected.

The local staff simulator uses usernames `support`, `operations`, `finance-a`, `finance-b`, and `admin`, with the demonstration password `handshake-demo-2026`. Set `HANDSHAKE_STAFF_PASSWORD` in the process environment to replace it. Other optional environment settings are listed in `.env.example`; the server does not load that file automatically.
