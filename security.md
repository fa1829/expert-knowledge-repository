# SECURITY

Designed for trusted LAN / private use.
If exposed publicly, add:
- Auth + roles
- HTTPS reverse proxy
- Rate limiting
- Audit logs

Path traversal is blocked using `is_safe_path()`.
Protect admin endpoints with `EKR_ADMIN_TOKEN`.

- Path traversal protected
- Admin reindex protected by token
- Recommended behind Nginx + HTTPS for internet exposure