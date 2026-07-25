# Model Selection Note

**Date:** 2026-07-25  
**Author:** Veronika Zavgorodnia — UX/UI Designer  
**Project:** Omnichannel Commerce Platform  
**Task:** Generate a first-draft user journey map for the click-and-collect flow, tailored to regional requirements (Italy and Japan), using AI to synthesize research data and persona insights.  
**Committed location:** [Repo path or shared folder URL]

---

## Evaluation Criteria

| # | Criterion         | Why it matters for this task                                      |
|---|-------------------|-------------------------------------------------------------------|
| 1 | Accuracy          | Ensures the journey map reflects real user research and personas. |
| 2 | Completeness      | Captures all key steps, touchpoints, and pain points.             |
| 3 | Regional Nuance   | Adapts to local requirements and cultural expectations.           |
| 4 | Clarity of Format | Makes the journey map easy to interpret for stakeholders.         |

---

## Prompt Used

Based on user research and persona insights, generate a first-draft user journey map for the click-and-collect flow, highlighting key steps and pain points for both Italian and Japanese customers. Include regional nuances and cultural expectations.

---

## Output Comparison

### Model A: OpenAI ChatGPT-4 Latest (GPT-4o)
> 1. Awareness & Discovery  
> Italy  
> Key Actions: Customers discover the service through online search, social media ads, or word-of-mouth. A strong visual layout with promotions or discounts sparks interest.  
> Pain Points: Lack of clarity about how the service works or what items are available for click-and-collect. Confusion arises if the service isn’t clearly differentiated from delivery.  
> Cultural Nuance: Italians value trust and transparency, so clear descriptions, prominently featured reviews, and a local-friendly tone are crucial.

### Model B: Dial ChatHub - Anthropic Claude 4 Sonnet
> PHASE 1: DISCOVERY & AWARENESS  
> 🇮🇹 Italian Customer Journey  
> Touchpoints:  
> - Social media ads (Facebook, Instagram)  
> - Mobile-first browsing  
> - Word-of-mouth recommendations  
> - Price comparison sites  
> Emotions: 😊 Curious, 🤔 Comparison-focused  
> Cultural Nuances:  
> - High social media influence (large percentage follow brands on Facebook)  
> - Mobile-first approach (smartphones preferred for shopping)  
> - Price-sensitive mindset (90% consider price key factor)  
> Pain Points: ⚠️  
> - Overwhelming choice of retailers  
> - Unclear total costs upfront  
> - Limited local pickup options in southern regions

---

## Scorecard

| Criterion         | Model A score (1–3) | Model A evidence                                            | Model B score (1–3) | Model B evidence                                            |
|-------------------|---------------------|-------------------------------------------------------------|---------------------|-------------------------------------------------------------|
| Accuracy          | 2                   | Captures main actions and pain points, but lacks some detail on touchpoints. | 3                   | Lists specific touchpoints and pain points clearly.          |
| Completeness      | 2                   | Covers actions and pain points, but not emotions or all touchpoints. | 3                   | Includes touchpoints, emotions, pain points, and cultural nuances. |
| Regional Nuance   | 3                   | Addresses trust, transparency, and local tone.              | 3                   | Highlights social media, mobile-first, price sensitivity, and regional pickup issues. |
| Clarity of Format | 2                   | Structured but less visually clear; lacks bullet points and emotion cues. | 3                   | Clear structure, bullet points, and emotion cues.            |
| **Total**         | 9                   |                                                             | 12                  |                                                             |

---

## Decision

**Selected model:** Dial ChatHub - Anthropic Claude 4 Sonnet

**Rationale:** Claude 4 Sonnet scored highest on completeness and clarity of format, which are critical for communicating user journey maps to stakeholders. It provided a more detailed and structured output, including specific touchpoints, emotions, and regional nuances. GPT-4o’s main shortcoming was less detail and less clarity in formatting, making it harder to interpret at a glance.

---

## Active Constraint

**What could change this decision within 30 days:**  
If the client tool approval changes or a new model with improved context window or regional adaptation is introduced, the decision may be revisited.

---

## Revision history

| Version | Date       | Change         |
|---------|------------|---------------|
| 1.0     | 2026-07-25 | Initial commit |