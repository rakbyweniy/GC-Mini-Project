import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta
import random

# 1. Page Configuration (Full layout with custom icon and collapsed sidebar)
st.set_page_config(page_title="Spenda - High-End Expense Analytics", layout="wide", initial_sidebar_state="collapsed")

# 2. Complete High-Fidelity CSS overrides mimicking the uploaded design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global Overrides */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #0f172a;
    }

    /* Background of the overall workspace to mimic the mockup's soft gray */
    .stApp {
        background-color: #f4f5f7 !important;
    }

    /* Card Container classes */
    .saas-card {
        background-color: #ffffff;
        border: 1px solid #eef0f3;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.02), 0 10px 30px -5px rgba(15, 23, 42, 0.03);
        margin-bottom: 20px;
        transition: all 0.2s ease;
    }
    .saas-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.06);
    }

    /* Custom KPI Labels */
    .kpi-title {
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
        text-transform: capitalize;
        letter-spacing: -0.01em;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: #0f172a;
        font-weight: 800;
        font-size: 32px;
        line-height: 1.1;
        letter-spacing: -0.03em;
        margin-bottom: 12px;
    }

    /* Soft Pill Badges - Colorways matching a premium layout */
    .saas-pill {
        display: inline-flex;
        align-items: center;
        padding: 5px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
        margin-right: 6px;
        margin-bottom: 4px;
        border: 1px solid transparent;
    }
    .pill-purple {
        background-color: #f5f3ff;
        color: #5244e3;
        border-color: #ede9fe;
    }
    .pill-green {
        background-color: #ecfdf5;
        color: #10b981;
        border-color: #d1fae5;
    }
    .pill-gray {
        background-color: #f8fafc;
        color: #64748b;
        border-color: #f1f5f9;
    }
    .pill-red {
        background-color: #fef2f2;
        color: #ef4444;
        border-color: #fee2e2;
    }
    .pill-blue {
        background-color: #eff6ff;
        color: #3b82f6;
        border-color: #dbeafe;
    }
    .pill-orange {
        background-color: #fff7ed;
        color: #f97316;
        border-color: #ffedd5;
    }
    .pill-pink {
        background-color: #fdf2f8;
        color: #ec4899;
        border-color: #fce7f3;
    }

    /* Customized Form Inputs & Labels */
    label[data-testid="stWidgetLabel"] {
        font-weight: 600 !important;
        color: #334155 !important;
        font-size: 13px !important;
        letter-spacing: -0.01em !important;
        margin-bottom: 6px !important;
    }

    /* Styled Form Card Wrap */
    div[data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 1px solid #eef0f3 !important;
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.02) !important;
    }

    /* Target form input containers - outer wrapping boundaries */
    div[data-testid="stForm"] [data-baseweb="input"], 
    div[data-testid="stForm"] [data-baseweb="select"], 
    div[data-testid="stForm"] [role="button"] {
        background-color: #ffffff !important;
        background: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
        transition: all 0.2s ease !important;
    }

    /* Focus State overrides */
    div[data-testid="stForm"] [data-baseweb="input"]:focus-within, 
    div[data-testid="stForm"] [data-baseweb="select"]:focus-within,
    div[data-testid="stForm"] [role="button"]:focus-within {
        border-color: #5244e3 !important;
        box-shadow: 0 0 0 1px #5244e3 !important;
    }

    /* Ultimate Aggressive Children override to force solid white background and pure black typography */
    div[data-testid="stForm"] [data-baseweb="input"] *, 
    div[data-testid="stForm"] [data-baseweb="select"] *, 
    div[data-testid="stForm"] [role="button"] *,
    div[data-testid="stForm"] input,
    div[data-testid="stForm"] select,
    div[data-testid="stForm"] textarea {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-size: 14px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Set input placeholder elements to visible slate gray */
    div[data-testid="stForm"] input::placeholder,
    div[data-testid="stForm"] textarea::placeholder {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
        opacity: 1 !important;
    }

    /* Custom icons fill */
    div[data-testid="stForm"] svg {
        fill: #475569 !important;
    }

    /* Style the Stepper Buttons (+ / -) in number inputs */
    div[data-testid="stForm"] button[data-testid="stNumberInputStepDown"],
    div[data-testid="stForm"] button[data-testid="stNumberInputStepUp"] {
        background-color: #f1f5f9 !important;
        color: #475569 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
    }
    div[data-testid="stForm"] button[data-testid="stNumberInputStepDown"] *,
    div[data-testid="stForm"] button[data-testid="stNumberInputStepUp"] * {
        background-color: #f1f5f9 !important;
        color: #475569 !important;
        -webkit-text-fill-color: #475569 !important;
    }

    /* Premium Violet-Indigo Buttons (Mockup: 'Analyze This', 'Export Now') */
    div[data-testid="stFormSubmitButton"] button,
    .stButton>button {
        background-color: #5244e3 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #5244e3 !important;
        padding: 10px 22px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: -0.01em !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover,
    .stButton>button:hover {
        background-color: #4338ca !important;
        border-color: #4338ca !important;
        box-shadow: 0 8px 16px -4px rgba(82, 68, 227, 0.35) !important;
        transform: translateY(-1px);
    }
    div[data-testid="stFormSubmitButton"] button:active,
    .stButton>button:active {
        transform: translateY(0px);
    }

    /* Secondary/Demo Button Styling */
    div.row-widget.stButton button[key*="demo"] {
        background-color: #ffffff !important;
        color: #5244e3 !important;
        border: 1px solid #e2e8f0 !important;
    }
    div.row-widget.stButton button[key*="demo"]:hover {
        background-color: #f8fafc !important;
        border-color: #cbd5e1 !important;
        box-shadow: none !important;
    }

    /* Premium table styling for recent logs */
    .saas-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-top: 10px;
    }
    .saas-table th {
        background-color: #f8fafc;
        color: #64748b;
        font-weight: 700;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 14px 18px;
        text-align: left;
        border-bottom: 1px solid #eef0f3;
    }
    .saas-table td {
        padding: 16px 18px;
        font-size: 13.5px;
        color: #334155;
        border-bottom: 1px solid #f1f5f9;
        background-color: #ffffff;
    }
    .saas-table tr:hover td {
        background-color: #f8fafc;
    }
    .saas-table tr:last-child td {
        border-bottom: none;
    }
    .saas-table tr:first-child th:first-child { border-top-left-radius: 16px; }
    .saas-table tr:first-child th:last-child { border-top-right-radius: 16px; }
    .saas-table tr:last-child td:first-child { border-bottom-left-radius: 16px; }
    .saas-table tr:last-child td:last-child { border-bottom-right-radius: 16px; }

    /* Mini graphical flourishes to replicate mockup's fine details */
    .mini-bar-chart {
        display: flex;
        align-items: flex-end;
        gap: 4px;
        height: 45px;
        margin-top: -10px;
    }
    .mini-bar {
        width: 8px;
        background: linear-gradient(180deg, #ede9fe 0%, #5244e3 100%);
        border-radius: 4px;
        min-height: 5px;
    }

    /* Decorative horizontal rule */
    hr {
        border: 0;
        height: 1px;
        background: #eef0f3;
        margin: 40px 0;
    }
    </style>
""", unsafe_allow_html=True)

CSV_FILE = "expenses.csv"


# 3. Data Loading, Writing and Mock Generators
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        return pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])


def save_data(df):
    df.to_csv(CSV_FILE, index=False)


def generate_mock_data():
    categories = ["Food & Dining", "Rent & Housing", "Utilities", "Entertainment", "Shopping", "Transportation",
                  "Other"]
    descriptions = {
        "Food & Dining": ["Chipotle Lunch", "Whole Foods grocery", "Sushi dinner with team", "Blue Bottle espresso",
                          "Boba Tea escape"],
        "Rent & Housing": ["Monthly Premium Apartment", "IKEA study lamp", "Target home organization"],
        "Utilities": ["City Grid Power", "Fiber Gigabit Internet", "Premium Cellular Plan"],
        "Entertainment": ["Netflix Family Plan", "Local indie theater", "Spotify Premium", "Vocal concert voucher"],
        "Shopping": ["Amazon delivery", "Nike athletic sneakers", "Winter coat upgrade", "Designer sunglasses"],
        "Transportation": ["Uber Ride premium", "Gas Station fillup", "Metro Transit card"],
        "Other": ["Elite Gym membership", "Quarterly dental copay", "Eco dry cleaning"]
    }

    mock_rows = []
    base_date = datetime.now() - timedelta(days=30)

    for _ in range(25):
        cat = random.choice(categories)
        desc = random.choice(descriptions[cat])
        t_date = base_date + timedelta(days=random.randint(0, 30))

        if cat == "Rent & Housing":
            amt = float(random.randint(850, 1400))
        elif cat == "Utilities":
            amt = float(random.randint(50, 180))
        elif cat == "Shopping":
            amt = round(random.uniform(45.00, 320.00), 2)
        else:
            amt = round(random.uniform(6.50, 85.00), 2)

        mock_rows.append({
            "Date": t_date.strftime('%Y-%m-%d'),
            "Amount": amt,
            "Category": cat,
            "Description": desc
        })
    df = pd.DataFrame(mock_rows)
    df['Date'] = pd.to_datetime(df['Date'])
    save_data(df)


# Initialize Data
df_expenses = load_data()

# 4. Header Area matching the crisp mockup alignment
col_header, col_action = st.columns([3, 1])
with col_header:
    st.markdown(
        "<h1 style='color: #0f172a; margin-bottom: 0px; font-weight: 800; letter-spacing: -0.03em; font-size: 34px;'>Dashboard</h1>",
        unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #64748b; font-size: 14.5px; margin-top: 4px; margin-bottom: 30px; font-weight: 500;'>All general information and parsed expense outlays appear in this field.</p>",
        unsafe_allow_html=True)

with col_action:
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    # Styled like secondary buttons in design
    if st.button("🚀 Load Demo Data", key="demobutton"):
        generate_mock_data()
        st.rerun()

# 5. Empty State Handling with a beautiful card
if df_expenses.empty:
    st.markdown("""
        <div style="background-color: #ffffff; border: 1px dashed #cbd5e1; border-radius: 24px; padding: 70px 40px; text-align: center; margin-top: 10px; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.02);">
            <div style="font-size: 54px; margin-bottom: 20px;">⚡</div>
            <h3 style="color: #0f172a; font-weight: 700; font-size: 20px; margin-bottom: 8px;">Your dashboard is currently quiet</h3>
            <p style="color: #64748b; font-size: 14px; max-width: 440px; margin: 0 auto 30px auto; line-height: 1.5;">Populate this space using the quick record card at the bottom of the page, or tap the premium 'Load Demo Data' shortcut to render the full visualization suite instantly.</p>
        </div>
    """, unsafe_allow_html=True)

    # First Entry Form (styled premium form)
    st.markdown("<h3 style='margin-top: 40px; font-weight: 700; letter-spacing: -0.02em;'>Log Your First Outflow</h3>",
                unsafe_allow_html=True)
    with st.form("first_expense_form", clear_on_submit=True):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            amount = st.number_input("Amount ($)", min_value=0.01, step=1.0)
            category = st.selectbox("Category",
                                    ["Food & Dining", "Rent & Housing", "Utilities", "Entertainment", "Shopping",
                                     "Transportation", "Other"])
        with f_col2:
            description = st.text_input("Description", placeholder="e.g., Gas, Groceries, Netflix")
            date = st.date_input("Date", datetime.now())

        submit = st.form_submit_button("Record Expense")
        if submit:
            new_row = pd.DataFrame(
                [{"Date": pd.to_datetime(date), "Amount": amount, "Category": category, "Description": description}])
            df_expenses = pd.concat([df_expenses, new_row], ignore_index=True)
            save_data(df_expenses)
            st.rerun()

else:
    # --- KPI METRICS (Rendered using high-fidelity SaaS markup directly mirroring uploaded image) ---
    total_spent = df_expenses["Amount"].sum()
    total_transactions = len(df_expenses)
    avg_expense = df_expenses["Amount"].mean() if total_transactions > 0 else 0

    # Identify top spending category for the descriptive sub-tags
    if not df_expenses.empty:
        top_category_series = df_expenses.groupby("Category")["Amount"].sum()
        top_cat = top_category_series.idxmax() if not top_category_series.empty else "N/A"
    else:
        top_cat = "N/A"

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

    # KPI 1: December Report style card
    with col_kpi1:
        st.markdown(f"""
            <div class="saas-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <span style="font-size: 28px;">📊</span>
                    <span class="saas-pill pill-purple">Interactive Analytics</span>
                </div>
                <h4 style="margin: 0px 0px 4px 0px; font-weight: 700; font-size: 18px; color: #0f172a;">Spending Report</h4>
                <p style="color: #64748b; font-size: 13px; line-height: 1.4; margin-bottom: 24px; margin-top: 0px;">Analyze overall outflow reports and categorical ratios to make informed strategic decisions.</p>
                <div style="display: flex; gap: 10px;">
                    <div style="background-color: #5244e3; color: white; border-radius: 12px; padding: 10px 18px; font-weight: 700; font-size: 13px; cursor: pointer; text-align: center; flex: 1;">Analyze Live</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # KPI 2: Total Outflow with mini bar graphics & percent trends
    with col_kpi2:
        # Create a tiny pseudo graph using real heights
        bar_heights = [random.randint(15, 45) for _ in range(8)]
        bars_html = "".join([f'<div class="mini-bar" style="height: {h}px;"></div>' for h in bar_heights])

        st.markdown(f"""
            <div class="saas-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div class="kpi-title">Total Outflow</div>
                    <span style="color: #64748b; font-size: 18px; font-weight: 700;">···</span>
                </div>
                <div class="kpi-value">${total_spent:,.2f}</div>
                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 15px;">
                    <div>
                        <span class="saas-pill pill-purple"># Top Outlay: {top_cat}</span>
                    </div>
                    <div class="mini-bar-chart">
                        {bars_html}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # KPI 3: Logged Transactions and Average Size
    with col_kpi3:
        bar_heights_alt = [random.randint(15, 45) for _ in range(8)]
        bars_html_alt = "".join([
                                    f'<div class="mini-bar" style="height: {h}px; background: linear-gradient(180deg, #e0f2fe 0%, #0284c7 100%);"></div>'
                                    for h in bar_heights_alt])

        st.markdown(f"""
            <div class="saas-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div class="kpi-title">Average Spending Size</div>
                    <span style="color: #64748b; font-size: 18px; font-weight: 700;">···</span>
                </div>
                <div class="kpi-value">${avg_expense:,.2f}</div>
                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 15px;">
                    <div>
                        <span class="saas-pill pill-green">{total_transactions} Transactions</span>
                        <span class="saas-pill pill-gray">Active Database</span>
                    </div>
                    <div class="mini-bar-chart">
                        {bars_html_alt}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- TOP FOCUS SECTION: LARGE DONUT CHART (The Core Focus Element) ---
    st.markdown(
        "<h3 style='color: #0f172a; margin-bottom: 2px; font-weight: 800; letter-spacing: -0.02em;'>Category Outlay Breakdown</h3>",
        unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #64748b; font-size: 13.5px; margin-bottom: 25px; font-weight: 500;'>Direct evaluation of expenditures by category sector.</p>",
        unsafe_allow_html=True)

    # Styled Outer Card for the chart
    with st.container():
        category_totals = df_expenses.groupby("Category")["Amount"].sum().reset_index()

        # Color palettes from the mockup (Indigo, Violet, Soft Lavenders, Grays, Pastel Blues)
        mockup_colors = ["#5244E3", "#6366F1", "#A5B4FC", "#C7D2FE", "#E0E7FF", "#4338CA", "#1E1B4B"]

        fig = px.pie(
            category_totals,
            values="Amount",
            names="Category",
            hole=0.65,  # Slightly wider opening for modern aesthetic
            color_discrete_sequence=mockup_colors
        )

        # Premium updates to rendering
        fig.update_traces(
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Outflow: $% {value:,.2f}<br>Ratio: %{percent}<extra></extra>",
            marker=dict(line=dict(color='#ffffff', width=3))  # Gap lines for premium look
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            height=380,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#334155")
        )

        # Standard container wrap for spacing
        st.markdown('<div class="saas-card" style="padding: 10px 0px;">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # --- BOTTOM SECTION: PREMIUM DUAL LAYOUT (Form & Styled Table Grid) ---
    bottom_col1, bottom_col2 = st.columns([1, 1.4])

    with bottom_col1:
        st.markdown(
            "<h3 style='color: #0f172a; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 5px;'>Record Outflow</h3>",
            unsafe_allow_html=True)
        st.markdown(
            "<p style='color: #64748b; font-size: 13px; margin-bottom: 15px;'>Manually log a single transaction into local storage.</p>",
            unsafe_allow_html=True)

        with st.form("input_form", clear_on_submit=True):
            amount = st.number_input("Amount ($)", min_value=0.01, step=1.0)
            category = st.selectbox("Category",
                                    ["Food & Dining", "Rent & Housing", "Utilities", "Entertainment", "Shopping",
                                     "Transportation", "Other"])
            description = st.text_input("Description", placeholder="e.g., Apple Store, Shell Gas, Starbucks")
            date = st.date_input("Date", datetime.now())

            submit = st.form_submit_button("Log Transaction")
            if submit:
                new_row = pd.DataFrame([{
                    "Date": pd.to_datetime(date),
                    "Amount": amount,
                    "Category": category,
                    "Description": description
                }])
                df_expenses = pd.concat([df_expenses, new_row], ignore_index=True)
                save_data(df_expenses)
                st.toast("Expense logged successfully!")
                st.rerun()

    with bottom_col2:
        st.markdown(
            "<h3 style='color: #0f172a; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 5px;'>Recent Transactions</h3>",
            unsafe_allow_html=True)
        st.markdown(
            "<p style='color: #64748b; font-size: 13px; margin-bottom: 15px;'>Sorted by most recent ledger occurrences.</p>",
            unsafe_allow_html=True)

        # Sort values
        df_display = df_expenses.copy()
        df_display = df_display.sort_values(by="Date", ascending=False).head(10)

        # Generate raw HTML Table to EXACTLY match the clean layout shown in user image
        # Note: We keep all string lines flush-left to prevent markdown from converting it into a literal code-block.
        table_html = """<table class="saas-table">
<thead>
<tr>
<th>Description</th>
<th>Category</th>
<th>Date Logged</th>
<th style="text-align: right;">Amount</th>
</tr>
</thead>
<tbody>"""


        # Category pill dynamic assignment helper
        def get_pill_class(cat):
            if "Rent" in cat:
                return "pill-red"
            elif "Food" in cat:
                return "pill-purple"
            elif "Utilities" in cat:
                return "pill-green"
            elif "Transportation" in cat:
                return "pill-blue"
            elif "Shopping" in cat:
                return "pill-orange"
            elif "Entertainment" in cat:
                return "pill-pink"
            else:
                return "pill-gray"


        for idx, row in df_display.iterrows():
            date_formatted = row['Date'].strftime('%b %d, %Y')
            pill_color = get_pill_class(row['Category'])

            table_html += f"""<tr>
<td style="font-weight: 600; color: #0f172a;">{row['Description']}</td>
<td><span class="saas-pill {pill_color}">{row['Category']}</span></td>
<td style="color: #64748b; font-weight: 500;">{date_formatted}</td>
<td style="text-align: right; font-weight: 700; color: #0f172a;">${row['Amount']:,.2f}</td>
</tr>"""

        table_html += "</tbody></table>"

        # Render the custom-designed tabular view
        st.markdown(table_html, unsafe_allow_html=True)