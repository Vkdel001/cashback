#!/bin/bash
# Setup systemd services for NIC Policy Processor

# Create Streamlit service
sudo tee /etc/systemd/system/nic-cashback.service > /dev/null <<EOF
[Unit]
Description=NIC Policy Processor - Streamlit App
After=network.target

[Service]
Type=simple
User=nicapp
Group=nicapp
WorkingDirectory=/var/www/cashback
Environment=PATH=/var/www/cashback/venv/bin
ExecStart=/var/www/cashback/venv/bin/streamlit run pdf_processor_final_working.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
Restart=always
RestartSec=10

# Environment variables
EnvironmentFile=/var/www/cashback/.env

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/var/www/cashback/storage /var/www/cashback/backups /var/www/cashback/logs /var/www/cashback/temp

[Install]
WantedBy=multi-user.target
EOF

# Create backup service
sudo tee /etc/systemd/system/nic-backup.service > /dev/null <<EOF
[Unit]
Description=NIC Policy Processor - Backup Service
After=network.target

[Service]
Type=simple
User=nicapp
Group=nicapp
WorkingDirectory=/var/www/cashback
Environment=PATH=/var/www/cashback/venv/bin
ExecStart=/var/www/cashback/venv/bin/python backup_system.py
Restart=always
RestartSec=30

# Environment variables
EnvironmentFile=/var/www/cashback/.env

[Install]
WantedBy=multi-user.target
EOF

# Create backup timer (daily at 2 AM)
sudo tee /etc/systemd/system/nic-backup.timer > /dev/null <<EOF
[Unit]
Description=Daily backup for NIC Policy Processor
Requires=nic-backup.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Reload systemd and enable services
sudo systemctl daemon-reload

# Enable and start services
sudo systemctl enable nic-cashback.service
sudo systemctl enable nic-backup.timer

echo "✅ Systemd services created and enabled"
echo ""
echo "To start services:"
echo "sudo systemctl start nic-cashback"
echo "sudo systemctl start nic-backup.timer"
echo ""
echo "To check status:"
echo "sudo systemctl status nic-cashback"
echo "sudo systemctl status nic-backup.timer"
echo ""
echo "To view logs:"
echo "sudo journalctl -u nic-cashback -f"
echo "sudo journalctl -u nic-backup -f"