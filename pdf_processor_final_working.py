import streamlit as st
import pandas as pd
import PyPDF2
import re
import os
import zipfile
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

def merge_pdfs_streamlit():
    """Streamlit interface for PDF merging"""
    
    st.subheader("🖨️ Merge PDFs for Printing")
    
    # Check if folder exists
    if not Path("policies_without_email").exists():
        st.warning("❌ No 'policies_without_email' folder found.")
        return
    
    # Count PDFs
    pdf_files = list(Path("policies_without_email").glob("*.pdf"))
    
    if not pdf_files:
        st.info("✅ No policies without email found. All policies have email addresses!")
        return
    
    st.info(f"📁 Found {len(pdf_files)} policies without email addresses")
    st.info("🖨️ These policies need to be printed and distributed manually")
    
    # Show list of policies
    with st.expander("📋 Policies to be merged for printing"):
        for pdf_file in sorted(pdf_files):
            st.write(f"• {pdf_file.stem}")
    
    # Merge button
    if st.button("🖨️ Merge PDFs for Printing", type="primary"):
        st.info("🔄 Use the command line to merge PDFs for printing:")
        st.code("python merge_final.py", language="bash")
        
        # Check if merged file already exists
        if os.path.exists("policies_for_printing.pdf"):
            st.success("✅ Found existing merged PDF file!")
            with open("policies_for_printing.pdf", "rb") as file:
                st.download_button(
                    label="📥 Download Existing Merged PDF",
                    data=file.read(),
                    file_name="policies_for_printing.pdf",
                    mime="application/pdf",
                    key="download_existing_printing_pdf"
                )



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
        
        # Email sending section - NO SUBPROCESS, JUST INSTRUCTIONS
        if results['with_email'] > 0:
            st.markdown("---")
            st.subheader("📧 Email Sending")
            
            st.info(f"📊 {results['with_email']} policies are ready for email sending")
            st.info("📧 Sender: cremur9@gmail.com (NIC Mauritius)")
            
            # Show instructions instead of trying to run subprocess
            st.markdown("### 🚀 To Send Emails:")
            st.markdown("**Step 1:** Open a new command prompt/terminal")
            st.markdown("**Step 2:** Navigate to this folder")
            st.markdown("**Step 3:** Run the email script:")
            
            st.code("python send_emails_brevo.py", language="bash")
            
            st.success("✅ All policy files are ready in the 'policies_with_email' folder")
        
        # PDF Merging for Printing section
        if results['without_email'] > 0:
            st.markdown("---")
            merge_pdfs_streamlit()
        
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
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>PDF Policy Processor v1.0 | Built with Streamlit</p>
        <p>For email sending, use the command line after processing</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()