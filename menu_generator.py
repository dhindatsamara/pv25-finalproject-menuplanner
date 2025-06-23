import random
from PyQt5 import QtWidgets
from database_manager import DatabaseManager
from utils import validate_inputs, get_selected_meal_time, get_selected_goal

class MenuGenerator:
    def __init__(self, app):
        self.app = app
        self.db_manager = DatabaseManager()
        self.db_manager.load_history(app)

    def generate_menu(self):
        try:
            is_valid, error_message = validate_inputs(self.app)
            if not is_valid:
                QtWidgets.QMessageBox.warning(self.app, "Input Error", error_message)
                return
            name = self.app.nameInput.text().strip()
            flavor = self.app.tasteCombo.currentText()
            meal_time = get_selected_meal_time(self.app)
            goal = get_selected_goal(self.app)
            prep_time = self.app.prepTimeCombo.currentText() if hasattr(self.app, 'prepTimeCombo') else ""
            prep_time_estimate = {
                "Cepat": "<15 menit",
                "Sedang": "15-30 menit",
                "Lama": ">30 menit"
            }.get(prep_time, "")
            result_text = f"🍽️ Menu Rekomendasi Hari Ini untuk {name}\n"
            result_text += "────────────────────────────────────\n"
            result_text += f"Waktu Persiapan: {prep_time} ({prep_time_estimate})\n\n"
            menu_item, used_flavor_label, reason, fallback_used = self.db_manager.get_menu_options(
                meal_time, flavor, prep_time, goal
            )
            emoji = {
                "Sarapan": "🍳",
                "Makan Siang": "🍛",
                "Makan Malam": "🍲",
                "Snack": "🍪"
            }.get(meal_time, "🍽️")
            result_text += f"{emoji} {meal_time} (Rasa: {used_flavor_label}):\n"
            if reason:
                result_text += f"⚠️ Catatan: {reason}\n"
            menu = menu_item[0] if menu_item else "Tidak ada menu cocok 🥲"
            ingredients = menu_item[1] if menu_item else ""
            tag = " (Alternatif)" if fallback_used else ""
            result_text += f"{menu}{tag}\n"
            if ingredients:
                result_text += f"Bahan: {ingredients}\n"
            self.app.resultTextEdit.clear()
            self.app.resultTextEdit.setText(result_text)
            status = "Alternatif" if fallback_used else "Direkomendasikan"
            notes = reason if reason else "Sesuai preferensi"
            menu_name = menu_item[0] if menu_item else "Tidak ada menu"
            if name and menu_name and meal_time:
                self.db_manager.save_history(name, menu_name, meal_time, status, notes, self.app)
                self.db_manager.load_history(self.app)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.app, "Error", f"Gagal menghasilkan menu: {str(e)}")

    def surprise_menu(self):
        try:
            name = self.app.nameInput.text().strip() or "User"
            result_text = f"🎉 Menu Surprise Hari Ini untuk {name}\n"
            result_text += "────────────────────────────────────────────\n\n"
            meal_times = ["Sarapan", "Makan Siang", "Makan Malam", "Snack"]
            flavors = ["Manis", "Asin", "Pedas", "Asam"]
            goals = ["Hemat", "Fancy", "Sehat"]
            prep_options = ["Cepat", "Sedang", "Lama"]
            for mt in meal_times:
                random_flavor = random.choice(flavors)
                goal = random.choice(goals)
                prep_time = random.choice(prep_options)
                prep_time_estimate = {
                    "Cepat": "<15 menit",
                    "Sedang": "15-30 menit",
                    "Lama": ">30 menit"
                }.get(prep_time, "<15 menit")
                menu_item, used_flavor_label, reason, fallback_used = self.db_manager.get_menu_options(
                    mt, random_flavor, prep_time, goal
                )
                emoji = {
                    "Sarapan": "🍳",
                    "Makan Siang": "🍛",
                    "Makan Malam": "🍲",
                    "Snack": "🍪"
                }.get(mt, "🍽️")
                result_text += f"{emoji} {mt} (Rasa: {used_flavor_label}, Waktu Persiapan: {prep_time} ({prep_time_estimate})):\n"
                if reason:
                    result_text += f"⚠️ Catatan: {reason}\n"
                menu = menu_item[0] if menu_item else "Tidak ada menu cocok 🥲"
                ingredients = menu_item[1] if menu_item else ""
                tag = " (Alternatif)" if fallback_used and used_flavor_label != random_flavor else ""
                result_text += f"{menu}{tag}\n"
                if ingredients:
                    result_text += f"Bahan: {ingredients}\n"
                result_text += "\n"
                status = "Alternatif" if fallback_used else "Direkomendasikan"
                notes = reason if reason else "Surprise menu"
                if name and menu and mt:
                    self.db_manager.save_history(name, menu, mt, status, notes, self.app)
            self.app.resultTextEdit.clear()
            self.app.resultTextEdit.setText(result_text.rstrip())
            self.db_manager.load_history(self.app)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.app, "Error", f"Gagal menghasilkan menu surprise: {str(e)}")