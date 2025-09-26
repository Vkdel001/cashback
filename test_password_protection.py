#!/usr/bin/env python3
"""
Test script to verify PDF password protection is working
"""

import PyPDF2
import pandas as pd
from pathlib import Path

def test_password_protection():
    """Test if PDFs are properly password protected"""
    
    print("🔐 Testing PDF Password Protection")
    print("=" * 40)
    
    # Check if we have the Excel file
    excel_file = "Compile CBOpt Nov25.xlsx"
    if not Path(excel_file).exists():
        print(f"❌ Excel file not found: {excel_file}")
        return
    
    # Load Excel data
    try:
        df = pd.read_excel(excel_file)
        print(f"✅ Loaded Excel file with {len(df)} records")
    except Exception as e:
        print(f"❌ Error reading Excel: {e}")
        return
    
    # Check if we have processed PDFs
    pdf_folder = Path("policies_with_email")
    if not pdf_folder.exists():
        print("❌ No processed PDFs found. Run the main processor first.")
        return
    
    pdf_files = list(pdf_folder.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in policies_with_email folder")
        return
    
    print(f"📁 Found {len(pdf_files)} PDF files to test")
    print()
    
    # Test a few PDFs
    test_count = min(3, len(pdf_files))  # Test first 3 PDFs
    
    for i, pdf_file in enumerate(pdf_files[:test_count]):
        print(f"Testing {i+1}/{test_count}: {pdf_file.name}")
        
        # Extract policy number from filename
        filename = pdf_file.stem
        if '_' in filename and not filename.isdigit():
            policy_lookup = filename.replace('_', '/', 1)
        else:
            policy_lookup = filename
        
        # Find NIC for this policy in Excel using column names
        nic_password = None
        for _, row in df.iterrows():
            # Get policy number from 'Policy No' column or first column
            if 'Policy No' in df.columns:
                excel_policy = str(row['Policy No']).strip()
            else:
                excel_policy = str(row.iloc[0]).strip()
            
            # Get NIC from 'NIC' column
            excel_nic = None
            if 'NIC' in df.columns and pd.notna(row['NIC']):
                excel_nic = str(row['NIC']).strip()
            
            # Check if policies match
            if (excel_policy == policy_lookup or 
                excel_policy.replace('/', '') == policy_lookup.replace('/', '') or
                excel_policy.lstrip('0') == policy_lookup.lstrip('0')):
                nic_password = excel_nic
                break
        
        if not nic_password:
            print(f"  ⚠️  No NIC found for policy {policy_lookup}")
            continue
        
        # Test PDF password protection
        try:
            with open(pdf_file, 'rb') as f:
                # Try to read PDF without password
                try:
                    pdf_reader = PyPDF2.PdfReader(f)
                    if pdf_reader.is_encrypted:
                        print(f"  🔐 PDF is encrypted ✅")
                        
                        # Try to decrypt with NIC password
                        if pdf_reader.decrypt(nic_password):
                            print(f"  🔑 Password '{nic_password}' works ✅")
                            
                            # Try to read a page to confirm
                            try:
                                page = pdf_reader.pages[0]
                                text = page.extract_text()
                                if text and len(text) > 10:
                                    print(f"  📄 Content readable after decryption ✅")
                                else:
                                    print(f"  ⚠️  Content seems empty after decryption")
                            except Exception as e:
                                print(f"  ❌ Error reading content: {e}")
                        else:
                            print(f"  ❌ Password '{nic_password}' doesn't work")
                    else:
                        print(f"  ❌ PDF is NOT encrypted!")
                        
                except Exception as e:
                    print(f"  ❌ Error testing PDF: {e}")
                    
        except Exception as e:
            print(f"  ❌ Error opening PDF: {e}")
        
        print()
    
    print("🎯 Password Protection Test Summary:")
    print("- If PDFs show '🔐 PDF is encrypted ✅', password protection is working")
    print("- If passwords work '🔑 Password works ✅', NIC matching is correct")
    print("- If content is readable '📄 Content readable ✅', everything is perfect")
    print()
    print("💡 To test manually:")
    print("1. Try opening a PDF from policies_with_email folder")
    print("2. It should ask for a password")
    print("3. Use the corresponding NIC number from your Excel file")

if __name__ == "__main__":
    test_password_protection()