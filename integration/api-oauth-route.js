/**
 * Add this route to api/server/index.js, after app.get('/health', ...)
 * and before the /* Middleware */ section.
 *
 * Requires: const { spawn } = require('child_process'); at top of file.
 * Uses python3 on Linux/Mac, python on Windows.
 */

app.get('/api/google-workspace/oauth/start', (req, res) => {
  const scriptPath = path.join(process.cwd(), 'scripts', 'google_auth_start.py');
  const commandArgs = [scriptPath];

  if (req.query.force === '1') {
    commandArgs.push('--force');
  }

  try {
    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
    const child = spawn(pythonCmd, commandArgs, {
      cwd: process.cwd(),
      env: {
        ...process.env,
        GOOGLE_MCP_REDIRECT_URI: 'http://localhost:8080/',
      },
      detached: true,
      stdio: 'ignore',
    });
    child.unref();

    res.type('html');
    res.send(`<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Google Workspace OAuth</title>
    <style>
      body { font-family: Arial, sans-serif; max-width: 720px; margin: 48px auto; padding: 0 20px; line-height: 1.5; }
      a, button { display: inline-block; margin-top: 16px; }
      button { padding: 10px 16px; border: 1px solid #ccc; border-radius: 8px; background: #fff; cursor: pointer; }
    </style>
  </head>
  <body>
    <h1>Google Workspace sign-in is starting</h1>
    <p>This page launched the local OAuth helper for your Google Workspace tools.</p>
    <p>If the Google consent screen did not appear, use the button below to force Google sign-in again.</p>
    <button onclick="window.location.href='/api/google-workspace/oauth/start?force=1'">Retry Google sign-in</button>
  </body>
</html>`);
  } catch (error) {
    logger.error('Failed to start Google Workspace OAuth process:', error);
    res.status(500).json({ message: 'Failed to start Google Workspace OAuth' });
  }
});
