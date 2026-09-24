import json
import os
import tempfile
import unittest
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display

from app.domain.clients_management import (
    Client,
    ClientManager,
    build_clients_report_text,
    format_contact_number,
    generate_contract_months,
)
from app.ui.windows.clients_progress_ui import (
    Plan,
    ProgressApp,
    T,
    apply_bidi_text,
    build_all_clients_row_values,
    build_review_log_report_text,
    build_task_log_report_text,
    get_emoji_font_families,
    load_shop_electrical_meter_map,
    parse_task_items,
    resolve_log_output_dir,
    resolve_shop_electrical_meter,
    save_guest_profile,
    set_language,
    strip_task_number_prefix,
    sync_session_profile,
    user_registeration,
    validate_translation_coverage,
)
from app.services.sync_documents import TARGET


class ClientManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, "clients.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_list_clients(self):
        manager = ClientManager(self.file_path)
        manager.add_client("Bin Salim", "99999999", "machineries suppliers 'Hilti'")

        self.assertEqual(len(manager.clients), 1)
        self.assertEqual(manager.clients[0].name, "Bin Salim")
        self.assertIn("Bin Salim", manager.list_clients())

    def test_contact_numbers_default_to_oman_country_code(self):
        self.assertEqual(format_contact_number("5551234"), "+9685551234")

        manager = ClientManager(self.file_path)
        manager.add_client("Nora", "5551234", "Consulting", "nora@example.com")

        self.assertEqual(manager.clients[0].contact, "+9685551234")
        self.assertEqual(manager.clients[0].to_dict()["contact"], "+9685551234")

    def test_apply_bidi_handles_arabic_review_text(self):
        label = "ملاحظات العميل"
        expected = get_display(arabic_reshaper.reshape(label))
        self.assertEqual(apply_bidi_text(label), expected)
        self.assertIn("ملاحظات", apply_bidi_text(label))

    def test_language_switch_supports_english_and_arabic(self):
        self.assertEqual(T("Client Details"), "Client Details")
        set_language("ar")
        self.assertEqual(T("Client Details"), "تفاصيل العميل")
        self.assertEqual(T("Address"), "العنوان")
        self.assertEqual(T("Electrical Meter"), "عداد الكهرباء")
        set_language("eng")
        self.assertEqual(T("Client Details"), "Client Details")

    def test_reservation_save_resolves_electrical_meter_from_shop_number(self):
        self.assertEqual(resolve_shop_electrical_meter("12"), "28609687")
        self.assertEqual(resolve_shop_electrical_meter("Office"), "28609686")
        self.assertEqual(resolve_shop_electrical_meter("999"), "")

    def test_parse_task_items_reads_comma_and_newline_lists(self):
        tasks = parse_task_items("Research, Design, Launch\nReview")
        self.assertEqual(tasks, ["Research", "Design", "Launch", "Review"])

    def test_plan_sync_keeps_pending_tasks_in_sync(self):
        plan = Plan(Client("Sam", "123", "Marketing"), all_tasks=["Task 1", "Task 2", "Task 3"])
        plan.pending_tasks = ["Task 1", "Task 3"]
        plan.sync_task_lists(all_tasks=["Task 1", "Task 2", "Task 3", "Task 4"], pending_tasks=["Task 2", "Task 4"])

        self.assertEqual(plan.all_tasks, ["Task 1", "Task 2", "Task 3", "Task 4"])
        self.assertEqual(plan.pending_tasks, ["Task 2", "Task 4"])

    def test_generate_contract_months(self):
        months = generate_contract_months("2026-01-15", "2026-03-10")
        self.assertEqual(months[0], "2026-01")
        self.assertEqual(months[-1], "2026-03")
        self.assertIn("2026-02", months)

    def test_client_reservation_status_round_trips(self):
        client = Client(
            "Nora",
            "+9685551234",
            "Consulting",
            "nora@example.com",
            "12",
            reservation_status={
                "client_name": "Nora",
                "contact": "+9685551234",
                "shop_number": "12",
                "contract_status": "under progress",
            },
        )

        payload = client.to_dict()
        rebuilt = Client.from_dict(payload)
        self.assertEqual(rebuilt.reservation_status["shop_number"], "12")
        self.assertEqual(rebuilt.reservation_status["contract_status"], "under progress")

    def test_contract_months_are_generated_from_contract_dates(self):
        months = generate_contract_months("2026-01-15", "2026-03-10")
        self.assertEqual(months[0], "2026-01")
        self.assertIn("2026-02", months)

    def test_progress_app_exposes_separate_export_actions(self):
        self.assertTrue(hasattr(ProgressApp, "export_client_log"))
        self.assertTrue(hasattr(ProgressApp, "export_task_log"))
        self.assertTrue(hasattr(ProgressApp, "export_observation_log"))

    def test_emoji_font_families_include_windows_emoji_support(self):
        families = get_emoji_font_families()
        self.assertIn("Segoe UI Emoji", families)
        self.assertIn("Segoe UI Symbol", families)

    def test_sync_documents_target_uses_current_project_root(self):
        project_root = Path(__file__).resolve().parents[1]
        expected_target = project_root / "data" / "docs" / "documents.txt"
        self.assertEqual(TARGET.resolve(), expected_target.resolve())


if __name__ == "__main__":
    unittest.main()
