import json
import os
import subprocess
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk

from clients_management import (
    Client,
    ClientManager,
    DEFAULT_CONTACT_COUNTRY_CODE,
    format_contact_number,
    normalize_contract_details,
    normalize_reservation_status,
    resolve_clients_data_path,
)

APP_ICON = None
for candidate in [
    Path(__file__).resolve().parent.parent / "starco_icon.ico",
    Path(__file__).resolve().parent / "starco_icon.ico",
]:
    if candidate.exists():
        APP_ICON = candidate
        break

if APP_ICON is None:
    APP_ICON = Path(__file__).resolve().parent.parent / "starco_icon.ico"


class ShopReservationForm(tk.Tk):
    def __init__(self, client_name=None, client_data=None):
        super().__init__()
        self.title("Advanced Shop Reservation Form - Starco Commercial Complex")
        self.geometry("980x760")
        self.minsize(920, 680)
        self.configure(bg="#f3f6fb")

        try:
            self.iconbitmap(str(APP_ICON))
        except tk.TclError:
            pass

        self.saved_client_data = client_data or self.load_saved_client_data(client_name)
        self.client_name = str(client_name or self.saved_client_data.get("name") or "").strip()
        self.client_manager = ClientManager(resolve_clients_data_path())

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Header.TLabel", background="#f3f6fb", foreground="#1f3b5b", font=("Segoe UI", 16, "bold"))
        style.configure("Section.TLabel", background="#ffffff", foreground="#1f3b5b", font=("Segoe UI", 10, "bold"))
        style.configure("Info.TLabel", background="#ffffff", foreground="#3b4a5a", font=("Segoe UI", 10))

        header = ttk.Frame(self, padding=(20, 18, 20, 10))
        header.pack(fill="x")
        header.configure(style="Card.TFrame")

        logo_frame = ttk.Frame(header)
        logo_frame.pack(side="left")
        try:
            from PIL import Image, ImageTk
            icon_path = APP_ICON
            if icon_path and icon_path.exists():
                image = Image.open(icon_path)
                if image.size[0] > 0 and image.size[1] > 0:
                    thumb = image.resize((42, 42), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(thumb)
                    ttk.Label(logo_frame, image=photo).pack(side="left", padx=(0, 12))
                    logo_frame.image = photo
        except Exception:
            pass

        title_frame = ttk.Frame(header)
        title_frame.pack(side="left", fill="x", expand=True)
        ttk.Label(title_frame, text="Starco Commercial Complex", style="Header.TLabel").pack(anchor="w")
        ttk.Label(title_frame, text="Reservation Contract Form", style="Info.TLabel").pack(anchor="w", pady=(2, 0))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        self.main_tab = ttk.Frame(notebook, padding=18)
        self.shops_tab = ttk.Frame(notebook, padding=18)
        self.payment_tab = ttk.Frame(notebook, padding=18)

        notebook.add(self.main_tab, text="Contract Details")
        notebook.add(self.shops_tab, text="Shop Information")
        notebook.add(self.payment_tab, text="Payment & Bank")

        self.create_main_tab()
        self.create_shops_tab()
        self.create_payment_tab()
        self.prefill_from_saved_client()

        button_row = ttk.Frame(self, padding=(0, 0, 0, 18))
        button_row.pack()
        ttk.Button(button_row, text="Save Contract", command=self.save_contract, width=18).pack(side="left", padx=(0, 10))
        ttk.Button(button_row, text="Preview Contract", command=self.preview_saved_contract, width=18).pack(side="left")

    def load_saved_client_data(self, client_name=None):
        data_file = resolve_clients_data_path()
        if not data_file.exists():
            return {}

        try:
            with data_file.open("r", encoding="utf-8") as infile:
                payload = json.load(infile)
        except (json.JSONDecodeError, OSError, TypeError):
            return {}

        if not isinstance(payload, list):
            return {}

        matches = []
        for entry in payload:
            if not isinstance(entry, dict):
                continue
            if client_name:
                entry_name = str(entry.get("name") or entry.get("Client Name") or "").strip().lower()
                if entry_name != str(client_name).strip().lower():
                    continue
            if entry.get("reservation_status") or entry.get("shop_number") or entry.get("electrical_meter") or entry.get("contact") or entry.get("Contact"):
                matches.append(entry)

        if not matches:
            return {}
        return matches[-1]

    def prefill_from_saved_client(self):
        data = self.saved_client_data or {}
        if not data:
            self.main_vars["lessor"].set("")
            self.main_vars["lessee"].set("Khalid Salim Said")
            self.main_vars["date"].set(datetime.now().strftime("%d/%m/%Y"))
            self.main_vars["duration"].set("")
            self.renew_var.set("Yes")
            self.payment_vars["rent"].set("")
            self.payment_vars["deposit"].set("")
            self.payment_vars["bank"].set("01041108028002")
            self.payment_vars["holder"].set("Khalid Salim Said Al Shanfari")
            return

        client_name = str(data.get("name") or data.get("Client Name") or "").strip()
        contact = str(data.get("contact") or data.get("Contact") or "").strip()
        shop_number = str(data.get("shop_number") or data.get("Shop Number") or "").strip()
        electrical_meter = str(data.get("electrical_meter") or data.get("notes") or "").strip()
        contract_details = data.get("contract_details") if isinstance(data.get("contract_details"), dict) else {}
        reservation_status = data.get("reservation_status") if isinstance(data.get("reservation_status"), dict) else {}

        self.main_vars["lessor"].set(client_name)
        self.main_vars["lessee"].set("Khalid Salim Said")
        self.main_vars["date"].set(str(contract_details.get("starting_date") or datetime.now().strftime("%d/%m/%Y")).strip())
        duration_value = str(
            contract_details.get("duration_years")
            or contract_details.get("Municipal Contract Duration")
            or contract_details.get("duration")
            or reservation_status.get("contract_duration")
            or ""
        ).strip()
        self.main_vars["duration"].set(duration_value)

        renewable_value = str(contract_details.get("renewable") or "Yes")
        self.renew_var.set("Yes" if renewable_value.strip().lower() in {"yes", "true", "y"} else "No")

        rent_value = str(
            contract_details.get("rent_value")
            or contract_details.get("monthly_rent")
            or contract_details.get("rent")
            or reservation_status.get("rent_value")
            or ""
        ).strip()
        deposit_value = str(
            contract_details.get("security_deposit")
            or contract_details.get("deposit")
            or reservation_status.get("deposit_amount")
            or "0"
        ).strip()

        self.payment_vars["rent"].set(rent_value)
        self.payment_vars["deposit"].set(deposit_value)
        self.payment_vars["bank"].set("01041108028002")
        self.payment_vars["holder"].set("Khalid Salim Said Al Shanfari")

        if shop_number:
            self.shop_var.set(shop_number)
            self.elec_var.set(electrical_meter)
            self.add_shop(shop_number=shop_number, elec_value=electrical_meter, silent=True)

        if contact:
            self.main_vars.setdefault("contact", tk.StringVar(value=contact))

    def create_main_tab(self):
        fields = [
            ("Date", "date"),
            ("First Party (Lessor)", "lessor"),
            ("Second Party (Lessee)", "lessee"),
            ("Municipal Contract Duration (Years)", "duration"),
        ]

        self.main_vars = {}

        info_card = ttk.Frame(self.main_tab, padding=18)
        info_card.pack(fill="both", expand=True)

        ttk.Label(info_card, text="Contract Information", style="Section.TLabel").pack(anchor="w", pady=(0, 12))

        for label, key in fields:
            row = ttk.Frame(info_card)
            row.pack(fill="x", pady=8)
            ttk.Label(row, text=label, width=28, anchor="w", style="Info.TLabel").pack(side="left")
            var = tk.StringVar()
            self.main_vars[key] = var
            ttk.Entry(row, textvariable=var, width=52).pack(side="left", fill="x", expand=True)

        row = ttk.Frame(info_card)
        row.pack(fill="x", pady=(8, 0))
        ttk.Label(row, text="Renewable", width=28, anchor="w", style="Info.TLabel").pack(side="left")
        self.renew_var = tk.StringVar(value="Yes")
        ttk.Combobox(row, textvariable=self.renew_var, values=["Yes", "No"], width=50, state="readonly").pack(side="left", fill="x", expand=True)

    def create_shops_tab(self):
        card = ttk.Frame(self.shops_tab, padding=16)
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="Shop Registration", style="Section.TLabel").pack(anchor="w", pady=(0, 12))

        self.shop_tree = ttk.Treeview(card, columns=("shop", "electricity"), show="headings", height=10)
        self.shop_tree.heading("shop", text="Shop Number")
        self.shop_tree.heading("electricity", text="Electricity Account")
        self.shop_tree.column("shop", width=180, anchor="center")
        self.shop_tree.column("electricity", width=220, anchor="center")
        self.shop_tree.pack(fill="both", expand=True, pady=(0, 12))

        form_frame = ttk.Frame(card)
        form_frame.pack(fill="x")

        ttk.Label(form_frame, text="Shop Number", width=18, anchor="w", style="Info.TLabel").grid(row=0, column=0, padx=(0, 8), pady=(0, 6), sticky="w")
        ttk.Label(form_frame, text="Electricity Account", width=20, anchor="w", style="Info.TLabel").grid(row=0, column=1, padx=(0, 8), pady=(0, 6), sticky="w")

        self.shop_var = tk.StringVar()
        self.elec_var = tk.StringVar()

        ttk.Entry(form_frame, textvariable=self.shop_var, width=22).grid(row=1, column=0, padx=(0, 8), sticky="ew")
        ttk.Entry(form_frame, textvariable=self.elec_var, width=22).grid(row=1, column=1, padx=(0, 8), sticky="ew")
        ttk.Button(form_frame, text="Add Shop", command=self.add_shop, width=16).grid(row=1, column=2, sticky="ew")

        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(2, weight=0)

    def add_shop(self, shop_number=None, elec_value=None, silent=False):
        shop = (shop_number if shop_number is not None else self.shop_var.get()).strip()
        elec = (elec_value if elec_value is not None else self.elec_var.get()).strip()

        if not shop or not elec:
            if not silent:
                messagebox.showerror("Error", "Both fields are required.")
            return

        self.shop_tree.insert("", "end", values=(shop, elec))
        if not silent:
            self.shop_var.set("")
            self.elec_var.set("")

    def create_payment_tab(self):
        fields = [
            ("Monthly Rent (OMR)", "rent"),
            ("Security Deposit (OMR)", "deposit"),
            ("Bank Account Number", "bank"),
            ("Account Holder", "holder"),
        ]

        self.payment_vars = {}

        card = ttk.Frame(self.payment_tab, padding=18)
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="Payment Details", style="Section.TLabel").pack(anchor="w", pady=(0, 12))

        for label, key in fields:
            row = ttk.Frame(card)
            row.pack(fill="x", pady=8)
            ttk.Label(row, text=label, width=28, anchor="w", style="Info.TLabel").pack(side="left")
            var = tk.StringVar()
            self.payment_vars[key] = var
            ttk.Entry(row, textvariable=var, width=52).pack(side="left", fill="x", expand=True)

        self.payment_vars["bank"].set("01041108028002")
        self.payment_vars["holder"].set("Khalid Salim Said Al Shanfari")

    def _get_field_value(self, key, default=""):
        var = self.main_vars.get(key)
        if var is None:
            return str(default)
        try:
            value = var.get()
        except Exception:
            return str(default)
        return str(value if value is not None else default)

    def _get_contract_output_paths(self):
        project_root = Path(__file__).resolve().parent.parent
        output_dir = project_root / "application_outputs" / "contracts"
        output_dir.mkdir(parents=True, exist_ok=True)
        mapping_path = output_dir / "reservation_contracts.json"
        return project_root, output_dir, mapping_path

    def _get_current_shop_number(self):
        shop_entries = []
        for item in self.shop_tree.get_children():
            values = self.shop_tree.item(item)["values"]
            if values:
                shop_entries.append(str(values[0]).strip())
        if shop_entries:
            return shop_entries[0]
        return str(self.shop_var.get().strip() or "general")

    def _get_contract_as_text(self):
        shops = []
        for item in self.shop_tree.get_children():
            shops.append(self.shop_tree.item(item)["values"])

        lines = [
            "Starco Commercial Complex - Reservation Contract",
            "=" * 52,
            "",
            f"Date: {self.main_vars['date'].get().strip()}",
            f"First Party (Lessor): {self.main_vars['lessor'].get().strip()}",
            f"Second Party (Lessee): {self.main_vars['lessee'].get().strip()}",
            f"Municipal Contract Duration (Years): {self.main_vars['duration'].get().strip()}",
            f"Renewable: {self.renew_var.get().strip()}",
            f"Monthly Rent (OMR): {self.payment_vars['rent'].get().strip()}",
            f"Security Deposit (OMR): {self.payment_vars['deposit'].get().strip()}",
            f"Bank Account Number: {self.payment_vars['bank'].get().strip()}",
            f"Account Holder: {self.payment_vars['holder'].get().strip()}",
            "",
            "Shop Information:",
        ]

        if shops:
            for shop_number, elec_value in shops:
                lines.append(f"- Shop Number: {shop_number} | Electricity Account: {elec_value}")
        else:
            lines.append("- No shops added.")

        return "\n".join(lines) + "\n"

    def save_contract_document(self):
        _, output_dir, mapping_path = self._get_contract_output_paths()
        shop_number = self._get_current_shop_number()
        safe_key = str(shop_number or "general").strip() or "general"
        safe_key = safe_key.replace("/", "_").replace("\\", "_")
        file_name = f"contract_{safe_key}.txt"
        target_path = output_dir / file_name
        target_path.write_text(self._get_contract_as_text(), encoding="utf-8")

        index_data = {}
        if mapping_path.exists():
            try:
                with mapping_path.open("r", encoding="utf-8") as infile:
                    payload = json.load(infile)
                if isinstance(payload, dict):
                    index_data = payload
            except (json.JSONDecodeError, OSError, TypeError):
                index_data = {}

        index_data[safe_key] = str(target_path.resolve())
        with mapping_path.open("w", encoding="utf-8") as outfile:
            json.dump(index_data, outfile, indent=2, ensure_ascii=False)

        self.last_contract_path = str(target_path.resolve())
        self.last_contract_key = safe_key
        return self.last_contract_path

    def preview_saved_contract(self):
        _, _, mapping_path = self._get_contract_output_paths()
        shop_number = self._get_current_shop_number()
        safe_key = str(shop_number or "general").strip() or "general"
        safe_key = safe_key.replace("/", "_").replace("\\", "_")

        contract_path = None
        if mapping_path.exists():
            try:
                with mapping_path.open("r", encoding="utf-8") as infile:
                    payload = json.load(infile)
                if isinstance(payload, dict) and safe_key in payload:
                    contract_path = Path(payload[safe_key])
            except (json.JSONDecodeError, OSError, TypeError):
                contract_path = None

        if contract_path is not None and contract_path.exists():
            target = contract_path
        else:
            target = Path(self.save_contract_document())

        if hasattr(os, "startfile"):
            os.startfile(str(target))
        elif os.name == "nt":
            subprocess.Popen(["notepad.exe", str(target)])
        else:
            subprocess.Popen(["xdg-open", str(target)])

    def _get_contract_details(self):
        base_details = normalize_contract_details({})
        data = {
            "contract_number": base_details.get("contract_number", ""),
            "starting_date": self.main_vars["date"].get().strip(),
            "ending_date": "",
            "commercial_registration_number": "",
            "authorized_signature_name": self.main_vars["lessee"].get().strip(),
            "rent_value": self.payment_vars["rent"].get().strip(),
            "currency_type": "OMR",
            "open_issues": "",
            "duration_years": self.main_vars["duration"].get().strip(),
            "renewable": self.renew_var.get().strip(),
            "first_party": self.main_vars["lessor"].get().strip(),
            "second_party": self.main_vars["lessee"].get().strip(),
        }
        base_details.update(data)
        return base_details

    def save_contract(self):
        try:
            float(self.payment_vars["rent"].get().strip() or "0")
            float(self.payment_vars["deposit"].get().strip() or "0")
        except ValueError:
            messagebox.showerror("Error", "Rent and Deposit must be numeric.")
            return

        shops = []
        for item in self.shop_tree.get_children():
            shops.append(self.shop_tree.item(item)["values"])

        contract_details = self._get_contract_details()
        contact_value = self._get_field_value("contact")
        reservation_status = normalize_reservation_status(
            {
                "client_name": self.main_vars["lessor"].get().strip(),
                "contact": contact_value.strip(),
                "shop_number": shops[0][0] if shops else "",
                "deposit_status": "Deposite recieved" if str(self.payment_vars["deposit"].get().strip() or "0") not in {"", "0", "0.0"} else "Deposite not recieved",
                "contract_status": "completed" if str(self.payment_vars["deposit"].get().strip() or "0") not in {"", "0", "0.0"} else "under progress",
            }
        )

        if not messagebox.askyesno("Confirm", "Save contract data?"):
            return

        self.client_manager.load_clients()
        client = None
        target_name = self.main_vars["lessor"].get().strip()
        if target_name:
            client = next((entry for entry in self.client_manager.clients if entry.name.strip().lower() == target_name.lower()), None)

        if client is None:
            client = Client(
                target_name or "Unnamed Client",
                contact_value.strip() or "",
                "Reserved",
                email="",
                shop_number=shops[0][0] if shops else "",
                address="",
                electrical_meter=shops[0][1] if shops else "",
                notes=shops[0][1] if shops else "",
                contract_details=contract_details,
                reservation_status=reservation_status,
            )
            self.client_manager.clients.append(client)
        else:
            client.name = target_name or client.name
            client.contact = format_contact_number(
                contact_value.strip() or client.contact,
                DEFAULT_CONTACT_COUNTRY_CODE,
            )
            client.shop_number = shops[0][0] if shops else client.shop_number
            client.electrical_meter = shops[0][1] if shops else client.electrical_meter
            client.notes = client.electrical_meter
            client.contract_details = contract_details
            client.reservation_status = reservation_status

        self.client_manager.save_clients()
        self.save_contract_document()
        messagebox.showinfo("Saved", "Contract data and text file were saved successfully.")


def main():
    app = ShopReservationForm()
    app.mainloop()
    return app


if __name__ == "__main__":
    main()
