"""
visualization.py

Chart and map functions. Redesigned for visual polish.
"""

import matplotlib.pyplot as plt
import numpy as np
import folium
from folium.plugins import MarkerCluster

from config import WORKPLACE_LAT, WORKPLACE_LON, WORKPLACE_NAME

# ---------------------------------------------------------------------------
# Design system
# ---------------------------------------------------------------------------
PALETTE = {
    "primary": "#2451B7",
    "primary_light": "#7FA6E8",
    "accent": "#00A896",
    "good": "#3E9B4F",
    "warn": "#F0A63A",
    "bad": "#D9534F",
    "neutral": "#8A94A6",
    "text": "#1F2430",
    "subtext": "#6B7280",
    "grid": "#E7E9EE",
}

GROUP_COLORS = {
    "<=30 min": "#3E9B4F", "31-45 min": "#8FBF52", "46-60 min": "#F0A63A", ">60 min": "#D9534F",
}
ADOPTION_COLORS = {
    "High potential": "#3E9B4F", "Medium potential": "#F0A63A", "Low potential": "#D9534F",
}

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": PALETTE["grid"],
    "axes.labelcolor": PALETTE["subtext"],
    "axes.titlecolor": PALETTE["text"],
    "text.color": PALETTE["text"],
    "xtick.color": PALETTE["subtext"],
    "ytick.color": PALETTE["subtext"],
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 10.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.grid": True,
    "grid.color": PALETTE["grid"],
    "grid.linewidth": 0.8,
    "axes.axisbelow": True,
    "figure.dpi": 130,
})


def _style_axes(ax, hide_y_grid=False):
    ax.tick_params(length=0)
    if hide_y_grid:
        ax.yaxis.grid(False)
    else:
        ax.xaxis.grid(False)


def plot_commute_time_distribution(df, save_path=None):
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.hist(df["door_to_door_time_min"], bins=28, color=PALETTE["primary"],
            edgecolor="white", linewidth=0.6, alpha=0.9)
    for x, label in [(30, "30"), (45, "45"), (60, "60")]:
        ax.axvline(x, color=PALETTE["neutral"], linestyle=(0, (3, 3)), linewidth=1)
        ax.text(x, ax.get_ylim()[1] * 0.98, label, ha="center", va="top",
                fontsize=9, color=PALETTE["subtext"])
    ax.set_title("How long would the commute take?")
    ax.set_xlabel("Estimated door-to-door time (minutes)")
    ax.set_ylabel("Employees")
    _style_axes(ax)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
    return fig


def plot_commute_groups(df, save_path=None):
    order = ["<=30 min", "31-45 min", "46-60 min", ">60 min"]
    counts = df["commute_group"].value_counts().reindex(order)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    colors = [GROUP_COLORS[g] for g in order]
    bars = ax.bar(order, counts.values, color=colors, width=0.62)
    ax.set_title("Employees by commute-time group")
    ax.set_ylabel("Employees")
    for bar, val in zip(bars, counts.values):
        pct = 100 * val / len(df)
        ax.text(bar.get_x() + bar.get_width() / 2, val + max(counts.values) * 0.02,
                f"{pct:.0f}%", ha="center", va="bottom", fontsize=10.5,
                color=PALETTE["text"], fontweight="bold")
    ax.set_ylim(0, max(counts.values) * 1.18)
    _style_axes(ax)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
    return fig


def plot_adoption_distribution(df, save_path=None):
    order = ["Low potential", "Medium potential", "High potential"]
    counts = df["adoption_potential_group"].value_counts().reindex(order)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    colors = [ADOPTION_COLORS[g] for g in order]
    bars = ax.barh(order, counts.values, color=colors, height=0.55)
    ax.set_title("Deutschlandticket adoption potential")
    ax.set_xlabel("Employees")
    for bar, val in zip(bars, counts.values):
        pct = 100 * val / len(df)
        ax.text(val + max(counts.values) * 0.02, bar.get_y() + bar.get_height() / 2,
                f"{val}  ({pct:.0f}%)", va="center", fontsize=10.5, color=PALETTE["text"])
    ax.set_xlim(0, max(counts.values) * 1.28)
    _style_axes(ax, hide_y_grid=True)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
    return fig


def plot_area_summary(area_summary_df, save_path=None):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    d1 = area_summary_df.sort_values("mean_door_to_door_min")
    axes[0].barh(d1["home_area"], d1["mean_door_to_door_min"], color=PALETTE["primary"], height=0.6)
    axes[0].set_title("Mean commute time by area", fontsize=12.5)
    axes[0].set_xlabel("Minutes")
    _style_axes(axes[0], hide_y_grid=True)

    d2 = area_summary_df.sort_values("mean_adoption_score")
    axes[1].barh(d2["home_area"], d2["mean_adoption_score"], color=PALETTE["accent"], height=0.6)
    axes[1].set_title("Mean adoption-potential score by area", fontsize=12.5)
    axes[1].set_xlabel("Score (0-100)")
    _style_axes(axes[1], hide_y_grid=True)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
    return fig


def plot_commute_vs_adoption(df, save_path=None):
    fig, ax = plt.subplots(figsize=(7, 4.8))
    colors = df["adoption_potential_group"].map(ADOPTION_COLORS)
    ax.scatter(df["door_to_door_time_min"], df["adoption_potential_score"],
               c=colors, alpha=0.55, s=22, linewidths=0)
    ax.set_xlabel("Door-to-door commute time (minutes)")
    ax.set_ylabel("Adoption-potential score")
    ax.set_title("Commute time vs. adoption potential")
    handles = [plt.Line2D([0], [0], marker="o", linestyle="", color=c, markersize=8)
               for c in ADOPTION_COLORS.values()]
    ax.legend(handles, ADOPTION_COLORS.keys(), frameon=False, loc="upper right", fontsize=9.5)
    _style_axes(ax)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
    return fig


def plot_employees_by_area(df, save_path=None):
    counts = df["home_area"].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(7, 4.8))
    ax.barh(counts.index, counts.values, color=PALETTE["primary_light"], height=0.6)
    ax.set_title("Synthetic employees by home area")
    ax.set_xlabel("Employees")
    _style_axes(ax, hide_y_grid=True)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
    return fig


def plot_distance_to_station(df, save_path=None):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(df["distance_to_station_km"], bins=24, color=PALETTE["accent"],
            edgecolor="white", linewidth=0.6, alpha=0.9)
    ax.set_title("Distance to nearest reference station")
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Employees")
    _style_axes(ax)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
    return fig


def plot_geography_overview(stations_df, residential_areas, save_path=None):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(stations_df["lon"], stations_df["lat"], c=PALETTE["neutral"], s=40,
               label="Reference station", zorder=3, edgecolors="white", linewidths=0.5)
    ax.scatter([WORKPLACE_LON], [WORKPLACE_LAT], c=PALETTE["bad"], marker="*", s=320,
               label="Workplace", zorder=4, edgecolors="white", linewidths=0.5)
    for r in residential_areas:
        ax.scatter(r["lon"], r["lat"], c=PALETTE["primary_light"], s=70, zorder=2,
                   edgecolors="white", linewidths=0.5)
        ax.annotate(r["name"], (r["lon"], r["lat"]), fontsize=8.5, color=PALETTE["subtext"],
                    xytext=(5, 4), textcoords="offset points")
    ax.set_title("Workplace, stations, and residential anchors")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend(frameon=False, loc="lower left", fontsize=9.5)
    _style_axes(ax)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
    return fig


def build_interactive_map(df, stations_df, save_path=None):
    """
    Folium map: workplace, HVV reference stations, synthetic employee homes
    coloured by commute-time group, plus a simple layer highlighting
    high-adoption-potential employees. All employee markers are explicitly
    labelled as synthetic in the popup.
    """
    m = folium.Map(location=[WORKPLACE_LAT, WORKPLACE_LON], zoom_start=11, tiles="cartodbpositron")

    folium.Marker(
        [WORKPLACE_LAT, WORKPLACE_LON],
        popup=f"<b>{WORKPLACE_NAME}</b><br>Workplace",
        icon=folium.Icon(color="black", icon="briefcase", prefix="fa"),
    ).add_to(m)

    station_layer = folium.FeatureGroup(name="HVV/AKN reference stations")
    for _, s in stations_df.iterrows():
        folium.CircleMarker(
            [s["lat"], s["lon"]], radius=5, color="#333333", fill=True, fill_opacity=0.8,
            popup=f"{s['name']} ({s['line']})",
        ).add_to(station_layer)
    station_layer.add_to(m)

    employee_layer = folium.FeatureGroup(name="Synthetic employees (by commute group)")
    cluster = MarkerCluster().add_to(employee_layer)
    for _, e in df.iterrows():
        folium.CircleMarker(
            [e["home_lat"], e["home_lon"]], radius=4,
            color=GROUP_COLORS.get(e["commute_group"], "grey"), fill=True, fill_opacity=0.7,
            popup=(
                f"<b>Synthetic employee</b> {e['employee_id']}<br>"
                f"Area: {e['home_area']}<br>"
                f"Est. door-to-door: {e['door_to_door_time_min']:.0f} min<br>"
                f"Adoption potential: {e['adoption_potential_group']} "
                f"({e['adoption_potential_score']:.0f})"
            ),
        ).add_to(cluster)
    employee_layer.add_to(m)

    high_potential_layer = folium.FeatureGroup(name="High-potential DT users", show=False)
    high_df = df[df["adoption_potential_group"] == "High potential"]
    for _, e in high_df.iterrows():
        folium.CircleMarker(
            [e["home_lat"], e["home_lon"]], radius=6, color="#1B5E20", fill=True, fill_opacity=0.9,
            popup=f"High potential: {e['employee_id']} ({e['adoption_potential_score']:.0f})",
        ).add_to(high_potential_layer)
    high_potential_layer.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    if save_path:
        m.save(save_path)
    return m
