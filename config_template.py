#!/usr/bin/env python3
"""
Configuration Template for NIC Policy Processor
===============================================

SECURITY INSTRUCTIONS:
1. Copy this file to 'config.py'
2. Update the values below with your actual credentials
3. NEVER commit 'config.py' to version control
4. The .gitignore file will protect 'config.py' from being uploaded

"""

# Brevo Email Configuration
BREVO_API_KEY = "your-brevo-api-key-here"

# Email Settings
SENDER_EMAIL = "your-sender-email@domain.com"
SENDER_NAME = "Your Company Name"
REPLY_TO_EMAIL = "your-reply-email@domain.com"
REPLY_TO_NAME = "Your Reply Name"

# Email Template Settings
EMAIL_SUBJECT = "Your Email Subject Here"

# File Paths (optional - can be left as default)
EXCEL_FILE_PATH = "your-excel-file.xlsx"
PDF_INPUT_PATH = "your-input-pdf.pdf"

# Processing Settings
BATCH_SIZE = 100  # Number of emails to send in one batch
DELAY_BETWEEN_EMAILS = 0.1  # Seconds to wait between emails

# Security Settings
ENABLE_PASSWORD_PROTECTION = True
USE_NIC_AS_PASSWORD = True

# Debug Settings
DEBUG_MODE = False
VERBOSE_LOGGING = True

"""
EXAMPLE CONFIGURATION:
======================

BREVO_API_KEY = "xkeysib-abc123def456..."
SENDER_EMAIL = "noreply@yourcompany.com"
SENDER_NAME = "Your Company Name"
REPLY_TO_EMAIL = "support@yourcompany.com"
REPLY_TO_NAME = "Customer Support"

"""