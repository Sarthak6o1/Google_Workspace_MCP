# Google Workspace MCP for LibreChat

Add Gmail, Calendar, Drive, Docs, Sheets, Slides, Forms, Tasks, and Chat to [LibreChat](https://github.com/danny-avila/LibreChat).

---

## 3-Step Setup

### 1. API key (LLM)

Add any LLM provider key to `.env`. LibreChat supports Gemini, OpenRouter, OpenAI, Anthropic, etc. See [LibreChat docs](https://docs.librechat.ai/) for your provider.

```env
# Examples - add the one(s) you use
GEMINI_API_KEY=your_key
# or OPENROUTER_KEY=your_key
# or OPENAI_API_KEY=your_key
# or ANTHROPIC_API_KEY=your_key
```

### 2. GCP (Google Workspace OAuth)

1. [Google Cloud Console](https://console.cloud.google.com/) → **APIs & Services** → **Credentials**
2. **Create Credentials** → **OAuth client ID** → **Web application**
3. Add these **Authorized redirect URIs**:
   ```
   http://localhost:8080/
   http://localhost:3080/oauth/google/callback
   ```
4. Copy **Client ID** and **Client Secret** → add to `.env`:
   ```
   GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=xxx
   ```

### 3. LibreChat config

**Install add-on:**

```bash
cd LibreChat  # your LibreChat root
git clone https://github.com/Sarthak6o1/Google_Workspace_MCP.git
cp -r Google_Workspace_MCP/scripts .
pip install -r scripts/requirements.txt
```

**Apply patches:** See `integration/README.md` (2 file edits)

**Copy config:** Copy `librechat.google-workspace.example.yaml` into your `librechat.yaml`, or merge the `mcpServers` block.

**Copy env:** `cp Google_Workspace_MCP/.env.example .env` then add your keys.

---

## All-in-one .env template

Copy `.env.example` to your LibreChat `.env`:

```bash
cp Google_Workspace_MCP/.env.example .env
```

Then edit `.env` and add your API key and GCP credentials.

---

## Run

```bash
npm run backend:dev
npm run frontend:dev
```

Open `http://localhost:3090` → click **google_workspace** in MCP menu → complete Google sign-in.

---

## Capabilities

Gmail | Calendar | Drive | Docs | Sheets | Slides | Forms | Tasks | Chat

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| OAuth not opening | Add `http://localhost:8080/` to GCP redirect URIs |
| MCP fails | `pip install -r scripts/requirements.txt`; Python 3.11+ |
| LLM not working | Check your provider key in `.env` (e.g. GEMINI_API_KEY, OPENROUTER_KEY) |

---

## License

MIT
