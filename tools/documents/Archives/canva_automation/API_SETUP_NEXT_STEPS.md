## Canva Integration Setup Instructions

### Integration Configuration:

**Basic Info:**
- Name: `HKBU LANG2077 Automation`
- Description: `Automated slide creation for Language Centre courses`

**Scopes (check these boxes):**
- ✅ `profile:read`
- ✅ `design:content:read`  
- ✅ `design:content:write`
- ✅ `design:meta:read`
- ✅ `brandtemplate:content:read`
- ✅ `brandtemplate:meta:read`
- ✅ `asset:read`
- ✅ `asset:write`

**Authentication:**
- Redirect URL: `http://127.0.0.1:3001/oauth/redirect`

### After Creating Integration:

1. Copy the **Client ID** (starts with OC-)
2. Generate and copy the **Client Secret**
3. Run these commands:

```bash
export CANVA_CLIENT_ID="your_client_id_here"
export CANVA_CLIENT_SECRET="your_client_secret_here"
```

4. Test the API:
```bash
python3 test_canva_api.py
```

### Current Status:
- ✅ PowerPoint slides created from your content
- ✅ HKBU branding applied
- ✅ 4 slides with course information
- 🔄 API setup in progress
