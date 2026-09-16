---
trigger: always_on
description: "Zero-Trust Dependencies - Supply chain security. Scans all new npm/pip packages before installation. Blocks typosquatting and known-vulnerable packages."
---
# Zero-Trust Dependencies (An toàn chuỗi cung ứng)

## Purpose
Prevent supply chain attacks by vetting all new third-party dependencies before installation.

## Trigger
Load when the AI proposes adding any new package via `npm install`, `pip install`, `cargo add`, or similar.

## Pre-Install Checklist

### 1. Package Verification
Before installing any new package:
- Confirm the exact package name matches the official registry (check for typosquatting variants).
- Verify the package exists on the official registry (npmjs.com, pypi.org).
- Check download count and last publish date. Flag packages with <1000 weekly downloads or no updates in >2 years.

### 2. Duplicate Detection
- Check if equivalent functionality already exists in the project's current dependencies.
- Check if the standard library provides the same capability (e.g., `fs` instead of `fs-extra` for simple ops).

### 3. Security Scan
- For npm: run `npm audit` after adding.
- For pip: check against known vulnerability databases.
- Block installation if critical or high severity vulnerabilities are reported.

### 4. Scope Minimization
- Prefer packages with zero or minimal transitive dependencies.
- Between two equivalent packages, choose the one with fewer dependencies.

### 5. User Approval Gate
- Present the package name, version, purpose, and audit results.
- Wait for explicit User approval before running the install command.
