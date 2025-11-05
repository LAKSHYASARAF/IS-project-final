# File Integrity Checker
A Simple browser friendly Flask app  that lets a user register a file (stores its SHA256 checksum) and later verify the same file hasn't changed.

Project Core Idea

- Every file has a fingerprint called a HASH. If even one bit changes in the file the hash changes drastically. By comparing hashes we can detect tampering or corruption.
- This project demonstrates the Data Integrity property of the CIA triad using SHA-256 hashing.

What this system can do (two related approaches)

1) Browser-based, passwordless verification (concept / preferred demo)
- User selects a trusted/original file in the browser.
- The app computes the SHA-256 hash (the "Baseline Fingerprint") and stores it in the browser's localStorage (no server, no passwords).
- Later, the user selects a file again and the app recomputes SHA-256 and compares it to the baseline.
- If the hashes match → file is original. If not → file was modified/corrupted/tempered.

Technologies for browser-based approach (concept)
- HTML + CSS for the UI.
- PyScript (optional) to run Python in the browser or plain JavaScript.
- Web Crypto API (recommended) for fast and secure SHA-256 hashing.
- localStorage for storing the baseline fingerprint in the user's browser (passwordless, per-device storage).

Why this matters for Information Security
- Demonstrates Integrity (one of CIA): ensures that a file hasn't been altered.
- SHA-256 is a standard used widely in blockchain, digital signatures, ISO image verification, and secure file checks.

Real-world examples where hashes are used
- Verifying downloaded ISO images or installers.
- Blockchain block linking and immutability proofs.
- Tamper-proof evidence storage and audit trails.

2) Server-backed Flask demonstration
A simple Flask app that implements similar functionality but stores files and checksums on the server:

- `main.py` — Flask server with endpoints to register and verify files.
	- Register: uploads file to `uploads/`, computes SHA-256 and stores it in `checksums.json`.
	- Verify: accepts an uploaded file, computes SHA-256 and compares with stored checksum for that filename.
- `templates/index.html` — simple UI used by the Flask app.
- `uploads/` — directory where uploaded files are saved.
- `checksums.json` — JSON file that maps filenames to their recorded SHA-256 and timestamp.

Run the Flask app locally (Windows PowerShell)

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate; pip install -r requirements.txt
```

2. Start the server:

```powershell
python main.py
```

3. Open your browser:

http://127.0.0.1:8000


Security and privacy considerations

- Browser-based localStorage approach keeps fingerprints only on the user's device (good for privacy and passwordless use) but is per-device — users won't share baselines across devices unless you add sync.
- Server-backed approach stores checksums on the server and requires proper access controls, backups, and possibly authentication for multi-user safety.
- Always validate file sizes and types on upload if you run the server in a public environment to avoid abuse.

Where to look in this repo

- `main.py` — main Flask logic (compute SHA-256 and store/compare checksums).
- `templates/index.html` — UI used by the Flask demo.
- `uploads/` and `checksums.json` — runtime artifacts.

How you can extend this project

- Add a browser-only demo using Web Crypto API and localStorage (no backend). This matches the passwordless concept described above.
- Switch storage to map by content hash instead of filename to avoid name collisions.
- Add user accounts and access control if multiple users must share baselines.
- Provide an export/import of baseline fingerprints so users can sync across devices.
