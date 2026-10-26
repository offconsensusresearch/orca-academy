# Off Consensus Research Academy: certificate time-stamps

This repository holds OpenTimestamps proofs for certificates issued by Off Consensus Research Academy.
Each file in `proofs/` is named after a salted fingerprint of one certificate. The files contain no names,
emails or serial numbers. Anyone can verify a proof at https://opentimestamps.org.

The `docs/` folder is the small public website served at academy.offconsensusresearch.com (GitHub Pages).

## Folders
- `docs/`: the public website served at academy.offconsensusresearch.com (GitHub Pages). It shows a holding page until the certificate portal is live.
- `portal_pages_ready/`: the final pages that embed the certificate portal. They replace `docs/` once the portal web app is deployed.
- `proofs/`: OpenTimestamps proofs, added by the time-stamping job.
