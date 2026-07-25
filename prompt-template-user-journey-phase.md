# Prompt Template: User Journey Map Phase Generator

**Date:** 2026-07-25
**Author:** Veronika Zavgorodnia — UX/UI Designer
**Project:** Omnichannel Commerce Platform
**Model:** Claude 4 Sonnet via DIAL
**DIAL location:** https://chat.lab.epam.com/share/hP6HqMVcFSQ1f8zYrprFhJUe8XuK8omgx9j2L52kGJxiCbuNvDbwoBU2iqQGcRaJogK7W679K3PCYcN8funbecSonNbod3TwjBg58zY14Yh1R5ACCup9FrkXXNkUQahqpgqGRLj9wrEwJgd3Y7R8n8ZDs
**Committed location:** https://github.com/veronikazavgorodnia47/AI.RUN2026

---

## Purpose

Generate a user journey map phase for click-and-collect flow in a specific region for UX designers during the discovery and design stage.

---

## Variable Placeholders

| Placeholder | Description | Example value |
|---|---|---|
| `{{region}}` | Target geographic region for the user journey | Italy |
| `{{phase}}` | Specific phase of the user journey to focus on | Discovery |
| `{{pain_point}}` | Key pain point to address in this phase. *Source: user research findings, project documentation, stakeholder feedback, or analytics data.* | Unclear total costs upfront |

---

## Output Format Instruction

Return a structured list with exactly these sections:
- Touchpoints: [list 3-4 specific touchpoints]
- Emotions: [2-3 emotions with emojis]
- Pain Points: [2-3 specific issues]
- Regional Notes: [1-2 cultural/local considerations]

Keep it concise and actionable. No preamble or additional text.

---

## Prompt Body

You are a UX researcher. Create a user journey map phase for click-and-collect shopping.

Region: {{region}}
Journey Phase: {{phase}} (e.g., Discovery, Consideration, Purchase, Pickup)
Key Pain Point: {{pain_point}} (Source: user research findings, project documentation, stakeholder feedback, or analytics data)

Output format:
- Touchpoints: [list 3-4 specific touchpoints]
- Emotions: [2-3 emotions with emojis]
- Pain Points: [2-3 specific issues]
- Regional Notes: [1-2 cultural/local considerations]

Keep it concise and actionable.

---

## Test Run (Author)

**Input values used:**
- `{{region}}` = Italy
- `{{phase}}` = Discovery
- `{{pain_point}}` = Unclear total costs upfront

**Output quality:** The output was usable as-is and provided clear, structured insights for the Italian discovery phase.

---

## Peer Review

**Reviewer:** Anastasiia Yermolenko — UX Designer
**Date reviewed:** 2026-07-25
**Model used by reviewer:** Claude Sonnet

**Reviewer input values used:**
- `{{region}}` = USA
- `{{phase}}` = Purchase
- `{{pain_point}}` = Uncertainty about the value

| Review question | Reviewer answer |
|---|---|
| Could you run the template without asking the author anything? | Yes |
| Was the output format what you expected? | Yes — A bulleted list |
| Would you use this template on your own work? | Yes |
| One concrete improvement suggestion | Add info where to search pain-points for |

---

## Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 2026-07-25 | Initial commit | Veronika Zavgorodnia |
| 1.1 | 2026-07-25 | Post-review update: Added pain point sourcing guidance | Veronika Zavgorodnia |
