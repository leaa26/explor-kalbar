# Dokumentasi Proyek: Kalbar Explore

## 1. Tentang Proyek
Kalbar Explore adalah aplikasi pariwisata Kalimantan Barat yang dikembangkan dalam dua versi:
- **Aplikasi Desktop** (Python & Tkinter) untuk penggunaan lokal/offline.
- **Aplikasi Web** (Python Flask/HTTP Server, HTML5, CSS3, JavaScript) untuk akses browser yang interaktif.

Proyek ini mencakup 21 destinasi wisata unggulan di Kalimantan Barat lengkap dengan informasi kategori, lokasi, harga tiket, deskripsi, tips berkunjung, serta fitur pendukung seperti kalkulator anggaran dan *wishlist*.

---

## 2. Teknologi yang Digunakan
- **Bahasa Pemrograman:** Python
- **Backend / Server:** Flask / Python HTTP Server, Gunicorn
- **Frontend (Web):** HTML5, CSS3, JavaScript
- **GUI Desktop:** Python Tkinter & Pillow (PIL)
- **Manajemen Data:** Modul data terstruktur (`kalbar_explore_data.py`)

---

## 3. Tahapan Pembuatan Proyek

### A. Tahap Konsep & Perencanaan
1. **Penentuan Topik:** Memilih pariwisata Kalimantan Barat untuk mengenalkan destinasi ikonik (Tugu Khatulistiwa, Danau Sentarum, Pulau Lemukutan, dll.).
2. **Arsitektur Aplikasi:** Memutuskan untuk membangun versi desktop interaktif sekaligus versi web agar dapat diakses melalui berbagai platform.

### B. Tahap Pengumpulan & Manajemen Data
1. Membuat file pusat data (`kalbar_explore_data.py`).
2. Menghimpun 21 destinasi wisata beserta atribut detailnya (nama, kabupaten, kategori, harga tiket, deskripsi, dan tips).

### C. Tahap Pengembangan Aplikasi Desktop
1. Membuat skrip utama `kalbar_explore.py`.
2. Merancang antarmuka login dan dashboard utama menggunakan Tkinter.
3. Menambahkan fitur pendukung:
   - Pencarian dan filter kategori destinasi.
   - Sistem *Wishlist* untuk menyimpan tempat favorit.
   - Kalkulator estimasi anggaran perjalanan berdasarkan durasi dan jumlah orang.

### D. Tahap Pengembangan Aplikasi Web
1. Merancang halaman antarmuka web modern (`index.html`).
2. Membuat skrip server web (`server.py` / `kalbar_explore_web.py`) untuk merender data secara dinamis.
3. Menerapkan JavaScript untuk interaktivitas pengguna (filter instan, modal detail destinasi, kalkulator budget web).

### E. Tahap Pengujian & Finalisasi
1. Menjalankan pengujian lokal pada server dan aplikasi desktop.
2. Menyusun file pendukung (`requirements.txt`, `Procfile`, shortcut aplikasi) agar proyek siap digunakan maupun di-deploy.
