# File Integrity Checker

Simple Flask app that lets a user register a file (stores its SHA256 checksum) and later verify the same file hasn't changed.

How it works
- Upload a file using the "Register file" form. The app saves the file to `uploads/` and records its SHA256 checksum in `checksums.json`.
- To verify, upload the same file with the "Verify file" form. The app computes the SHA256 again and compares it to the stored value. It reports a match (true) or mismatch (false).

Run locally (Windows PowerShell)

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate; pip install -r requirements.txt
```

2. Run the app:

```powershell
python main.py
```

3. Open http://127.0.0.1:8000 in your browser. The UI uses Tailwind CSS via the CDN for simple styling.

Notes
- Checksums are stored in `checksums.json` in the project root.
- Files are stored in `uploads/` and will be overwritten when a file with the same name is re-registered.
- This implementation maps checksums by filename. For multi-user or collision-safe usage, extend the system to use user IDs or compute and index by file content hash instead.

