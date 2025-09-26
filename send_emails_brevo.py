import pandas as pd
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import base64
import os
from pathlib import Path
import time

def setup_brevo_client(api_key):
    """Setup Brevo API client"""
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    return sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_policy_emails():
    """Send emails with PDF attachments using Brevo"""
    
    # CONFIGURATION - UPDATE THESE VALUES
    SENDER_EMAIL = "CashBack@niclmauritius.site"    # Your verified sender email
    SENDER_NAME = "NIC Life Insurance Mauritius"     # Your company name
    REPLY_TO_EMAIL = "nicarlife@nicl.mu"            # Reply-to email
    REPLY_TO_NAME = "NIC Life Insurance"             # Reply-to name
    
    # Verify sender email first
    print(f"🔍 Using sender: {SENDER_NAME} <{SENDER_EMAIL}>")
    print(f"📧 Reply-to: {REPLY_TO_NAME} <{REPLY_TO_EMAIL}>")
    print("⚠️  IMPORTANT: Make sure sender domain is verified in your Brevo account!")
    
    # Email template - improved subject line
    SUBJECT = "NIC Life Insurance - Policy Cash Back Communication"
    # Professional HTML email template
    EMAIL_TEMPLATE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NIC Life Insurance - Policy Cash Back Documentation</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    
    <!-- Header -->
    <div style="background-color: #3498db; color: #ffffff; padding: 30px 20px; text-align: center;">
        <h1 style="margin: 0; font-size: 24px; font-weight: bold; color: #ffffff;">NIC Life Insurance Mauritius</h1>
        <p style="margin: 5px 0 0 0; font-size: 14px; color: #ffffff;">Policy Cash Back Documentation</p>
    </div>
    
    <!-- Main Content -->
    <div style="background: #ffffff; padding: 30px 20px; border: 1px solid #e0e0e0; border-top: none;">
        
        <p style="font-size: 16px; margin-bottom: 20px;">Dear <strong>{customer_name}</strong>,</p>
        
        <p style="font-size: 14px; margin-bottom: 20px;">
            We are pleased to provide you with your Life Insurance Policy Cash Back documentation.
        </p>
        
        <!-- Policy Info Box -->
        <table style="width: 100%; background-color: #f8f9fa; border-left: 4px solid #3498db; margin: 20px 0;" cellpadding="15" cellspacing="0">
            <tr>
                <td>
                    <p style="margin: 0; font-size: 16px;"><strong>Policy Number:</strong> <span style="color: #3498db; font-weight: bold;">{policy_number}</span></p>
                </td>
            </tr>
        </table>
        
        <p style="font-size: 14px; margin-bottom: 15px;">
            Please find your personalized documents attached to this email. The attachment contains:
        </p>
        
        <ul style="font-size: 14px; margin-bottom: 20px; padding-left: 20px;">
            <li style="margin-bottom: 8px;">Your official cash back letter</li>
            <li style="margin-bottom: 8px;">The corresponding cash back form</li>
        </ul>
        
        <!-- Security Notice -->
        <table style="width: 100%; background-color: #fff3cd; border: 1px solid #ffeaa7; margin: 25px 0;" cellpadding="20" cellspacing="0">
            <tr>
                <td style="width: 40px; vertical-align: top; font-size: 20px; color: #856404;">🔐</td>
                <td style="vertical-align: top;">
                    <h3 style="color: #856404; margin: 0 0 10px 0; font-size: 16px; font-weight: bold;">Important Security Information</h3>
                    <p style="margin: 0; font-size: 14px; color: #856404;">
                        Your PDF document is password-protected for your security. Please use your <strong>NID number</strong> as the password to open the document.
                    </p>
                </td>
            </tr>
        </table>
        
        <p style="font-size: 14px; margin-bottom: 25px;">
            If you have any questions or need assistance, please don't hesitate to contact us using the information below.
        </p>
        
        <p style="font-size: 14px; margin-bottom: 30px;">
            Best regards,<br>
            <strong>{sender_name}</strong>
        </p>
        
    </div>
    
    <!-- Footer -->
    <div style="background: #f8f9fa; padding: 25px 20px; border: 1px solid #e0e0e0; border-top: none; border-radius: 0 0 8px 8px;">
        
        <!-- Contact Information -->
        <table style="width: 100%; margin-bottom: 20px;" cellpadding="0" cellspacing="0">
            <tr>
                <td style="text-align: center;">
                    <h3 style="color: #3498db; margin: 0 0 15px 0; font-size: 16px; font-weight: bold;">Contact Information</h3>
                    
                    <table style="margin: 0 auto; text-align: left;" cellpadding="5" cellspacing="0">
                        <tr>
                            <td style="font-size: 14px; color: #666666; padding: 5px 0;">
                                <strong>📧 Email:</strong> <a href="mailto:nicarlife@nicl.mu" style="color: #3498db; text-decoration: none;">nicarlife@nicl.mu</a>
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size: 14px; color: #666666; padding: 5px 0;">
                                <strong>📞 Phone:</strong> <a href="tel:+2306023000" style="color: #3498db; text-decoration: none;">+230 602 3000</a>
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size: 14px; color: #666666; padding: 5px 0;">
                                <strong>📍 Address:</strong> NIC Centre, 217 Royal Road, Curepipe, Republic of Mauritius
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        
        <!-- Divider -->
        <table style="width: 100%; margin: 20px 0;" cellpadding="0" cellspacing="0">
            <tr>
                <td style="border-top: 1px solid #e0e0e0; height: 1px; font-size: 1px;">&nbsp;</td>
            </tr>
        </table>
        
        <!-- Footer Note -->
        <table style="width: 100%;" cellpadding="0" cellspacing="0">
            <tr>
                <td style="text-align: center;">
                    <p style="font-size: 12px; color: #888888; margin: 0;">
                        This is an automated message from NIC Life Insurance Mauritius. For assistance, please reply to this email or contact us using the information above.
                    </p>
                </td>
            </tr>
        </table>
        
    </div>
    
</body>
</html>
"""

    # Plain text version for email clients that don't support HTML
    EMAIL_TEMPLATE_TEXT = """
Dear {customer_name},

We are pleased to provide you with your Life Insurance Policy Cash Back documentation.

Policy Number: {policy_number}

Please find your personalized documents attached to this email. The attachment contains:
- Your official cash back letter
- The corresponding cash back form

IMPORTANT SECURITY INFORMATION:
Your PDF document is password-protected for your security. Please use your NIC number as the password to open the document.

If you have any questions or need assistance, please don't hesitate to contact us.

Best regards,
{sender_name}

---
CONTACT INFORMATION
Email: nicarlife@nicl.mu
Phone: +230 602 3000
Address: NIC Centre, 217 Royal Road, Curepipe, Republic of Mauritius

NIC Life Insurance Mauritius
This is an automated message. For assistance, please reply to this email or contact us using the information above.
"""
    
    # Get API key from environment variable
    BREVO_API_KEY = os.getenv('BREVO_API_KEY')
    if not BREVO_API_KEY:
        print("❌ Error: BREVO_API_KEY environment variable not set")
        print("Please set your Brevo API key as an environment variable:")
        print("Windows: set BREVO_API_KEY=your-api-key-here")
        print("Linux/Mac: export BREVO_API_KEY=your-api-key-here")
        return
    
    # Setup Brevo client
    try:
        api_instance = setup_brevo_client(BREVO_API_KEY)
        print("✅ Brevo API client initialized successfully")
    except Exception as e:
        print(f"❌ Error setting up Brevo client: {e}")
        return
    
    # Read Excel file to get policy-email mapping
    try:
        df = pd.read_excel("Compile CBOpt Nov25.xlsx")
        print(f"📊 Loaded {len(df)} policies from Excel")
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return
    
    # Check if policies_with_email folder exists
    pdf_folder = Path("policies_with_email")
    if not pdf_folder.exists():
        print("❌ 'policies_with_email' folder not found. Run create_complete_analysis.py first.")
        return
    
    # Get list of available PDF files
    pdf_files = list(pdf_folder.glob("*.pdf"))
    print(f"📁 Found {len(pdf_files)} PDF files ready for sending")
    
    # Create policy-email mapping
    policy_email_map = {}
    for _, row in df.iterrows():
        policy_str = str(row['Policy No'])
        email = row['Owner 1 Email']
        if pd.notna(email) and email.strip():  # Check for valid email
            policy_email_map[policy_str] = email
    
    print(f"📧 Found {len(policy_email_map)} valid email addresses")
    
    # Send emails
    sent_count = 0
    failed_count = 0
    failed_policies = []
    
    for pdf_file in pdf_files:
        # Extract policy number from filename
        filename = pdf_file.stem  # filename without extension
        
        # Convert filename back to policy format for lookup
        if '_' in filename and not filename.isdigit():
            # Slash format: 00407_0054316 -> 00407/0054316
            policy_lookup = filename.replace('_', '/', 1)
        else:
            # Numeric format: 29031933 -> 29031933
            policy_lookup = filename
        
        # Find email for this policy
        if policy_lookup not in policy_email_map:
            print(f"⚠️  No email found for policy: {policy_lookup}")
            failed_count += 1
            failed_policies.append(policy_lookup)
            continue
        
        recipient_email = policy_email_map[policy_lookup]
        
        try:
            # Read PDF file and encode to base64
            with open(pdf_file, 'rb') as f:
                pdf_content = f.read()
                pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            
            # Extract customer name (basic extraction from policy number)
            customer_name = "Valued Customer"  # You can enhance this if names are available
            
            # Prepare email content (both HTML and text versions)
            email_content_html = EMAIL_TEMPLATE_HTML.format(
                customer_name=customer_name,
                policy_number=policy_lookup,
                sender_name=SENDER_NAME
            )
            
            email_content_text = EMAIL_TEMPLATE_TEXT.format(
                customer_name=customer_name,
                policy_number=policy_lookup,
                sender_name=SENDER_NAME
            )
            
            # Create email object with professional HTML template
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": recipient_email}],
                sender={"name": SENDER_NAME, "email": SENDER_EMAIL},
                reply_to={"name": REPLY_TO_NAME, "email": REPLY_TO_EMAIL},
                subject=SUBJECT,
                html_content=email_content_html,
                text_content=email_content_text,
                attachment=[{
                    "content": pdf_base64,
                    "name": f"Policy_{filename}.pdf"
                }]
            )
            
            # Send email
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(f"✅ Sent to {recipient_email} - Policy: {policy_lookup}")
            sent_count += 1
            
            # Rate limiting - Brevo free tier has limits
            time.sleep(0.1)  # Small delay between emails
            
        except ApiException as e:
            print(f"❌ Failed to send to {recipient_email} - Policy: {policy_lookup}")
            print(f"   Error: {e}")
            failed_count += 1
            failed_policies.append(policy_lookup)
        except Exception as e:
            print(f"❌ Unexpected error for policy {policy_lookup}: {e}")
            failed_count += 1
            failed_policies.append(policy_lookup)
    
    # Final summary
    print(f"\n🎉 EMAIL SENDING COMPLETED!")
    print(f"📊 SUMMARY:")
    print(f"- Total PDFs processed: {len(pdf_files)}")
    print(f"- Emails sent successfully: {sent_count}")
    print(f"- Failed to send: {failed_count}")
    print(f"- Success rate: {sent_count/(sent_count+failed_count)*100:.1f}%")
    
    if failed_policies:
        print(f"\n⚠️  Failed policies:")
        for policy in failed_policies[:10]:  # Show first 10
            print(f"   - {policy}")
        if len(failed_policies) > 10:
            print(f"   ... and {len(failed_policies)-10} more")
    
    # Create sending report
    report_content = f"""EMAIL SENDING REPORT - BREVO
============================

SUMMARY:
- Total PDFs processed: {len(pdf_files)}
- Emails sent successfully: {sent_count}
- Failed to send: {failed_count}
- Success rate: {sent_count/(sent_count+failed_count)*100:.1f}%

CONFIGURATION USED:
- Sender: {SENDER_NAME} <{SENDER_EMAIL}>
- Subject: {SUBJECT}
- API: Brevo (Sendinblue)

FAILED POLICIES:
{chr(10).join([f"- {policy}" for policy in failed_policies])}

NEXT STEPS:
- Review failed policies and retry if needed
- Check Brevo dashboard for delivery statistics
- Monitor bounce rates and spam reports
"""
    
    with open("email_sending_report.txt", "w") as f:
        f.write(report_content)
    
    print(f"\n📄 Detailed report saved to: email_sending_report.txt")

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    os.system("pip install sib-api-v3-sdk pandas")

if __name__ == "__main__":
    print("BREVO EMAIL SENDER FOR POLICY DOCUMENTS")
    print("=" * 50)
    print()
    print("⚠️  BEFORE RUNNING:")
    print("1. Get your Brevo API key from: https://app.brevo.com/settings/keys/api")
    print("2. Set BREVO_API_KEY environment variable with your API key")
    print("3. Update SENDER_EMAIL, SENDER_NAME, and REPLY_TO_EMAIL in this script")
    print("4. Make sure your sender email is verified in Brevo")
    print("5. Run 'create_complete_analysis.py' first to generate PDF files")
    print()
    
    choice = input("Do you want to proceed? (y/n): ").lower().strip()
    if choice == 'y':
        # Check if required packages are installed
        try:
            import sib_api_v3_sdk
        except ImportError:
            install_requirements()
        
        send_policy_emails()
    else:
        print("Email sending cancelled.")