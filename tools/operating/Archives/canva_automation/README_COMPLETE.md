# HKBU Canva Automation Suite

Complete toolkit for programmatic slide creation for Hong Kong Baptist University Language Centre.

## 🎯 Available Solutions

### 1. **Official Canva Connect API** ⭐ *RECOMMENDED*
- **File**: `canva_connect_cli.py`
- **Status**: ✅ Production ready
- **Requirements**: Canva Developer Portal integration
- **Features**: Official API access, brand templates, enterprise features

### 2. **PowerPoint CLI** 
- **File**: `powerpoint_cli.py`
- **Status**: ✅ Working
- **Requirements**: python-pptx library
- **Features**: Native .pptx generation, HKBU branding

### 3. **HTML Slide Generator**
- **File**: `academic_slide_generator.py`
- **Status**: ✅ Working
- **Requirements**: Browser for viewing
- **Features**: Web-based presentations, responsive design

### 4. **Browser Automation** 
- **File**: `canva_direct_creator.py`
- **Status**: ⚠️ Chrome driver issues
- **Requirements**: Selenium, Chrome WebDriver
- **Features**: Direct Canva manipulation

## 🚀 Quick Start - Official API

### Setup

1. **Developer Portal Registration**
   ```bash
   # Visit: https://www.canva.com/developers/integrations/connect-api
   # Create integration with required scopes
   ```

2. **Environment Configuration**
   ```bash
   export CANVA_CLIENT_ID="your_client_id_here"
   export CANVA_CLIENT_SECRET="your_client_secret_here"
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the API**
   ```bash
   python test_canva_api.py
   ```

5. **Interactive CLI**
   ```bash
   python canva_connect_cli.py
   ```

### Usage Examples

```python
from canva_connect_cli import CanvaConnectCLI

# Initialize and authenticate
canva = CanvaConnectCLI()
canva.authenticate()  # Opens browser for OAuth

# Create blank presentation
design_id = canva.create_blank_design(
    design_type="presentation",
    title="LANG 2077: Academic Presentation Skills"
)

# List templates (requires Enterprise)
templates = canva.list_brand_templates()

# Create from template with autofill
autofill_data = {
    'title': {'type': 'text', 'text': 'HKBU LANG 2077'},
    'subtitle': {'type': 'text', 'text': 'Academic Presentation Skills'},
    'presenter': {'type': 'text', 'text': 'Language Centre'}
}

design_id = canva.create_design_autofill(
    template_id="BAExxxxx",
    data=autofill_data,
    title="HKBU Presentation"
)

# Export as PDF
urls = canva.export_design(design_id, "PDF")
print(f"Download: {urls[0]}")
```

## 📊 Feature Comparison

| Feature | Canva API | PowerPoint | HTML Generator | Browser Automation |
|---------|-----------|------------|----------------|-------------------|
| **Official Support** | ✅ | ✅ | ✅ | ❌ |
| **No GUI Required** | ✅ | ✅ | ✅ | ❌ |
| **Brand Templates** | ✅ | ❌ | ❌ | ✅ |
| **Asset Management** | ✅ | ❌ | ❌ | ✅ |
| **Export Formats** | PDF/JPG/PNG | PPTX | HTML | Various |
| **Setup Complexity** | Medium | Low | Low | High |
| **Enterprise Features** | ✅ | ❌ | ❌ | ✅ |
| **Reliability** | High | High | High | Low |

## 🎯 Recommended Workflow

### For Individual Use
1. Start with **PowerPoint CLI** for quick presentations
2. Use **HTML Generator** for web-based sharing
3. Upgrade to **Canva API** when ready for advanced features

### For Enterprise Use
1. Set up **Canva Connect API** with Developer Portal
2. Create HKBU brand templates in Canva
3. Use API for programmatic generation at scale

## 📁 File Structure

```
canva_automation/
├── canva_connect_cli.py      # Official Canva Connect API client ⭐
├── test_canva_api.py         # API testing and demo script
├── powerpoint_cli.py         # Native PowerPoint generation
├── academic_slide_generator.py # HTML presentation generator
├── canva_direct_creator.py   # Browser automation (deprecated)
├── canva_quick_creator.py    # Manual guidance system
├── requirements.txt          # Python dependencies
├── SETUP_GUIDE.md           # Detailed API setup instructions
└── README.md               # This file
```

## 🔧 Advanced Configuration

### HKBU Branding
All tools include HKBU brand configuration:

```python
hkbu_config = {
    "brand_colors": {
        "primary": "#8B0000",      # Deep Red
        "secondary": "#FFD700",    # Gold
        "accent": "#2E8B57",       # Sea Green
    },
    "university_info": {
        "name": "Hong Kong Baptist University",
        "department": "Language Centre",
        "website": "https://www.hkbu.edu.hk"
    }
}
```

### Batch Processing
Process multiple presentations:

```python
presentations = [
    {"title": "Week 1: Introduction", "content": "..."},
    {"title": "Week 2: Methods", "content": "..."},
    {"title": "Week 3: Analysis", "content": "..."}
]

for data in presentations:
    design_id = canva.create_design_autofill(template_id, data)
    urls = canva.export_design(design_id, "PDF")
    print(f"Created: {data['title']} -> {urls[0]}")
```

## 🚨 Important Notes

### API Limitations
- **Brand templates** require Canva for Enterprise
- **Free accounts** have limited API access
- **Rate limits** apply to all endpoints

### Authentication
- OAuth tokens expire and need refresh
- Store tokens securely for automation
- Re-authenticate when tokens expire

### Browser Automation Issues
- Chrome WebDriver has compatibility problems
- Selenium approach not recommended for production
- Use official API instead

## 📚 API Documentation

- **Canva Connect API**: https://www.canva.dev/docs/connect/
- **Developer Portal**: https://www.canva.com/developers/
- **GitHub Examples**: https://github.com/canva-sdks/canva-connect-api-starter-kit

## 🆘 Troubleshooting

### Common Issues

**"400 Bad Request" on API calls**
- Check client ID and secret are correct
- Verify redirect URL matches Developer Portal
- Ensure all required scopes are enabled

**"No templates found"**
- Templates require Canva for Enterprise account
- Check if user is in Enterprise organization
- Verify `brandtemplate:*` scopes are enabled

**Chrome WebDriver errors**
- Use official API instead of browser automation
- WebDriver approach is deprecated due to compatibility issues

### Getting Help

1. Check the `SETUP_GUIDE.md` for detailed instructions
2. Run `python test_canva_api.py` to diagnose issues
3. Verify environment variables are set correctly
4. Check Canva Developer Portal integration settings

## 🎓 HKBU Integration

This toolkit is specifically designed for HKBU Language Centre's LANG 2077 course and similar academic presentation needs. All tools include:

- HKBU brand colors and typography
- Academic presentation templates
- Course-specific content structures
- Collaboration features for team projects

Ready to create professional presentations programmatically! 🚀
