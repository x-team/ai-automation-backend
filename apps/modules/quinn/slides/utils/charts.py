import base64
import collections
import io
import secrets
import time
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


def get_random_hex_colors(n: int) -> list[str]:
    """Generate n random hex colors."""

    return [
        secrets.choice(
            [
                "#6D24E5",
                "#DFCEFC",
                "#E2E2E3",
                "#F2F2F2",
                "#B6B6B6",
            ],
        )
        for _ in range(n)
    ]


def create_bar_chart(chart_data: dict[str, Any], title: str, colors: list[str]) -> str:
    """Create a bar chart."""

    plt.figure(figsize=(10, 6))
    plt.bar(chart_data.get("x", []), chart_data.get("y", []), color=colors)

    plt.title(title, fontsize=16, pad=20)
    plt.ylabel(chart_data.get("y_label", ""), fontsize=12)
    plt.xlabel(chart_data.get("x_label", ""), fontsize=12)

    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close()
    image_bytes = buf.getvalue()
    buf.close()

    return base64.b64encode(image_bytes).decode("utf-8")


def create_line_chart(chart_data: dict[str, Any], title: str) -> str:
    """Create a line chart."""

    plt.figure(figsize=(10, 6))
    plt.plot(
        chart_data.get("x", []),
        chart_data.get("y", []),
        color="#4A90E2",
        marker="o",
        linestyle="-",
    )

    plt.title(title, fontsize=16, pad=20)
    plt.ylabel(chart_data.get("y_label", ""), fontsize=12)
    plt.xlabel(chart_data.get("x_label", ""), fontsize=12)

    plt.xticks(rotation=45, ha="right")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close()
    image_bytes = buf.getvalue()
    buf.close()

    return base64.b64encode(image_bytes).decode("utf-8")


def create_pie_chart(
    chart_data: dict[str, Any],
    title: str,
    colors: list[str],
) -> str:
    """Create a pie chart."""

    plt.figure(figsize=(8, 8))
    plt.pie(
        chart_data.get("sizes", []),
        labels=chart_data.get("labels", []),
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"width": 0.4, "edgecolor": "w"},
        pctdistance=0.8,
        textprops={"color": "w", "weight": "bold"},
    )
    plt.title(title, fontsize=16, pad=20)
    plt.axis("equal")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close()
    image_bytes = buf.getvalue()
    buf.close()

    return base64.b64encode(image_bytes).decode("utf-8")


def prepare_chart_data(  # noqa: C901
    chart_info: dict[str, Any],
    survey_data: list[dict[str, Any]],
) -> dict[str, Any]:
    """Prepare chart data for plotting."""

    chart_type = chart_info.get("type")
    chart_data = chart_info.get("data", {})
    data_for_plotting = {}

    if chart_type == "pie":
        header = chart_data.get("values", {}).get("header_column", None)
        responses = collections.Counter(
            [row.get(header) for row in survey_data if row.get(header)],
        )

        data_for_plotting = {
            "labels": list(responses.keys()),
            "sizes": list(responses.values()),
        }
    elif chart_type in ["bar", "line"]:
        group_by_col = chart_data.get("x", {}).get("header_column")
        value_col = chart_data.get("y", {}).get("header_column")

        if not group_by_col or not value_col:
            return {}

        grouped_data = collections.defaultdict(list)
        is_numeric_data = None

        for row in survey_data:
            key = row.get(group_by_col)
            value = row.get(value_col)

            if key and value is not None and str(value).strip() != "":
                if is_numeric_data is None:
                    is_numeric_data = str(value).replace(".", "", 1).isdigit()

                if is_numeric_data:
                    if str(value).replace(".", "", 1).isdigit():
                        grouped_data[key].append(float(value))
                else:
                    grouped_data[key].append(value)

        data_for_plotting = {}
        if grouped_data:
            if is_numeric_data:
                sorted_results = sorted(
                    [(k, np.mean(v)) for k, v in grouped_data.items()],
                    key=lambda item: item[1],
                    reverse=True,
                )
                y_label_text = "Average " + (
                    chart_data.get("y", {}).get("label") or "Value"
                )
            else:
                sorted_results = sorted(
                    [(k, np.float64(len(v))) for k, v in grouped_data.items()],
                    key=lambda item: item[1],
                    reverse=True,
                )
                y_label_text = "Count of " + (
                    chart_data.get("y", {}).get("label") or "Responses"
                )

            data_for_plotting = {
                "x": [item[0] for item in sorted_results],
                "x_label": chart_data.get("x", {}).get("label", None),
                "y": [round(item[1], 2) for item in sorted_results],
                "y_label": y_label_text,
            }

    return data_for_plotting


def process_slides_and_generate_charts(
    slides_definition: list[dict[str, Any]],
    survey_data: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Process slides and generate charts."""

    base64_charts = []

    for index, slide in enumerate(slides_definition):
        if slide.get("chart"):
            chart_info = slide["chart"]
            chart_title = chart_info.get("title", slide.get("title", "Untitled"))
            chart_type = chart_info.get("type")

            plot_data = prepare_chart_data(chart_info, survey_data)
            if not plot_data:
                continue

            num_points = len(plot_data.get("x", [])) or len(plot_data.get("labels", []))
            colors = get_random_hex_colors(num_points) if num_points > 0 else []
            base64_string = None

            if chart_type == "bar":
                base64_string = create_bar_chart(plot_data, chart_title, colors)
            elif chart_type == "pie":
                base64_string = create_pie_chart(plot_data, chart_title, colors)
            elif chart_type == "line":
                base64_string = create_line_chart(plot_data, chart_title)

            if base64_string:
                timestamp = time.time_ns()
                unique_title = f"{slide.get('title', 'chart').lower().replace(' ', '_')}_{timestamp}"
                base64_charts.append(
                    {
                        "title": unique_title,
                        "data": base64_string,
                        "index": index,
                    },
                )

    return base64_charts
