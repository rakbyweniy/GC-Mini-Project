import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os
import math
from html import escape
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

CATEGORY_COLORS = {
    "Food & Dining": "#5244E3",
    "Rent & Housing": "#EF4444",
    "Utilities": "#10B981",
    "Entertainment": "#EC4899",
    "Shopping": "#F97316",
    "Transportation": "#3B82F6",
    "Other": "#64748B",
}
FALLBACK_CHART_COLORS = ["#5244E3", "#6366F1", "#10B981", "#3B82F6", "#F97316", "#EC4899", "#64748B"]


def mix_hex_color(color, mix="#ffffff", amount=0.28):
    color = color.lstrip("#")
    mix = mix.lstrip("#")
    base_rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
    mix_rgb = tuple(int(mix[i:i + 2], 16) for i in (0, 2, 4))
    blended = tuple(round(base + (target - base) * amount) for base, target in zip(base_rgb, mix_rgb))
    return "#" + "".join(f"{channel:02X}" for channel in blended)


def get_category_color(category, index=0):
    return CATEGORY_COLORS.get(category, FALLBACK_CHART_COLORS[index % len(FALLBACK_CHART_COLORS)])


def polar_point(cx, cy, radius, angle):
    return cx + radius * math.cos(angle), cy + radius * math.sin(angle)


def donut_slice_path(start_angle, end_angle, outer_radius=148, inner_radius=82, cx=230, cy=185):
    span = end_angle - start_angle
    if span >= math.tau - 0.001:
        return (
            f"M {cx + outer_radius:.3f} {cy:.3f} "
            f"A {outer_radius} {outer_radius} 0 1 1 {cx - outer_radius:.3f} {cy:.3f} "
            f"A {outer_radius} {outer_radius} 0 1 1 {cx + outer_radius:.3f} {cy:.3f} "
            f"M {cx + inner_radius:.3f} {cy:.3f} "
            f"A {inner_radius} {inner_radius} 0 1 0 {cx - inner_radius:.3f} {cy:.3f} "
            f"A {inner_radius} {inner_radius} 0 1 0 {cx + inner_radius:.3f} {cy:.3f} Z"
        )

    outer_start = polar_point(cx, cy, outer_radius, start_angle)
    outer_end = polar_point(cx, cy, outer_radius, end_angle)
    inner_end = polar_point(cx, cy, inner_radius, end_angle)
    inner_start = polar_point(cx, cy, inner_radius, start_angle)
    large_arc = 1 if span > math.pi else 0

    return (
        f"M {outer_start[0]:.3f} {outer_start[1]:.3f} "
        f"A {outer_radius} {outer_radius} 0 {large_arc} 1 {outer_end[0]:.3f} {outer_end[1]:.3f} "
        f"L {inner_end[0]:.3f} {inner_end[1]:.3f} "
        f"A {inner_radius} {inner_radius} 0 {large_arc} 0 {inner_start[0]:.3f} {inner_start[1]:.3f} Z"
    )


def render_3d_donut_chart(category_totals):
    chart_data = category_totals[category_totals["Amount"] > 0].copy()
    chart_data = chart_data.sort_values("Amount", ascending=False).reset_index(drop=True)
    total = chart_data["Amount"].sum()

    if total <= 0:
        return

    depth_paths = []
    slice_paths = []
    legend_items = []
    current_angle = -math.pi / 2

    for index, row in chart_data.iterrows():
        amount = float(row["Amount"])
        category = str(row["Category"])
        span = (amount / total) * math.tau
        gap = min(0.018, span * 0.18) if len(chart_data) > 1 else 0
        segment_start = current_angle + gap
        segment_end = current_angle + span - gap
        mid_angle = current_angle + span / 2
        color = get_category_color(category, index)
        depth_color = mix_hex_color(color, "#0f172a", 0.38)
        category_label = escape(category, quote=True)
        percent = amount / total
        path = donut_slice_path(segment_start, segment_end)
        hover_dx = math.cos(mid_angle) * 10
        hover_dy = math.sin(mid_angle) * 10

        depth_paths.append(
            f'<path class="depth-path" d="{path}" fill="{depth_color}" fill-rule="evenodd"></path>'
        )
        slice_paths.append(f"""
            <g class="slice" data-index="{index}" data-label="{category_label}" data-value="${amount:,.2f}" data-percent="{percent:.1%}" style="--dx: {hover_dx:.2f}px; --dy: {hover_dy:.2f}px;">
                <path class="slice-main" d="{path}" fill="{color}" fill-rule="evenodd"></path>
            </g>
        """)
        legend_items.append(f"""
            <div class="legend-item" data-index="{index}">
                <span class="legend-swatch" style="background: {color};"></span>
                <span class="legend-copy">
                    <span class="legend-name">{category_label}</span>
                    <span class="legend-meta">{percent:.1%} · ${amount:,.2f}</span>
                </span>
            </div>
        """)
        current_angle += span

    depth_markup = "\n".join(depth_paths)
    slices_markup = "\n".join(slice_paths)
    legend_markup = "\n".join(legend_items)

    components.html(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
            * {{
                box-sizing: border-box;
            }}
            html,
            body {{
                margin: 0;
                background: transparent;
                font-family: 'Plus Jakarta Sans', sans-serif;
            }}
            .donut-card {{
                width: 100%;
                min-height: 410px;
                padding: 22px 24px;
                background: #ffffff;
                border: 1px solid #eef0f3;
                border-radius: 20px;
                box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.02), 0 10px 30px -5px rgba(15, 23, 42, 0.03);
            }}
            .donut-card:hover {{
                box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.06);
            }}
            .donut-layout {{
                display: grid;
                grid-template-columns: minmax(290px, 1fr) minmax(210px, 270px);
                align-items: center;
                gap: 18px;
            }}
            .chart-stage {{
                position: relative;
                min-height: 350px;
            }}
            .donut-svg {{
                width: 100%;
                height: 350px;
                display: block;
                overflow: visible;
            }}
            .depth-layer {{
                transform: translateY(16px);
                opacity: 0.34;
                filter: blur(0.1px);
                pointer-events: none;
            }}
            .slice {{
                cursor: pointer;
                transition: transform 160ms ease;
                transform-box: fill-box;
                transform-origin: center;
            }}
            .slice-main {{
                stroke: #ffffff;
                stroke-width: 4;
                paint-order: stroke fill;
                transition: filter 160ms ease, stroke-width 160ms ease;
            }}
            .slice:hover,
            .slice.is-active {{
                transform: translate(var(--dx), var(--dy));
            }}
            .slice:hover .slice-main,
            .slice.is-active .slice-main {{
                filter: brightness(1.08) saturate(1.08) drop-shadow(0 9px 14px rgba(15, 23, 42, 0.18));
                stroke-width: 5.5;
            }}
            .base-shadow {{
                fill: #0f172a;
                opacity: 0.06;
                pointer-events: none;
            }}
            .inner-hole {{
                fill: #ffffff;
                filter: drop-shadow(0 5px 12px rgba(15, 23, 42, 0.08));
                pointer-events: none;
            }}
            .total-value {{
                fill: #0f172a;
                font-size: 27px;
                font-weight: 800;
                letter-spacing: 0;
                text-anchor: middle;
            }}
            .total-label {{
                fill: #64748b;
                font-size: 12px;
                font-weight: 700;
                text-anchor: middle;
            }}
            .donut-tooltip {{
                position: absolute;
                z-index: 10;
                left: 0;
                top: 0;
                min-width: 160px;
                padding: 10px 12px;
                border-radius: 12px;
                background: #0f172a;
                color: #ffffff;
                box-shadow: 0 14px 30px rgba(15, 23, 42, 0.2);
                pointer-events: none;
                opacity: 0;
                transform: translate(14px, 14px);
                transition: opacity 120ms ease;
            }}
            .tooltip-title {{
                display: block;
                margin-bottom: 4px;
                font-size: 12px;
                font-weight: 800;
            }}
            .tooltip-meta {{
                display: block;
                color: #cbd5e1;
                font-size: 11.5px;
                font-weight: 600;
            }}
            .legend-list {{
                display: flex;
                flex-direction: column;
                gap: 7px;
            }}
            .legend-item {{
                display: flex;
                align-items: center;
                gap: 10px;
                min-height: 44px;
                padding: 8px 10px;
                border: 1px solid #eef0f3;
                border-radius: 12px;
                background: #ffffff;
                transition: background 160ms ease, border-color 160ms ease, transform 160ms ease;
            }}
            .legend-item:hover,
            .legend-item.is-active {{
                background: #f8fafc;
                border-color: #e2e8f0;
                transform: translateX(2px);
            }}
            .legend-swatch {{
                width: 10px;
                height: 28px;
                flex: 0 0 auto;
                border-radius: 999px;
            }}
            .legend-copy {{
                min-width: 0;
                display: flex;
                flex-direction: column;
                gap: 2px;
            }}
            .legend-name {{
                color: #0f172a;
                font-size: 12.5px;
                font-weight: 800;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            .legend-meta {{
                color: #64748b;
                font-size: 11px;
                font-weight: 700;
            }}
            @media (max-width: 680px) {{
                .donut-card {{
                    padding: 18px;
                }}
                .donut-layout {{
                    grid-template-columns: 1fr;
                }}
                .chart-stage,
                .donut-svg {{
                    min-height: 300px;
                    height: 300px;
                }}
            }}
        </style>
        <div class="donut-card">
            <div class="donut-layout">
                <div class="chart-stage">
                    <svg class="donut-svg" viewBox="0 0 460 380" role="img" aria-label="3D hollow spending donut chart">
                        <ellipse class="base-shadow" cx="230" cy="233" rx="151" ry="39"></ellipse>
                        <g class="depth-layer">
                            {depth_markup}
                        </g>
                        <g class="slice-layer">
                            {slices_markup}
                        </g>
                        <circle class="inner-hole" cx="230" cy="185" r="72"></circle>
                        <text class="total-value" x="230" y="180">${total:,.0f}</text>
                        <text class="total-label" x="230" y="202">Total Outflow</text>
                    </svg>
                    <div class="donut-tooltip" aria-hidden="true">
                        <span class="tooltip-title"></span>
                        <span class="tooltip-meta"></span>
                    </div>
                </div>
                <div class="legend-list">
                    {legend_markup}
                </div>
            </div>
        </div>
        <script>
            const root = document.currentScript.previousElementSibling;
            const tooltip = root.querySelector('.donut-tooltip');
            const tooltipTitle = root.querySelector('.tooltip-title');
            const tooltipMeta = root.querySelector('.tooltip-meta');
            const slices = Array.from(root.querySelectorAll('.slice'));
            const legendItems = Array.from(root.querySelectorAll('.legend-item'));

            function setActive(index) {{
                slices.forEach((slice) => slice.classList.toggle('is-active', slice.dataset.index === index));
                legendItems.forEach((item) => item.classList.toggle('is-active', item.dataset.index === index));
            }}

            function clearActive() {{
                setActive(null);
                tooltip.style.opacity = 0;
            }}

            function moveTooltip(event, slice) {{
                const bounds = root.querySelector('.chart-stage').getBoundingClientRect();
                tooltipTitle.textContent = slice.dataset.label;
                tooltipMeta.textContent = `${{slice.dataset.value}} · ${{slice.dataset.percent}}`;
                tooltip.style.left = `${{event.clientX - bounds.left}}px`;
                tooltip.style.top = `${{event.clientY - bounds.top}}px`;
                tooltip.style.opacity = 1;
            }}

            slices.forEach((slice) => {{
                slice.addEventListener('mouseenter', () => setActive(slice.dataset.index));
                slice.addEventListener('mousemove', (event) => moveTooltip(event, slice));
                slice.addEventListener('mouseleave', clearActive);
            }});

            legendItems.forEach((item) => {{
                item.addEventListener('mouseenter', () => setActive(item.dataset.index));
                item.addEventListener('mouseleave', clearActive);
            }});
        </script>
    """, height=455)


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
        render_3d_donut_chart(category_totals)

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
