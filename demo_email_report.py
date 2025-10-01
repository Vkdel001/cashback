#!/usr/bin/env python3
"""
Demo script to showcase enhanced email reporting
Simulates various email sending scenarios with failures
"""
import time
import random

def simulate_email_with_failures():
    """Simulate email sending with various types of failures"""
    
    # Test data with some problematic emails
    test_emails = [
        ("client1@example.com", "TEST001", "success"),
        ("client2@example.com", "TEST002", "success"),
        ("invalid-email", "TEST003", "invalid_format"),
        ("client4@example.com", "TEST004", "success"),
        ("client5@bounced.com", "TEST005", "bounced"),
        ("client6@example.com", "TEST006", "rate_limit"),
        ("client7@example.com", "TEST007", "success"),
        ("client8@example.com", "TEST008", "success"),
        ("", "TEST009", "empty_email"),
        ("client10@example.com", "TEST010", "success"),
    ]
    
    print("🔍 Using sender: NIC Life Insurance Mauritius <CashBack@niclmauritius.site>")
    print("📧 Reply-to: NIC Life Insurance <customerservice@nicl.mu>")
    print("✅ Brevo API client initialized successfully")
    print(f"📊 Loaded {len(test_emails)} policies from Excel")
    print(f"📁 Found {len(test_emails)} PDF files ready for sending")
    print(f"📧 Found {len(test_emails)} email addresses")
    time.sleep(1)
    
    for email, policy, result_type in test_emails:
        # Random delay
        time.sleep(random.uniform(0.3, 1.0))
        
        if result_type == "success":
            print(f"✅ Sent to {email} - Policy: {policy}")
        elif result_type == "invalid_format":
            print(f"❌ Failed to send to {email} - Policy: {policy}")
            print(f"   Reason: Invalid email format or request data")
        elif result_type == "bounced":
            print(f"❌ Failed to send to {email} - Policy: {policy}")
            print(f"   Reason: Email address bounced or does not exist")
        elif result_type == "rate_limit":
            print(f"❌ Failed to send to {email} - Policy: {policy}")
            print(f"   Reason: Rate limit exceeded - too many requests")
        elif result_type == "empty_email":
            print(f"❌ Failed to send to {email} - Policy: {policy}")
            print(f"   Reason: Empty or missing email address")
    
    time.sleep(0.5)
    print("🎉 EMAIL SENDING COMPLETED!")
    
    # Summary
    successful = sum(1 for _, _, result in test_emails if result == "success")
    failed = len(test_emails) - successful
    
    print(f"📊 SUMMARY:")
    print(f"- Total PDFs processed: {len(test_emails)}")
    print(f"- Emails sent successfully: {successful}")
    print(f"- Failed to send: {failed}")
    print(f"- Success rate: {(successful/len(test_emails)*100):.1f}%")

if __name__ == "__main__":
    print("📊 Email Reporting Demo")
    print("=" * 35)
    print("This simulates email sending with various failure scenarios.")
    print("Use this to test the enhanced reporting features!")
    print()
    
    input("Press Enter to start the demo...")
    print()
    
    simulate_email_with_failures()
    
    print()
    print("🎯 Demo completed!")
    print()
    print("📋 What you'll see in the Streamlit report:")
    print("✅ Detailed failed emails table with reasons")
    print("📊 Success/failure statistics and charts") 
    print("📥 Downloadable CSV reports")
    print("💡 Actionable recommendations")
    print()
    print("Run 'streamlit run pdf_processor_final_working.py' to see the full report!")