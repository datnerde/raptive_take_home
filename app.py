import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm, t, f, chi2

# ------------------------------------------------------------------------------
# App Configuration
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Raptive Data Science Insights",
    page_icon="📈",
    layout="wide"
)

# ------------------------------------------------------------------------------
# UI Styles & Headers
# ------------------------------------------------------------------------------
st.title("📈 Ad-Tech Statistical Insights")
st.markdown("""
Welcome to this interactive demonstration of statistical distributions in the context of **Ad-Tech** and **Creator Monetization**.
Explore the tabs below to understand how different statistical properties impact real-world metrics like Click-Through Rates (CTR), Creator Revenue (RPMs), and User Ad Impressions.
""")

# Create tabs for the four sections
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 CTR & The Central Limit Theorem",
    "💰 Creator Revenue & Heavy Tails",
    "👀 Ad Impressions & Overdispersion",
    "🧮 A/B Testing Equivalence (t² vs F vs χ²)"
])

# ------------------------------------------------------------------------------
# Tab 1: CTR & The Central Limit Theorem
# ------------------------------------------------------------------------------
with tab1:
    st.header("Click-Through Rate (CTR) & The Central Limit Theorem")
    st.markdown("""
    In A/B testing for ad creatives, we often look at the **Click-Through Rate (CTR)**.
    A single ad impression results in a click (1) or no click (0), which follows a **Bernoulli distribution**.
    However, when we calculate the *average* CTR over thousands of impressions, the distribution of that average
    approaches a **Normal distribution**, regardless of the underlying Bernoulli shape.
    This is the **Central Limit Theorem (CLT)** in action, and it's why we can use standard statistical tests (like Z-tests) for A/B testing!
    """)

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Simulation Parameters")
        true_ctr = st.slider("True CTR probability", min_value=0.01, max_value=0.20, value=0.05, step=0.01, format="%.2f")
        sample_size = st.select_slider("Impressions per Experiment", options=[10, 50, 100, 500, 1000, 5000], value=100)
        num_experiments = st.slider("Number of Experiments", min_value=100, max_value=5000, value=1000, step=100)

    with col2:
        # Simulate experiments
        # Each experiment is np.random.binomial(n=sample_size, p=true_ctr) / sample_size
        np.random.seed(42)
        experiments = np.random.binomial(n=sample_size, p=true_ctr, size=num_experiments) / sample_size

        # Plot distribution of average CTRs
        fig = px.histogram(
            x=experiments,
            nbins=30,
            histnorm='probability density',
            title=f"Distribution of Average CTR across {num_experiments} Experiments",
            labels={'x': 'Average CTR', 'y': 'Density'},
            color_discrete_sequence=['#ff5722']
        )

        # Overlay Normal distribution expected from CLT
        mean_expected = true_ctr
        std_expected = np.sqrt(true_ctr * (1 - true_ctr) / sample_size)
        x_range = np.linspace(min(experiments), max(experiments), 200)
        pdf_normal = norm.pdf(x_range, loc=mean_expected, scale=std_expected)

        fig.add_trace(go.Scatter(
            x=x_range, y=pdf_normal,
            mode='lines',
            name='Expected Normal Dist',
            line=dict(color='#2d3748', width=3, dash='dash')
        ))

        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    st.info(f"**Insight:** Notice how as you increase the 'Impressions per Experiment', the histogram becomes narrower and perfectly matches the dashed Normal curve. This proves that with enough traffic, our CTR estimates become highly predictable normally-distributed variables!")

# ------------------------------------------------------------------------------
# Tab 2: Creator Revenue & Heavy Tails
# ------------------------------------------------------------------------------
with tab2:
    st.header("Creator Revenue & The Power Law (Heavy Tails)")
    st.markdown("""
    Website traffic and creator revenue rarely follow a clean bell curve. Instead, they exhibit **Heavy Tails**—often following a **Pareto distribution** (the "80/20 rule").
    This means a small percentage of top-performing creators or articles generate the vast majority of the total revenue. Averages here can be incredibly misleading!
    """)

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Distribution Parameters")
        pareto_alpha = st.slider("Pareto Shape (Alpha)", min_value=1.1, max_value=3.0, value=1.5, step=0.1,
                                 help="Lower alpha means heavier tails (more extreme inequality).")
        sample_size_rev = st.number_input("Number of Creators", min_value=100, max_value=10000, value=5000, step=500)

    with col2:
        np.random.seed(42)
        # Generate Pareto data (xm = 1)
        revenue_data = (np.random.pareto(pareto_alpha, sample_size_rev) + 1) * 100  # Scale to look like dollars

        # To show the heavy tail, we'll plot the top N vs the rest, or a histogram
        # Because Pareto goes to infinity, we clip for visualization
        clip_val = np.percentile(revenue_data, 99)
        clipped_data = revenue_data[revenue_data < clip_val]

        fig2 = px.histogram(
            x=clipped_data,
            nbins=50,
            title=f"Revenue Distribution (Bottom 99% of Creators)",
            labels={'x': 'Monthly Revenue ($)', 'y': 'Count of Creators'},
            color_discrete_sequence=['#ff5722']
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Calculate stats to demonstrate the 80/20 rule
        revenue_data_sorted = np.sort(revenue_data)[::-1]
        top_20_percent_idx = int(0.2 * sample_size_rev)
        revenue_top_20 = np.sum(revenue_data_sorted[:top_20_percent_idx])
        total_revenue = np.sum(revenue_data)
        pct_from_top_20 = (revenue_top_20 / total_revenue) * 100

        st.metric(label="Revenue generated by Top 20% of Creators", value=f"{pct_from_top_20:.1f}%")

    st.info(f"**Insight:** With an alpha of {pareto_alpha}, the top 20% of creators drive **{pct_from_top_20:.1f}%** of the total network revenue. If you lower the alpha, the tail gets heavier and this percentage increases. This is why standard metrics like the 'average revenue' don't represent the typical creator's experience!")

# ------------------------------------------------------------------------------
# Tab 3: Ad Impressions & Overdispersion
# ------------------------------------------------------------------------------
with tab3:
    st.header("Ad Impressions per User: Poisson vs. Negative Binomial")
    st.markdown("""
    If users visited web pages entirely at random, the number of ads they see in a month would follow a **Poisson distribution** (where mean = variance).
    However, human behavior is "bursty". Some users binge-read a dozen articles in one day, while others visit once and leave. This creates **Overdispersion** (variance > mean),
    making the **Negative Binomial distribution** a much better model for ad impressions.
    """)

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Model Parameters")
        mean_impressions = st.slider("Average Ad Impressions per User", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
        dispersion = st.slider("Overdispersion Factor", min_value=0.1, max_value=5.0, value=1.0, step=0.1,
                               help="Higher values mean more 'bursty' behavior. 0 would be exactly Poisson.")
        n_users = 10000

    with col2:
        np.random.seed(42)

        # Poisson (no dispersion)
        poisson_data = np.random.poisson(lam=mean_impressions, size=n_users)

        # Negative Binomial (overdispersed)
        # mean = n(1-p)/p, var = n(1-p)/p^2.
        # For given mean (mu) and dispersion parameter (alpha), var = mu + alpha * mu^2
        var_nbinom = mean_impressions + dispersion * (mean_impressions ** 2)
        p_nbinom = mean_impressions / var_nbinom
        n_nbinom = (mean_impressions ** 2) / (var_nbinom - mean_impressions)

        nbinom_data = np.random.negative_binomial(n=n_nbinom, p=p_nbinom, size=n_users)

        df_counts = pd.DataFrame({
            'Impressions': np.concatenate([poisson_data, nbinom_data]),
            'Model': ['Poisson (Random)'] * n_users + ['Negative Binomial (Bursty)'] * n_users
        })

        fig3 = px.histogram(
            df_counts,
            x='Impressions',
            color='Model',
            barmode='group',
            histnorm='probability',
            title="Distribution of Ad Impressions per User",
            labels={'Impressions': 'Ads Seen', 'count': 'Probability'},
            color_discrete_sequence=['#2d3748', '#ff5722']
        )

        # Focus on a reasonable range
        fig3.update_xaxes(range=[0, max(mean_impressions * 3, 15)])
        st.plotly_chart(fig3, use_container_width=True)

    st.info(f"**Insight:** The Poisson model predicts almost everyone sees around {mean_impressions} ads. But the Negative Binomial model captures the real-world truth: a massive spike of users who see 0-1 ads (bouncers), and a long tail of power-users who binge and see many more ads than the average.")

# ------------------------------------------------------------------------------
# Tab 4: A/B Testing Equivalence (t^2 vs F vs Chi-Square)
# ------------------------------------------------------------------------------
with tab4:
    st.header(r"A/B Testing Equivalence: $t^2$, $F$, and $\chi^2$ Distributions")
    st.markdown(r"""
    When comparing metrics (like pageviews or time-on-page) between a Control and Variant group, we often use different statistical tests.
    However, many of these tests are mathematically identical!

    This tab demonstrates a beautiful mathematical property: the square of a Student's **$t$-distribution** with $\nu$ degrees of freedom is exactly an **$F$-distribution** with $(1, \nu)$ degrees of freedom.
    Furthermore, as our sample size (traffic) grows to infinity, this distribution perfectly converges to a **$\chi^2$ (Chi-Square) distribution** with 1 degree of freedom!
    """)

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Simulation Parameters")
        dof = st.slider(
            "Degrees of Freedom ($\\nu$) / Traffic",
            min_value=1, max_value=100, value=5, step=1,
            help="Low traffic means low degrees of freedom. High traffic approaches infinity."
        )
        n_samples_t = st.number_input(
            "Number of Experiments to Simulate",
            min_value=1000, max_value=50000, value=10000, step=1000
        )

    with col2:
        np.random.seed(42)

        # Draw from t-distribution and square it
        t_samples = t.rvs(df=dof, size=n_samples_t)
        t_squared_samples = t_samples**2

        # Filter extreme outliers for better visualization
        clip_t2 = np.percentile(t_squared_samples, 95)
        filtered_t_squared = t_squared_samples[t_squared_samples < clip_t2]

        # Create histogram of the simulated t^2
        fig4 = px.histogram(
            x=filtered_t_squared,
            nbins=50,
            histnorm='probability density',
            title=rf"Simulated $t^2$ vs Analytical $F$ and $\chi^2$ ($\nu$ = {dof})",
            labels={'x': 'Test Statistic Value', 'y': 'Density'},
            color_discrete_sequence=['#ff5722']
        )
        fig4.update_traces(name="Simulated $t^2$", showlegend=True)

        # Overlay Theoretical F-distribution
        x_range_4 = np.linspace(0, max(filtered_t_squared), 200)
        # Avoid exactly 0 for F and chi2 PDF to prevent infinity/warnings
        x_range_4_safe = np.maximum(x_range_4, 1e-4)

        pdf_f = f.pdf(x_range_4_safe, dfn=1, dfd=dof)

        fig4.add_trace(go.Scatter(
            x=x_range_4, y=pdf_f,
            mode='lines',
            name=f'F(1, {dof}) Dist',
            line=dict(color='#2d3748', width=3, dash='solid')
        ))

        # Overlay Theoretical Chi-Square distribution (df=1)
        pdf_chi2 = chi2.pdf(x_range_4_safe, df=1)

        fig4.add_trace(go.Scatter(
            x=x_range_4, y=pdf_chi2,
            mode='lines',
            name=r'$\chi^2(1)$ Dist (Infinite Traffic)',
            line=dict(color='#3b82f6', width=3, dash='dot')
        ))

        fig4.update_layout(showlegend=True, legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
        st.plotly_chart(fig4, use_container_width=True)

    st.info(rf"**Interactive Insight:** Move the Degrees of Freedom slider. Notice how the simulated orange $t^2$ histogram **always** perfectly matches the dark $F$-distribution. As you increase $\nu$ to simulate high traffic, both perfectly merge into the dotted blue $\chi^2$ distribution!")

    st.markdown("---")
    st.subheader("The Mathematical Deduction")
    st.markdown("Why does a two-sided two-sample T-test yield the exact same p-value as a one-way ANOVA? Because the underlying statistics are identical.")

    st.latex(r"""
    \text{By definition, a Student's } t\text{-variable with } \nu \text{ degrees of freedom is the ratio of a standard normal } Z \text{ to the square root of a scaled } \chi^2 \text{ variable:}
    """)
    st.latex(r"""
    T_\nu = \frac{Z}{\sqrt{\chi^2_\nu / \nu}}
    """)
    st.latex(r"""
    \text{If we square both sides:}
    """)
    st.latex(r"""
    (T_\nu)^2 = \frac{Z^2}{\chi^2_\nu / \nu}
    """)
    st.latex(r"""
    \text{We know that the square of a Standard Normal } (Z \sim N(0,1)) \text{ is exactly a Chi-Square with 1 degree of freedom } (Z^2 \sim \chi^2_1)\text{:}
    """)
    st.latex(r"""
    (T_\nu)^2 = \frac{\chi^2_1 / 1}{\chi^2_\nu / \nu}
    """)
    st.latex(r"""
    \text{By definition, an } F\text{-distribution } F(d_1, d_2) \text{ is the ratio of two independent Chi-Square variables, each divided by their degrees of freedom:}
    """)
    st.latex(r"""
    F(d_1, d_2) = \frac{\chi^2_{d_1} / d_1}{\chi^2_{d_2} / d_2}
    """)
    st.latex(r"""
    \text{Therefore, comparing the two equations, we get our exact proof:}
    """)
    st.latex(r"""
    (T_\nu)^2 \sim F(1, \nu)
    """)

    st.markdown("""
    **What happens as traffic (sample size) goes to infinity?**
    By the Law of Large Numbers, as $\\nu \\to \\infty$, the denominator $\\chi^2_\\nu / \\nu$ converges in probability to its expected value, which is 1.
    """)
    st.latex(r"""
    \lim_{\nu \to \infty} (T_\nu)^2 = \frac{\chi^2_1}{1} = \chi^2_1
    """)
    st.markdown("""
    **Ad-Tech Conclusion:** When running an A/B test with massive traffic (like we do at Raptive), comparing the squared Z-score (or squared T-statistic) is mathematically identical to a Chi-Square test for independence!
    """)