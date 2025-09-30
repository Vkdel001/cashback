# VPS Production Deployment Guide
## Complete Setup for NIC Policy Processor

### Phase 1: VPS Setup (Day 1)

#### 1.1 Choose VPS Provider
**Recommended Options:**
- **DigitalOcean**: $12/month (2GB RAM, 50GB SSD) - Best for beginners
- **Linode**: $12/month (2GB RAM, 50GB SSD) - Good performance
- **Vultr**: $10/month (2GB RAM, 55GB SSD) - Cost effective

**Recommended Specs for 100s of PDFs:**
- **RAM**: 2GB minimum (4GB preferred)
- **Storage**: 50GB minimum (100GB preferred)
- **CPU**: 2 cores
- **OS**: Ubuntu 22.04 LTS

#### 1.2 Initial Server Setup
```bash
# 1. Create VPS and get IP address
# 2. SSH into server
ssh root@your-server-ip

# 3. Update system
apt update && apt upgrade -y

# 4. Create application user
adduser nicapp
usermod -aG sudo nicapp
su - nicapp
```

### Phase 2: Environment Setup (Day 1-2)

#### 2.1 Install Required Software
```bash
# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx git -y

# Install Node.js (for some dependencies)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Redis (for job queue)
sudo apt install redis-server -y
sudo systemctl enable redis-server
```

#### 2.2 Setup Application Directory
```bash
# Create application structure
sudo mkdir -p /var/www/cashback
sudo chown nicapp:nicapp /var/www/cashback
cd /var/www/cashback

# Create directory structure
mkdir -p {storage,backups,logs,temp}
mkdir -p storage/{generated_pdfs,uploaded_files,processed}
```

#### 2.3 Clone and Setup Application
```bash
# Clone your repository
git clone https://github.com/Vkdel001/cashback.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# If requirements.txt doesn't exist, install manually:
pip install streamlit pandas PyPDF2 reportlab sib-api-v3-sdk redis rq gunicorn
```

### Phase 3: Production Configuration (Day 2)

#### 3.1 Environment Variables
```bash
# Create environment file
nano /var/www/cashback/.env

# Add your configuration:
BREVO_API_KEY=your-brevo-api-key-here
ENVIRONMENT=production
STORAGE_PATH=/var/www/cashback/storage
BACKUP_PATH=/var/www/cashback/backups
LOG_LEVEL=INFO
MAX_WORKERS=5
BATCH_SIZE=50
```

#### 3.2 Production Settings
```bash
# Create production config
nano /var/www/cashback/production_config.py
```