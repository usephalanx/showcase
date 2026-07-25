# Phalanx × FetchSandbox — mirror showcase

This is a **real** end-to-end artifact, not a mockup.

`acme-billing/` is a demo app (Stripe + Paddle + Clerk) that lived on a laptop.
FetchSandbox extracted it and shipped it to Phalanx's live sandbox
(`POST /v1/run_probe`). **Phalanx reconstructed the repo in its own container and
checksummed every file there.** The checksums Phalanx reported match the laptop
original, file for file.

See **ATTESTATION.md** for the raw run.

## The chain

```
~/acme-billing  ──FS extract (tar_dir_b64)──►  POST /v1/run_probe  ──►  Phalanx container
  12 files                                      (the live prod box)      reconstructs +
                                                                          sha256s each file
                                          ◄──────────  stdout  ◄──────────  reports back
                             compared to the laptop original → identical
```

No local reconstruction anywhere in the verified chain.
