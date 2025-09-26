# 🚀 GitHub Upload Guide - NIC Policy Processor

## 🔒 **IMPORTANT SECURITY NOTICE**
Before uploading to GitHub, ensure sensitive data is protected!

### ⚠️ **Files to NEVER Upload:**
- ✅ API Keys (already in .gitignore)
- ✅ Excel files with real customer data
- ✅ PDF files with policy information
- ✅ Email reports with customer details
- ✅ Configuration files with credentials

## 📋 **Pre-Upload Checklist**

### 1. **Remove Sensitive Data**
```cmd
# Check for API keys in code
findstr /s "xkeysib" *.py
findstr /s "API_KEY" *.py
```

### 2. **Clean Up Files**
```cmd
# Remove temporary files
del *.xlsx
del *.pdf
del *_report.txt
rmdir /s policies_with_email
rmdir /s policies_without_email
```

### 3. **Verify .gitignore**
- ✅ Check .gitignore includes all sensitive patterns
- ✅ Test with `git status` to ensure no sensitive files are tracked

## 🚀 **Step-by-Step GitHub Upload**

### **Step 1: Initialize Git Repository**
```cmd
# Navigate to your project folder
cd "C:\Users\Ryan EZ\OneDrive - EZ DASH LTD\Documents\Nadine"

# Initialize git repository
git init

# Add .gitignore first
git add .gitignore
git commit -m "Add .gitignore for security"
```

### **Step 2: Create GitHub Repository**
1. **Go to GitHub.com**
2. **Click "New Repository"**
3. **Repository Details:**
   - **Name**: `nic-policy-processor`
   - **Description**: `NIC Life Insurance Policy Distribution System`
   - **Visibility**: `Private` (RECOMMENDED for business use)
   - **Don't initialize** with README (you already have files)

### **Step 3: Add Files to Git**
```cmd
# Add all files (respecting .gitignore)
git add .

# Check what will be committed (verify no sensitive files)
git status

# Commit files
git commit -m "Initial commit: NIC Policy Processor v1.0

Features:
- PDF policy extraction and processing
- Password protection with NIC numbers
- Professional email sending with Brevo
- Bulk PDF merging for printing
- Streamlit web interface
- Complete documentation"
```

### **Step 4: Connect to GitHub**
```cmd
# Add GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/nic-policy-processor.git

# Push to GitHub
git push -u origin main
```

### **Step 5: Verify Upload**
1. **Check GitHub repository**
2. **Verify no sensitive files are visible**
3. **Test clone in different location**

## 📁 **What Will Be Uploaded**

### ✅ **Safe Files (Will Upload):**
- `pdf_processor_final_working.py` - Main application
- `send_emails_brevo.py` - Email sender (API key removed)
- `merge_final.py` - PDF merger
- `HOW_TO_USE.md` - User documentation
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `run_app.bat` - Startup script
- `.gitignore` - Security file
- `README.md` - Project description

### ❌ **Protected Files (Won't Upload):**
- `*.xlsx` - Excel files with customer data
- `*.pdf` - Policy documents
- `policies_with_email/` - Customer PDFs
- `policies_without_email/` - Customer PDFs
- `*_report.txt` - Email sending reports
- API keys and credentials

## 🔐 **Security Best Practices**

### **1. Use Environment Variables**
Instead of hardcoded API keys, use:
```python
import os
BREVO_API_KEY = os.getenv('BREVO_API_KEY', 'your-default-key')
```

### **2. Create Template Config**
Create `config_template.py`:
```python
# Configuration Template
# Copy to config.py and update with your values

BREVO_API_KEY = "your-brevo-api-key-here"
SENDER_EMAIL = "your-sender-email@domain.com"
SENDER_NAME = "Your Company Name"
REPLY_TO_EMAIL = "your-reply-email@domain.com"
```

### **3. Add Security Notice to README**
```markdown
## Security Setup
1. Copy `config_template.py` to `config.py`
2. Update `config.py` with your credentials
3. Never commit `config.py` to version control
```

## 🔄 **Future Updates**

### **Adding New Features:**
```cmd
# Make changes to code
# Add and commit changes
git add .
git commit -m "Add new feature: [description]"
git push
```

### **Updating Documentation:**
```cmd
git add HOW_TO_USE.md DEPLOYMENT_GUIDE.md
git commit -m "Update documentation"
git push
```

## 🌐 **Repository Structure**
```
nic-policy-processor/
├── 📄 pdf_processor_final_working.py    # Main application
├── 📄 send_emails_brevo.py              # Email sender
├── 📄 merge_final.py                    # PDF merger
├── 📄 HOW_TO_USE.md                     # User guide
├── 📄 DEPLOYMENT_GUIDE.md               # Deployment guide
├── 📄 README.md                         # Project overview
├── 📄 .gitignore                        # Security file
├── 📄 run_app.bat                       # Startup script
├── 📄 config_template.py                # Configuration template
└── 📂 docs/                             # Additional documentation
```

## 🎯 **Next Steps After Upload**

1. **Share Repository** with team members (if needed)
2. **Set up Branch Protection** for main branch
3. **Create Issues** for future enhancements
4. **Add Wiki** for detailed documentation
5. **Set up Actions** for automated testing (optional)

## 📞 **Support**

If you encounter issues:
1. **Check .gitignore** is working correctly
2. **Verify no sensitive data** in repository
3. **Test clone** in different location
4. **Review commit history** for sensitive data

## ✅ **Success Checklist**

- [ ] .gitignore created and tested
- [ ] Sensitive files removed/ignored
- [ ] Repository created on GitHub
- [ ] Code uploaded successfully
- [ ] No API keys visible in repository
- [ ] Documentation updated
- [ ] Team members added (if applicable)

**Your NIC Policy Processor is now safely stored on GitHub! 🎉**