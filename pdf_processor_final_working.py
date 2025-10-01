import streamlit as st
import pandas as pd
import PyPDF2
import re
import os
import zipfile
import time
from pathlib import Path
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="PDF Policy Processor",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False

def process_uploaded_files(pdf_file, excel_file, progress_bar, status_text):
    """Process uploaded PDF and Excel files"""
    
    # Save uploaded files to current directory
    pdf_path = "temp_uploaded.pdf"
    excel_path = "temp_uploaded.xlsx"
    
    with open(pdf_path, "wb") as f:
        f.write(pdf_file.getvalue())
    
    with open(excel_path, "wb") as f:
        f.write(excel_file.getvalue())
    
    # Read Excel data
    try:
        df = pd.read_excel(excel_path)
        st.success(f"✅ Excel file loaded: {len(df)} policies found")
    except Exception as e:
        st.error(f"❌ Error reading Excel file: {e}")
        return None
    
    # Read PDF and keep file open during processing
    try:
        pdf_file_handle = open(pdf_path, 'rb')
        
        # Handle both old and new PyPDF2 versions
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file_handle)
            total_pages = len(pdf_reader.pages)
        except AttributeError:
            # Older PyPDF2 version
            pdf_reader = PyPDF2.PdfFileReader(pdf_file_handle)
            total_pages = pdf_reader.numPages
        
        st.success(f"✅ PDF file loaded: {total_pages} pages")
    except Exception as e:
        st.error(f"❌ Error reading PDF file: {e}")
        return None
    
    # Create output directories and clean old files
    os.makedirs("policies_with_email", exist_ok=True)
    os.makedirs("policies_without_email", exist_ok=True)
    
    # Clean old PDF files from previous sessions
    import glob
    for old_file in glob.glob("policies_with_email/*.pdf"):
        os.remove(old_file)
    for old_file in glob.glob("policies_without_email/*.pdf"):
        os.remove(old_file)
    
    st.info("🧹 Cleaned old PDF files from previous sessions")
    
    # First pass: collect all pages for each policy
    policy_pages = {}  # Dictionary to store policy_number -> list of pages
    
    status_text.text("🔍 Scanning PDF for policies...")
    
    try:
        for page_num in range(total_pages):
            progress_bar.progress((page_num + 1) / (total_pages * 2))  # First half of progress
            status_text.text(f"📄 Scanning page {page_num + 1}/{total_pages}")
            
            # Handle both old and new PyPDF2 versions
            try:
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
            except AttributeError:
                # Older PyPDF2 version
                page = pdf_reader.getPage(page_num)
                text = page.extractText()
            
            # Look for policy numbers (both formats: 00407/0054316 and 29031933)
            policy_patterns = [
                r'\b\d{5}/\d{7}\b',  # Format: 00407/0054316
                r'\b\d{8}\b'         # Format: 29031933
            ]
            
            policy_match = None
            for pattern in policy_patterns:
                match = re.search(pattern, text)
                if match:
                    policy_match = match
                    break
            
            if policy_match:
                policy_number = policy_match.group(0)
                if policy_number not in policy_pages:
                    policy_pages[policy_number] = []
                policy_pages[policy_number].append(page_num)
        
        # Second pass: create PDFs for each policy
        policies_found = 0
        for policy_number, pages in policy_pages.items():
            progress_bar.progress(0.5 + (policies_found + 1) / (len(policy_pages) * 2))  # Second half
            status_text.text(f"💾 Creating PDF for policy {policy_number} ({len(pages)} pages)")
            
            save_policy_pdf(pdf_reader, pages, policy_number, df)
            policies_found += 1
        
    finally:
        # Close the PDF file
        pdf_file_handle.close()
        
        # Clean up temp files
        try:
            os.remove(pdf_path)
            os.remove(excel_path)
        except:
            pass
    
    # Count results
    policies_with_email = len(list(Path("policies_with_email").glob("*.pdf")))
    policies_without_email = len(list(Path("policies_without_email").glob("*.pdf")))
    
    status_text.text("✅ Processing completed!")
    progress_bar.progress(1.0)
    
    return {
        'total_found': policies_found,
        'with_email': policies_with_email,
        'without_email': policies_without_email
    }

def save_policy_pdf(pdf_reader, page_numbers, policy_number, df):
    """Save individual policy as PDF with password protection"""
    
    # Check if policy has email and NIC
    has_email = False
    email = None
    nic_password = None
    
    # Look for policy in Excel (try both formats) - using column names for flexibility
    for _, row in df.iterrows():
        # Get policy number from first column or 'Policy No' column
        if 'Policy No' in df.columns:
            excel_policy = str(row['Policy No']).strip()
        else:
            excel_policy = str(row.iloc[0]).strip()
        
        # Get email from 'Owner 1 Email' column or similar
        excel_email = None
        for email_col in ['Owner 1 Email', 'Email', 'Owner Email', 'email']:
            if email_col in df.columns and pd.notna(row[email_col]):
                excel_email = str(row[email_col]).strip()
                break
        
        # Get NIC from 'NIC' column
        excel_nic = None
        if 'NIC' in df.columns and pd.notna(row['NIC']):
            excel_nic = str(row['NIC']).strip()
        
        # Check if policies match (handle different formats)
        if (excel_policy == policy_number or 
            excel_policy.replace('/', '') == policy_number.replace('/', '') or
            excel_policy.lstrip('0') == policy_number.lstrip('0')):
            
            if excel_email and '@' in excel_email:
                has_email = True
                email = excel_email
            
            if excel_nic:
                nic_password = excel_nic
            
            break
    
    # Create new PDF - handle both old and new PyPDF2 versions
    try:
        from PyPDF2 import PdfWriter
        writer = PdfWriter()
        
        for page_num in page_numbers:
            try:
                if page_num < len(pdf_reader.pages):
                    writer.add_page(pdf_reader.pages[page_num])
            except AttributeError:
                # Older PyPDF2 version
                if page_num < pdf_reader.numPages:
                    writer.addPage(pdf_reader.getPage(page_num))
    except ImportError:
        # Very old PyPDF2 version
        from PyPDF2 import PdfFileWriter
        writer = PdfFileWriter()
        
        for page_num in page_numbers:
            if page_num < pdf_reader.numPages:
                writer.addPage(pdf_reader.getPage(page_num))
    
    # Add password protection ONLY if policy has email (will be sent electronically)
    if has_email and nic_password:
        try:
            # For newer PyPDF2 versions
            writer.encrypt(nic_password)
        except AttributeError:
            try:
                # For older PyPDF2 versions
                writer.encrypt(user_pwd=nic_password, owner_pwd=nic_password)
            except:
                # If encryption fails, continue without password
                st.warning(f"⚠️ Could not encrypt PDF for policy {policy_number}")
    elif has_email and not nic_password:
        st.warning(f"⚠️ Policy {policy_number} has email but no NIC for password protection")
    
    # Save to appropriate folder
    folder = "policies_with_email" if has_email else "policies_without_email"
    # Replace invalid filename characters
    safe_policy_number = policy_number.replace('/', '_').replace('\\', '_')
    filename = f"{safe_policy_number}.pdf"
    filepath = Path(folder) / filename
    
    with open(filepath, 'wb') as output_file:
        writer.write(output_file)

def create_download_zip(folder_path, zip_name):
    """Create ZIP file for download"""
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        folder = Path(folder_path)
        for file_path in folder.glob("*.pdf"):
            zip_file.write(file_path, file_path.name)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()



def check_excel_file_exists():
    """Check if Excel file exists for email sending"""
    excel_locations = [
        "Compile CBOpt Nov25.xlsx",
        "storage/uploaded_files/latest_excel.xlsx",
        "temp/temp_uploaded.xlsx"
    ]
    
    for location in excel_locations:
        if os.path.exists(location):
            return location
    return None

def check_pdf_files_exist():
    """Check if PDF files exist for email sending"""
    pdf_locations = [
        "policies_with_email",
        "storage/generated_pdfs/with_email"
    ]
    
    for location in pdf_locations:
        if os.path.exists(location):
            pdf_files = list(Path(location).glob("*.pdf"))
            if pdf_files:
                return len(pdf_files)
    return 0

def check_pdf_files_without_email():
    """Check if PDF files exist without email addresses (for printing)"""
    pdf_locations = [
        "policies_without_email",
        "storage/generated_pdfs/without_email"
    ]
    
    for location in pdf_locations:
        if os.path.exists(location):
            pdf_files = list(Path(location).glob("*.pdf"))
            if pdf_files:
                return len(pdf_files)
    return 0

def send_emails_via_subprocess():
    """Send emails using subprocess to run the existing email script"""
    import subprocess
    import sys
    
    st.subheader("📧 Sending Emails...")
    
    # Create placeholders for real-time updates
    status_placeholder = st.empty()
    progress_placeholder = st.empty()
    metrics_placeholder = st.empty()
    output_placeholder = st.empty()
    
    try:
        # Prepare the command with automated flag
        cmd = [sys.executable, "send_emails_brevo.py", "--automated"]
        
        # Set up environment variables
        env = os.environ.copy()
        env['BREVO_API_KEY'] = os.getenv('BREVO_API_KEY', '')
        
        if not env['BREVO_API_KEY']:
            st.error("❌ BREVO_API_KEY not set. Please set your API key in environment variables.")
            st.code("set BREVO_API_KEY=your-api-key-here")
            return
        
        status_placeholder.info("🚀 Starting email sending process...")
        
        # Start the subprocess with UTF-8 encoding
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
            encoding='utf-8',
            errors='replace'
        )
        
        # Initialize counters and timing
        sent_count = 0
        failed_count = 0
        total_count = 0
        output_lines = []
        failed_emails = []  # Track failed emails with details
        successful_emails = []  # Track successful emails
        start_time = time.time()
        last_email_time = start_time
        
        # Read output in real-time
        while True:
            try:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    output_lines.append(line)
            except UnicodeDecodeError as e:
                # Handle encoding errors gracefully
                line = f"⚠️ Encoding error in output: {str(e)}"
                output_lines.append(line)
                continue
                
                # Parse different types of output
                if "✅ Sent to" in line:
                    sent_count += 1
                    last_email_time = time.time()
                    
                    # Extract email and policy info from success message
                    import re
                    match = re.search(r'Sent to (.+?) - Policy: (.+)', line)
                    if match:
                        email, policy = match.groups()
                        successful_emails.append({
                            'email': email.strip(),
                            'policy': policy.strip(),
                            'timestamp': time.strftime("%H:%M:%S")
                        })
                    
                    status_placeholder.success(f"📧 Successfully sent email #{sent_count}")
                    
                elif "❌ Failed" in line or ("Error" in line and "@" in line):
                    failed_count += 1
                    
                    # Extract failure details
                    import re
                    # Try to extract email and policy from failure message
                    email_match = re.search(r'(?:Failed to send to|Error.*?)(.+?@.+?)(?:\s|$)', line)
                    policy_match = re.search(r'Policy: (.+?)(?:\s|$)', line)
                    
                    failed_info = {
                        'email': email_match.group(1).strip() if email_match else 'Unknown',
                        'policy': policy_match.group(1).strip() if policy_match else 'Unknown',
                        'reason': line.strip(),
                        'timestamp': time.strftime("%H:%M:%S")
                    }
                    failed_emails.append(failed_info)
                    
                    status_placeholder.error(f"❌ Email failed (Total failures: {failed_count})")
                elif "📊 Loaded" in line and "policies" in line:
                    # Extract total count from "📊 Loaded X policies from Excel"
                    import re
                    match = re.search(r'(\d+) policies', line)
                    if match:
                        total_count = int(match.group(1))
                elif "📁 Found" in line and "PDF files" in line:
                    progress_placeholder.info(line)
                elif "🎉 EMAIL SENDING COMPLETED" in line:
                    status_placeholder.success("🎉 Email sending completed!")
                
                # Update progress bar and metrics
                if total_count > 0:
                    processed = sent_count + failed_count
                    progress = processed / total_count
                    remaining = total_count - processed
                    
                    # Calculate estimated time remaining
                    elapsed_time = time.time() - start_time
                    if processed > 0:
                        avg_time_per_email = elapsed_time / processed
                        eta_seconds = avg_time_per_email * remaining
                        eta_minutes = int(eta_seconds // 60)
                        eta_seconds = int(eta_seconds % 60)
                        eta_text = f" (ETA: {eta_minutes}m {eta_seconds}s)" if remaining > 0 else " (Complete!)"
                    else:
                        eta_text = ""
                    
                    # Enhanced progress bar with detailed info
                    progress_placeholder.progress(
                        progress, 
                        f"📊 Progress: {processed}/{total_count} emails processed ({progress*100:.1f}%){eta_text}"
                    )
                    
                    # Real-time metrics
                    with metrics_placeholder.container():
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("✅ Sent", sent_count, delta=None)
                        with col2:
                            st.metric("❌ Failed", failed_count, delta=None)
                        with col3:
                            st.metric("⏳ Remaining", remaining, delta=None)
                        with col4:
                            success_rate = (sent_count / processed * 100) if processed > 0 else 0
                            st.metric("📈 Success Rate", f"{success_rate:.1f}%", delta=None)
                
                # Show recent output with better formatting
                if output_lines:
                    recent_output = "\n".join(output_lines[-8:])  # Show last 8 lines
                    output_placeholder.text_area("📋 Recent Activity:", recent_output, height=180)
        
        # Wait for process to complete
        return_code = process.wait()
        
        # Show final results with enhanced feedback
        total_time = time.time() - start_time
        total_minutes = int(total_time // 60)
        total_seconds = int(total_time % 60)
        
        if return_code == 0:
            st.success(f"🎉 Email sending completed successfully in {total_minutes}m {total_seconds}s!")
            st.balloons()
            
            # Show completion progress bar at 100%
            progress_placeholder.progress(1.0, "✅ All emails processed - 100% Complete!")
        else:
            st.error(f"❌ Email sending failed with return code: {return_code} after {total_minutes}m {total_seconds}s")
        
        # Show comprehensive final summary
        if sent_count > 0 or failed_count > 0:
            st.markdown("---")
            st.subheader("📊 Email Delivery Report")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("✅ Sent", sent_count)
            with col2:
                st.metric("❌ Failed", failed_count)
            with col3:
                success_rate = (sent_count / (sent_count + failed_count) * 100) if (sent_count + failed_count) > 0 else 0
                st.metric("📊 Success Rate", f"{success_rate:.1f}%")
            with col4:
                st.metric("⏱️ Total Time", f"{total_minutes}m {total_seconds}s")
            
            # Detailed reports in tabs
            tab1, tab2, tab3 = st.tabs(["❌ Failed Emails", "✅ Successful Emails", "📋 Summary"])
            
            with tab1:
                if failed_emails:
                    st.error(f"⚠️ {len(failed_emails)} emails failed to send")
                    
                    # Create DataFrame for failed emails
                    failed_df = pd.DataFrame(failed_emails)
                    
                    # Display failed emails table
                    st.dataframe(
                        failed_df,
                        column_config={
                            "email": "📧 Email Address",
                            "policy": "📄 Policy Number", 
                            "reason": "❌ Failure Reason",
                            "timestamp": "⏰ Time"
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                    
                    # Download failed emails as CSV
                    csv_data = failed_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Failed Emails Report",
                        data=csv_data,
                        file_name=f"failed_emails_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                    # Common failure reasons and solutions
                    st.markdown("### 🔧 Common Issues & Solutions")
                    st.info("""
                    **Common failure reasons:**
                    - **Invalid email format**: Check email addresses in Excel file
                    - **Brevo API limits**: Check your Brevo plan limits
                    - **Network timeout**: Retry sending failed emails
                    - **Sender domain not verified**: Verify domain in Brevo dashboard
                    """)
                    
                else:
                    st.success("🎉 All emails were sent successfully!")
            
            with tab2:
                if successful_emails:
                    st.success(f"✅ {len(successful_emails)} emails sent successfully")
                    
                    # Create DataFrame for successful emails
                    success_df = pd.DataFrame(successful_emails)
                    
                    # Display successful emails table
                    st.dataframe(
                        success_df,
                        column_config={
                            "email": "📧 Email Address",
                            "policy": "📄 Policy Number",
                            "timestamp": "⏰ Time Sent"
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                    
                    # Download successful emails as CSV
                    csv_data = success_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Successful Emails Report",
                        data=csv_data,
                        file_name=f"successful_emails_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.error("❌ No emails were sent successfully")
            
            with tab3:
                st.markdown("### 📈 Delivery Statistics")
                
                # Create summary statistics
                total_processed = sent_count + failed_count
                if total_processed > 0:
                    # Success rate chart
                    chart_data = pd.DataFrame({
                        'Status': ['Successful', 'Failed'],
                        'Count': [sent_count, failed_count],
                        'Percentage': [
                            (sent_count / total_processed) * 100,
                            (failed_count / total_processed) * 100
                        ]
                    })
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.bar_chart(chart_data.set_index('Status')['Count'])
                    
                    with col2:
                        st.markdown(f"""
                        **📊 Summary Statistics:**
                        - **Total Processed**: {total_processed} emails
                        - **Success Rate**: {success_rate:.1f}%
                        - **Average Speed**: {total_processed / (total_time / 60):.1f} emails/minute
                        - **Processing Time**: {total_minutes}m {total_seconds}s
                        """)
                
                # Recommendations based on results
                if failed_count > 0:
                    failure_rate = (failed_count / total_processed) * 100
                    if failure_rate > 20:
                        st.warning("⚠️ High failure rate detected. Consider checking email addresses and Brevo account status.")
                    elif failure_rate > 10:
                        st.info("💡 Some emails failed. Review the failed emails report for details.")
                    else:
                        st.success("✅ Low failure rate. Most emails were delivered successfully.")
                else:
                    st.success("🎉 Perfect delivery! All emails were sent successfully.")
        
        # Show complete output in expander
        if output_lines:
            with st.expander("📋 Complete Log"):
                st.text("\n".join(output_lines))
    
    except Exception as e:
        st.error(f"❌ Error running email script: {str(e)}")
        st.exception(e)

def merge_pdfs_for_printing():
    """Merge PDFs without email addresses into a single printable file"""
    st.subheader("🔗 Merging PDFs for Printing...")
    
    # Create placeholders for updates
    status_placeholder = st.empty()
    progress_placeholder = st.empty()
    details_placeholder = st.empty()
    
    try:
        # Find the correct input folder
        input_folders = [
            "policies_without_email",
            "storage/generated_pdfs/without_email"
        ]
        
        input_folder = None
        for folder in input_folders:
            if os.path.exists(folder):
                pdf_files = list(Path(folder).glob("*.pdf"))
                if pdf_files:
                    input_folder = folder
                    break
        
        if not input_folder:
            st.error("❌ No PDFs without email addresses found")
            return
        
        output_file = "policies_for_printing.pdf"
        
        status_placeholder.info("🔍 Scanning PDF files...")
        
        # Get all PDF files
        pdf_files = list(Path(input_folder).glob("*.pdf"))
        pdf_files.sort()  # Sort for consistent order
        
        if not pdf_files:
            st.error(f"❌ No PDF files found in '{input_folder}' folder")
            return
        
        status_placeholder.success(f"📁 Found {len(pdf_files)} PDF files to merge")
        
        # Delete existing output file if it exists
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
                status_placeholder.info("🗑️ Removed existing merged file")
            except Exception as e:
                st.error(f"⚠️ Could not delete existing file: {e}")
                st.warning("Please close any PDF viewers and try again")
                return
        
        # Initialize progress tracking
        progress_placeholder.progress(0, "Starting PDF merge...")
        
        # Use PyPDF2 PdfFileMerger for robust merging
        merger = PyPDF2.PdfFileMerger()
        successful_merges = 0
        failed_files = []
        
        # Merge PDFs with progress updates
        for i, pdf_path in enumerate(pdf_files):
            try:
                # Update progress
                progress = (i + 1) / len(pdf_files)
                progress_placeholder.progress(
                    progress, 
                    f"Processing {i+1}/{len(pdf_files)}: {pdf_path.name}"
                )
                
                # Add PDF to merger
                merger.append(str(pdf_path))
                successful_merges += 1
                
                # Show details every 10 files or for small batches
                if i % 10 == 0 or len(pdf_files) <= 20:
                    details_placeholder.info(f"📄 Added: {pdf_path.name}")
                
            except Exception as e:
                failed_files.append((pdf_path.name, str(e)))
                details_placeholder.warning(f"⚠️ Skipped {pdf_path.name}: {str(e)}")
                continue
        
        if successful_merges == 0:
            st.error("❌ No PDFs could be merged")
            return
        
        # Write the merged PDF
        status_placeholder.info("💾 Writing merged PDF file...")
        progress_placeholder.progress(0.95, "Finalizing merged PDF...")
        
        try:
            with open(output_file, 'wb') as output:
                merger.write(output)
            merger.close()
            
        except Exception as e:
            st.error(f"❌ Error writing output file: {e}")
            st.warning("Make sure no PDF viewer has the file open")
            return
        
        # Get final statistics
        file_size = os.path.getsize(output_file)
        
        # Count pages in final PDF
        try:
            with open(output_file, 'rb') as f:
                reader = PyPDF2.PdfFileReader(f)
                total_pages = reader.numPages
        except:
            total_pages = "Unknown"
        
        # Complete progress
        progress_placeholder.progress(1.0, "✅ PDF merge completed!")
        
        # Show success message
        st.success("🎉 PDF merging completed successfully!")
        st.balloons()
        
        # Display merge statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📄 PDFs Merged", successful_merges)
        with col2:
            st.metric("📊 Total Pages", total_pages)
        with col3:
            st.metric("💾 File Size", f"{file_size / 1024 / 1024:.1f} MB")
        with col4:
            st.metric("❌ Failed", len(failed_files))
        
        # Download button for the merged PDF
        with open(output_file, 'rb') as f:
            pdf_data = f.read()
        
        st.download_button(
            label="📥 Download Merged PDF for Printing",
            data=pdf_data,
            file_name=f"policies_for_printing_{time.strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        # Show merge details
        with st.expander("📋 Merge Details"):
            st.markdown(f"""
            **📊 Merge Summary:**
            - **Input Folder**: {input_folder}
            - **Output File**: {output_file}
            - **Successfully Merged**: {successful_merges} PDFs
            - **Total Pages**: {total_pages}
            - **File Size**: {file_size / 1024 / 1024:.1f} MB
            """)
            
            if failed_files:
                st.markdown("**⚠️ Failed Files:**")
                for filename, error in failed_files:
                    st.text(f"• {filename}: {error}")
            else:
                st.success("✅ All PDFs merged successfully!")
        
        # Instructions for printing
        st.markdown("---")
        st.info("""
        **🖨️ Printing Instructions:**
        1. Download the merged PDF file above
        2. Open it in a PDF viewer (Adobe Reader, etc.)
        3. Print using your preferred printer settings
        4. Consider duplex printing to save paper
        5. Use the merged file for bulk mailing of policies without email addresses
        """)
        
    except Exception as e:
        st.error(f"❌ Error during PDF merging: {str(e)}")
        st.exception(e)

def main():
    st.title("📄 PDF Policy Processor")
    st.markdown("Extract individual policies from merged PDF and organize by email availability")
    
    # File uploads
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Upload PDF File")
        pdf_file = st.file_uploader("Choose PDF file", type=['pdf'], key="pdf_uploader")
        if pdf_file:
            st.success(f"✅ PDF uploaded: {pdf_file.name}")
    
    with col2:
        st.subheader("📊 Upload Excel File")
        excel_file = st.file_uploader("Choose Excel file", type=['xlsx', 'xls'], key="excel_uploader")
        if excel_file:
            st.success(f"✅ Excel uploaded: {excel_file.name}")
    
    # Processing section
    if pdf_file and excel_file and not st.session_state.processing_done:
        st.markdown("---")
        
        if st.button("🚀 Process Files", type="primary", key="process_btn"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Process files
            with st.spinner("Processing files..."):
                results = process_uploaded_files(pdf_file, excel_file, progress_bar, status_text)
                
                # STORE IN SESSION STATE
                st.session_state.results = results
                st.session_state.processing_done = True
                
                # Force rerun to show results
                st.experimental_rerun()
    
    # Results section - ALWAYS show if we have results in session state
    if st.session_state.results:
        results = st.session_state.results
        
        st.success("🎉 Processing completed!")
        
        # Show results
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Total Policies", results['total_found'])
        with col2:
            st.metric("✅ With Email", results['with_email'])
        with col3:
            st.metric("❌ Without Email", results['without_email'])
        
        # Download options
        st.markdown("---")
        st.subheader("📥 Download Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if results['with_email'] > 0:
                zip_data = create_download_zip("policies_with_email", "policies_with_email.zip")
                st.download_button(
                    label="📧 Download Policies WITH Email",
                    data=zip_data,
                    file_name="policies_with_email.zip",
                    mime="application/zip",
                    key="download_with_email"
                )
        
        with col2:
            if results['without_email'] > 0:
                zip_data = create_download_zip("policies_without_email", "policies_without_email.zip")
                st.download_button(
                    label="❓ Download Policies WITHOUT Email",
                    data=zip_data,
                    file_name="policies_without_email.zip",
                    mime="application/zip",
                    key="download_without_email"
                )
        

        

        
        # Reset button
        st.markdown("---")
        if st.button("🔄 Start Over", key="reset_btn"):
            # Clear session state
            st.session_state.results = None
            st.session_state.processing_done = False
            st.experimental_rerun()
    
    elif pdf_file and excel_file:
        st.info("👆 Click 'Process Files' to extract policies")
    else:
        st.info("👆 Please upload both PDF and Excel files to begin processing")
    
    # Email Management Section
    if st.session_state.processing_done and st.session_state.results:
        st.markdown("---")
        st.header("📧 Email Management")
        
        # Check if we have the necessary files for email sending
        excel_file_exists = check_excel_file_exists()
        pdf_files_exist = check_pdf_files_exist()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Email Readiness Check")
            if excel_file_exists:
                st.success("✅ Excel file with email addresses found")
            else:
                st.error("❌ Excel file not found")
            
            if pdf_files_exist:
                st.success(f"✅ {pdf_files_exist} PDF files ready for sending")
            else:
                st.error("❌ No PDF files found")
        
        with col2:
            st.subheader("🚀 Send Emails")
            if excel_file_exists and pdf_files_exist:
                if st.button("📧 Send Emails Now", type="primary", use_container_width=True):
                    send_emails_via_subprocess()
            else:
                st.button("📧 Send Emails Now", disabled=True, use_container_width=True)
                st.caption("⚠️ Upload and process files first")
        
        # PDF Merging Section for Printing
        st.markdown("---")
        st.header("🖨️ PDF Merging for Printing")
        
        # Check if we have PDFs without email addresses
        pdf_without_email_count = check_pdf_files_without_email()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Printing Readiness Check")
            if pdf_without_email_count > 0:
                st.success(f"✅ {pdf_without_email_count} PDFs ready for printing")
                st.info("💡 These are policies without email addresses that need to be printed and mailed manually.")
            else:
                st.info("ℹ️ No PDFs without email addresses found")
        
        with col2:
            st.subheader("🔗 Merge PDFs")
            if pdf_without_email_count > 0:
                if st.button("🖨️ Create Printable PDF", type="secondary", use_container_width=True):
                    merge_pdfs_for_printing()
            else:
                st.button("🖨️ Create Printable PDF", disabled=True, use_container_width=True)
                st.caption("⚠️ No PDFs without email addresses to merge")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>PDF Policy Processor v1.0 | Built with Streamlit</p>
        <p>Complete workflow: Upload → Process → Send Emails</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()