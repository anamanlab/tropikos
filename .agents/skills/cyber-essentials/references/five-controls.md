# The Five Control Themes — Requirements Detail (v3.3 / Danzell)

Source of truth: NCSC "Cyber Essentials: Requirements for IT Infrastructure v3.3" (April 2026). Applies to: boundary firewalls/routers, desktops, laptops, servers, tablets, phones, and cloud services in scope.

## 1. Firewalls
- Every in-scope device protected by a correctly configured firewall (boundary and/or software firewall).
- Change default administrative passwords, or disable remote administrative access.
- Administrative interface not reachable from the internet unless there is a documented business need AND it is protected by MFA or an IP allow-list plus managed passwords.
- Block unauthenticated inbound connections by default; inbound rules approved and documented with business need; remove/disable rules no longer needed.
- Software firewall required on devices used on untrusted networks (home, public Wi-Fi).

## 2. Secure Configuration
- Remove or disable unnecessary user accounts, software and services.
- Change default or guessable passwords; remove auto-run/auto-play for removable media and network mounting.
- Users authenticate before accessing organisational data or services.
- Device unlocking: biometrics, password or PIN of at least 6 characters (where the credential only unlocks the device); brute-force protection: throttle to max 10 guesses in 5 minutes, or lock out after no more than 10 unsuccessful attempts.

## 3. Security Update Management
- All software on in-scope devices: licensed and vendor-supported.
- Unsupported software: removed from devices, or moved out of scope into a defined sub-set that prevents ALL traffic to and from the internet. Unsupported software inside scope = certification failure.
- Enable automatic updates wherever possible.
- **14-day rule**: install updates within 14 days of release when the update (a) fixes vulnerabilities the vendor describes as 'critical' or 'high risk', (b) addresses a vulnerability with CVSS v3 base score 7.0 or above, or (c) the vendor provides no severity detail. A bundled update containing any critical/high fix inherits the 14-day clock. Installing ALL updates within 14 days is recommended, not required.
- Under Danzell, questions A6.4 (OS and router/firewall firmware) and A6.5 (applications) on the 14-day rule are AUTOMATIC-FAIL questions.
- Firmware counts as software; firewall/router firmware needs listing (make/model) per Willow-era change.

## 4. User Access Control
- Account creation through an approval process; unique credentials per user; accounts removed/disabled when no longer needed (leavers, role changes).
- Administrative privileges: separate accounts for admin activities — no email or web browsing from admin accounts; privileged access removed when no longer required.
- **MFA: authentication to cloud services must ALWAYS use MFA** — missing MFA where the service offers it is an automatic fail under Danzell. MFA password element: minimum 8 characters.
- Password policy (choose one): MFA everywhere; or minimum 12 characters; or minimum 8 characters with automatic deny-listing of common passwords. No enforced regular expiry; no enforced complexity rules. Protect against brute force (throttling/lockout as above).
- Passwordless accepted: passkeys/FIDO2, biometrics, security keys, one-time codes, push notifications; FIDO2 authenticators count as MFA.
- Organisation-owned accounts operated by third parties/MSPs remain in scope.

## 5. Malware Protection
Every in-scope device runs one of:
- **Anti-malware software** — updated per vendor recommendations (signature/engine auto-updates), prevents execution of known malware and malicious code, blocks access to malicious websites; or
- **Application allow-listing** — only approved applications, restricted by code signing, may execute; the approved list is actively maintained.
Sandboxing alone no longer appears as a stand-alone option in current requirements — anchor answers on the two mechanisms above.
