@echo off
echo ========================================
echo    PDF Policy Processor - Streamlit
echo ========================================
echo.
echo Starting web application...
echo Open your browser to: http://localhost:8501
echo.
echo Backend email integration: ENABLED
echo Email script: send_emails_brevo.py
echo.
python -m streamlit run pdf_processor_final_working.py --server.headless false --server.port 8501