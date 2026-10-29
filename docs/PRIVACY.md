# Privacy Policy — Kessoku Games

**Effective Date:** 29 October 2026  
**Last Updated:** 29 October 2026  
**Website:** [Kessoku Games Platform](https://kessokuweb.streamlit.app) / [GitHub Repository](https://github.com/SanoSagara198/kessokuweb)

Kessoku Games ("we", "our", or "the Studio") develops systemic gaming experiences on the Roblox platform, including **Battle Builds** and **Heist City**. This Privacy Policy explains how our web application and companion tools collect, use, and protect your information when you access our website or connect your Roblox account via Roblox OAuth 2.0.

---

## 1. What Information We Collect

### A. Information Provided via Roblox OAuth 2.0
When you choose to sign in to the Kessoku Games web companion using the official "Sign in with Roblox" feature, Roblox transmits authenticated basic profile data based strictly on the approved permissions (`openid`, `profile`):
- **Roblox User ID (`sub` / `id`):** Unique numerical identifier assigned to your Roblox account.
- **Roblox Username & Display Name:** Public account identifiers.
- **Avatar Thumbnail URL:** Public image render of your Roblox avatar.

We do **not** request, access, or store:
- Your Roblox password or authentication credentials.
- Your email address, phone number, physical address, or real name.
- Your billing, payment, or financial details.

### B. In-Game Data via Roblox Open Cloud
When authenticated, our backend uses read-only Roblox Open Cloud DataStore APIs to query public gameplay records associated with your verified User ID:
- In-game non-monetary currency balances (such as earned Credits, Jigsaw pieces, and Keys).
- Unlocked Operators, Weapon progression levels, and configured loadout presets.
- Career statistics (such as match history, K/D records, and Zombie Descent floor progress).

---

## 2. How We Use Your Information

We use the collected information exclusively to:
1. Authenticate your session and display your in-game identity on the web companion.
2. Render your personalized game statistics, armory progress, and active loadouts.
3. Display your deterministic 6-hour in-game shop rotation.
4. Allow you to plan builds and test weapon synergies outside of the active game client.

We do **not**:
- Sell, rent, lease, or monetize your personal or gameplay data.
- Share your information with third-party advertising or marketing brokers.
- Track your activity across external non-Kessoku websites.

---

## 3. Data Storage, Retention, and Security

- **Session-Only Persistence:** Your OAuth authentication tokens and profile session data are retained temporarily in encrypted session state for the duration of your browser visit.
- **No Unsolicited Permanent Records:** We do not maintain off-platform databases containing your personal information.
- **Security Standards:** All data transfers between your browser, our web service, and the Roblox Open Cloud APIs occur exclusively over secure, encrypted TLS/HTTPS connections.

---

## 4. Third-Party Services (Roblox Corporation)

Our authentication and data retrieval rely directly on official services provided by **Roblox Corporation**. Your interactions with Roblox authentication prompts are subject to the [Roblox Privacy Policy](https://en.help.roblox.com/hc/en-us/articles/115004630823-Roblox-Privacy-and-Cookie-Policy) and [Roblox Terms of Use](https://en.help.roblox.com/hc/en-us/articles/115004647846-Roblox-Terms-of-Use).

---

## 5. Your Rights and Revoking Authorization

You have complete control over your Roblox data:
- **Revoke App Access:** You can revoke Kessoku Games' access to your account at any time by navigating to your Roblox Account Settings > **Security** > **Authorized Apps** and clicking Revoke.
- **Clear Session:** Logging out of the web companion or clearing your browser cookies terminates the active session immediately.

---

## 6. Children's Online Privacy (COPPA Compliance)

Kessoku Games experiences and companion tools comply with COPPA (Children's Online Privacy Protection Act). We do not knowingly collect personal information from children under the age of 13. All data retrieved is restricted to public Roblox identifiers authorized through Roblox's secure parental-compliant OAuth flow.

---

## 7. Contact Us

If you have questions, inquiries, or feedback regarding this Privacy Policy, please contact the development team:
- **Studio Repository:** [https://github.com/SanoSagara198/kessokuweb](https://github.com/SanoSagara198/kessokuweb)
- **Studio Location:** Kessoku Games, Argentina
