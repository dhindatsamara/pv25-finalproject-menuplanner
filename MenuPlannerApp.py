import sys
import random
import sqlite3
import csv
import os
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class MenuPlannerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        random.seed(None)
        try:
            loadUi('menu_planner.ui', self)
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", "Gagal memuat file UI! Pastikan menu_planner.ui ada.")
            sys.exit(1)
        self.load_stylesheet()
        try:
            if not hasattr(self, 'statusbar') or self.statusbar is None:
                self.statusbar = QtWidgets.QStatusBar()
                self.setStatusBar(self.statusbar)
            self.statusbar.setVisible(True)
            self.statusbar.setMinimumHeight(24)
            self.statusbar.setStyleSheet("QStatusBar { background-color: #f5f5f5; color: #222; font-size: 12px; padding: 4px; border-top: 1px solid #ccc; }")
            self.statusbar.showMessage("Nama: Dhinda Tsamara Shalsabilla | ID: F1D022005")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Warning", f"Gagal menginisialisasi status bar: {str(e)}")
        try:
            if all(hasattr(self, attr) for attr in ['timeBreakfast', 'timeLunch', 'timeDinner', 'timeSnack']):
                self.meal_group = QtWidgets.QButtonGroup(self)
                self.meal_group.addButton(self.timeBreakfast, 1)
                self.meal_group.addButton(self.timeLunch, 2)
                self.meal_group.addButton(self.timeDinner, 3)
                self.meal_group.addButton(self.timeSnack, 4)
        except Exception as e:
            pass
        try:
            if all(hasattr(self, attr) for attr in ['goalBudget', 'goalFancy', 'goalHealthy']):
                self.goal_group = QtWidgets.QButtonGroup(self)
                self.goal_group.addButton(self.goalBudget, 1)
                self.goal_group.addButton(self.goalFancy, 2)
                self.goal_group.addButton(self.goalHealthy, 3)
        except Exception as e:
            pass
        try:
            if hasattr(self, 'prepTimeCombo'):
                self.prepTimeCombo.setCurrentIndex(-1)
                self.prepTimeCombo.currentTextChanged.connect(self.update_prep_time)
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Input waktu persiapan tidak ditemukan.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", "Gagal menginisialisasi input waktu persiapan!")
        try:
            if hasattr(self, 'tasteCombo'):
                self.tasteCombo.setCurrentIndex(-1)
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Input selera rasa tidak ditemukan.")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", "Gagal menginisialisasi input selera rasa!")
        self.init_database()
        self.setup_menu_bar()
        try:
            required_widgets = [
                'startButton', 'generateButton', 'surpriseButton', 'resetButton',
                'exportCsvButton', 'exportPdfButton', 'clearHistoryButton',
                'nameInput', 'tasteCombo'
            ]
            missing = [w for w in required_widgets if not hasattr(self, w)]
            if missing:
                QtWidgets.QMessageBox.critical(self, "Error", f"Widget tidak ditemukan: {', '.join(missing)}")
                sys.exit(1)
            self.startButton.clicked.connect(self.show_main_page)
            self.generateButton.clicked.connect(self.generate_menu)
            self.surpriseButton.clicked.connect(self.surprise_menu)
            self.resetButton.clicked.connect(self.reset_fields)
            self.exportCsvButton.clicked.connect(self.export_to_csv)
            self.exportPdfButton.clicked.connect(self.export_to_pdf)
            self.clearHistoryButton.clicked.connect(self.clear_history)
            self.nameInput.textChanged.connect(self.update_button_states)
            self.tasteCombo.currentTextChanged.connect(self.update_button_states)
            if hasattr(self, 'meal_group'):
                self.meal_group.buttonClicked.connect(self.update_button_states)
            if hasattr(self, 'goal_group'):
                self.goal_group.buttonClicked.connect(self.update_button_states)
            if hasattr(self, 'prepTimeCombo'):
                self.prepTimeCombo.currentTextChanged.connect(self.update_button_states)
            self.generateButton.setEnabled(False)
            self.surpriseButton.setEnabled(True)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal menghubungkan sinyal: {str(e)}")
        try:
            self.stackedWidget.setCurrentIndex(0)
            self.tabWidget.setCurrentIndex(0)
        except AttributeError:
            pass

    def load_stylesheet(self):
        try:
            with open('styles.qss', 'r') as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, "Warning", "File styles.qss tidak ditemukan!")
        except Exception as e:
            pass

    def setup_menu_bar(self):
        try:
            if not hasattr(self, 'menubar'):
                QtWidgets.QMessageBox.critical(self, "Error", "Menu bar tidak ditemukan di UI!")
                return
            if hasattr(self, 'actionExportCsv'):
                self.actionExportCsv.triggered.connect(self.export_to_csv)
            if hasattr(self, 'actionExportPdf'):
                self.actionExportPdf.triggered.connect(self.export_to_pdf)
            if hasattr(self, 'actionExit'):
                self.actionExit.triggered.connect(self.close)
            if hasattr(self, 'actionClearHistory'):
                self.actionClearHistory.triggered.connect(self.clear_history)
            if hasattr(self, 'actionClearForm'):
                self.actionClearForm.triggered.connect(self.reset_fields)
            if hasattr(self, 'actionAbout'):
                self.actionAbout.triggered.connect(self.show_about_dialog)
            if hasattr(self, 'actionUserGuide'):
                self.actionUserGuide.triggered.connect(self.show_user_guide)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal mengatur menu bar: {str(e)}")

    def show_user_guide(self):
        try:
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("User Guide")
            dialog.setFixedSize(500, 400)
            layout = QtWidgets.QVBoxLayout()
            text_browser = QtWidgets.QTextBrowser()
            text_browser.setOpenExternalLinks(True)
            guide_content = """
            <h2>MenuPlanner+ User Guide</h2>
            <p>Selamat datang di <b>MenuPlanner+</b>, aplikasi untuk merencanakan menu makanan!</p>
            <h3>Cara Penggunaan:</h3>
            <ul>
                <li><b>Landing Page:</b> Klik tombol <b>START</b> untuk masuk ke halaman utama.</li>
                <li><b>Plan Your Meal:</b>
                    <ul>
                        <li>Masukkan nama di kolom <b>Nama</b>.</li>
                        <li>Pilih waktu makan (Sarapan, Makan Siang, dll.).</li>
                        <li>Pilih rasa (Manis, Pedas, dll.) dari dropdown.</li>
                        <li>Pilih tujuan konsumsi (Hemat, Mewah, Diet).</li>
                        <li>Pilih waktu persiapan (Cepat, Sedang, Lama).</li>
                        <li>Klik <b>Generate Menu</b> untuk rekomendasi atau <b>Surprise Me!</b> untuk menu acak.</li>
                        <li>Klik <b>Reset</b> untuk mengosongkan input.</li>
                    </ul>
                </li>
                <li><b>Meal History:</b>
                    <ul>
                        <li>Lihat riwayat rekomendasi di tabel.</li>
                        <li>Klik <b>Export to CSV</b> atau <b>Export to PDF</b> untuk menyimpan riwayat.</li>
                        <li>Klik <b>Clear History</b> untuk menghapus riwayat.</li>
                    </ul>
                </li>
                <li><b>Menu Bar:</b>
                    <ul>
                        <li><b>File > Export to CSV/PDF:</b> Ekspor riwayat.</li>
                        <li><b>File > Exit:</b> Keluar dari aplikasi (konfirmasi akan muncul).</li>
                        <li><b>Edit > Clear History:</b> Hapus riwayat.</li>
                        <li><b>Edit > Reset Form:</b> Kosongkan formulir input.</li>
                        <li><b>Help > About:</b> Info aplikasi.</li>
                        <li><b>Help > User Guide:</b> Baca panduan ini.</li>
                    </ul>
                </li>
            </ul>
            <p><b>Catatan:</b> Pastikan database <i>menu.db</i> terisi dan <i>styles.qss</i> ada di direktori aplikasi.</p>
            """
            text_browser.setHtml(guide_content)
            layout.addWidget(text_browser)
            close_button = QtWidgets.QPushButton("Close")
            close_button.clicked.connect(dialog.accept)
            layout.addWidget(close_button)
            dialog.setLayout(layout)
            dialog.exec_()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal menampilkan panduan pengguna: {str(e)}")

    def update_prep_time(self, text):
        try:
            self.prep_time = text if text else None
        except Exception as e:
            self.prep_time = None

    def init_database(self):
        try:
            self.conn = sqlite3.connect('menu.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_list (
                    name VARCHAR,
                    category VARCHAR,
                    taste VARCHAR,
                    prep_time VARCHAR,
                    cost VARCHAR,
                    method VARCHAR,
                    ingredients VARCHAR
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS history_list (
                    Name VARCHAR,
                    Title VARCHAR,
                    Category VARCHAR,
                    Date VARCHAR,
                    Status VARCHAR,
                    Notes VARCHAR
                )
            ''')
            self.conn.commit()
            self.load_history()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", "Gagal menginisialisasi database!")

    def load_history(self):
        try:
            if not hasattr(self, 'historyTable'):
                return
            self.historyTable.setRowCount(0)
            self.historyTable.setColumnCount(6)
            self.historyTable.setHorizontalHeaderLabels(["Name", "Title", "Category", "Date", "Status", "Notes"])
            self.cursor.execute("SELECT Name, Title, Category, Date, Status, Notes FROM history_list")
            for row_data in self.cursor.fetchall():
                row = self.historyTable.rowCount()
                self.historyTable.insertRow(row)
                for col, data in enumerate(row_data):
                    self.historyTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(data or "")))
        except Exception as e:
            pass

    def show_about_dialog(self):
        try:
            QtWidgets.QMessageBox.information(
                self, "About MenuPlanner+",
                "MenuPlanner+ v1.0\nAplikasi rekomendasi menu makanan untuk masak sendiri.\nDibuat oleh Dhinda Tsamara Shalsabilla (F1D022005)"
            )
        except Exception as e:
            pass

    def update_button_states(self):
        try:
            name = self.nameInput.text().strip() if hasattr(self, 'nameInput') else ""
            flavor = self.tasteCombo.currentText() if hasattr(self, 'tasteCombo') else ""
            meal_time = self.get_selected_meal_time()
            goal = self.get_selected_goal()
            prep_time = self.prepTimeCombo.currentText() if hasattr(self, 'prepTimeCombo') else ""
            all_filled = bool(name and flavor and meal_time and goal and prep_time)
            if hasattr(self, 'generateButton') and hasattr(self, 'surpriseButton'):
                self.generateButton.setEnabled(all_filled)
                self.surpriseButton.setEnabled(True)
        except Exception as e:
            pass

    def show_main_page(self):
        try:
            if hasattr(self, 'stackedWidget') and hasattr(self, 'main_page'):
                self.stackedWidget.setCurrentWidget(self.main_page)
        except Exception as e:
            pass

    def get_selected_meal_time(self):
        try:
            if hasattr(self, 'meal_group'):
                meal_id = self.meal_group.checkedId()
                return {1: "Sarapan", 2: "Makan Siang", 3: "Makan Malam", 4: "Snack"}.get(meal_id)
            return None
        except Exception as e:
            return None

    def get_selected_goal(self):
        try:
            if hasattr(self, 'goal_group'):
                goal_id = self.goal_group.checkedId()
                return {1: "Hemat", 2: "Fancy", 3: "Sehat"}.get(goal_id)
            return None
        except Exception as e:
            return None

    def validate_inputs(self):
        try:
            name = self.nameInput.text().strip() if hasattr(self, 'nameInput') else ""
            flavor = self.tasteCombo.currentText() if hasattr(self, 'tasteCombo') else ""
            meal_time = self.get_selected_meal_time()
            goal = self.get_selected_goal()
            prep_time = self.prepTimeCombo.currentText() if hasattr(self, 'prepTimeCombo') else ""
            if not name:
                return False, "Nama harus diisi!"
            if not flavor:
                return False, "Pilih rasa makanan!"
            if not meal_time:
                return False, "Pilih waktu makan!"
            if not goal:
                return False, "Pilih tujuan konsumsi!"
            if not prep_time:
                return False, "Pilih waktu persiapan!"
            return True, ""
        except Exception as e:
            return False, "Gagal memvalidasi input!"

    def get_menu_options(self, category, taste, prep_time, cost):
        try:
            options = []
            fallback_used = False
            used_flavor_label = taste
            reason = ""
            query = """
                SELECT name, ingredients FROM menu_list 
                WHERE category = ? AND taste = ? AND cost = ? AND method = 'Masak Sendiri'
                AND (prep_time = ? OR prep_time = 'Any')
            """
            self.cursor.execute(query, [category, taste, cost, prep_time])
            options = [(row[0], row[1]) for row in self.cursor.fetchall()]
            if not options:
                query = """
                    SELECT name, ingredients FROM menu_list 
                    WHERE category = ? AND taste = ? AND cost = ? AND method = 'Masak Sendiri'
                """
                self.cursor.execute(query, [category, taste, cost])
                options = [(row[0], row[1]) for row in self.cursor.fetchall()]
                if options:
                    fallback_used = True
                    reason = f"Waktu persiapan '{prep_time}' tidak tersedia untuk rasa {taste}."
            if not options:
                fallback_used = True
                valid_tastes = ["Manis", "Asin", "Pedas", "Asam"]
                if taste == "Pedas" and category == "Sarapan":
                    reason = f"Rasa {taste} kurang cocok untuk {category}, mencoba rasa lain."
                elif taste == "Asam" and category == "Sarapan":
                    reason = f"Rasa {taste} kurang umum untuk {category}, mencoba rasa lain."
                else:
                    reason = f"Tidak ada menu dengan rasa {taste} untuk {category}."
                for fallback_taste in valid_tastes:
                    query = """
                        SELECT name, ingredients FROM menu_list 
                        WHERE category = ? AND taste = ? AND cost = ? AND method = 'Masak Sendiri'
                    """
                    self.cursor.execute(query, [category, fallback_taste, cost])
                    new_options = [(row[0], row[1]) for row in self.cursor.fetchall()]
                    options.extend(new_options)
                    if new_options:
                        used_flavor_label = fallback_taste
                        break
            if not options:
                query = "SELECT name, ingredients FROM menu_list WHERE category = ? AND method = 'Masak Sendiri'"
                self.cursor.execute(query, [category])
                options = [(row[0], row[1]) for row in self.cursor.fetchall()]
                used_flavor_label = taste
                reason = f"Tidak ada menu yang cocok untuk {category} dengan kriteria rasa atau tujuan."
                fallback_used = True
            if options:
                selected_menu = random.choice(options)
                return selected_menu, used_flavor_label, reason, fallback_used
            else:
                return None, used_flavor_label, reason, fallback_used
        except Exception as e:
            return None, taste, "", False

    def generate_menu(self):
        try:
            is_valid, error_message = self.validate_inputs()
            if not is_valid:
                QtWidgets.QMessageBox.warning(self, "Input Error", error_message)
                return
            name = self.nameInput.text().strip()
            flavor = self.tasteCombo.currentText()
            meal_time = self.get_selected_meal_time()
            goal = self.get_selected_goal()
            prep_time = self.prepTimeCombo.currentText() if hasattr(self, 'prepTimeCombo') else ""
            prep_time_estimate = {
                "Cepat": "<15 menit",
                "Sedang": "15-30 menit",
                "Lama": ">30 menit"
            }.get(prep_time, "")
            result_text = f"🍽️ Menu Rekomendasi Hari Ini untuk {name}\n"
            result_text += "────────────────────────────────────────────────────────────\n"
            result_text += f"Waktu Persiapan: {prep_time} ({prep_time_estimate})\n\n"
            menu_item, used_flavor_label, reason, fallback_used = self.get_menu_options(
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
            self.resultTextEdit.clear()
            self.resultTextEdit.setText(result_text)
            status = "Alternatif" if fallback_used else "Direkomendasikan"
            notes = reason if reason else "Sesuai preferensi"
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            menu_name = menu_item[0] if menu_item else "Tidak ada menu"
            self.cursor.execute(
                "INSERT INTO history_list (Name, Title, Category, Date, Status, Notes) VALUES (?, ?, ?, ?, ?, ?)",
                (name, menu_name, meal_time, date, status, notes)
            )
            self.conn.commit()
            self.load_history()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal menghasilkan menu: {str(e)}")

    def surprise_menu(self):
        try:
            name = self.nameInput.text().strip() or "User"
            result_text = f"🎉 Menu Surprise Hari Ini untuk {name}\n"
            result_text += "──────────────────────────────────────────────────────────────\n\n"
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
                menu_item, used_flavor_label, reason, fallback_used = self.get_menu_options(
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
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute(
                    "INSERT INTO history_list (Name, Title, Category, Date, Status, Notes) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, menu, mt, date, status, notes)
                )
            self.conn.commit()
            self.resultTextEdit.clear()
            self.resultTextEdit.setText(result_text.rstrip())
            self.load_history()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal menghasilkan menu surprise: {str(e)}")

    def export_to_pdf(self):
        try:
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save PDF File", "", "PDF Files (*.pdf)"
            )
            if file_name:
                doc = SimpleDocTemplate(
                    file_name,
                    pagesize=letter,
                    leftMargin=50,
                    rightMargin=50,
                    topMargin=50,
                    bottomMargin=50
                )
                data = [["Name", "Title", "Category", "Date", "Status", "Notes"]]
                self.cursor.execute("SELECT Name, Title, Category, Date, Status, Notes FROM history_list")
                styles = getSampleStyleSheet()
                style_normal = styles['Normal']
                style_normal.fontName = 'Helvetica'
                style_normal.fontSize = 8
                style_normal.wordWrap = 'CJK'
                for row in self.cursor.fetchall():
                    wrapped_row = [
                        Paragraph(str(col or ""), style_normal) if col else ""
                        for col in row
                    ]
                    data.append(wrapped_row)
                page_width = letter[0] - 100
                col_widths = [
                    page_width * 0.15,
                    page_width * 0.20,
                    page_width * 0.10,
                    page_width * 0.15,
                    page_width * 0.10,
                    page_width * 0.30
                ]
                table = Table(data, colWidths=col_widths)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                header_style = ParagraphStyle(
                    name='Header',
                    fontName='Helvetica-Bold',
                    fontSize=14,
                    alignment=1
                )
                subheader_style = ParagraphStyle(
                    name='Subheader',
                    fontName='Helvetica',
                    fontSize=10,
                    alignment=1
                )
                elements = [
                    Paragraph("MenuPlanner+ Riwayat Menu", header_style),
                    Spacer(1, 12),
                    Paragraph(f"Dieksport pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subheader_style),
                    Spacer(1, 24),
                    table
                ]
                doc.build(elements)
                QtWidgets.QMessageBox.information(self, "Sukses", "Riwayat berhasil diekspor ke PDF!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal mengekspor PDF: {str(e)}")

    def reset_fields(self):
        try:
            confirm = QtWidgets.QMessageBox.question(
                self, "Konfirmasi Reset",
                "Yakin ingin menghapus semua input dan hasil?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.No:
                return
            self.nameInput.clear()
            self.tasteCombo.setCurrentIndex(-1)
            if hasattr(self, 'meal_group'):
                self.meal_group.setExclusive(False)
                for btn in self.meal_group.buttons():
                    btn.setChecked(False)
                self.meal_group.setExclusive(True)
            if hasattr(self, 'goal_group'):
                self.goal_group.setExclusive(False)
                for btn in self.goal_group.buttons():
                    btn.setChecked(False)
                self.goal_group.setExclusive(True)
            if hasattr(self, 'prepTimeCombo'):
                self.prepTimeCombo.setCurrentIndex(-1)
                self.prep_time = None
            self.resultTextEdit.clear()
            self.generateButton.setEnabled(False)
            self.surpriseButton.setEnabled(True)
        except Exception as e:
            pass

    def export_to_csv(self):
        try:
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save CSV File", "", "CSV Files (*.csv)"
            )
            if file_name:
                with open(file_name, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Name", "Title", "Category", "Date", "Status", "Notes"])
                    self.cursor.execute("SELECT Name, Title, Category, Date, Status, Notes FROM history_list")
                    writer.writerows(self.cursor.fetchall())
                QtWidgets.QMessageBox.information(self, "Sukses", "Riwayat berhasil diekspor ke CSV!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal mengekspor CSV: {str(e)}")

    def clear_history(self):
        try:
            confirm = QtWidgets.QMessageBox.question(
                self, "Konfirmasi Hapus",
                "Yakin ingin menghapus semua riwayat?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.No:
                return
            self.cursor.execute("DELETE FROM history_list")
            self.conn.commit()
            self.load_history()
            QtWidgets.QMessageBox.information(self, "Sukses", "Riwayat berhasil dihapus!")
        except Exception as e:
            pass

    def closeEvent(self, event):
        try:
            confirm = QtWidgets.QMessageBox.question(
                self, "Konfirmasi Keluar",
                "Yakin ingin keluar dari MenuPlanner+?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirm == QtWidgets.QMessageBox.Yes:
                if hasattr(self, 'conn'):
                    self.conn.close()
                event.accept()
            else:
                event.ignore()
        except Exception as e:
            event.accept()

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MenuPlannerApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error: Application failed to start: {str(e)}")
        sys.exit(1)