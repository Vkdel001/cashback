#!/usr/bin/env python3
"""
Production optimizations for handling hundreds of PDF files
"""
import os
import time
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import threading

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('production.log'),
        logging.StreamHandler()
    ]
)

class ProductionEmailProcessor:
    def __init__(self, max_workers=5, batch_size=50):
        self.max_workers = max_workers
        self.batch_size = batch_size
        self.email_queue = queue.Queue()
        self.results = []
        
    def process_files_in_batches(self, pdf_files, policy_email_map):
        """Process files in batches to avoid overwhelming the system"""
        
        # Split files into batches
        batches = [pdf_files[i:i + self.batch_size] 
                  for i in range(0, len(pdf_files), self.batch_size)]
        
        logging.info(f"Processing {len(pdf_files)} files in {len(batches)} batches")
        
        for batch_num, batch in enumerate(batches, 1):
            logging.info(f"Processing batch {batch_num}/{len(batches)}")
            
            # Process batch with thread pool
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []
                
                for pdf_file in batch:
                    future = executor.submit(self.process_single_file, pdf_file, policy_email_map)
                    futures.append(future)
                
                # Wait for batch completion
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        self.results.append(result)
                    except Exception as e:
                        logging.error(f"Error processing file: {e}")
            
            # Rate limiting between batches
            if batch_num < len(batches):
                logging.info("Waiting 30 seconds before next batch...")
                time.sleep(30)
        
        return self.results
    
    def process_single_file(self, pdf_file, policy_email_map):
        """Process a single PDF file and send email"""
        try:
            # Your existing email sending logic here
            # Return success/failure status
            return {"file": pdf_file.name, "status": "success"}
        except Exception as e:
            logging.error(f"Failed to process {pdf_file.name}: {e}")
            return {"file": pdf_file.name, "status": "failed", "error": str(e)}

# Production configuration
PRODUCTION_CONFIG = {
    "MAX_WORKERS": 5,  # Concurrent email sending threads
    "BATCH_SIZE": 50,  # Files per batch
    "RATE_LIMIT_DELAY": 0.5,  # Seconds between emails
    "RETRY_ATTEMPTS": 3,  # Retry failed emails
    "BACKUP_ENABLED": True,  # Backup processed files
    "MONITORING_ENABLED": True  # Enable detailed logging
}

def setup_production_environment():
    """Setup production environment and checks"""
    
    # Check required environment variables
    required_vars = ['BREVO_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing environment variables: {missing_vars}")
    
    # Create necessary directories
    directories = ['logs', 'backups', 'temp', 'processed']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    # Setup logging
    logging.info("Production environment setup complete")
    
    return True

if __name__ == "__main__":
    setup_production_environment()
    processor = ProductionEmailProcessor()
    logging.info("Production email processor ready")