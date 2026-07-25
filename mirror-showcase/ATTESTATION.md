# ATTESTATION — Phalanx reconstructed this repo (live run)

Endpoint: `POST https://usephalanx.com/v1/run_probe` (prod, token-gated)
Method: FetchSandbox shipped the workspace; the checksum probe ran INSIDE
Phalanx's container. `available=True`, `exit_code=0`.

```
=== LAPTOP: /Users/raj/acme-billing — 12 files ===
=== FS -> PHALANX: shipping workspace to the LIVE /v1/run_probe ===
  available=True exit_code=0 error=None
=== PHALANX's container reported 12 files ===

  [OK] .env.example   local=7c3687e1a1c7  phalanx=7c3687e1a1c7
  [OK] README.md   local=c8d547a1a746  phalanx=c8d547a1a746
  [OK] assets/logo.png   local=8721d07f211e  phalanx=8721d07f211e
  [OK] config/billing.json   local=d4f64ac06b0a  phalanx=d4f64ac06b0a
  [OK] package.json   local=d74d7bcc18bd  phalanx=d74d7bcc18bd
  [OK] src/middleware/auth.js   local=9467dfe051cc  phalanx=9467dfe051cc
  [OK] src/routes/checkout.js   local=0cca8bafd7b5  phalanx=0cca8bafd7b5
  [OK] src/routes/paddle-webhook.js   local=087ea0722469  phalanx=087ea0722469
  [OK] src/routes/stripe-webhook.js   local=88830f202e04  phalanx=88830f202e04
  [OK] src/server.js   local=b75f81881607  phalanx=b75f81881607
  [OK] src/services/db.js   local=a8d3085195a6  phalanx=a8d3085195a6
  [OK] src/services/entitlements.js   local=5deb398fe8a6  phalanx=5deb398fe8a6

  PHALANX RE-CREATED THE REPO FAITHFULLY: True  (12 files verified by Phalanx's own box)
```
