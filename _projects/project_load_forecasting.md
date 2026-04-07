---
layout: page
title: Electricity Load Forecasting API
description: End-to-end ML system for hourly electricity demand forecasting with FastAPI deployment.
img: assets/img/projects/load_forecasting.jpg
importance: 1
category: personal
---

<div class="project-links mb-3">
  <a href="https://github.com/utkarshsrivastava94/data_science/tree/main/load_forecasting_project" target="_blank" class="btn btn-sm z-depth-0" role="button">
    <i class="fa-brands fa-github"></i> GitHub
  </a>
</div>

**Period:** May 2025 – Jun 2025 &nbsp;|&nbsp; **Type:** Machine Learning Project

---

### Overview

An end-to-end machine learning system for forecasting hourly electricity demand using real-world weather and load data. The project covers the full ML lifecycle — from raw data ingestion and feature engineering through model training, evaluation, and live REST API deployment.

### Key Achievements

- **Model Performance:** Trained a `RandomForestRegressor` model achieving **R² = 0.991** on Kaggle time-series electricity load data, demonstrating high predictive accuracy across varying demand conditions.
- **Feature Engineering:** Engineered lag-based features (previous hour, previous day, previous week demand) and time-based features (hour of day, day of week, month, weekend flag) to capture temporal patterns and improve forecasting accuracy.
- **API Deployment:** Saved the trained model and deployed it using **FastAPI** with live REST inference endpoints, served via Uvicorn for production-grade performance.
- **Observability:** Implemented structured logging and API usage monitoring to track inference requests, response times, and model behavior in production.

### Tech Stack

`Python` · `Scikit-learn` · `FastAPI` · `Uvicorn` · `Pandas` · `NumPy` · `Time Series Forecasting` · `REST APIs` · `API Logging`
