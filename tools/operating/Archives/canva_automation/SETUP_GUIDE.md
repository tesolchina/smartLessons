# Canva Connect API Setup Guide for HKBU

This guide walks you through setting up the official Canva Connect API for programmatic slide creation.

## 🚀 Quick Start

### 1. Developer Portal Setup

1. **Visit the Developer Portal**
   ```
   https://www.canva.com/developers/integrations/connect-api
   ```

2. **Create an Integration**
   - Click "Create an integration"
   - Choose "Private integration" (for HKBU internal use)

3. **Configure Integration**
   - **Integration name**: `HKBU Presentation Creator`
   - **Client ID**: Copy this value (you'll need it later)
   - **Generate secret**: Click and save securely

### 2. Required Scopes

Check these permissions in the Developer Portal:

```
✅ profile: Read
✅ design:content: Read and Write
✅ design:meta: Read  
✅ brandtemplate:content: Read
✅ brandtemplate:meta: Read
✅ asset: Read and Write
```

### 3. Authentication Setup

Under "Authentication" → "Add Authentication":

- **URL 1**: `http://127.0.0.1:3001/oauth/redirect`

### 4. Environment Variables

Create a `.env` file or export these variables:

```bash
export CANVA_CLIENT_ID="your_client_id_here"
export CANVA_CLIENT_SECRET="your_client_secret_here"
```

## 📋 Usage Examples

### Install Dependencies

```bash
pip install requests
```

### Basic Usage

```python
from canva_connect_cli import CanvaConnectCLI

# Initialize client
canva = CanvaConnectCLI()

# Authenticate (opens browser)
canva.authenticate()

# Create blank presentation
design_id = canva.create_blank_design(
    design_type="presentation",
    title="LANG 2077 Academic Presentation"
)

# List available templates
templates = canva.list_brand_templates()
for template in templates[:5]:
    print(f"Template: {template['name']} (ID: {template['id']})")

# Upload an image asset
asset_id = canva.upload_asset("hkbu_logo.png", "HKBU Logo")

# Create from template with autofill
autofill_data = {
    'title': {
        'type': 'text',
        'text': 'LANG 2077: Academic Presentation Skills'
    },
    'subtitle': {
        'type': 'text', 
        'text': 'Hong Kong Baptist University'
    },
    'logo': {
        'type': 'image',
        'asset_id': asset_id
    }
}

design_id = canva.create_design_autofill(
    template_id="BAExxxxx",  # Your template ID
    data=autofill_data,
    title="HKBU LANG2077 Presentation"
)

# Export design
urls = canva.export_design(design_id, "PDF")
for url in urls:
    print(f"Download: {url}")
```

### Command Line Interface

```bash
python canva_connect_cli.py
```

This launches an interactive CLI with these options:

1. **List Brand Templates** - Browse available templates
2. **Create Blank Presentation** - Start from scratch
3. **Create From Template** - Use autofill with templates
4. **Upload Asset** - Add images/logos
5. **Export Design** - Download as PDF/JPG/PNG
6. **View Design Info** - Get design metadata

## 🎯 API Capabilities

### Design Creation
- ✅ Create blank designs (presentations, social media, documents)
- ✅ Create from brand templates with autofill
- ✅ Upload and manage assets (images, logos)

### Brand Templates
- ✅ List available templates
- ✅ Get template data field definitions
- ✅ Autofill templates with custom content

### Asset Management
- ✅ Upload images, logos, documents
- ✅ Organize assets with tags
- ✅ Base64 encoding for file names

### Export & Sharing
- ✅ Export as PDF, JPG, PNG
- ✅ Get shareable URLs
- ✅ Download generated designs

## 🔧 Advanced Features

### Batch Processing

```python
# Create multiple presentations from data
presentations_data = [
    {"title": "Week 1: Introduction", "content": "..."},
    {"title": "Week 2: Research Methods", "content": "..."},
    {"title": "Week 3: Data Analysis", "content": "..."}
]

for data in presentations_data:
    design_id = canva.create_design_autofill(
        template_id="BAExxxxx",
        data={
            'title': {'type': 'text', 'text': data['title']},
            'content': {'type': 'text', 'text': data['content']}
        },
        title=data['title']
    )
    
    # Export immediately
    urls = canva.export_design(design_id, "PDF")
    print(f"Created: {data['title']} -> {urls[0]}")
```

### Custom HKBU Branding

```python
# HKBU brand configuration is built into the CLI
hkbu_colors = canva.hkbu_config['brand_colors']
# {
#     'primary': '#8B0000',    # Deep Red
#     'secondary': '#FFD700',  # Gold
#     'accent': '#2E8B57',     # Sea Green
# }

# Use in template data
brand_data = {
    'university_name': {
        'type': 'text',
        'text': canva.hkbu_config['university_info']['name']
    },
    'department': {
        'type': 'text',
        'text': canva.hkbu_config['university_info']['department']
    }
}
```

## 🚨 Important Notes

### Enterprise Features
- **Brand templates** require Canva for Enterprise
- **Autofill functionality** needs Enterprise subscription
- Individual accounts have limited API access

### Rate Limits
- API has rate limiting (check response headers)
- Use polling for async operations (autofill, export)
- Implement exponential backoff for retries

### Authentication
- OAuth tokens expire and need refresh
- Store refresh tokens securely
- Re-authenticate when tokens expire

## 📚 API Reference

Based on the official Canva Connect API:

- **Base URL**: `https://api.canva.com/v1`
- **Authentication**: OAuth 2.0 Bearer tokens
- **Documentation**: https://www.canva.dev/docs/connect/

### Key Endpoints

```
POST /oauth/token                    # Get access tokens
GET  /users/me                      # User profile
GET  /brand-templates               # List templates
GET  /brand-templates/{id}/dataset  # Template fields
POST /designs                       # Create blank design
POST /autofills                     # Create from template
GET  /autofills/{jobId}            # Check autofill status
POST /asset-uploads                 # Upload assets
POST /exports                       # Export design
GET  /exports/{jobId}              # Check export status
```

## 🔗 Next Steps

1. **Set up Developer Portal account**
2. **Configure OAuth integration**
3. **Test with sample templates**
4. **Create HKBU brand templates**
5. **Integrate into presentation workflows**

## 🆘 Troubleshooting

### Common Issues

**400 Bad Request**
- Check client ID and secret
- Verify redirect URL matches exactly
- Ensure required scopes are enabled

**403 Forbidden** 
- Template requires Enterprise account
- User not in Enterprise organization
- Missing required permissions

**Rate Limited**
- Wait for rate limit reset
- Implement exponential backoff
- Use batch operations when possible

### Support Resources

- **Developer Portal**: https://www.canva.com/developers/
- **API Docs**: https://www.canva.dev/docs/connect/
- **GitHub Examples**: https://github.com/canva-sdks/canva-connect-api-starter-kit
