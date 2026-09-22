"""Report generation functions for task, review, and payment summaries."""

from pathlib import Path

from clients_management import ClientManager, build_client_payment_report_text
from translations import T


def build_task_log_report_text(plan=None, client_name=""):
    lines = [T("Task log"), "====================", ""]
    if plan is not None:
        plan_client = getattr(plan, "client_name", "") or client_name
        if getattr(plan, "client", None) is not None and not plan_client:
            plan_client = getattr(plan.client, "name", "")
        name = str(plan_client or T("No client selected")).strip()
        progress = getattr(plan, "progress", 0)
        lines.extend([f"Client: {name}", f"Progress: {progress}%", ""])
        tasks = list(getattr(plan, "all_tasks", []) or [])
        if tasks:
            lines.extend(f"- {task}" for task in tasks)
        else:
            lines.append(T("No tasks yet"))
    else:
        lines.append(T("No task plan available"))
    return "\n".join(str(item) for item in lines).rstrip() + "\n"


def build_review_log_report_text(client_name="", review_text=""):
    lines = [T("Review log"), "====================", ""]
    name = str(client_name or T("No client selected")).strip()
    review = str(review_text or T("No review")).strip()
    lines.extend([f"Client: {name}", f"Review: {review}"])
    return "\n".join(str(item) for item in lines).rstrip() + "\n"


def build_client_payment_report_text_for_app(client_name, client_manager=None):
    return build_client_payment_report_text(client_name, client_manager)


__all__ = [
    "build_task_log_report_text",
    "build_review_log_report_text",
    "build_client_payment_report_text_for_app",
]
