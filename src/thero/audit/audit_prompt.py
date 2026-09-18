AUDIT_PROMPT = r"""
You are performing a technical audit of an existing software
project.

THIS IS AN AUDIT-FIRST OPERATION.

During this first pass, DO NOT modify source code.

The goal is to identify real problems in the existing project,
especially problems that a disciplined senior engineering
workflow should detect.

---

## STEP 1 — UNDERSTAND THE PROJECT

Inspect:

- repository structure;
- package files;
- framework versions;
- configuration;
- source organization;
- tests;
- database integrations;
- authentication;
- deployment configuration.

Determine the actual technology stack.

Do not assume it from filenames alone.

---

## STEP 2 — AUDIT

Inspect relevant areas for:

- TypeScript correctness;
- React architecture;
- Next.js architecture;
- Server/Client boundaries;
- state management;
- unnecessary effects;
- API design;
- validation;
- error handling;
- authentication;
- authorization;
- Supabase;
- Firebase;
- Stripe;
- database access;
- security;
- data integrity;
- performance;
- accessibility;
- UI consistency;
- tests;
- dependency misuse;
- duplicated abstractions;
- architectural inconsistencies.

Only report issues supported by evidence.

Do not report something merely because you personally prefer
another coding style.

---

## SEVERITY

Classify findings as:

CRITICAL
Potential security, data-loss or severe correctness issue.

BUG
Demonstrably incorrect behavior.

RISK
Credible failure mode that is not currently demonstrated.

MAINTENANCE
Concrete maintainability problem.

IMPROVEMENT
Optional improvement that is not currently a defect.

Do not turn IMPROVEMENT into a defect.

---

## EACH FINDING

Include:

- severity;
- file;
- symbol or approximate location;
- problem;
- why it matters;
- evidence;
- recommended correction.

---

## DO NOT MODIFY

Do not:

- edit source files;
- reformat files;
- update dependencies;
- change configuration;
- create migrations;
- fix issues during this first pass.

The only output should be the audit report.

---

## FINAL REPORT

Use:

# Technical Audit

## Executive Summary

## Critical

## Bugs

## Risks

## Maintenance

## Improvements

## Recommended Correction Order

Keep the report concise and evidence-based.
"""
