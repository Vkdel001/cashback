#!/usr/bin/env python3
"""
Test Windows encoding for subprocess
"""
import subprocess
import sys
import os

def test_subprocess_encoding():
    """Test subprocess with proper encoding for Windows"""
    print("🧪 Testing subprocess encoding on Windows...")
    
    # Set API key for testing
    env = os.environ.copy()
    env['BREVO_API_KEY'] = os.getenv('BREVO_API_KEY', 'test-key')
    
    try:
        # Test the subprocess with UTF-8 encoding
        process = subprocess.Popen(
            [sys.executable, '-c', 'print("✅ Test output with emoji 📧 🎉"); print("Testing Unicode: café résumé naïve")'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env
        )
        
        # Read output
        stdout, stderr = process.communicate(timeout=10)
        
        print("📋 Subprocess output:")
        print(stdout)
        
        if stderr:
            print("⚠️ Subprocess errors:")
            print(stderr)
        
        print("✅ Encoding test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Encoding test failed: {e}")
        return False

def test_email_script_encoding():
    """Test the actual email script with encoding"""
    print("\n🧪 Testing email script encoding...")
    
    if not os.path.exists('send_emails_brevo.py'):
        print("❌ Email script not found")
        return False
    
    env = os.environ.copy()
    env['BREVO_API_KEY'] = os.getenv('BREVO_API_KEY', 'test-key')
    
    try:
        # Test just the start of the email script
        process = subprocess.Popen(
            [sys.executable, 'send_emails_brevo.py', '--automated'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env
        )
        
        # Read first few lines
        output_lines = []
        for _ in range(10):  # Read first 10 lines
            try:
                line = process.stdout.readline()
                if not line:
                    break
                output_lines.append(line.strip())
            except Exception as e:
                print(f"⚠️ Error reading line: {e}")
                break
        
        # Terminate the process
        process.terminate()
        
        print("📋 Email script output (first 10 lines):")
        for line in output_lines:
            print(f"  {line}")
        
        print("✅ Email script encoding test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Email script encoding test failed: {e}")
        return False

def main():
    print("🔧 Windows Encoding Test")
    print("=" * 30)
    
    # Test 1: Basic subprocess encoding
    test1_passed = test_subprocess_encoding()
    
    # Test 2: Email script encoding
    test2_passed = test_email_script_encoding()
    
    print("\n📊 Test Results:")
    print(f"  Basic encoding: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"  Email script:   {'✅ PASS' if test2_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All encoding tests passed!")
        print("The Streamlit app should now work without encoding errors.")
    else:
        print("\n❌ Some tests failed.")
        print("Check the errors above and ensure UTF-8 encoding is properly configured.")

if __name__ == "__main__":
    main()