# MenuPlanner+

**MenuPlanner+** adalah aplikasi yang merekomendasikan menu makanan yang akan dimasak berbasis **PyQt5**. Aplikasi ini dirancang untuk memberikan rekomendasi makanan berdasarkan preferensi pengguna, seperti **waktu makan**, **preferensi rasa**, **tujuan konsumsi**, serta **waktu persiapan** pengguna. Aplikasi ini menggabungkan antarmuka pengguna (GUI) yang menarik dengan logika pemrosesan menu yang efisien, modular, dan mudah digunakan sehingga cocok untuk merencanakan menu masak sendiri. Aplikasi ini sangat berguna dalam kehidupan sehari-hari, terutama bagi user yang sering kebingungan untuk masak apa hari ini.

---

## Fitur Utama

**Rekomendasi Menu Berdasarkan:**

- Waktu makan (Sarapan, Makan Siang, Makan Malam, Snack)
- Preferensi rasa (Manis, Asin, Pedas, Asam)
- Tujuan konsumsi (Hemat, Mewah, Diet)
- Waktu persiapan makanan (Cepat, Sedang, Lama)

**Mode Surprise Menu**

- Memberikan rekomendasi menu acak untuk semua waktu makan tanpa perlu mengisi semua input. Tombol "Surprise Me" aktif hanya jika semua input kosong atau hanya nama pengguna yang diisi.

**Riwayat Menu**

- Menyimpan riwayat rekomendasi menu di database (menu.db) dan menampilkannya di tab Meal History dengan tabel yang mengisi penuh ruang tab.
- Fitur ekspor riwayat ke format CSV dan PDF.
- Opsi untuk menghapus riwayat dengan tombol "Clear History".

**Validasi Input**

- Tombol "Generate Menu" hanya aktif jika semua input terisi (nama, waktu makan, rasa, tujuan, waktu persiapan).
- Menampilkan pesan error jika input tidak valid atau tidak lengkap.
- Dropdown rasa dan waktu persiapan kosong saat aplikasi dimulai untuk fleksibilitas pengguna.

## Fitur Tambahan

- Menu bar dengan opsi untuk ekspor ke CSV/PDF, reset form, hapus riwayat, panduan pengguna, dan informasi aplikasi.
- Status bar yang menampilkan informasi pengembang.
- Konfirmasi sebelum reset form, hapus riwayat, atau keluar dari aplikasi.

---

## Tampilan Aplikasi

### 1. Tampilan Awal

![Tampilan Awal](output/start.png)

### 2. Halaman Utama

![Plan Your Meal](output/main_page.png)
![Meal History](output/meal_history.png)

#### Plan Your Meal

##### a. Generate Menu

![Generate Menu](output/generate_menu.png)

##### b. Surprise Me!

![SM](output/surprise_me.png)

##### c. Reset

![Reset](output/reset_form.png)

##### d. Tombol Surprise Me Tidak Aktif

![off](output/suprise_off.png)

##### e. Plan Your Meal Full Screen

![fs](output/full_screen2.png)

#### Meal History

##### a. Clear History

![clear](output/clear_history.png)

##### b. Export CSV

![csv](output/ekspor_csv.png)
![hasil csv](output/csv.png)

##### c. Ekspor PDF

![pdf](output/ekspor_pdf.png)
![hasil pdf](output/pdf.png)

##### d. Meal History Full Screen

![mh](output/full_screen1.png)

### 3. Menu Bar

##### a. File

![file](output/file.png)

##### b. Edit

![edit](output/edit.png)

##### c. Help

![help](output/help.png)
![help](output/about.png)
![help](output/user_guide.png)

### 4. Exit

![file](output/exit.png)

## Struktur Code

Aplikasi ini dibangun dengan pendekatan modular untuk memudahkan pemeliharaan dan pengembangan:

- main.py: Menginisialisasi aplikasi dan menjalankan instance utama.
- ui_manager.py: Mengelola antarmuka pengguna, sinyal, dan status tombol.
- database_manager.py: Menangani operasi database (inisialisasi, penyimpanan riwayat, pemuatan data).
- menu_generator.py: Logika untuk menghasilkan rekomendasi menu dan mode "Surprise Me".
- export_manager.py: Mengelola ekspor riwayat ke CSV dan PDF.
- utils.py: Fungsi utilitas untuk validasi input dan pengambilan data.
- menu_planner.ui: File UI yang dibuat dengan Qt Designer.
- styles.qss: Stylesheet untuk desain visual aplikasi.
- menu.db: Database SQLite untuk menyimpan data menu dan riwayat.

## Panduan Penggunaan Aplikasi

1. Tampilan Awal: Klik tombol "START" untuk masuk ke halaman utama.
2. Plan Your Meal:
   - Masukkan nama pengguna.
   - Pilih waktu makan (Sarapan, Makan Siang, Makan Malam, Snack).
   - Pilih rasa dari dropdown (Manis, Asin, Pedas, Asam).
   - Pilih tujuan konsumsi (Hemat, Sehat, Fancy).
   - Pilih waktu persiapan (Cepat, Sedang, Lama).
   - Klik "Generate Menu" untuk rekomendasi sesuai preferensi, atau "Surprise Me" untuk menu acak (jika hanya nama diisi atau semua kosong).
   - Klik "Reset" untuk mengosongkan formulir.
3. Meal History:
   - Lihat riwayat rekomendasi di tabel.
   - Ekspor riwayat ke CSV atau PDF menggunakan tombol atau menu bar.
   - Hapus riwayat dengan tombol "Clear History".
4. Menu Bar:
   - File: Ekspor riwayat, keluar dari aplikasi.
   - Edit: Hapus riwayat, reset formulir.
   - Help: Lihat panduan pengguna atau informasi aplikasi.
