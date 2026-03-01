# Raptive Ad-Tech Statistical Insights

**🚀 Live Demo:** [View the deployed dashboard here](https://raptivetakehome-uuahafg664syhdrqvo835d.streamlit.app/)

This repository contains an interactive [Streamlit](https://streamlit.io/) dashboard built as a data science demonstration for **Raptive**. It visualizes interesting statistical properties of random distributions, specifically contextualized for ad-tech, creator monetization, and user behavior.

## Overview

The dashboard is divided into four main tabs:

1.  **🧮 A/B Testing Equivalence ($t^2$ vs $F$ vs $\chi^2$)**
    *   **Context:** Statistical equivalence in A/B testing.
    *   **Property:** Demonstrates a beautiful mathematical property: the square of a Student's **$t$-distribution** is an **$F$-distribution**, and as traffic grows towards infinity, it perfectly converges to a **Chi-Square ($\chi^2$) distribution**. The tab includes interactive simulations and the step-by-step mathematical deduction proving why a T-test yields the identical p-value to an ANOVA or a large-sample Chi-Square test!

2.  **🎯 CTR & The Central Limit Theorem (CLT)**
    *   **Context:** Click-Through Rates (CTR) in A/B testing.
    *   **Property:** Demonstrates how the distribution of average click-through rates (a sample proportion of a Bernoulli process) approaches a Normal distribution as the number of ad impressions increases, showcasing the foundational math behind standard A/B testing.

3.  **💰 Creator Revenue & Heavy Tails**
    *   **Context:** Creator monetization and the 80/20 rule.
    *   **Property:** Uses the **Pareto distribution** to demonstrate Heavy Tails, showing how a tiny percentage of top-performing pages/creators drive the vast majority of total network revenue.

4.  **👀 Ad Impressions & Overdispersion**
    *   **Context:** Modeling how many ad impressions a user sees in a given timeframe.
    *   **Property:** Compares a **Poisson** model (random visits) against a **Negative Binomial** model (bursty behavior), demonstrating **Overdispersion** (variance exceeding the mean) in real-world human behavior.

## Custom Theme

The dashboard features a custom UI theme configured in `.streamlit/config.toml` that aligns with Raptive's modern, clean aesthetic:
*   Primary Accent: Coral/Orange (`#ff5722`)
*   Background: Light gray/blue tint (`#f4f4f9`)
*   Text: Deep slate (`#2d3748`)

## How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/raptive-stats-dashboard.git
    cd raptive-stats-dashboard
    ```

2.  **Install the requirements:**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## Deployment to Streamlit Community Cloud

This repository is ready to be deployed directly to [share.streamlit.io](https://share.streamlit.io/).

1.  Push this code to a public GitHub repository.
2.  Log in to Streamlit Community Cloud.
3.  Click "New app".
4.  Select your GitHub repository, branch, and specify `app.py` as the Main file path.
5.  Click "Deploy"! Streamlit will automatically read the `requirements.txt` and `.streamlit/config.toml` files.
