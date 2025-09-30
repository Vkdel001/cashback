#!/bin/bash
# Complete VPS deployment script for NIC Policy Processor
# Run this script on your VPS as the nicapp user

set -e  # Exit on any error

echo "🚀 NIC Policy Processor - VPS Deployment"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as nicapp user
if [ "$USER" != "nicapp" ]; then
    print_error "Please run this script as the 'nicapp' user"
    exit 1
fi

# Step 1: Setup directory structure
print_status "Setting up directory structure..."
cd /var/www/cashback

# Create all necessary directories
mkdir -p storage/{generated_pdfs/{with_email,without_email},uploaded_files,processed}
mkdir -p {backups,logs,temp,static}

print_status "Directory structure created"

# Step 2: Setup Python environment
print_status "Setting up Python virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
print_status "Installing Python dependencies..."
pip install streamlit pandas PyPDF2 reportlab sib-api-v3-sdk redis rq gunicorn python-dotenv schedule

print_status "Python environment ready"

# Step 3: Setup configuration
print_status "Setting up configuration..."

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cat > .env << EOF
# NIC Policy Processor Configuration
BREVO_API_KEY=your-brevo-api-key-here
ENVIRONMENT=production
STORAGE_PATH=/var/www/cashback/storage
BACKUP_PATH=/var/www/cashback/backups
LOG_LEVEL=INFO
MAX_WORKERS=2
BATCH_SIZE=25
EMAIL_RATE_LIMIT=1.0
EOF
    print_warning "Please edit .env file and add your BREVO_API_KEY"
fi

# Step 4: Initialize production configuration
print_status "Initializing production configuration..."
python production_config.py

# Step 5: Setup Nginx configuration
print_status "Setting up Nginx configuration..."

# Copy nginx config
sudo cp nginx_config.conf /etc/nginx/sites-available/cashback

# Enable site (remove default if exists)
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/cashback /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

print_status "Nginx configured"

# Step 6: Setup systemd services
print_status "Setting up systemd services..."
chmod +x systemd_services.sh
./systemd_services.sh

# Step 7: Setup firewall
print_status "Configuring firewall..."
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw --force enable

print_status "Firewall configured"

# Step 8: Start services
print_status "Starting services..."

# Start and enable services
sudo systemctl start nginx
sudo systemctl enable nginx

sudo systemctl start nic-cashback
sudo systemctl start nic-backup.timer

# Wait a moment for services to start
sleep 5

# Check service status
if sudo systemctl is-active --quiet nic-cashback; then
    print_status "Streamlit app is running"
else
    print_error "Streamlit app failed to start"
    sudo journalctl -u nic-cashback --no-pager -n 20
fi

if sudo systemctl is-active --quiet nginx; then
    print_status "Nginx is running"
else
    print_error "Nginx failed to start"
fi

# Step 9: Create initial backup
print_status "Creating initial backup..."
python backup_system.py

# Step 10: Display final information
echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo ""
echo "📋 Next Steps:"
echo "1. Edit /var/www/cashback/.env and add your BREVO_API_KEY"
echo "2. Update domain name in /etc/nginx/sites-available/cashback"
echo "3. Setup SSL certificate with Let's Encrypt (optional)"
echo "4. Test the application by visiting your server IP"
echo ""
echo "🔧 Useful Commands:"
echo "- Check app status: sudo systemctl status nic-cashback"
echo "- View app logs: sudo journalctl -u nic-cashback -f"
echo "- Restart app: sudo systemctl restart nic-cashback"
echo "- Check backups: ls -la /var/www/cashback/backups/"
echo ""
echo "📊 Storage Locations:"
echo "- Generated PDFs: /var/www/cashback/storage/generated_pdfs/"
echo "- Backups: /var/www/cashback/backups/"
echo "- Logs: /var/www/cashback/logs/"
echo ""
echo "🌐 Access your application at: http://$(curl -s ifconfig.me)"
echo ""

# Final status check
print_status "Deployment script completed successfully!"

# Show current status
echo "📈 Current Status:"
sudo systemctl status nic-cashback --no-pager -l
echo ""
echo "🔍 To troubleshoot issues, check logs with:"
echo "sudo journalctl -u nic-cashback -f"