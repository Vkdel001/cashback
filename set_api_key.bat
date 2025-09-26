@echo off
echo Setting up Brevo API Key Environment Variable
echo =============================================
echo.
echo Please enter your Brevo API key (get it from https://app.brevo.com/settings/keys/api):
set /p BREVO_API_KEY="API Key: "
echo.
echo Setting environment variable...
setx BREVO_API_KEY "%BREVO_API_KEY%"
echo.
echo ✅ Environment variable set successfully!
echo ⚠️  Please restart your command prompt or IDE for changes to take effect.
echo.
pause