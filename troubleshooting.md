### **Email Script Debug Mode**
```bash
# Run email script with verbose output
cd /var/www/cashback
source venv/bin/activate
export BREVO_API_KEY="your-api-key"
python3 -u send_emails_brevo.py  # -u for unbuffered output
```



# 🔧 NIC Policy Processor - Troubleshooting Guide

## 📋 System Overview

### **What We Deployed**
- **Application**: NIC Policy Processor - Streamlit web application
- **Server**: DigitalOcean VPS (1 CPU, 2GB RAM, Ubuntu 25.04)
- **IP Address**: 206.189.121.37
- **Web Access**: http://206.189.121.37
- **Email Service**: Brevo API integration
- **Storage**: Local VPS storage with automated backups

### **System Architecture**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │───▶│   Streamlit App  │───▶│  File Storage   │
│   Port 80       │    │   Port 8501      │    │  /var/www/      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Brevo Email    │
                       │   API Service    │
                       └──────────────────┘
```

### **Key Components**
1. **Streamlit App**: PDF processing and web interface
2. **Nginx**: Web server and reverse proxy
3. **Email Script**: Brevo integration for sending emails
4. **Backup System**: Automated daily backups
5. **File Storage**: Organized directory structure

---

## 🗂️ File Structure

### **Application Directory: `/var/www/cashback/`**
```
/var/www/cashback/
├── pdf_processor_final_working.py    # Main Streamlit application
├── send_emails_brevo.py             # Email sending script
├── backup_system.py                 # Automated backup system
├── production_config.py             # Production configuration
├── nginx_config.conf               # Nginx configuration
├── .env                            # Environment variables (API keys)
├── venv/                           # Python virtual environment
├── storage/                        # File storage
│   ├── generated_pdfs/
│   │   ├── with_email/            # PDFs ready for email
│   │   └── without_email/         # PDFs without email addresses
│   └── uploaded_files/
│       └── latest_excel.xlsx      # Preserved Excel file
├── backups/                       # Automated backups
├── logs/                          # Application logs
└── temp/                          # Temporary processing files
```

### **System Services**
- **nic-cashback.service**: Main Streamlit application
- **nic-backup.timer**: Daily backup automation
- **nginx.service**: Web server

---

## 🚨 Common Issues & Solutions

### **1. Application Not Loading (Nginx Welcome Page)**

**Symptoms:**
- Browser shows "Welcome to nginx!" instead of the application
- URL: http://206.189.121.37 shows default nginx page

**Diagnosis:**
```bash
# Check nginx configuration
sudo nginx -t

# Check if our site is enabled
ls -la /etc/nginx/sites-enabled/

# Check Streamlit service
sudo systemctl status nic-cashback
```

**Solution:**
```bash
# Fix nginx configuration
sudo cp /var/www/cashback/nginx_config.conf /etc/nginx/sites-available/cashback
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/cashback /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Restart Streamlit service
sudo systemctl restart nic-cashback
```

### **2. Streamlit Service Not Running**

**Symptoms:**
- Application not accessible
- 502 Bad Gateway error

**Diagnosis:**
```bash
# Check service status
sudo systemctl status nic-cashback

# Check logs
sudo journalctl -u nic-cashback -n 50

# Check if port 8501 is listening
sudo netstat -tlnp | grep 8501
```

**Solution:**
```bash
# Restart the service
sudo systemctl restart nic-cashback

# If service fails to start, check Python environment
su - nicapp
cd /var/www/cashback
source venv/bin/activate
python3 pdf_processor_final_working.py

# Fix common issues
pip install streamlit pandas PyPDF2 reportlab sib-api-v3-sdk openpyxl
```

### **3. File Upload Errors (Read-only File System)**

**Symptoms:**
- "OSError: [Errno 30] Read-only file system" when uploading files
- Cannot process PDF or Excel files

**Diagnosis:**
```bash
# Check directory permissions
ls -la /var/www/cashback/
ls -la /var/www/cashback/temp/
ls -la /var/www/cashback/storage/

# Check ownership
sudo ls -la /var/www/cashback/
```

**Solution:**
```bash
# Fix permissions and ownership
sudo chown -R nicapp:nicapp /var/www/cashback/
sudo chmod -R 755 /var/www/cashback/

# Ensure directories exist
mkdir -p /var/www/cashback/temp
mkdir -p /var/www/cashback/storage/generated_pdfs/{with_email,without_email}
mkdir -p /var/www/cashback/storage/uploaded_files

# Restart service
sudo systemctl restart nic-cashback
```

### **4. Email Sending Issues**

**Symptoms:**
- "BREVO_API_KEY environment variable not set"
- "No Excel file found in any expected location"
- Email sending fails

**Diagnosis:**
```bash
# Check API key
echo $BREVO_API_KEY

# Check Excel file preservation
ls -la /var/www/cashback/storage/uploaded_files/
ls -la /var/www/cashback/*.xlsx

# Check PDF files
ls -la /var/www/cashback/storage/generated_pdfs/with_email/
```

**Solution:**
```bash
# Set API key
export BREVO_API_KEY="your-brevo-api-key-here"

# Or add to .env file
echo 'BREVO_API_KEY="your-brevo-api-key-here"' >> /var/www/cashback/.env

# Test email script
cd /var/www/cashback
source venv/bin/activate
python3 send_emails_brevo.py
```

### **5. Missing Dependencies**

**Symptoms:**
- "ModuleNotFoundError: No module named 'openpyxl'"
- "AttributeError: module 'streamlit' has no attribute 'experimental_rerun'"

**Solution:**
```bash
# Activate virtual environment
cd /var/www/cashback
source venv/bin/activate

# Install missing packages
pip install openpyxl python-dotenv

# Fix deprecated Streamlit functions
sed -i 's|st.experimental_rerun()|st.rerun()|g' pdf_processor_final_working.py

# Restart service
sudo systemctl restart nic-cashback
```

---

## 🔍 Diagnostic Commands

### **System Health Check**
```bash
# Check all services
sudo systemctl status nic-cashback nginx

# Check disk space
df -h

# Check memory usage
free -h

# Check CPU usage
top -n 1

# Check network connectivity
curl -I http://localhost:8501
```

### **Application Logs**
```bash
# Real-time Streamlit logs
sudo journalctl -u nic-cashback -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# System logs
sudo journalctl -xe
```

### **File System Check**
```bash
# Check file permissions
ls -la /var/www/cashback/
ls -la /var/www/cashback/storage/

# Check available space
du -sh /var/www/cashback/*

# Check recent files
find /var/www/cashback -type f -mmin -60  # Files modified in last hour
```

---

## 🔄 Service Management

### **Start/Stop/Restart Services**
```bash
# Streamlit application
sudo systemctl start nic-cashback
sudo systemctl stop nic-cashback
sudo systemctl restart nic-cashback

# Nginx web server
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx  # Reload config without stopping

# Check service status
sudo systemctl status nic-cashback
sudo systemctl status nginx
```

### **Enable/Disable Auto-start**
```bash
# Enable services to start on boot
sudo systemctl enable nic-cashback
sudo systemctl enable nginx

# Disable auto-start
sudo systemctl disable nic-cashback
```

---

## 📧 Email System Troubleshooting

### **Brevo API Issues**
```bash
# Test API key validity
curl -X GET "https://api.brevo.com/v3/account" \
  -H "api-key: your-brevo-api-key-here"

# Check email sending limits
# Login to https://app.brevo.com/settings/keys/api
```

### **Email Script Debug Mode**
```bash
# Run email script with verbose output
cd /var/www/cashback
source venv/bin/activate
export BREVO_API_KEY="your-api-key"
python3 -u send_emails_brevo.py  # -u for unbuffered output
```

### **Common Email Errors**
- **"Sender domain not verified"**: Verify domain in Brevo dashboard
- **"Daily limit exceeded"**: Check Brevo plan limits
- **"Invalid email format"**: Check Excel file email column format

---

## 💾 Backup & Recovery

### **Manual Backup**
```bash
# Create manual backup
cd /var/www/cashback
python3 backup_system.py

# Check backups
ls -la /var/www/cashback/backups/
```

### **Restore from Backup**
```bash
# List available backups
cd /var/www/cashback
python3 -c "
from backup_system import BackupSystem
bs = BackupSystem()
backups = bs.list_backups()
for backup in backups:
    print(f'{backup[\"name\"]} - {backup[\"created\"]} - {backup[\"size_mb\"]} MB')
"

# Restore specific backup
python3 -c "
from backup_system import BackupSystem
bs = BackupSystem()
bs.restore_backup('nic_backup_YYYYMMDD_HHMMSS.tar.gz')
"
```

### **Automated Backup Status**
```bash
# Check backup timer
sudo systemctl status nic-backup.timer

# View backup logs
sudo journalctl -u nic-backup -n 20
```

---

## 🔧 Configuration Files

### **Environment Variables (.env)**
```bash
# Edit environment variables
nano /var/www/cashback/.env

# Required variables:
BREVO_API_KEY=your-brevo-api-key-here
ENVIRONMENT=production
STORAGE_PATH=/var/www/cashback/storage
BACKUP_PATH=/var/www/cashback/backups
LOG_LEVEL=INFO
MAX_WORKERS=2
BATCH_SIZE=25
EMAIL_RATE_LIMIT=1.0
```

### **Nginx Configuration**
```bash
# Edit nginx config
sudo nano /etc/nginx/sites-available/cashback

# Test configuration
sudo nginx -t

# Reload configuration
sudo systemctl reload nginx
```

### **Systemd Service Configuration**
```bash
# Edit service file
sudo nano /etc/systemd/system/nic-cashback.service

# Reload systemd after changes
sudo systemctl daemon-reload
sudo systemctl restart nic-cashback
```

---

## 🚀 Performance Optimization

### **For Higher Loads (Upgrade to 2+ CPUs)**
```bash
# Update configuration for more CPUs
nano /var/www/cashback/.env

# Increase these values:
MAX_WORKERS=5
BATCH_SIZE=50
EMAIL_RATE_LIMIT=0.5

# Restart service
sudo systemctl restart nic-cashback
```

### **Monitor Performance**
```bash
# Monitor CPU and memory
htop

# Monitor disk I/O
iotop

# Monitor network
nethogs

# Check application performance
sudo journalctl -u nic-cashback -f | grep -E "(✅|❌|📊)"
```

---

## 📞 Emergency Procedures

### **Complete System Reset**
```bash
# Stop all services
sudo systemctl stop nic-cashback nginx

# Restore from backup
cd /var/www/cashback
python3 backup_system.py  # Create current backup first
# Then restore from known good backup

# Restart services
sudo systemctl start nginx nic-cashback
```

### **Rollback to Previous Version**
```bash
# Restore from git
cd /var/www/cashback
git log --oneline -10  # See recent commits
git checkout <commit-hash>  # Rollback to specific commit
sudo systemctl restart nic-cashback
```

### **Contact Information**
- **Server Provider**: DigitalOcean
- **Email Service**: Brevo (https://app.brevo.com)
- **Server IP**: 206.189.121.37
- **SSH Access**: `ssh nicapp@206.189.121.37`

---

## 📊 Success Indicators

### **Healthy System Checklist**
- [ ] **Web interface loads**: http://206.189.121.37 shows NIC Policy Processor
- [ ] **File upload works**: Can upload PDF and Excel files
- [ ] **Processing works**: Generates password-protected PDFs
- [ ] **Excel preservation**: Files saved in `/var/www/cashback/storage/uploaded_files/`
- [ ] **Email sending**: Script finds Excel and PDF files, sends emails
- [ ] **Services running**: `sudo systemctl status nic-cashback nginx` shows active
- [ ] **Backups working**: Daily backups created in `/var/www/cashback/backups/`

### **Performance Benchmarks**
- **File upload**: < 30 seconds for 100MB files
- **PDF processing**: ~2-3 PDFs per minute (1 CPU)
- **Email sending**: ~60 emails per hour
- **Memory usage**: < 500MB for normal operations
- **Disk usage**: < 10GB for 1000 processed policies

---

## 🎯 Quick Reference Commands

```bash
# Check everything is working
sudo systemctl status nic-cashback nginx
curl -I http://localhost:8501

# Restart everything
sudo systemctl restart nic-cashback nginx

# View logs
sudo journalctl -u nic-cashback -f

# Test email sending
cd /var/www/cashback && source venv/bin/activate
export BREVO_API_KEY="your-key" && python3 send_emails_brevo.py

# Check file storage
ls -la /var/www/cashback/storage/generated_pdfs/with_email/
ls -la /var/www/cashback/storage/uploaded_files/

# Create manual backup
cd /var/www/cashback && python3 backup_system.py
```

---

**📝 Last Updated**: September 30, 2025  
**🔧 System Version**: NIC Policy Processor v1.0  
**💻 Server**: DigitalOcean VPS (206.189.121.37)  
**👤 Admin User**: nicapp