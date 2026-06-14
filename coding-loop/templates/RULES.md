# Project Rule Constraints (RULES.md)

This file defines the absolute constraints that the coding agent loop must verify against the candidate git diff. If any changes violate these guidelines, the verification pass will fail.

---

## 🔒 Security Guidelines
- [ ] No raw SQL statements allowed in client-facing components or handlers. Use prepared statements or ORM builders.
- [ ] Do not check in cleartext API keys, secrets, or authorization tokens. All variables must use environment lookups (e.g., `process.env` or `os.getenv`).
- [ ] No hardcoded encryption keys or local cryptographic salts.

## 🛠️ Code Style & Syntax
- [ ] No raw `print()` or `console.log()` statements in production code. Use the project logger module.
- [ ] All components must export functional declarations (avoid class components).
- [ ] Do not leave debugging comments (e.g., `debugger;`, `var_dump`).
- [ ] Resolve all placeholder `TODO` and `FIXME` comments before requesting review.

## 📦 Dependency Restrictions
- [ ] Do not install new third-party packages or edit `package.json` / `requirements.txt` without prior approval.
- [ ] Use native platform APIs (like Web Fetch) instead of adding custom request libraries.
