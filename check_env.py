#!/usr/bin/env python3
"""
Quick script to check if your environment variables are set correctly
"""
import os

def check_environment():
    print("🔍 Environment Variable Check")
    print("=" * 40)
    
    api_key = os.getenv('BREVO_API_KEY')
    if api_key:
        # Show only first and last 4 characters for security
        masked_key = f"{api_key[:8]}...{api_key[-8:]}" if len(api_key) > 16 else "***"
        print(f"✅ BREVO_API_KEY: {masked_key}")
        print("✅ Environment setup looks good!")
    else:
        print("❌ BREVO_API_KEY not found")
        print("💡 Run 'set_api_key.bat' to set it up")
    
    print("\n📋 Next steps:")
    print("1. Run: run_app.bat")
    print("2. Open: http://localhost:8501")
    print("3. Upload your files and test!")

if __name__ == "__main__":
    check_environment()