#!/usr/bin/env python3
"""
Production storage solution for PDF files
Handles cloud storage integration for generated PDFs
"""
import os
import boto3
from pathlib import Path
import tempfile
import shutil
from datetime import datetime

class ProductionStorage:
    def __init__(self, storage_type="local"):
        self.storage_type = storage_type
        self.setup_storage()
    
    def setup_storage(self):
        """Setup storage based on deployment environment"""
        
        if self.storage_type == "aws_s3":
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION', 'us-east-1')
            )
            self.bucket_name = os.getenv('AWS_S3_BUCKET', 'nic-policy-pdfs')
        
        elif self.storage_type == "local_persistent":
            # For VPS/server deployment
            self.base_path = Path("/var/www/cashback/storage")
            self.base_path.mkdir(parents=True, exist_ok=True)
        
        else:  # local development
            self.base_path = Path(".")
    
    def get_pdf_storage_path(self):
        """Get the path where PDFs should be stored"""
        
        if self.storage_type == "aws_s3":
            # Return temporary local path, will upload to S3 later
            temp_dir = Path(tempfile.mkdtemp())
            return temp_dir / "policies_with_email"
        
        elif self.storage_type == "local_persistent":
            return self.base_path / "policies_with_email"
        
        else:  # local development
            return Path("policies_with_email")
    
    def save_generated_pdfs(self, local_pdf_folder):
        """Save generated PDFs to persistent storage"""
        
        if self.storage_type == "aws_s3":
            return self._upload_to_s3(local_pdf_folder)
        
        elif self.storage_type == "local_persistent":
            return self._copy_to_persistent_storage(local_pdf_folder)
        
        else:
            # Local development - files already in right place
            return str(local_pdf_folder)
    
    def _upload_to_s3(self, local_folder):
        """Upload PDFs to AWS S3"""
        uploaded_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for pdf_file in Path(local_folder).glob("*.pdf"):
            s3_key = f"generated_pdfs/{timestamp}/{pdf_file.name}"
            
            try:
                self.s3_client.upload_file(
                    str(pdf_file),
                    self.bucket_name,
                    s3_key
                )
                uploaded_files.append(s3_key)
                print(f"✅ Uploaded: {pdf_file.name} to S3")
            
            except Exception as e:
                print(f"❌ Failed to upload {pdf_file.name}: {e}")
        
        return f"s3://{self.bucket_name}/generated_pdfs/{timestamp}/"
    
    def _copy_to_persistent_storage(self, local_folder):
        """Copy PDFs to persistent server storage"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        persistent_folder = self.base_path / f"generated_pdfs_{timestamp}"
        
        try:
            shutil.copytree(local_folder, persistent_folder)
            print(f"✅ PDFs saved to: {persistent_folder}")
            return str(persistent_folder)
        
        except Exception as e:
            print(f"❌ Failed to save PDFs: {e}")
            return None

# Production configuration based on environment
def get_storage_config():
    """Determine storage configuration based on environment"""
    
    # Check if running on cloud platform
    if os.getenv('RAILWAY_ENVIRONMENT'):
        return "aws_s3"  # Railway + S3
    
    elif os.getenv('RENDER'):
        return "aws_s3"  # Render + S3
    
    elif os.getenv('STREAMLIT_CLOUD'):
        return "aws_s3"  # Streamlit Cloud + S3
    
    elif os.path.exists('/var/www'):
        return "local_persistent"  # VPS/Server
    
    else:
        return "local"  # Local development

# Usage in your main app
def setup_production_pdf_storage():
    """Setup PDF storage for production"""
    storage_type = get_storage_config()
    storage = ProductionStorage(storage_type)
    
    print(f"📁 Storage configured: {storage_type}")
    return storage

if __name__ == "__main__":
    storage = setup_production_pdf_storage()
    pdf_path = storage.get_pdf_storage_path()
    print(f"PDFs will be generated in: {pdf_path}")