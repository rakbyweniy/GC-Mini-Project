import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import os
import math
import re
import hmac
import secrets
import hashlib
from html import escape
from datetime import datetime, timedelta
import random

# 1. Page Configuration (Full layout with custom icon and collapsed sidebar)
st.set_page_config(page_title="Budget Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. Complete High-Fidelity CSS overrides mimicking the uploaded design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global Overrides */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #0f172a;
    }

    .block-container {
        padding-top: 112px !important;
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
        caret-color: #5244e3 !important;
        font-size: 14px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    input,
    textarea,
    [contenteditable="true"] {
        caret-color: #5244e3 !important;
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

    /* Clear auth mode switcher */
    div[data-testid="stTabs"] [role="tablist"] {
        gap: 10px;
        margin-bottom: 16px;
    }
    div[data-testid="stTabs"] button[role="tab"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        color: #334155 !important;
        font-weight: 800 !important;
        padding: 10px 18px !important;
    }
    div[data-testid="stTabs"] button[role="tab"] * {
        color: inherit !important;
        font-size: 14px !important;
        font-weight: 800 !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background-color: #5244e3 !important;
        border-color: #5244e3 !important;
        color: #ffffff !important;
        box-shadow: 0 8px 16px -4px rgba(82, 68, 227, 0.3) !important;
    }
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* Fixed top-right dashboard actions */
    .st-key-top_actions {
        position: fixed;
        top: 74px;
        right: 28px;
        z-index: 9999;
        width: 310px;
    }
    .st-key-top_actions [data-testid="stHorizontalBlock"] {
        display: flex;
        gap: 12px;
        flex-wrap: nowrap;
    }
    .st-key-top_actions [data-testid="column"] {
        padding: 0 !important;
        min-width: 0 !important;
    }
    .st-key-top_actions .stButton>button {
        min-height: 44px;
        padding: 0 18px;
        white-space: nowrap;
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
    
    .weekly-bar-card {
        background: #ffffff;
        border: 1px solid #eef0f3;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.02), 0 10px 30px -5px rgba(15, 23, 42, 0.03);
        margin-top: 18px;
    }

    .weekly-bars {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 14px;
        align-items: end;
        min-height: 280px;
        padding-top: 20px;
    }

    .weekly-bar-wrap {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        min-width: 0;
    }

    .weekly-bar-value {
        color: #0f172a;
        font-size: 12px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 8px;
    }

    .weekly-bar {
        width: 100%;
        min-height: 8px;
        border-radius: 14px 14px 8px 8px;
        background: linear-gradient(180deg, #ede9fe 0%, #5244e3 100%);
        box-shadow: 0 10px 22px -10px rgba(82, 68, 227, 0.55);
    }

    .weekly-bar-date {
        color: #64748b;
        font-size: 11px;
        font-weight: 800;
        text-align: center;
        margin-top: 10px;
        white-space: nowrap;
    }
        .st-key-category_button_food_dining button {
        background-color: #5244e3 !important;
        color: #ffffff !important;
        border-color: #5244e3 !important;
    }

    .st-key-category_button_rent_housing button {
        background-color: #ef4444 !important;
        color: #ffffff !important;
        border-color: #ef4444 !important;
    }

    .st-key-category_button_utilities button {
        background-color: #10b981 !important;
        color: #ffffff !important;
        border-color: #10b981 !important;
    }

    .st-key-category_button_entertainment button {
        background-color: #ec4899 !important;
        color: #ffffff !important;
        border-color: #ec4899 !important;
    }

    .st-key-category_button_shopping button {
        background-color: #f97316 !important;
        color: #ffffff !important;
        border-color: #f97316 !important;
    }

    .st-key-category_button_transportation button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border-color: #3b82f6 !important;
    }

    .st-key-category_button_other button {
        background-color: #64748b !important;
        color: #ffffff !important;
        border-color: #64748b !important;
    }

    [class*="st-key-category_button_"] button:hover {
        filter: brightness(0.92);
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

LEGACY_CSV_FILE = "expenses.csv"
DATA_DIR = "data"
USER_DATA_DIR = os.path.join(DATA_DIR, "expenses")
USERS_FILE = os.path.join(DATA_DIR, "users.csv")
CSV_FILE = LEGACY_CSV_FILE
USER_COLUMNS = ["username", "salt", "password_hash", "created_at"]
EXPENSE_COLUMNS = ["Date", "Amount", "Category", "Description"]
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,32}$")

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

def clear_category_view():
    st.session_state["selected_category"] = None


def build_weekly_category_spending(df, category):
    category_df = df[df["Category"] == category].copy()

    if category_df.empty:
        end_date = pd.Timestamp(datetime.now().date())
    else:
        end_date = category_df["Date"].max().normalize()

    start_date = end_date - pd.Timedelta(days=6)
    week_dates = pd.date_range(start=start_date, end=end_date, freq="D")

    weekly = (
        category_df[
            (category_df["Date"] >= start_date)
            & (category_df["Date"] <= end_date + pd.Timedelta(days=1))
        ]
        .assign(Day=lambda data: data["Date"].dt.normalize())
        .groupby("Day")["Amount"]
        .sum()
        .reindex(week_dates, fill_value=0)
        .reset_index()
    )

    weekly.columns = ["Date", "Amount"]
    return weekly

def get_category_graph_color(category):
    if "Rent" in category:
        return "#ef4444"
    elif "Food" in category:
        return "#5244e3"
    elif "Utilities" in category:
        return "#10b981"
    elif "Transportation" in category:
        return "#3b82f6"
    elif "Shopping" in category:
        return "#f97316"
    elif "Entertainment" in category:
        return "#ec4899"
    else:
        return "#64748b"
def render_weekly_category_bar_chart(weekly_df, category):
    max_amount = weekly_df["Amount"].max()
    max_amount = max_amount if max_amount > 0 else 1
    total = weekly_df["Amount"].sum()
    bar_color = get_category_graph_color(category)
    bar_light_color = mix_hex_color(bar_color, "#ffffff", 0.78)

    bars_html = ""

    for _, row in weekly_df.iterrows():
        amount = float(row["Amount"])
        height = max(8, (amount / max_amount) * 220) if amount > 0 else 8
        date_label = row["Date"].strftime("%b %d")

        bars_html += f"""
        <div class="weekly-bar-wrap">
            <div class="weekly-bar-value">${amount:,.0f}</div>
            <div class="weekly-bar" style="height: {height:.0f}px; background: linear-gradient(180deg, {bar_light_color} 0%, {bar_color} 100%); box-shadow: 0 10px 22px -10px {bar_color};"></div>
            <div class="weekly-bar-date">{date_label}</div>
        </div>
        """

    components.html(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        body {{
            margin: 0;
            background: transparent;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}

        .weekly-bar-card {{
            background: #ffffff;
            border: 1px solid #eef0f3;
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.02), 0 10px 30px -5px rgba(15, 23, 42, 0.03);
        }}

        .kpi-title {{
            color: #64748b;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .kpi-value {{
            color: #0f172a;
            font-weight: 800;
            font-size: 32px;
            line-height: 1.1;
            margin-bottom: 12px;
        }}

        .saas-pill {{
            display: inline-flex;
            align-items: center;
            padding: 5px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
            margin-right: 6px;
            margin-bottom: 4px;
            border: 1px solid transparent;
        }}

        .pill-purple {{
            background-color: #f5f3ff;
            color: #5244e3;
            border-color: #ede9fe;
        }}

        .pill-gray {{
            background-color: #f8fafc;
            color: #64748b;
            border-color: #f1f5f9;
        }}

        .weekly-bars {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 14px;
            align-items: end;
            min-height: 280px;
            padding-top: 20px;
        }}

        .weekly-bar-wrap {{
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            min-width: 0;
        }}

        .weekly-bar-value {{
            color: #0f172a;
            font-size: 12px;
            font-weight: 800;
            text-align: center;
            margin-bottom: 8px;
        }}

        .weekly-bar {{
            width: 100%;
            min-height: 8px;
            border-radius: 14px 14px 8px 8px;
            background: linear-gradient(180deg, #ede9fe 0%, #5244e3 100%);
            box-shadow: 0 10px 22px -10px rgba(82, 68, 227, 0.55);
        }}

        .weekly-bar-date {{
            color: #64748b;
            font-size: 11px;
            font-weight: 800;
            text-align: center;
            margin-top: 10px;
            white-space: nowrap;
        }}
    </style>

    <div class="weekly-bar-card">
        <div>
            <div class="kpi-title">Weekly Category Spend</div>
            <div class="kpi-value">${total:,.2f}</div>
            <span class="saas-pill" style="background-color: {bar_light_color}; color: {bar_color}; border-color: {bar_light_color};">
                {escape(category)}
            </span>
            <span class="saas-pill pill-gray">Most recent 7 days</span>
        </div>

        <div class="weekly-bars">
            {bars_html}
        </div>
    </div>
    """, height=430)

def render_category_detail_view(df_expenses, category):
    category_color = get_category_color(category)
    weekly_df = build_weekly_category_spending(df_expenses, category)

    st.markdown(f"""
        <h1 style='color: #0f172a; margin-bottom: 0px; font-weight: 800; letter-spacing: -0.03em; font-size: 34px;'>
            {escape(category)}
        </h1>
        <p style='color: #64748b; font-size: 14.5px; margin-top: 4px; margin-bottom: 22px; font-weight: 500;'>
            See spending for last 7 days.
        </p>
    """, unsafe_allow_html=True)

    if st.button("← Back to Dashboard", key="back_to_dashboard"):
        clear_category_view()
        st.rerun()

    render_weekly_category_bar_chart(weekly_df, category)

    category_transactions = (
        df_expenses[df_expenses["Category"] == category]
        .sort_values("Date", ascending=False)
        .head(8)
    )

    st.markdown(
        "<h3 style='color: #0f172a; font-weight: 800; letter-spacing: -0.02em; margin-top: 34px;'>Recent Category Transactions</h3>",
        unsafe_allow_html=True,
    )

    if category_transactions.empty:
        st.info("No transactions found for this category.")
    else:
        for _, row in category_transactions.iterrows():
            st.markdown(f"""
                <div class="saas-card" style="padding: 16px 18px; margin-bottom: 10px; border-left: 5px solid {category_color};">
                    <div style="display: flex; justify-content: space-between; gap: 16px; align-items: center;">
                        <div>
                            <div style="font-weight: 800; color: #0f172a; font-size: 14px;">
                                {escape(str(row["Description"]))}
                            </div>
                            <div style="color: #64748b; font-size: 12px; font-weight: 700; margin-top: 3px;">
                                {row["Date"].strftime("%b %d, %Y")}
                            </div>
                        </div>
                        <div style="font-weight: 800; color: #0f172a; font-size: 16px;">
                            ${row["Amount"]:,.2f}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

def get_category_button_key(category):
    key = category.lower()
    key = key.replace("&", "")
    key = re.sub(r"[^a-z0-9]+", "_", key)
    key = key.strip("_")
    return key


def render_category_buttons(category_totals):
    st.markdown(
        "<p style='color: #64748b; font-size: 13.5px; margin-top: 18px; margin-bottom: 12px; font-weight: 700;'>Click a category to inspect weekly spending.</p>",
        unsafe_allow_html=True,
    )

    categories = category_totals.sort_values("Amount", ascending=False)["Category"].tolist()
    cols = st.columns(min(4, max(1, len(categories))))

    for index, category in enumerate(categories):
        safe_key = get_category_button_key(category)

        with cols[index % len(cols)]:
            with st.container(key=f"category_button_{safe_key}"):
                if st.button(category, key=f"category_detail_{safe_key}", use_container_width=True):
                    st.session_state["selected_category"] = category
                    st.rerun()
# 3. Account Management, Data Loading, Writing and Mock Generators
def ensure_storage():
    os.makedirs(USER_DATA_DIR, exist_ok=True)


def normalize_username(username):
    return username.strip().lower()


def is_valid_username(username):
    return bool(USERNAME_PATTERN.fullmatch(username))


def hash_password(password, salt):
    password_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")
    digest = hashlib.pbkdf2_hmac("sha256", password_bytes, salt_bytes, 120_000)
    return digest.hex()


def load_users():
    ensure_storage()
    if not os.path.exists(USERS_FILE):
        return pd.DataFrame(columns=USER_COLUMNS)

    try:
        users = pd.read_csv(USERS_FILE, dtype=str)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=USER_COLUMNS)

    for column in USER_COLUMNS:
        if column not in users.columns:
            users[column] = ""

    return users[USER_COLUMNS].fillna("")


def save_users(users):
    ensure_storage()
    users[USER_COLUMNS].to_csv(USERS_FILE, index=False)


def get_user_expense_file(username):
    user_key = hashlib.sha256(username.encode("utf-8")).hexdigest()[:24]
    return os.path.join(USER_DATA_DIR, f"{user_key}.csv")


def ensure_user_expense_file(username):
    expense_file = get_user_expense_file(username)
    if not os.path.exists(expense_file):
        pd.DataFrame(columns=EXPENSE_COLUMNS).to_csv(expense_file, index=False)


def register_user(username, password):
    username = normalize_username(username)
    if not is_valid_username(username):
        return False, "Username must be 3-32 characters and use only letters, numbers, or underscores."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    users = load_users()
    if username in users["username"].str.lower().tolist():
        return False, "That username already exists."

    salt = secrets.token_hex(16)
    new_user = pd.DataFrame([{
        "username": username,
        "salt": salt,
        "password_hash": hash_password(password, salt),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }])
    save_users(pd.concat([users, new_user], ignore_index=True))
    ensure_user_expense_file(username)
    return True, "Account created."


def authenticate_user(username, password):
    username = normalize_username(username)
    users = load_users()
    matches = users[users["username"].str.lower() == username]

    if matches.empty:
        return False

    user = matches.iloc[0]
    expected_hash = str(user["password_hash"])
    password_hash = hash_password(password, str(user["salt"]))
    return hmac.compare_digest(password_hash, expected_hash)


def sign_in(username):
    username = normalize_username(username)
    ensure_user_expense_file(username)
    st.session_state["authenticated"] = True
    st.session_state["username"] = username


def sign_out():
    st.session_state["authenticated"] = False
    st.session_state.pop("username", None)
    st.session_state.pop("selected_category", None)


def render_top_actions():
    with st.container(key="top_actions"):
        demo_action, logout_action = st.columns([1.45, 1])
        with demo_action:
            if st.button("🚀 Load Demo Data", key="demobutton"):
                generate_mock_data()
                st.rerun()
        with logout_action:
            if st.button("Log Out", key="logoutbutton"):
                sign_out()
                st.rerun()


def render_auth_screen():
    _, auth_col, _ = st.columns([1.35, 0.9, 1.35])
    with auth_col:
        st.markdown("""
            <div class="saas-card" style="margin-top: 80px; margin-bottom: 12px; padding: 20px;">
                <p style="color: #64748b; font-size: 14px; margin: 0; line-height: 1.5;">Sign in or create an account to keep each person's dashboard and transactions separate.</p>
            </div>
        """, unsafe_allow_html=True)

        login_tab, register_tab = st.tabs(["Log In", "Create Account"])

        with login_tab:
            with st.form("login_form"):
                login_username = st.text_input("Username", key="login_username")
                login_password = st.text_input("Password", type="password", key="login_password")
                login_submit = st.form_submit_button("Login")

                if login_submit:
                    if authenticate_user(login_username, login_password):
                        sign_in(login_username)
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        with register_tab:
            with st.form("register_form"):
                register_username = st.text_input("Username", key="register_username")
                register_password = st.text_input("Password", type="password", key="register_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
                register_submit = st.form_submit_button("Create New Account")

                if register_submit:
                    if register_password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        created, message = register_user(register_username, register_password)
                        if created:
                            sign_in(register_username)
                            st.rerun()
                        else:
                            st.error(message)


def load_data():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=EXPENSE_COLUMNS)

        for column in EXPENSE_COLUMNS:
            if column not in df.columns:
                df[column] = None

        df = df[EXPENSE_COLUMNS]
        df['Date'] = pd.to_datetime(df['Date'], errors="coerce")
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
        df = df.dropna(subset=["Date"])
        return df
    else:
        return pd.DataFrame(columns=EXPENSE_COLUMNS)


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


ensure_storage()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = None

if not st.session_state["authenticated"]:
    render_auth_screen()
    st.stop()

current_user = st.session_state.get("username")
if not current_user:
    sign_out()
    st.rerun()

CSV_FILE = get_user_expense_file(current_user)
ensure_user_expense_file(current_user)

# Initialize Data
df_expenses = load_data()
current_user_label = escape(current_user, quote=True)
render_top_actions()
selected_category = st.session_state.get("selected_category")

if selected_category:
    render_category_detail_view(df_expenses, selected_category)
    st.stop()
# 4. Header Area matching the crisp mockup alignment
col_header, _ = st.columns([2.15, 1.15])
with col_header:
    st.markdown(
        "<h1 style='color: #0f172a; margin-bottom: 0px; font-weight: 800; letter-spacing: -0.03em; font-size: 34px;'>Dashboard</h1>",
        unsafe_allow_html=True)
    st.markdown(f"""
        <p style='color: #64748b; font-size: 14.5px; margin-top: 4px; margin-bottom: 30px; font-weight: 500;'>
            Signed in as <strong>@{current_user_label}</strong>. This dashboard only shows this account's expense data.
        </p>
    """, unsafe_allow_html=True)

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
        render_category_buttons(category_totals)

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
            category_text = str(row['Category'])
            description_text = str(row['Description'])
            pill_color = get_pill_class(category_text)

            table_html += f"""<tr>
<td style="font-weight: 600; color: #0f172a;">{escape(description_text)}</td>
<td><span class="saas-pill {pill_color}">{escape(category_text)}</span></td>
<td style="color: #64748b; font-weight: 500;">{date_formatted}</td>
<td style="text-align: right; font-weight: 700; color: #0f172a;">${row['Amount']:,.2f}</td>
</tr>"""

        table_html += "</tbody></table>"

        # Render the custom-designed tabular view
        st.markdown(table_html, unsafe_allow_html=True)
