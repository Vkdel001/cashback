#!/usr/bin/env python3
"""
Demo script to showcase the enhanced progress bar
Creates a simulation of email sending with realistic timing
"""
import time
import random

def simulate_email_sending():
    """Simulate email sending with realistic output"""
    
    # Simulate initial setup
    print("🔍 Using sender: NIC Life Insurance Mauritius <CashBack@niclmauritius.site>")
    print("📧 Reply-to: NIC Life Insurance <customerservice@nicl.mu>")
    print("⚠️  IMPORTANT: Make sure sender domain is verified in your Brevo account!")
    print("✅ Brevo API client initialized successfully")
    time.sleep(1)
    
    # Simulate loading data
    total_policies = 25  # Smaller number for demo
    print(f"📊 Loaded {total_policies} policies from Excel")
    time.sleep(0.5)
    
    print(f"📁 Found {total_policies} PDF files ready for sending")
    print(f"📧 Found {total_policies} valid email addresses")
    time.sleep(0.5)
    
    # Simulate email sending
    for i in range(1, total_policies + 1):
        # Random delay between emails (0.5 to 2 seconds)
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)
        
        # Simulate occasional failures (10% failure rate)
        if random.random() < 0.1:
            print(f"❌ Failed to send to client{i}@example.com - Policy: TEST{i:03d}")
            print(f"   Error: Temporary server error")
        else:
            print(f"✅ Sent to client{i}@example.com - Policy: TEST{i:03d}")
    
    # Simulate completion
    time.sleep(1)
    print("🎉 EMAIL SENDING COMPLETED!")
    print(f"📊 SUMMARY:")
    print(f"- Total PDFs processed: {total_policies}")
    print(f"- Emails sent successfully: {int(total_policies * 0.9)}")
    print(f"- Failed to send: {int(total_policies * 0.1)}")
    print(f"- Success rate: 90.0%")

if __name__ == "__main__":
    print("🎬 Email Sending Demo")
    print("=" * 30)
    print("This simulates the email sending process with realistic timing.")
    print("Use this output to test the progress bar in Streamlit!")
    print()
    
    input("Press Enter to start the demo...")
    print()
    
    simulate_email_sending()
    
    print()
    print("🎯 Demo completed!")
    print("Now run 'streamlit run pdf_processor_final_working.py' to see the enhanced progress bar!")