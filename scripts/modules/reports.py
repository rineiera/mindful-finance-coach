"""报告渲染模块"""
import html
import os
from datetime import datetime

from modules.store import ensure_dir, OUTPUT_DIR


def render_report(params: dict) -> dict:
    title = params.get("title", "报告")
    content = params.get("content", "")
    filename = params.get("filename", f"report_{datetime.now().strftime('%Y-%m-%d')}.html")

    ensure_dir()

    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")
    template_path = os.path.join(template_dir, "base.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    else:
        template = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>{{ title }}</title></head><body>{{ content }}</body></html>"

    safe_title = html.escape(title)
    safe_content = html.escape(content)
    html_output = template.replace("{{ title }}", safe_title).replace("{{ content }}", safe_content)

    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    return {"success": True, "path": output_path, "filename": filename}


COMMANDS = {
    "render_report": render_report,
}
