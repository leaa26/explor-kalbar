import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from kalbar_explore_data import DESTINASI_WISATA

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Kalbar Explore")
        self.root.geometry("420x480")
        self.root.config(bg="#1b4332")
        self.center_window(420, 480)

        container = tk.Frame(root, bg="#1b4332")
        container.pack(fill="both", expand=True, padx=30, pady=30)

        lbl_title = tk.Label(
            container,
            text="🌿 KALBAR EXPLORE",
            font=("Segoe UI", 20, "bold"),
            bg="#1b4332",
            fg="#ffffff"
        )
        lbl_title.pack(pady=(10, 5))

        lbl_sub = tk.Label(
            container,
            text="Jelajahi Pesona Wisata Kalimantan Barat",
            font=("Segoe UI", 10),
            bg="#1b4332",
            fg="#d8f3dc"
        )
        lbl_sub.pack(pady=(0, 25))

        card = tk.Frame(container, bg="#ffffff", bd=0, highlightbackground="#d8f3dc", highlightthickness=2)
        card.pack(fill="both", expand=True, padx=5, pady=5)

        lbl_user = tk.Label(
            card, text="Username", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#1b4332", anchor="w"
        )
        lbl_user.pack(fill="x", padx=25, pady=(25, 5))

        self.entry_user = tk.Entry(card, font=("Segoe UI", 11), bg="#f8f9fa", bd=1, relief="solid")
        self.entry_user.pack(fill="x", padx=25, ipady=4, pady=5)
        self.entry_user.insert(0, "admin")

        lbl_pass = tk.Label(
            card, text="Password", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#1b4332", anchor="w"
        )
        lbl_pass.pack(fill="x", padx=25, pady=(15, 5))

        self.entry_pass = tk.Entry(card, font=("Segoe UI", 11), show="*", bg="#f8f9fa", bd=1, relief="solid")
        self.entry_pass.pack(fill="x", padx=25, ipady=4, pady=5)
        self.entry_pass.insert(0, "12345")

        btn_login = tk.Button(
            card,
            text="MASUK APLIKASI",
            font=("Segoe UI", 11, "bold"),
            bg="#2d6a4f",
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.proses_login
        )
        btn_login.pack(fill="x", padx=25, ipady=8, pady=25)

        lbl_info = tk.Label(
            card,
            text="Default: admin / 12345",
            font=("Segoe UI", 8, "italic"),
            bg="#ffffff",
            fg="#888888"
        )
        lbl_info.pack(pady=(0, 20))

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def proses_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        if username == "admin" and password == "12345":
            self.root.destroy()
            root_utama = tk.Tk()
            app = KalbarExploreApp(root_utama)
            root_utama.mainloop()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")


class KalbarExploreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalbar Explore - Wisata Kalimantan Barat")
        self.root.geometry("750x850")
        self.root.config(bg="#1b4332")
        self.center_window(750, 850)
        self.wishlist = set()
        self.current_image = None

        header_frame = tk.Frame(root, bg="#1b4332")
        header_frame.pack(fill="x", padx=25, pady=(15, 10))

        title_label = tk.Label(
            header_frame,
            text="🌿 KALBAR EXPLORE",
            font=("Segoe UI", 20, "bold"),
            bg="#1b4332",
            fg="#ffffff",
            anchor="w"
        )
        title_label.pack(side="left")

        sub_label = tk.Label(
            header_frame,
            text="Wonderful West Kalimantan",
            font=("Segoe UI", 10, "italic"),
            bg="#1b4332",
            fg="#d8f3dc",
            anchor="e"
        )
        sub_label.pack(side="right", pady=(6, 0))

        card_main = tk.Frame(root, bg="#ffffff", bd=0, highlightbackground="#d8f3dc", highlightthickness=2)
        card_main.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        # Top Bar (Pilih Wisata & Wishlist Toggle)
        top_row = tk.Frame(card_main, bg="#ffffff")
        top_row.pack(fill="x", padx=20, pady=(15, 5))

        lbl_wisata = tk.Label(
            top_row, text="Pilih Destinasi Wisata", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#2d6a4f", anchor="w"
        )
        lbl_wisata.pack(side="left")

        self.btn_wishlist_toggle = tk.Button(
            top_row,
            text="🤍 Simpan ke Wishlist",
            font=("Segoe UI", 9, "bold"),
            bg="#f8f9fa",
            fg="#d90429",
            bd=1,
            relief="solid",
            cursor="hand2",
            command=self.toggle_wishlist
        )
        self.btn_wishlist_toggle.pack(side="right")

        self.daftar_nama = [item["nama"] for item in DESTINASI_WISATA]
        self.combo_wisata = ttk.Combobox(
            card_main, values=self.daftar_nama, font=("Segoe UI", 11), state="readonly"
        )
        self.combo_wisata.pack(fill="x", padx=20, pady=5)
        if self.daftar_nama:
            self.combo_wisata.current(0)
        self.combo_wisata.bind("<<ComboboxSelected>>", lambda e: self.tampilkan_detail())

        # Frame Foto & Detail
        middle_frame = tk.Frame(card_main, bg="#ffffff")
        middle_frame.pack(fill="x", padx=20, pady=5)

        # Label Foto Destinasi
        self.lbl_foto = tk.Label(
            middle_frame,
            text="[Foto Destinasi]\n(Letakkan file gambar di folder proyek)",
            font=("Segoe UI", 9),
            bg="#e9ecef",
            fg="#6c757d",
            width=30,
            height=8,
            relief="groove",
            bd=1
        )
        self.lbl_foto.pack(side="left", padx=(0, 15))

        # Input Jumlah & Tombol Aksi di sebelah kanan foto
        right_action_frame = tk.Frame(middle_frame, bg="#ffffff")
        right_action_frame.pack(side="left", fill="both", expand=True)

        lbl_jumlah = tk.Label(
            right_action_frame,
            text="Jumlah Pengunjung (Orang):",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#2d6a4f",
            anchor="w"
        )
        lbl_jumlah.pack(fill="x", pady=(0, 2))

        self.entry_jumlah = tk.Entry(right_action_frame, font=("Segoe UI", 11), bg="#f8f9fa", bd=1, relief="solid")
        self.entry_jumlah.pack(fill="x", ipady=3, pady=(0, 10))
        self.entry_jumlah.insert(0, "1")

        # Tombol Aksi
        self.btn_detail = tk.Button(
            right_action_frame,
            text="📍 Lihat Detail",
            font=("Segoe UI", 9, "bold"),
            bg="#2d6a4f",
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.tampilkan_detail
        )
        self.btn_detail.pack(fill="x", ipady=5, pady=3)

        self.btn_hitung = tk.Button(
            right_action_frame,
            text="💰 Hitung Anggaran",
            font=("Segoe UI", 9, "bold"),
            bg="#d4a373",
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.hitung_total_biaya
        )
        self.btn_hitung.pack(fill="x", ipady=5, pady=3)

        self.btn_view_wishlist = tk.Button(
            right_action_frame,
            text="❤️ Wishlist Saya",
            font=("Segoe UI", 9, "bold"),
            bg="#52b788",
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.tampilkan_wishlist
        )
        self.btn_view_wishlist.pack(fill="x", ipady=5, pady=3)

        # Output Area Header
        lbl_hasil = tk.Label(
            card_main,
            text="Informasi & Rincian Perjalanan:",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#2d6a4f",
            anchor="w"
        )
        lbl_hasil.pack(fill="x", padx=20, pady=(10, 2))

        # Output Text Box with Scrollbar
        text_frame = tk.Frame(card_main, bg="#ffffff")
        text_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        self.txt_hasil = tk.Text(
            text_frame,
            height=10,
            font=("Segoe UI", 10),
            bg="#f8f9fa",
            fg="#212529",
            bd=1,
            relief="solid",
            yscrollcommand=scrollbar.set
        )
        self.txt_hasil.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.txt_hasil.yview)
        self.txt_hasil.config(state="disabled")

        self.tampilkan_detail()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def cari_data_wisata(self, nama_pilihan):
        for item in DESTINASI_WISATA:
            if item["nama"] == nama_pilihan:
                return item
        return None

    def cek_status_wishlist_button(self):
        nama = self.combo_wisata.get()
        if nama in self.wishlist:
            self.btn_wishlist_toggle.config(text="❤️ Tersimpan", fg="#d90429")
        else:
            self.btn_wishlist_toggle.config(text="🤍 Simpan ke Wishlist", fg="#6c757d")

    def toggle_wishlist(self):
        nama = self.combo_wisata.get()
        if nama in self.wishlist:
            self.wishlist.remove(nama)
            messagebox.showinfo("Wishlist", f"'{nama}' dihapus dari wishlist.")
        else:
            self.wishlist.add(nama)
            messagebox.showinfo("Wishlist", f"'{nama}' berhasil disimpan ke wishlist! ❤️")
        self.cek_status_wishlist_button()

    def tampilkan_wishlist(self):
        self.lbl_foto.config(image="", text="📋\nWishlist View")
        self.current_image = None
        if not self.wishlist:
            hasil_str = "📋 DAFTAR WISHLIST SAYA:\n\nBelum ada destinasi wisata yang disimpan di wishlist."
        else:
            hasil_str = "📋 DAFTAR WISHLIST (FAVORIT) SAYA:\n" + "—"*45 + "\n\n"
            for idx, item in enumerate(self.wishlist, 1):
                hasil_str += f"{idx}. 🌿 {item}\n"

        self.txt_hasil.config(state="normal")
        self.txt_hasil.delete("1.0", tk.END)
        self.txt_hasil.insert(tk.END, hasil_str)
        self.txt_hasil.config(state="disabled")

    def tampilkan_detail(self):
        nama_pilihan = self.combo_wisata.get()
        wisata = self.cari_data_wisata(nama_pilihan)
        if not wisata:
            return

        # Load Foto jika ada
        gambar_file = wisata.get("gambar", "")
        if gambar_file and os.path.exists(gambar_file):
            try:
                pil_img = Image.open(gambar_file)
                pil_img = pil_img.resize((220, 140), Image.Resampling.LANCZOS)
                self.current_image = ImageTk.PhotoImage(pil_img)
                self.lbl_foto.config(image=self.current_image, text="")
            except Exception:
                self.lbl_foto.config(image="", text="[Gagal Memuat Gambar]")
        else:
            self.lbl_foto.config(image="", text=f"[Foto: {gambar_file}]\n(File gambar belum ada)")

        status_tiket = "Gratis" if wisata["harga_tiket"] == 0 else f"Rp {wisata['harga_tiket']:,}"
        status_wishlist = "❤️ Di Wishlist" if wisata["nama"] in self.wishlist else "🤍 Belum Disimpan"
        ulasan_teks = "\n   - ".join(wisata["ulasan"])

        detail_str = (
            f"📌 Destinasi       : {wisata['nama']} ({status_wishlist})\n"
            f"⭐ Rating Bintang  : {wisata['rating']} / 5.0\n"
            f"📍 Lokasi          : {wisata['lokasi']}\n"
            f"⏰ Jam Operasional : {wisata['jam_operasional']}\n"
            f"🎟️ Harga Tiket     : {status_tiket}\n"
            f"🗺️ Rute Maps       : {wisata['rute_maps']}\n\n"
            f"📖 Deskripsi       :\n{wisata['deskripsi']}\n\n"
            f"💬 Ulasan Pengguna :\n   - {ulasan_teks}"
        )

        self.txt_hasil.config(state="normal")
        self.txt_hasil.delete("1.0", tk.END)
        self.txt_hasil.insert(tk.END, detail_str)
        self.txt_hasil.config(state="disabled")
        self.cek_status_wishlist_button()

    def hitung_total_biaya(self):
        nama_pilihan = self.combo_wisata.get()
        input_jumlah = self.entry_jumlah.get()

        if not input_jumlah:
            messagebox.showerror("Error", "Jumlah pengunjung tidak boleh kosong!")
            return

        try:
            jumlah = int(input_jumlah)
            if jumlah <= 0:
                messagebox.showerror("Error", "Jumlah pengunjung harus lebih besar dari 0!")
                return

            wisata = self.cari_data_wisata(nama_pilihan)
            if not wisata:
                return

            harga_satuan = wisata["harga_tiket"]
            total_biaya = harga_satuan * jumlah
            status_tiket = "Gratis" if harga_satuan == 0 else f"Rp {harga_satuan:,} / orang"

            hasil_str = (
                f"🌿 KALBAR EXPLORE - ESTIMASI ANGGARAN\n"
                f"—"*45 + "\n\n"
                f"📌 Destinasi      : {wisata['nama']}\n"
                f"⭐ Rating         : {wisata['rating']} / 5.0\n"
                f"👥 Jml Pengunjung : {jumlah} Orang\n"
                f"🎟️ Harga Tiket    : {status_tiket}\n"
                f"⏰ Jam Operasional: {wisata['jam_operasional']}\n"
                f"💵 TOTAL ANGGARAN : Rp {total_biaya:,.2f}\n\n"
                f"🗺️ Rute Maps      : {wisata['ruto_maps'] if 'ruto_maps' in wisata else wisata['rute_maps']}"
            )

            self.txt_hasil.config(state="normal")
            self.txt_hasil.delete("1.0", tk.END)
            self.txt_hasil.insert(tk.END, hasil_str)
            self.txt_hasil.config(state="disabled")

        except ValueError:
            messagebox.showerror("Error", "Masukkan angka jumlah pengunjung yang valid!")

if __name__ == "__main__":
    root_login = tk.Tk()
    login_app = LoginWindow(root_login)
    root_login.mainloop()
