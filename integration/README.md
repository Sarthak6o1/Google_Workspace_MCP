# LibreChat Integration Patches

**2 file edits** to add OAuth popup when clicking `google_workspace`. Tested with LibreChat main (March 2025).

---

## 1. Backend: OAuth route

**File:** `api/server/index.js`

### Step 1: Add the `spawn` import (required)

Upstream LibreChat does **not** include `spawn`. Add this near the top, after the other `require` statements (e.g. after `const path = require('path');`):

```js
const { spawn } = require('child_process');
```

### Step 2: Add the OAuth route

Insert the **entire contents** of `api-oauth-route.js` between:

```js
app.get('/health', (_req, res) => res.status(200).send('OK'));
```

and:

```js
/* Middleware */
```

So the order becomes: `/health` → **your new route** → `/* Middleware */`.

---

## 2. Frontend: OAuth trigger on MCP selection

**File:** `client/src/hooks/MCP/useMCPServerManager.ts`

Find the `toggleServerSelection` callback. It looks like:

```ts
const toggleServerSelection = useCallback(
  (serverName: string) => {
    if (isInitializing(serverName)) {
      return;
    }

    const currentValues = mcpValues ?? [];
    const isCurrentlySelected = currentValues.includes(serverName);

    if (isCurrentlySelected) {
      // ... deselect logic
    } else {
      // ... select logic
    }
  },
  [mcpValues, setMCPValues, isInitializing],
);
```

**Add this block** immediately after `const isCurrentlySelected = ...` and **before** `if (isCurrentlySelected)`:

```ts
      if (serverName === 'google_workspace') {
        const oauthStartUrl = '/api/google-workspace/oauth/start?force=1';
        const oauthWindow = window.open('', 'google-workspace-oauth');
        if (oauthWindow) {
          oauthWindow.location.href = oauthStartUrl;
          oauthWindow.focus();
        } else {
          window.open(oauthStartUrl, '_blank');
        }
        if (!isCurrentlySelected) {
          setMCPValues([...currentValues, serverName]);
        }
        return;
      }
```

---

## 3. MCPServerMenuItem (optional)

**File:** `client/src/components/MCP/MCPServerMenuItem.tsx`

Upstream uses `onClick` for the toggle. If the OAuth popup is blocked by the browser, ensure the `Ariakit.MenuItemCheckbox` uses `onClick={() => onToggle(server.serverName)}` (not `onChange`).

---

## Verification

1. Backend: `grep -n "google-workspace" api/server/index.js` should show the new route.
2. Frontend: `grep -n "google_workspace" client/src/hooks/MCP/useMCPServerManager.ts` should show the new block.
3. Run LibreChat, click **google_workspace** in the MCP menu → OAuth page should open in a new window.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `spawn is not defined` | Add `const { spawn } = require('child_process');` at top of `api/server/index.js` |
| OAuth window doesn't open | Check browser popup blocker; ensure patch is in `toggleServerSelection` |
| `python: command not found` | OAuth route uses `python3` on Linux/Mac, `python` on Windows. For YAML, use `command: python3` (or `python` on Windows) |
