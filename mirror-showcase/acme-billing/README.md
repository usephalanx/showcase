# acme-workspace-billing

Seat billing for workspaces.

Cards are taken directly in most markets. In merchant-of-record regions the
checkout hands off instead, and seats are granted when that provider confirms.

## Run

```
cp .env.example .env
npm install
npm start
```

## Routes

| route | purpose |
|---|---|
| `POST /checkout/session` | start a checkout for N seats |
| `POST /webhooks/stripe` | subscription + checkout events |
| `POST /webhooks/paddle` | transaction + subscription events |
