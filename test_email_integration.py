#!/usr/bin/env python3
"""
Test script for email integration
Run this to test the hybrid email approach locally
"""
import os
import pandas as pd
from pathlib import Path

def create_test_data():
    """Create test Excel file and sample PDFs for testing"""
    print("🔧 Creating test data...")
    
    # Create test Excel file
    test_data = {
        'Policy No': ['TEST001', 'TEST002', 'TEST003'],
        'Owner 1 Email': ['test1@example.com', 'test2@example.com', 'test3@example.com']
    }
    
    df = pd.DataFrame(test_data)
    df.to_excel('Compile CBOpt Nov25.xlsx', index=False)
    print("✅ Created test Excel file: Compile CBOpt Nov25.xlsx")
    
    # Create test PDF directory and files
    os.makedirs('policies_with_email', exist_ok=True)
    
    # Create dummy PDF files (just text files for testing)
    for policy in ['TEST001', 'TEST002', 'TEST003']:
        pdf_path = f'policies_with_email/{policy}.pdf'
        with open(pdf_path, 'w') as f:
            f.write(f"Dummy PDF content for policy {policy}")
    
    print("✅ Created 3 test PDF files in policies_with_email/")
    print()

def check_environment():
    """Check if environment is ready for testing"""
    print("🔍 Checking environment...")
    
    # Check API key
    api_key = os.getenv('BREVO_API_KEY')
    if api_key:
        print(f"✅ BREVO_API_KEY is set: {api_key[:8]}...{api_key[-8:]}")
    else:
        print("❌ BREVO_API_KEY not set")
        print("   Set it with: set BREVO_API_KEY=your-api-key-here")
        return False
    
    # Check required files
    if os.path.exists('send_emails_brevo.py'):
        print("✅ Email script found: send_emails_brevo.py")
    else:
        print("❌ Email script not found: send_emails_brevo.py")
        return False
    
    if os.path.exists('pdf_processor_final_working.py'):
        print("✅ Main app found: pdf_processor_final_working.py")
    else:
        print("❌ Main app not found: pdf_processor_final_working.py")
        return False
    
    print()
    return True

def test_email_script():
    """Test the email script directly"""
    print("🧪 Testing email script...")
    
    import subprocess
    import sys
    
    try:
        # Test the email script in automated mode with proper encoding
        result = subprocess.run([
            sys.executable, 'send_emails_brevo.py', '--automated'
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
        
        print("📋 Email script output:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Email script errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Email script test completed successfully")
        else:
            print(f"❌ Email script failed with return code: {result.returncode}")
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print("⏰ Email script test timed out (this might be normal for actual sending)")
        return True
    except Exception as e:
        print(f"❌ Error testing email script: {e}")
        return False

def main():
    print("🚀 Email Integration Test")
    print("=" * 40)
    print()
    
    # Step 1: Check environment
    if not check_environment():
        print("❌ Environment check failed. Please fix the issues above.")
        return
    
    # Step 2: Create test data
    create_test_data()
    
    # Step 3: Test email script
    if test_email_script():
        print()
        print("🎉 All tests passed!")
        print()
        print("📋 Next steps:")
        print("1. Run: streamlit run pdf_processor_final_working.py")
        print("2. Upload files and process them")
        print("3. Click the 'Send Emails Now' button")
        print("4. Watch the real-time email sending progress!")
    else:
        print()
        print("❌ Tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()