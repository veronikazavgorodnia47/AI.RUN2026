# Security agent — 8-platform compatibility + governance matrix

Reference for `threat-modeling-mrg-checkout` Skill (`SKILL.md`).
Decision rules are inline in `SKILL.md` — not here.

| Platform | Deployment role | Data residency | Audit logging | Compliance notes |
|---|---|---|---|---|
| **EPAM DIAL** (primary) | DIAL custom assistant | EU — processed within EPAM-managed EU tenant | DIAL session logs per EPAM data-retention policy | GDPR compliant; approved for internal Meridian threat-modeling work; minimise PII in prompt context |
| **CodeMie (Claude Code)** | IDE-integrated runtime | Anthropic API under EPAM enterprise agreement | Per CodeMie audit-log config | Approved for EPAM AI-Native SDLC work; confirm PII handling with CodeMie admin before regulated-data use |
| **Claude Code (CLI)** | Local interactive session | Anthropic API; processed by Anthropic | Claude Code session logs; no centralised retention | Used in this kata; internal-only; DPO clearance required before external-facing or regulated-data use |
| **GitHub Copilot** | IDE assistant | Microsoft Azure (org-selected region) | Enterprise audit log (Copilot Business/Enterprise) | Check your org's Copilot policy before using prompts containing architecture details |
| **Amazon Q Developer** | IDE assistant | AWS region selected at org level | AWS CloudTrail (if enabled) | Permitted under AWS BAA for relevant data classes; check EPAM AWS org policy |
| **GitLab Duo** | GitLab-integrated assistant | GitLab.com (multi-region) or self-hosted | GitLab audit events | Approved for GitLab CI/CD context; do not send PII in prompt context |
| **Cursor** | IDE assistant (agentic mode) | Cursor cloud; Anthropic / OpenAI API routing | No centralised org-level audit log | Not approved for regulated-data prompts; acceptable for DFD drafting without PII |
| **Tabnine** | IDE code completion | Self-hosted or Tabnine SaaS | Per deployment config | Code-completion only; no prompt-in / threat-model-out workflow; lowest risk tier |

**Governance intake:** before deploying this Skill to an external-facing or regulated-data context, raise a request via the EPAM AI governance intake and attach this matrix plus `SKILL.md` as evidence.
