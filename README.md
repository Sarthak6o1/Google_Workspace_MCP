# Google Workspace MCP for LibreChat

Add Gmail, Calendar, Drive, Docs, Sheets, Slides, Forms, Tasks, and Chat to [LibreChat](https://github.com/danny-avila/LibreChat).

---

## 3-Step Setup

### 1. API key (LLM)

Add your LLM provider key(s) to `.env`. LibreChat supports many providers. **OpenAI, Claude, and Gemini work with env vars only**; Azure OpenAI needs YAML config in `librechat.yaml`.

| Provider | Env var(s) | Get key |
|----------|------------|---------|
| **OpenAI** (GPT-4, GPT-4o, o1) | `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com/api-keys) |
| **Anthropic** (Claude) | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com/) |
| **Google / Gemini** | `GOOGLE_KEY` or `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com/apikey) |
| **Azure OpenAI** | `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_API_INSTANCE_NAME`, `AZURE_OPENAI_API_DEPLOYMENT_NAME` + YAML | [portal.azure.com](https://portal.azure.com/) |
| **OpenRouter** (many models) | `OPENROUTER_KEY` | [openrouter.ai](https://openrouter.ai/keys) |
| **Groq** | `GROQ_API_KEY` | [console.groq.com](https://console.groq.com/) |
| **Mistral** | `MISTRAL_API_KEY` | [console.mistral.ai](https://console.mistral.ai/) |
| **Cohere** | `COHERE_API_KEY` | [dashboard.cohere.com](https://dashboard.cohere.com/) |
| **Perplexity** | `PERPLEXITY_API_KEY` | [perplexity.ai](https://www.perplexity.ai/settings/api) |
| **Together AI** | `TOGETHERAI_API_KEY` | [platform.together.ai](https://api.together.ai/) |
| **Fireworks** | `FIREWORKS_API_KEY` | [fireworks.ai](https://fireworks.ai/) |
| **DeepSeek** | `DEEPSEEK_API_KEY` | [platform.deepseek.com](https://platform.deepseek.com/) |
| **xAI** (Grok) | `XAI_API_KEY` | [console.x.ai](https://console.x.ai/) |
| **Hugging Face** | `HUGGINGFACE_TOKEN` | [huggingface.co](https://huggingface.co/settings/tokens) |
| **AnyScale** | `ANYSCALE_API_KEY` | [console.anyscale.com](https://console.anyscale.com/) |
| **ShuttleAI** | `SHUTTLEAI_API_KEY` | [shuttleai.app](https://www.shuttleai.app/) |
| **Unify** | `UNIFY_API_KEY` | [unify.ai](https://unify.ai/) |
| **Helicone** (gateway) | `HELICONE_KEY` | [helicone.ai](https://helicone.ai/) |
| **AWS Bedrock** | `BEDROCK_AWS_ACCESS_KEY_ID` + `SECRET` | [AWS Console](https://console.aws.amazon.com/) |

**Azure OpenAI:** Add env vars in `.env` and uncomment the `azureOpenAI` block in `librechat.google-workspace.example.yaml` (or your `librechat.yaml`). Configure `groups` with `instanceName`, `deploymentName`, and `apiKey`.

See [LibreChat docs](https://docs.librechat.ai/configuration/librechat_yaml/ai_endpoints) for full config.

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

**Copy config:** Copy `librechat.google-workspace.example.yaml` into your `librechat.yaml`, or merge the `mcpServers` and `endpoints` blocks. The example includes:
- **Azure OpenAI** (commented): uncomment and configure for Azure
- **OpenAI / Claude / Gemini** (commented): optional overrides only if needed
- **OpenRouter** (active) plus commented configs for Groq, Mistral, Cohere, Together, Perplexity, DeepSeek, xAI, Hugging Face, Fireworks, AnyScale, ShuttleAI, Unify, and Helicone—uncomment the ones you use.

**Copy env:** `cp Google_Workspace_MCP/.env.example .env` then add your keys.

**Scripts path:** The `scripts` folder must live in the LibreChat project root. The YAML references `scripts/mcp_server.py` relative to that root.

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

| Service | Examples |
|---------|----------|
| **Gmail** | Search (`from:boss@company.com`, `is:unread`), read, send, labels, archive |
| **Calendar** | List agenda, create events, Meet links, update, delete |
| **Drive** | Search, upload, share, copy, move, folders, revisions |
| **Docs** | Create, read, append, search/replace text |
| **Sheets** | Read, append rows, clear ranges, tab management |
| **Slides** | Create, list slides, read content, add slides |
| **Forms** | Create, inspect, add questions, read responses |
| **Tasks** | List, create, complete, delete, manage task lists |
| **Chat** | Send messages, list spaces, members, history |

---

## GCP: Enable APIs

In [Google Cloud Console](https://console.cloud.google.com/) → **APIs & Services** → **Library**, enable:

- Gmail API, Google Calendar API, Google Drive API
- Google Docs API, Google Sheets API, Google Slides API
- Google Forms API, Google Tasks API, Google Chat API (if needed)

---

## Configuration Notes

- **`token.json`**: Created in LibreChat root after first OAuth. Delete it to re-authenticate.
- **Single-user**: One Google account per LibreChat instance. `token.json` is shared.
- **Production**: Change `GOOGLE_MCP_REDIRECT_URI` to your deployed URL (e.g. `https://your-domain.com/oauth/callback`).
- **Port 8080**: OAuth flow uses a local server on 8080. Ensure nothing else uses it.

---

## Example Prompts

- "Search my Gmail for emails from last week"
- "What's on my calendar today?"
- "Create a Google Doc titled Meeting Notes"
- "List my Drive files in the root folder"
- "Add a row to my spreadsheet"

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| OAuth not opening | Add `http://localhost:8080/` to GCP redirect URIs |
| MCP fails | `pip install -r scripts/requirements.txt`; Python 3.11+ |
| LLM not working | Check your provider key in `.env` (e.g. GEMINI_API_KEY, OPENROUTER_KEY) |
| `token.json` invalid | Delete `token.json` and click **google_workspace** again |
| Port 8080 in use | Stop other services; OAuth uses 8080 for callback |

---

## Security

- Never commit `token.json`, `.env`, or client secrets.
- OAuth scopes include Gmail, Drive, Calendar, etc. Review them in GCP before deploying.
- For production, use HTTPS redirect URIs and secure credential storage.

---

## License

MIT
