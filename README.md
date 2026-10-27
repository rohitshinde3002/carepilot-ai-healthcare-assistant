# CarePilot AI — Healthcare Companion Prototype

Prepared for the **AI Growth & Automation Associate — Task 1: AI Skills & Prompt Engineering Assessment**.

## Features
- AI Health Guide: general health Q&A interface, offline guide, and optional live Groq language-model responses.
- Appointment Planner: session-local appointment-preparation topics and CSV export. It does not book real appointments.
- Wellness Planner: interactive habit checklist and text download.
- Project & Submission: requirement mapping and final checklist.

## Safety and limitations
Educational prototype, not a medical device. It does not diagnose or prescribe. Do not enter identifying or confidential medical information. Planner data is held only in the current session. Live AI requires your own API key; without it, offline guidance is shown.

## Run on Windows / VS Code
1. Extract ZIP and open folder in VS Code.
2. Run in PowerShell:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If activation is blocked:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```
3. Install and launch:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Optional live AI
Create `.streamlit/secrets.toml` containing:
```toml
GROQ_API_KEY = "your_own_key_here"
```
Restart Streamlit. Never upload the key to GitHub. Test with a general non-sensitive question. Provider/model access can change; update the model identifier in `app.py` if needed.

## Submission requirements from the supplied PDF
1. Minimum 2-minute video covering AI tools/why, prompt revisions, approach, challenges/solutions, and final outcome.
2. Prompt documentation with all actual prompts and significant revisions (`prompts.md`).
3. Accessible project link (GitHub, live app, or public Drive). If not hosted, provide files and run instructions.

See `ASSESSMENT_REQUIREMENTS.md` and `VIDEO_DEMO_SCRIPT.md`.
