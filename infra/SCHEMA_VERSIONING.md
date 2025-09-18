# Schema Versioning & Admin Management

This document explains how the Dock2Gdansk infrastructure supports complete schema versioning and admin management.

## ✅ **Admin Schema Management Features**

### **1. 🔐 Admin Authentication**

- Cognito User Pool with admin group
- JWT token-based authentication for all admin endpoints
- Protected `/kapitanat/*` routes

### **2. 📊 Version Control System**

- **Semantic Versioning**: `major.minor.patch` (e.g., 1.2.3)
- **Auto-incrementing**: Admin creates new versions, system handles numbering
- **Active/Inactive**: Control which versions are available
- **Audit Trail**: Track creation dates, descriptions, and changes

### **3. 📝 Form Submission Tracking**

- **Schema Version**: Every submission records which schema was used
- **Form ID**: Track which form type was submitted
- **Timestamp**: When submission occurred
- **Auto-detection**: If frontend doesn't specify version, backend fetches current latest

## 🚀 **Admin Workflow**

### **Creating New Schema Versions**

```javascript
// Admin creates new version
POST /kapitanat/schemas
{
  "formId": "dock2gdansk-main",
  "description": "Added delivery date field",
  "schema": {
    "title": "Updated Form",
    "fields": [...]
  }
}
// → Creates version 1.1.0 automatically
```

### **Managing Existing Versions**

```javascript
// List all schemas and versions
GET /kapitanat/schemas

// Get versions for specific form
GET /kapitanat/schemas?formId=dock2gdansk-main

// Update version (activate/deactivate, change description)
PUT /kapitanat/schemas
{
  "formId": "dock2gdansk-main",
  "version": "1.0.0",
  "isActive": false,
  "description": "Deprecated version"
}

// Delete version (if not last active)
DELETE /kapitanat/schemas?formId=dock2gdansk-main&version=1.0.0
```

### **Cargo Types Management**

```javascript
// Admin can dynamically update cargo types
POST /kapitanat/cargo-types
{
  "name": "Dangerous Goods"
}
// → Gets next ID (114, 115, etc.)

// Update cargo type
PUT /kapitanat/cargo-types
{
  "id": "114",
  "name": "Hazardous Materials",
  "active": true
}
```

## 📋 **Form Submission with Version Tracking**

### **Frontend Integration**

```javascript
// Option 1: Let backend auto-detect latest version
const response = await fetch('/submit-form', {
  method: 'POST',
  body: JSON.stringify({
    formData: { ... },
    userEmail: 'user@example.com'
    // schemaVersion will be auto-detected
  })
});

// Option 2: Explicitly specify schema version
const response = await fetch('/submit-form', {
  method: 'POST',
  body: JSON.stringify({
    formData: { ... },
    userEmail: 'user@example.com',
    formId: 'dock2gdansk-main',
    schemaVersion: '1.2.0'  // Use specific version
  })
});

// Response includes version info
const result = await response.json();
// {
//   "success": true,
//   "submissionId": "uuid",
//   "formId": "dock2gdansk-main",
//   "schemaVersion": "1.2.0",
//   "timestamp": "2024-01-01T12:00:00Z"
// }
```

### **Submission Data Structure**

```json
{
  "id": "submission-uuid",
  "timestamp": "2024-01-01T12:00:00Z",
  "formId": "dock2gdansk-main",
  "schemaVersion": "1.2.0",
  "userEmail": "user@example.com",
  "formData": {
    "company": "ABC Logistics",
    "email": "contact@abc.com",
    "cargo_type": "100",
    ...
  },
  "status": "submitted",
  "submittedAt": "2024-01-01T12:00:00Z"
}
```

## 🎯 **Key Benefits**

### **For Admins:**

1. **Easy Form Updates**: Change forms without code deployment
2. **Version Control**: Track what changed and when
3. **A/B Testing**: Deploy multiple versions simultaneously
4. **Rollback**: Deactivate problematic versions instantly
5. **Audit Trail**: See complete history of form changes

### **For Data Analysis:**

1. **Version Tracking**: Know which form version generated each submission
2. **Migration Planning**: Understand impact of form changes
3. **Historical Analysis**: Compare data across form versions
4. **Quality Control**: Identify issues with specific versions

### **For Users:**

1. **Seamless Experience**: Always get latest active form
2. **Consistency**: Forms work even during admin updates
3. **No Downtime**: Updates happen without service interruption

## 🔄 **Version Management Rules**

### **Version Number Generation:**

- **New Form**: Starts at `1.0.0`
- **Minor Update**: `1.0.0` → `1.1.0` (new fields, changes)
- **Patch Update**: `1.1.0` → `1.1.1` (copy from existing with minor fixes)
- **Major Update**: Manual increment when significant changes

### **Protection Rules:**

- ✅ Can create unlimited versions
- ✅ Can deactivate versions (sets `isActive: false`)
- ✅ Can update descriptions and metadata
- ❌ Cannot delete last active version
- ❌ Cannot delete versions with submissions (future enhancement)

### **Schema Inheritance:**

- New versions can copy from existing versions
- Cargo types are global config (shared across all forms)
- Form-specific settings maintained per version

## 📊 **Admin Dashboard Views**

### **Schema Management Panel:**

- List all forms and their versions
- See active/inactive status
- View creation dates and descriptions
- Quick actions: activate, deactivate, create new version

### **Submission Analytics:**

- Group submissions by schema version
- Show version adoption rates
- Identify popular/problematic versions
- Export data with version information

### **Cargo Types Management:**

- Add/edit/disable cargo types
- See usage statistics per type
- Bulk operations for updates

This comprehensive system ensures that admins have full control over form schemas while maintaining complete audit trails and version tracking for all submissions.
