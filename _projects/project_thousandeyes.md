---
layout: page
title: ThousandEyes Telemetry Collector
description: High-throughput Python API collector streaming 3,000+ calls/min to Kafka for real-time network telemetry.
img: assets/img/projects/telemetry.png
importance: 2
category: work
---

**Period:** Nov 2021 – Apr 2025 &nbsp;|&nbsp; **Organization:** Charles Schwab

---

### Overview

A production-grade Python telemetry collection service built at Charles Schwab to ingest ThousandEyes network monitoring data at scale.

### Architecture

- **Async collection** using `asyncio` and `multiprocessing` to achieve **3,000+ API calls per minute**.
- **Queue-based pipeline**: `pure_q` → `PureCaller` → `Publisher` → `KafkaWriter`, with each stage handling rate limiting, retries, and state tracking.
- **SQLite state persistence** via a `collection_state` table tracking `(aid, category, trace_key, status)` with transitions: `queued → picked → complete`, preventing duplicate processing across restarts.
- **Kafka streaming** for real-time downstream anomaly detection and analysis.

### Key Achievements

- Eliminated duplicate telemetry ingestion via idempotent status checks on `(aid, category)` pairs.
- Implemented `supervisor` and `systemd` integration for production service lifecycle management.
- Reduced manual telemetry triage effort significantly through automated categorization and structured logging.

### Tech Stack

`Python` · `asyncio` · `multiprocessing` · `SQLite` · `Kafka` · `REST APIs` · `systemd` · `supervisor`
