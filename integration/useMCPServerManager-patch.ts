/**
 * In client/src/hooks/MCP/useMCPServerManager.ts, inside toggleServerSelection,
 * add this block at the start of the callback, before the standard toggle logic:
 *
 * Replace or add before: if (isCurrentlySelected) { ... }
 */

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
