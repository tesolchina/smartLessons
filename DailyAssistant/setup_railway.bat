@echo off
echo Setting up Railway CLI and OpenRouter API Key...
echo.

echo Step 1: Download Railway CLI
echo Please visit: https://github.com/railwayapp/cli/releases/latest
echo Download: railway_windows_amd64.exe
echo Save it to this folder: %CD%
echo Rename it to: railway.exe
echo.

echo Step 2: After downloading, run these commands:
echo railway login
echo railway link [your-project-id-if-needed]
echo railway variables set OPENROUTER_API_KEY=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
echo.

echo Your Railway deployment URL: new-bytewise-backend-production-8c33.up.railway.app
echo Your OpenRouter API Key: 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
echo.

pause
