#!/usr/bin/env python3
"""
Automated backup system for VPS deployment
"""
import os
import shutil
import tarfile
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging
from production_config import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_PATH / 'backup.log'),
        logging.StreamHandler()
    ]
)

class BackupSystem:
    def __init__(self):
        self.storage_path = config.STORAGE_PATH
        self.backup_path = config.BACKUP_PATH
        self.retention_days = config.BACKUP_RETENTION_DAYS
        
    def create_backup(self):
        """Create a timestamped backup of all generated files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"nic_backup_{timestamp}.tar.gz"
        backup_file = self.backup_path / backup_name
        
        try:
            logging.info(f"Starting backup: {backup_name}")
            
            # Create compressed backup
            with tarfile.open(backup_file, "w:gz") as tar:
                # Backup generated PDFs
                if config.PDF_WITH_EMAIL_PATH.exists():
                    tar.add(config.PDF_WITH_EMAIL_PATH, arcname="pdfs_with_email")
                
                if config.PDF_WITHOUT_EMAIL_PATH.exists():
                    tar.add(config.PDF_WITHOUT_EMAIL_PATH, arcname="pdfs_without_email")
                
                # Backup uploaded files
                if config.UPLOADED_FILES_PATH.exists():
                    tar.add(config.UPLOADED_FILES_PATH, arcname="uploaded_files")
                
                # Backup logs
                if config.LOG_PATH.exists():
                    tar.add(config.LOG_PATH, arcname="logs")
            
            # Get backup size
            backup_size = backup_file.stat().st_size / (1024 * 1024)  # MB
            
            logging.info(f"✅ Backup created: {backup_name} ({backup_size:.1f} MB)")
            
            # Clean old backups
            self.cleanup_old_backups()
            
            return str(backup_file)
            
        except Exception as e:
            logging.error(f"❌ Backup failed: {e}")
            return None
    
    def cleanup_old_backups(self):
        """Remove backups older than retention period"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        
        removed_count = 0
        for backup_file in self.backup_path.glob("nic_backup_*.tar.gz"):
            # Extract timestamp from filename
            try:
                timestamp_str = backup_file.stem.split('_', 2)[2]  # nic_backup_TIMESTAMP
                file_date = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                
                if file_date < cutoff_date:
                    backup_file.unlink()
                    removed_count += 1
                    logging.info(f"🗑️  Removed old backup: {backup_file.name}")
                    
            except (ValueError, IndexError):
                # Skip files that don't match expected format
                continue
        
        if removed_count > 0:
            logging.info(f"🧹 Cleaned up {removed_count} old backups")
    
    def restore_backup(self, backup_file):
        """Restore from a specific backup file"""
        backup_path = self.backup_path / backup_file
        
        if not backup_path.exists():
            logging.error(f"❌ Backup file not found: {backup_file}")
            return False
        
        try:
            logging.info(f"🔄 Restoring from backup: {backup_file}")
            
            # Extract backup
            with tarfile.open(backup_path, "r:gz") as tar:
                tar.extractall(self.storage_path)
            
            logging.info(f"✅ Backup restored successfully")
            return True
            
        except Exception as e:
            logging.error(f"❌ Restore failed: {e}")
            return False
    
    def list_backups(self):
        """List all available backups"""
        backups = []
        for backup_file in sorted(self.backup_path.glob("nic_backup_*.tar.gz")):
            size = backup_file.stat().st_size / (1024 * 1024)  # MB
            modified = datetime.fromtimestamp(backup_file.stat().st_mtime)
            
            backups.append({
                'name': backup_file.name,
                'size_mb': round(size, 1),
                'created': modified.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return backups
    
    def get_storage_stats(self):
        """Get storage usage statistics"""
        stats = {}
        
        # Calculate directory sizes
        for path_name, path in [
            ('pdfs_with_email', config.PDF_WITH_EMAIL_PATH),
            ('pdfs_without_email', config.PDF_WITHOUT_EMAIL_PATH),
            ('uploaded_files', config.UPLOADED_FILES_PATH),
            ('backups', config.BACKUP_PATH),
            ('logs', config.LOG_PATH)
        ]:
            if path.exists():
                size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                stats[path_name] = {
                    'size_mb': round(size / (1024 * 1024), 1),
                    'file_count': len(list(path.rglob('*')))
                }
            else:
                stats[path_name] = {'size_mb': 0, 'file_count': 0}
        
        return stats

def setup_automated_backups():
    """Setup automated backup schedule"""
    backup_system = BackupSystem()
    
    # Schedule daily backups at 2 AM
    schedule.every().day.at("02:00").do(backup_system.create_backup)
    
    # Schedule weekly cleanup at 3 AM on Sundays
    schedule.every().sunday.at("03:00").do(backup_system.cleanup_old_backups)
    
    logging.info("📅 Automated backup schedule configured")
    logging.info("- Daily backups at 2:00 AM")
    logging.info("- Weekly cleanup on Sundays at 3:00 AM")
    
    return backup_system

def run_backup_daemon():
    """Run the backup daemon"""
    backup_system = setup_automated_backups()
    
    logging.info("🚀 Backup daemon started")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    # Manual backup for testing
    backup_system = BackupSystem()
    
    print("🔧 NIC Backup System")
    print("=" * 30)
    
    # Show current storage stats
    stats = backup_system.get_storage_stats()
    print("\n📊 Storage Statistics:")
    for name, data in stats.items():
        print(f"  {name}: {data['size_mb']} MB ({data['file_count']} files)")
    
    # Create backup
    print("\n📦 Creating backup...")
    backup_file = backup_system.create_backup()
    
    if backup_file:
        print(f"✅ Backup created: {backup_file}")
    
    # List all backups
    print("\n📋 Available Backups:")
    backups = backup_system.list_backups()
    for backup in backups[-5:]:  # Show last 5 backups
        print(f"  {backup['name']} - {backup['size_mb']} MB - {backup['created']}")