# 🚀 PDF Policy Processor - Deployment Guide

## 📋 Files Ready for Deployment

Your project is now ready for public hosting with these files:

- ✅ `pdf_processor_final_working.py` - Main application (production-ready)
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Heroku configuration
- ✅ `runtime.txt` - Python version
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `.streamlit/secrets.toml` - API credentials (keep secure!)

## 🌐 Deployment Options

### 1. **Streamlit Community Cloud (RECOMMENDED - FREE)**

**Steps:**
1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/pdf-policy-processor.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Connect your GitHub repository
   - Set main file: `pdf_processor_final_working.py`
   - Add secrets in the dashboard (copy from `.streamlit/secrets.toml`)

3. **Configure Secrets**
   - In Streamlit Cloud dashboard, go to "Secrets"
   - Copy content from `.streamlit/secrets.toml`
   - Paste and save

**Pros:** ✅ Free, ✅ Easy, ✅ Official, ✅ Auto-updates from GitHub
**Cons:** ❌ Public repos only, ❌ Limited resources

### 2. **Heroku (POPULAR)**

**Steps:**
1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set BREVO_API_KEY="your-brevo-api-key-here"
   heroku config:set SENDER_EMAIL="CashBack@niclmauritius.site"
   heroku config:set SENDER_NAME="NIC Life Insurance Mauritius"
   heroku config:set REPLY_TO_EMAIL="nicarlife@nicl.mu"
   ```

**Pros:** ✅ Reliable, ✅ Scalable, ✅ Good documentation
**Cons:** ❌ No free tier anymore, ❌ Costs $7/month minimum

### 3. **Railway (MODERN & FAST)**

**Steps:**
1. **Go to** https://railway.app
2. **Connect GitHub repository**
3. **Deploy automatically**
4. **Set environment variables in dashboard**

**Pros:** ✅ Fast, ✅ Modern, ✅ Good free tier, ✅ Easy scaling
**Cons:** ❌ Newer platform

### 4. **Render (GOOD FREE TIER)**

**Steps:**
1. **Go to** https://render.com
2. **Connect GitHub repository**
3. **Choose "Web Service"**
4. **Set build command:** `pip install -r requirements.txt`
5. **Set start command:** `streamlit run pdf_processor_final_working.py --server.port=$PORT --server.address=0.0.0.0`

**Pros:** ✅ Good free tier, ✅ Easy setup, ✅ Reliable
**Cons:** ❌ Free tier has limitations

## 🔒 Security Considerations

### **Environment Variables**
Never commit API keys to GitHub. Use:
- **Local Development:** Set environment variables
  - Windows: Run `set_api_key.bat` or `set BREVO_API_KEY=your-key`
  - Linux/Mac: `export BREVO_API_KEY=your-key`
- **Streamlit Cloud:** Secrets management in dashboard
- **Heroku:** `heroku config:set`
- **Railway/Render:** Environment variables in dashboard

### **File Upload Limits**
- **Streamlit Cloud:** 200MB max
- **Heroku:** 500MB max
- **Railway:** 1GB max

### **Processing Time Limits**
- **Free tiers:** Usually 30-60 seconds max
- **Paid tiers:** Longer processing allowed

## 📊 Recommended Setup for Your Use Case

**For PDF Policy Processor, I recommend:**

### **Option 1: Streamlit Community Cloud (Best for testing)**
- ✅ Free
- ✅ Easy setup
- ✅ Perfect for your app size
- ❌ Public repository required

### **Option 2: Railway (Best for production)**
- ✅ Good free tier (500 hours/month)
- ✅ Private repositories supported
- ✅ Fast deployment
- ✅ Easy scaling

## 🚀 Quick Start - Streamlit Cloud

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "PDF Policy Processor"
   git remote add origin https://github.com/yourusername/pdf-policy-processor.git
   git push -u origin main
   ```

2. **Deploy:**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your repository
   - Main file: `pdf_processor_final_working.py`
   - Click "Deploy"

3. **Add Secrets:**
   - In app dashboard, click "Secrets"
   - Copy from `.streamlit/secrets.toml`
   - Save

4. **Your app will be live at:**
   `https://yourusername-pdf-policy-processor-pdf-processor-deploy-xyz123.streamlit.app`

## 🔧 Troubleshooting

### **Common Issues:**

1. **"Module not found"**
   - Check `requirements.txt` has all dependencies
   - Ensure correct versions

2. **"Secrets not found"**
   - Add secrets in hosting platform dashboard
   - Check secret names match exactly

3. **"File upload too large"**
   - Compress PDF files
   - Split large files
   - Use paid tier for larger limits

4. **"App timeout"**
   - Optimize processing code
   - Use paid tier for longer timeouts
   - Process files in smaller batches

## 📞 Support

If you need help with deployment:
1. Check hosting platform documentation
2. Review error logs in dashboard
3. Test locally first with `streamlit run pdf_processor_final_working.py`

## 🎉 Success!

Once deployed, your PDF Policy Processor will be accessible worldwide at your custom URL!

Users can:
- ✅ Upload PDF and Excel files
- ✅ Process policies automatically
- ✅ Send emails with live monitoring
- ✅ Track Brevo credits in real-time

**Your app is now ready for the world! 🌍**