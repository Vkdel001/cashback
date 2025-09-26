# 📄 PDF Policy Processor - User Guide

## 🚀 Quick Start


### Step 1: Start the Application
```cmd
run_app.bat
```
*Or manually:*
```cmd
python -m streamlit run pdf_processor_final_working.py
```

### Step 2: Open Your Browser
Navigate to: **http://localhost:8501**

---

## ⚡ Quick Reference

| Task | Command | Output |
|------|---------|--------|
| **Process PDFs** | Use web interface | Individual PDFs in folders |
| **Send Emails** | `python send_emails_brevo.py` | Emails sent to customers |
| **Merge for Printing** | `python merge_final.py` | Single `policies_for_printing.pdf` |
| **Test Password** | `python test_password_protection.py` | Verify encryption works |

---

## 📋 Complete Workflow

### 1. 📤 Upload Files
- **PDF File**: Your merged policy document (e.g., "CBOPT 5 yrs Nov25 letters.pdf")
- **Excel File**: File with policy numbers, email addresses, and NIC numbers (e.g., "Compile CBOpt Nov25.xlsx")
  - Column A: Policy Numbers
  - Column B: Email Addresses  
  - Column C: NIC Numbers (used as PDF passwords)

### 2. 🔄 Process Files
- Click **"🚀 Process Files"** button
- Wait for extraction to complete
- View results summary (Total/With Email/Without Email)

### 3. 📥 Download Results (Optional)
- **"📧 Download Policies WITH Email"** - Ready for email sending
- **"❓ Download Policies WITHOUT Email"** - Need manual email lookup

### 4. 📧 Send Emails
```cmd
python send_emails_brevo.py
```

### 5. 🖨️ Print Policies Without Email (Optional)
If some policies don't have email addresses:
**Option A: Use Web Interface**
- Click **"🖨️ Merge PDFs for Printing"** in the web interface
- Follow the command line instructions shown

**Option B: Use Command Line (Recommended)**
```cmd
python merge_final.py
```
- Creates `policies_for_printing.pdf` with all policies without email
- Single file ready for bulk printing and manual distribution

---

## 📁 File Structure After Processing

```
📂 Your Folder/
├── 📂 policies_with_email/        ← Ready for email sending (password-protected)
│   ├── 00407_0054316.pdf         ← Protected with NIC password
│   ├── 29031933.pdf              ← Protected with NIC password
│   └── ...
├── 📂 policies_without_email/     ← Ready for printing (no password)
│   ├── 00408_0054317.pdf         ← Unencrypted for easy printing
│   └── ...
├── 📄 policies_for_printing.pdf   ← Merged file for bulk printing
├── 📄 send_emails_brevo.py        ← Email sending script
├── 📄 merge_final.py              ← PDF merging script
└── 📄 Compile CBOpt Nov25.xlsx    ← Your email database
```

---

## ⚙️ System Requirements

- **Python 3.7+** with packages:
  - `streamlit`
  - `pandas`
  - `PyPDF2`
  - `openpyxl`
- **Internet connection** for email sending

---

## 🔧 Troubleshooting

### Problem: "streamlit command not found"
**Solution:**
```cmd
python -m streamlit run pdf_processor_final_working.py
```

### Problem: PDF processing fails
**Solution:**
- Check PDF file isn't corrupted
- Ensure PDF contains text (not just images)
- Try a smaller PDF file first

### Problem: Email sending fails
**Solution:**
- Check internet connection
- Verify Brevo API key is valid
- Ensure `policies_with_email` folder exists and has PDF files

### Problem: Excel file not recognized
**Solution:**
- Save Excel file as `.xlsx` format
- Ensure first column has policy numbers
- Ensure second column has email addresses
- Ensure third column has NIC numbers (for password protection)

### Problem: PDF merging fails or creates blank file
**Solution:**
- Use `python merge_final.py` instead of the web interface
- Close any PDF viewers that might have the output file open
- Ensure `policies_without_email` folder exists and has PDF files
- Check available disk space (merged file can be 5-10 MB)

---

## 📊 Supported Policy Formats

The system recognizes these policy number formats:
- **Slash format**: `00407/0054316`
- **Numeric format**: `29031933`

---

## 📧 Email Configuration

**Current Settings:**
- **Sender**: CashBack@niclmauritius.site
- **Reply-To**: nicarlife@nicl.mu
- **Service**: Brevo (SendinBlue)
- **Subject**: "NIC Life Insurance - Policy Cash Back Documentation"

---

## 🎯 Tips for Best Results

1. **File Names**: Use descriptive names for your uploads
2. **Excel Format**: Keep policy numbers in column A, emails in column B, NIC numbers in column C
3. **PDF Quality**: Ensure PDF text is searchable (not scanned images)
4. **Password Security**: NIC numbers from column C will be used to password-protect PDFs with email
5. **No Password for Printing**: Policies without email are saved unencrypted for easy printing
6. **Batch Size**: Process large files in smaller batches if needed
7. **Backup**: Keep original files as backup before processing
8. **Printing**: Use `python merge_final.py` for bulk printing preparation

---

## 📞 Support

If you encounter issues:
1. Check the console/terminal for error messages
2. Verify all files are in the correct format
3. Ensure all required Python packages are installed
4. Try processing a smaller test file first

---

## 🖨️ Printing Features

**PDF Merging for Printing**: Policies without email addresses can be merged into a single PDF file for easy printing and manual distribution.

**How to Merge:**
```cmd
python merge_final.py
```

**Benefits:**
- Single file for printing department (e.g., 647 policies → 1 file)
- Organized by policy number
- No password protection (easy printing)
- Reduces printing complexity
- Ready for bulk printing (typically 1000+ pages)
- Easy manual distribution

**Output:** `policies_for_printing.pdf` (typically 5-10 MB)

---

## 🔐 Security Features

**Smart Password Protection**: PDFs are password-protected based on distribution method:
- **Policies WITH email**: Protected with NIC number (secure email distribution)
- **Policies WITHOUT email**: No password (easy printing and manual distribution)

**Security Benefits:**
- Only policy holders can open emailed documents
- Protects sensitive policy information during electronic distribution
- Complies with data protection requirements
- Printing department can easily handle unencrypted files

## 🖨️ Bulk Printing Workflow

**For Policies Without Email:**
1. **Process PDFs** using the main application
2. **Merge for printing**: `python merge_final.py`
3. **Print** the single `policies_for_printing.pdf` file
4. **Distribute** manually to customers

**Typical Results:**
- 600+ individual policies → 1 merged file
- 1200+ pages ready for bulk printing
- 5-10 MB file size
- No password protection needed

---

---

## 🎯 Complete Workflow Summary

### For Policies WITH Email (Electronic Distribution):
1. **Upload** PDF and Excel files
2. **Process** → Creates password-protected PDFs in `policies_with_email/`
3. **Send emails** → `python send_emails_brevo.py`
4. **Result** → Customers receive secure PDFs via email

### For Policies WITHOUT Email (Manual Distribution):
1. **Upload** PDF and Excel files  
2. **Process** → Creates unencrypted PDFs in `policies_without_email/`
3. **Merge** → `python merge_final.py`
4. **Print** → Single file ready for bulk printing
5. **Result** → Manual distribution to customers

### Key Features:
- ✅ **Smart Security**: Email PDFs are encrypted, print PDFs are not
- ✅ **Bulk Processing**: Handle 600+ policies efficiently  
- ✅ **Two-Page Support**: Letters and forms properly grouped
- ✅ **Multiple Formats**: Supports slash (00407/0054316) and numeric (29031933) policy numbers
- ✅ **Progress Tracking**: Real-time processing and email sending status
- ✅ **Error Handling**: Clear feedback for any issues

---

**Built with ❤️ for NIC Mauritius Policy Distribution**