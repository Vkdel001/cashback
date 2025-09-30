#!/usr/bin/env python3
"""
Production configuration for VPS deployment
"""
import os
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class ProductionConfig:
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8501
    
    # Storage Paths
    BASE_PATH = Path("/var/www/cashback")
    STORAGE_PATH = BASE_PATH / "storage"
    BACKUP_PATH = BASE_PATH / "backups"
    LOG_PATH = BASE_PATH / "logs"
    TEMP_PATH = BASE_PATH / "temp"
    
    # PDF Generation Paths
    PDF_WITH_EMAIL_PATH = STORAGE_PATH / "generated_pdfs" / "with_email"
    PDF_WITHOUT_EMAIL_PATH = STORAGE_PATH / "generated_pdfs" / "without_email"
    UPLOADED_FILES_PATH = STORAGE_PATH / "uploaded_files"
    
    # Email Configuration
    BREVO_API_KEY = os.getenv('BREVO_API_KEY')
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', 2))  # Reduced for 1 CPU
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 25))   # Smaller batches
    EMAIL_RATE_LIMIT = float(os.getenv('EMAIL_RATE_LIMIT', 1.0))  # Slower rate
    
    # Backup Configuration
    BACKUP_ENABLED = True
    BACKUP_RETENTION_DAYS = 30
    AUTO_BACKUP_INTERVAL = 24  # hours
    
    # Security
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'.pdf', '.xlsx', '.xls'}
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def create_directories(cls):
        """Create all necessary directories"""
        directories = [
            cls.STORAGE_PATH,
            cls.BACKUP_PATH,
            cls.LOG_PATH,
            cls.TEMP_PATH,
            cls.PDF_WITH_EMAIL_PATH,
            cls.PDF_WITHOUT_EMAIL_PATH,
            cls.UPLOADED_FILES_PATH
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {directory}")
    
    @classmethod
    def validate_config(cls):
        """Validate production configuration"""
        errors = []
        
        if not cls.BREVO_API_KEY:
            errors.append("BREVO_API_KEY environment variable not set")
        
        if not cls.BASE_PATH.exists():
            errors.append(f"Base path does not exist: {cls.BASE_PATH}")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True

# Initialize configuration
config = ProductionConfig()

if __name__ == "__main__":
    print("🔧 Setting up production configuration...")
    config.create_directories()
    config.validate_config()
    print("✅ Production configuration ready!")