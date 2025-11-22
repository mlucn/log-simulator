# Google Workspace Activity Log Schemas

Application-specific schemas for generating Google Workspace Activity logs compatible with **Google SecOps Chronicle** WORKSPACE_ACTIVITY parser.

## Overview

These schemas generate logs in the format expected by:
- **Google SecOps Chronicle** WORKSPACE_ACTIVITY log type
- **Google Workspace Admin SDK Reports API v1**
- Chronicle's **Unified Data Model (UDM)** parser

All schemas follow the standard Google Workspace Activity log structure with `kind`, `id`, `actor`, `ipAddress`, and `events` fields.

## Available Schemas

| Schema | Application | Event Categories | Use Cases |
|--------|-------------|------------------|-----------|
| **admin.yaml** | Admin Console | User management, group management, domain settings, security settings, Chrome OS, mobile devices | User provisioning, access control changes, policy modifications |
| **drive.yaml** | Google Drive | File access, creation, editing, deletion, sharing, permissions | Data loss prevention, insider threat detection, file sharing monitoring |
| **login.yaml** | Authentication | Login success/failure, 2FA, password changes, suspicious activity | Authentication monitoring, brute force detection, account compromise |
| **calendar.yaml** | Google Calendar | Calendar/event creation, modifications, ACL changes, resource management | Meeting activity monitoring, calendar sharing, resource booking |
| **token.yaml** | OAuth Tokens | Token authorization, revocation, scope changes | Third-party app access monitoring, OAuth abuse detection |

## Schema Structure

All schemas include:

```yaml
schema_version: "1.0"
log_type: "WORKSPACE_ACTIVITY"           # Chronicle log type identifier
source_api: "Google Workspace Admin SDK Reports API v1"
application_name: "admin|drive|login|calendar|token"
chronicle_compatible: true
```

## Event Organization

Events are organized in a three-level hierarchy:

1. **Application Name** (schema file): `admin`, `drive`, `login`, `calendar`, `token`
2. **Event Type** (category): `user_settings`, `access`, `login`, `calendar_change`, `authorize`
3. **Event Name** (specific action): `create_user`, `view`, `login_success`, `create_event`, `authorize`

### Example Event Types by Application

**Admin (`admin.yaml`)**
- `user_settings`: create_user, delete_user, suspend_user, change_password
- `group_settings`: create_group, add_group_member, change_group_setting
- `domain_settings`: add_domain_alias, change_domain_name
- `security_settings`: change_2sv_settings, change_password_policy
- `chrome_os_settings`: enroll_chrome_os_device, disable_chrome_os_device
- `mobile_settings`: approve_mobile_device, block_mobile_device

**Drive (`drive.yaml`)**
- `access`: view, preview, print, download
- `create`: create, upload, copy
- `edit`: edit, rename
- `delete`: delete, trash, untrash
- `acl_change`: user_access_grant, user_access_revoke, change_document_visibility
- `move`: add_to_folder, remove_from_folder
- `approval`: approval_request_sent, approval_granted, approval_denied

**Login (`login.yaml`)**
- `login`: login_success, login_failure, login_verification
- `logout`: logout
- `account_warning`: account_disabled_password_leak, account_disabled_hijacked
- `suspicious_login`: suspicious_login
- `2sv_change`: 2sv_enroll, 2sv_disable
- `password_edit`: password_edit
- `recovery_email_edit`: recovery_email_edit

**Calendar (`calendar.yaml`)**
- `calendar_change`: create_calendar, delete_calendar, change_calendar_acls
- `event_change`: create_event, delete_event, add_event_guest, change_event_response
- `resource_change`: create_resource, delete_resource

**Token (`token.yaml`)**
- `authorize`: authorize (with various scopes)
- `revoke`: revoke
- `admin_revoke`: admin_revoke, admin_revoke_all
- `token_refresh`: token_refresh

## Usage

### Basic Usage

```python
from log_simulator.generators.schema_generator import SchemaBasedGenerator

# Initialize with specific application schema
generator = SchemaBasedGenerator(
    'src/log_simulator/schemas/cloud_identity/google_workspace/drive.yaml'
)

# List available scenarios
print(generator.list_scenarios())

# Generate logs with a specific scenario
logs = generator.generate(count=10, scenario='file_share_external')

# Generate logs with time spread
logs = generator.generate(
    count=100,
    scenario='file_view',
    time_spread_seconds=3600  # 1 hour
)
```

### Example: Admin User Management

```python
# Admin console - create users
admin_gen = SchemaBasedGenerator(
    'src/log_simulator/schemas/cloud_identity/google_workspace/admin.yaml'
)

# Generate user creation events
logs = admin_gen.generate(count=5, scenario='user_create')

# Generate admin privilege grants
logs = admin_gen.generate(count=3, scenario='grant_admin_privilege')
```

### Example: Drive File Sharing Monitoring

```python
# Drive - file sharing activity
drive_gen = SchemaBasedGenerator(
    'src/log_simulator/schemas/cloud_identity/google_workspace/drive.yaml'
)

# External sharing events (DLP use case)
external_shares = drive_gen.generate(count=20, scenario='file_share_external')

# Public sharing events (security risk)
public_shares = drive_gen.generate(count=5, scenario='file_share_public')
```

### Example: Login Activity Monitoring

```python
# Login - authentication monitoring
login_gen = SchemaBasedGenerator(
    'src/log_simulator/schemas/cloud_identity/google_workspace/login.yaml'
)

# Successful logins with 2FA
successful_logins = login_gen.generate(count=100, scenario='login_success_with_2fa')

# Failed login attempts (brute force detection)
failed_logins = login_gen.generate(count=50, scenario='login_failure')

# Suspicious login activity
suspicious = login_gen.generate(count=10, scenario='suspicious_login_blocked')
```

### Example: OAuth Token Monitoring

```python
# Token - third-party app access
token_gen = SchemaBasedGenerator(
    'src/log_simulator/schemas/cloud_identity/google_workspace/token.yaml'
)

# App authorizations
authorizations = token_gen.generate(count=30, scenario='authorize_3p_app')

# Admin revocations (security incident)
revocations = token_gen.generate(count=5, scenario='admin_revoke_user_tokens')
```

## Scenarios Available

Each schema contains 10-30+ pre-defined scenarios. Use `generator.list_scenarios()` to see all available scenarios for a schema.

### Common Scenarios per Application

**Admin**: user_create, user_delete, user_suspend, grant_admin_privilege, add_group_member, change_2sv_settings, etc.

**Drive**: file_view, file_download, file_create, file_share_with_user, file_share_external, file_share_public, etc.

**Login**: login_success, login_success_with_2fa, login_failure, suspicious_login, password_edit, 2sv_enroll, etc.

**Calendar**: calendar_create, event_create, event_edit, add_event_guest, event_response_accept, etc.

**Token**: authorize_3p_app, authorize_gmail_access, revoke_3p_app, admin_revoke_user_tokens, etc.

## Chronicle Compatibility

These schemas are designed to be directly ingestible by Google SecOps Chronicle:

1. **log_type**: Set to `WORKSPACE_ACTIVITY` (Chronicle's parser identifier)
2. **Field Structure**: Matches Google Workspace Admin SDK Reports API v1 format
3. **UDM Mapping**: Fields map to Chronicle's Unified Data Model
4. **Event Types**: Use official Google Workspace event type and event name values

## Testing with Chronicle

To test these logs with Chronicle:

1. Generate logs using the schemas
2. Configure Chronicle ingestion with `WORKSPACE_ACTIVITY` log type
3. Ingest the generated logs
4. Verify UDM field mapping in Chronicle UI
5. Test detection rules against the generated data

## Integration with Google SecOps Use Cases

### Data Loss Prevention (DLP)
- Monitor external file sharing: `drive.yaml` → `file_share_external`
- Track public file access: `drive.yaml` → `file_share_public`
- Detect mass downloads: `drive.yaml` → `file_download`

### Insider Threat Detection
- Track admin privilege escalation: `admin.yaml` → `grant_admin_privilege`
- Monitor user suspensions: `admin.yaml` → `user_suspend`
- File access anomalies: `drive.yaml` → `file_view`

### Authentication Security
- Brute force detection: `login.yaml` → `login_failure`
- Suspicious login patterns: `login.yaml` → `suspicious_login`
- Account compromise indicators: `login.yaml` → `account_disabled_hijacked`

### Third-Party App Risk
- OAuth abuse: `token.yaml` → `authorize_3p_app`
- Risky app permissions: `token.yaml` → `scope_expansion`
- Mass revocations: `token.yaml` → `admin_revoke_all_tokens`

## References

- [Google SecOps Chronicle - Collect Google Workspace logs](https://cloud.google.com/chronicle/docs/ingestion/default-parsers/collect-workspace-logs)
- [Google Workspace Admin SDK Reports API v1](https://developers.google.com/admin-sdk/reports/reference/rest/v1/activities)
- [Google Cloud Chronicle Documentation](https://cloud.google.com/chronicle/docs)

## Schema Version

Current version: **1.0**

All schemas follow the same versioning and are updated together to maintain compatibility.

---

**Last Updated**: 2025-11-22
**Chronicle Compatibility**: Tested with Google SecOps Chronicle WORKSPACE_ACTIVITY parser
**Total Event Scenarios**: 100+ across all applications
