---
profile: security-expert
purpose: Full taxonomy of application-security concerns. Use as a lens, not a to-do list. The reviewer reads through it and applies what fits the diff and the system surfaces it touches.
---

# Security expert checklist

Superset of security concerns for a typical full-stack application (frontend + backend/API). Read through it, apply judgment:

- Skip categories the diff doesn't touch
- Go deep on categories the diff is centered on
- Look opportunistically at adjacent categories — that's where exposed vulnerabilities live
- Flag gaps where a security control *should* exist for this surface but doesn't

Stack markers: `[H]` frontend, `[P]` backend/API, `[Both]`. (Adapt to your repo's app boundaries.)

## Contents

1. Injection
2. Output encoding & XSS
3. Authentication
4. Session & token handling
5. Authorization (code-level)
6. Authorization at the schema layer (access-control policies)
7. Cryptography
8. Secrets management
9. Sensitive data in transit / at rest / in logs
10. SSRF & outbound HTTP
11. CSRF
12. Open redirect
13. File upload handling
14. Deserialization & prototype pollution
15. Timing attacks & user enumeration
16. Security headers
17. CORS
18. Rate limiting & abuse prevention
19. Error hygiene
20. Dependency supply chain
21. Client-side storage of sensitive data
22. Race conditions & state-integrity attacks

---

## 1. Injection [P]

*"Does any user input reach an interpreter without a parameterized boundary?"*

- SQL — parameterized queries only; no string concatenation, no template-string interpolation of user input into queries
- Command — no `exec` / `spawn` / `eval` with user-controlled fragments
- Template injection — server-rendered templates not fed user input as template source
- LDAP / NoSQL injection where applicable
- Path traversal — user-controlled segments in `fs.read*` / `path.join`

## 2. Output encoding & XSS [H, P-where-rendered]

*"Could user-controlled content execute as code in any consumer's context?"*

- Raw-HTML-injection props in React used only with explicitly sanitized input (DOMPurify or equivalent), never raw user content
- Direct `innerHTML` assignment with user input
- React: `href={userUrl}` without `javascript:` filtering
- HTML emails / server-rendered HTML escape user input at every interpolation point
- Markdown rendering — sanitizer configured to strip script/event-handler attributes
- Template engines configured for auto-escape (don't disable it without a specific reason)

## 3. Authentication [P]

*"Are credentials handled with current best practice?"*

- Password hashing: bcrypt or argon2 only — never MD5, SHA1, plain SHA256
- Sufficient work factor (bcrypt cost ≥ 12, argon2 with parameters tuned)
- No DIY auth where a vetted library would do
- MFA / 2FA paths intact for sensitive accounts
- Account lockout / breach-detection signals
- Password reset flow doesn't leak account existence
- Magic-link / OTP tokens: short-lived, single-use, server-side state

## 4. Session & token handling [Both]

*"Once authenticated, is the session protected against theft, replay, and forgery?"*

- JWT: never `alg: none`; signature verified before trusting any claim; no client-held signing secrets
- JWT issued and verified with the **same** algorithm declared server-side; reject on mismatch
- Session tokens generated with CSPRNG; sufficient entropy
- Token expiry honored; refresh-token rotation; revocation list / session invalidation paths
- Logout actually invalidates server-side state, not just client-side cookie
- Sensitive operations re-prompt or step-up auth (password, OTP) — not "ambient session is enough"

## 5. Authorization (code-level) [P]

*"For every action and resource, is the actor proven to be allowed — server-side?"*

- Every endpoint has an explicit authorization check; "default deny" on missing
- IDOR: actor verified to own / be entitled to the specific resource referenced by ID, not just authenticated
- No `req.user.role === 'admin'` patterns scattered without a centralized check
- Sensitive operations (delete, role change, billing) extra-gated
- Impersonation / "act as" features have audit trail and don't bypass downstream checks
- "Trust the client" patterns (UI hides button → assume user can't trigger action) explicitly absent

## 6. Authorization at the schema layer (access-control policies) [P]

*"Do `@@allow` / `@@deny`-style policies (or your ORM's equivalent) match the real auth intent — neither over-permissive nor over-restrictive?"*

- Policies cover all CRUD operations, not just read
- Cross-tenant isolation enforced in policy, not relying on app-layer filters
- Subject-of-the-action correctly identified (the authenticated principal and its role)
- Policy doesn't trust fields the user can mutate (e.g., `auth().tenantId == this.tenantId` only safe if `tenantId` is server-set)
- Custom auth functions are pure, deterministic, side-effect-free
- Defense in depth: route handler also checks auth, doesn't rely solely on schema policy
- Negative tests exist (cross-tenant access denied, role-elevation denied)

## 7. Cryptography [Both]

*"Is the right primitive being used the right way?"*

- AES-256+ for symmetric, with authenticated mode (GCM, not ECB or unauthenticated CBC)
- Static IV / nonce reuse — never
- TLS 1.2+ in transit; HSTS preload-eligible config
- No DIY crypto; use `crypto` / `tweetnacl` / `libsodium` not hand-rolled
- Random tokens generated with `crypto.randomBytes` / `crypto.getRandomValues`, never `Math.random`
- Constant-time comparison for tokens, MACs, password hashes (`crypto.timingSafeEqual`)
- Key rotation strategy exists for at-rest encryption keys

## 8. Secrets management [Both]

*"Are secrets kept out of every place they shouldn't be?"*

- No secrets in source code (API keys, DB URIs, signing keys, vendor tokens)
- No secrets in `.env*` files committed to git (`.env.example` ok, must be free of real values)
- No secrets in logs (search for token-shaped strings, base64 blobs, JWT-shaped triplets)
- No secrets in error messages returned to clients
- No secrets in frontend bundles (public-env-var policy honored, e.g. framework-prefixed public vars)
- No secrets in client-side state (store, localStorage, URL params)
- Rotation strategy exists; old secrets revoked when rotated
- Service-account keys for external services scoped to minimum role

## 9. Sensitive data in transit / at rest / in logs [Both, privacy-relevant]

*"Where does PII / regulated data appear, and is it protected at every leg?"*

- HTTPS enforced; HTTP redirects use `Strict-Transport-Security`
- PII / regulated data redacted from operational logs (logger, error-tracking, metrics)
- Error-tracking breadcrumbs scrubbed for sensitive data before send
- API responses don't include fields beyond what the consumer needs (no over-fetching that returns sensitive data to wrong actors)
- Database backups encrypted; backup access controlled
- Sensitive fields (government IDs, payment info, regulated identifiers) tagged in schema for audit / export awareness

## 10. SSRF & outbound HTTP [P]

*"Could an attacker make the server fetch a URL they control?"*

- User-controlled URLs in `fetch` / `axios` / `http.get` — validated against allow-list
- No fetching from internal IPs (169.254.169.254, 127.0.0.1, RFC1918 ranges) when input is user-controlled
- Webhook URLs validated; metadata-service IPs blocked
- Redirect-following on user-supplied URLs disabled or controlled

## 11. CSRF [Both]

*"Are state-changing endpoints protected against forged cross-site requests?"*

- State-changing endpoints either use SameSite=Strict cookies, or require an explicit CSRF token, or use a non-cookie auth mechanism (Bearer token)
- Mixing cookie auth and Bearer auth on the same endpoint without CSRF protection
- `SameSite=Lax` is fine for top-level navigation but not for form-POST CSRF
- GET requests don't change state (CSRF is harder to defend if they do)

## 12. Open redirect [Both]

*"Is any redirect target user-controlled without an allow-list?"*

- `?returnTo=` / `?next=` / `?redirect=` params validated against an internal allow-list before `res.redirect`
- Same for client-side navigation reading query params
- Open redirects facilitate phishing — even a "harmless" external redirect is a finding

## 13. File upload handling [Both]

*"Can an uploaded file become an attack vector?"*

- MIME type validated server-side, not just by extension or client-claimed type
- File size limits enforced
- Filename sanitized (path-traversal segments stripped)
- Files stored outside the web root, served with explicit Content-Type and `Content-Disposition: attachment` for non-image types
- Image processing libraries up to date (libvips/sharp/imagemagick CVEs are common)
- Virus scanning where the threat model warrants it

## 14. Deserialization & prototype pollution [Both]

*"Can untrusted input mutate object internals or trigger gadget chains?"*

- `JSON.parse` of attacker-controlled data with a reviver that doesn't allow `__proto__` / `constructor` keys
- `Object.assign` / `lodash.merge` / spread with user-controlled keys — guard against `__proto__`
- `eval`, `Function`, `vm.runInNewContext` with any taint of user input — never
- YAML / XML parsers configured with safe defaults (no anchor expansion bombs, no XXE)

## 15. Timing attacks & user enumeration [Both]

*"Does the response time or content tell an attacker something they shouldn't know?"*

- Login: identical response time and message for "user not found" and "wrong password"
- Password reset: identical response for "email not found" vs "email sent"
- Token comparisons in constant time (`crypto.timingSafeEqual`)
- Cache hit/miss observable by an attacker — leaks user existence

## 16. Security headers [Both]

*"Is the browser given the right defenses by default?"*

- Content-Security-Policy with nonces or hashes for inline scripts; no `unsafe-inline` for scripts
- Strict-Transport-Security with `max-age` ≥ 31536000 and `includeSubDomains`
- X-Frame-Options or CSP `frame-ancestors` set to prevent clickjacking
- Referrer-Policy set (`strict-origin-when-cross-origin` or stricter)
- Permissions-Policy disabling features the app doesn't need (camera, mic, geolocation if not used)
- X-Content-Type-Options: nosniff
- Subresource Integrity (SRI) on third-party `<script>` and `<link>` tags

## 17. CORS [Both]

*"Is cross-origin access scoped to known callers, not the world?"*

- `Access-Control-Allow-Origin` is an allow-list, not `*`
- Never `Access-Control-Allow-Origin: *` paired with `Access-Control-Allow-Credentials: true`
- Preflight cached only as long as the policy is stable
- Sensitive endpoints reject cross-origin entirely if they shouldn't be cross-origin-callable

## 18. Rate limiting & abuse prevention [P]

*"Are the endpoints that matter protected against brute force, scraping, and resource exhaustion?"*

- Login, signup, password reset, OTP — rate-limited per IP and per account
- Expensive endpoints (search, export, AI/ML inference) — rate-limited per user / per tenant
- Webhook receivers — protected against replay (signature + nonce + timestamp window)
- Pagination has hard upper bound on page size
- Bulk endpoints have batch-size caps

## 19. Error hygiene [Both]

*"Do error responses leak internals to attackers?"*

- Stack traces never returned to clients
- SQL error strings, ORM error details, file-system paths never returned
- Generic error messages for auth failures
- Error IDs (correlation IDs) returned for support, internals stay server-side
- Error-tracking / logger captures full detail; client gets sanitized version

## 20. Dependency supply chain [Both]

*"Are package-registry and dependency-update vectors closed?"*

- Lockfile committed and integrity-verified in CI (`npm ci`, not `npm install`)
- Package versions pinned (no `^` or `~` in production deps where the team has been bitten)
- Newly-added dependencies vetted: maintainer reputation, age, weekly downloads, repository activity
- Pre/post install scripts disabled or whitelisted
- CI doesn't run on untrusted forks with secrets
- Dependency-scanning (Snyk / Dependabot / equivalent) active and acted on, not just enabled

## 21. Client-side storage of sensitive data [H]

*"What's stored where the browser stores it?"*

- Auth tokens in HttpOnly + Secure + SameSite cookies, not localStorage (vulnerable to XSS exfil)
- Sensitive form data not persisted in localStorage / sessionStorage
- IndexedDB usage reviewed for what's cached
- Cookies have correct flags (Secure, HttpOnly, SameSite=Strict for auth)

## 22. Race conditions & state-integrity attacks [P]

*"Could concurrent requests produce a state the system shouldn't reach?"*

- Read-then-write patterns (check entitlement, then act) wrapped in a transaction or use compare-and-swap
- Idempotency on payment / billing / state-transition endpoints
- Optimistic locking (version columns) where contention is real
- Webhook handlers process duplicates without double-applying
