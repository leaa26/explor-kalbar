import http.server
import socketserver
import urllib.parse
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from kalbar_explore_data import DESTINASI_WISATA

PORT = 8080

def render_page(active_cat="Semua"):
    if active_cat == "Semua":
        filtered = DESTINASI_WISATA
    else:
        filtered = [d for d in DESTINASI_WISATA if d["kategori"] == active_cat]

    cards_html = ""
    for item in filtered:
        wd = item.get('harga_weekday', item['harga_tiket'])
        we = item.get('harga_weekend', item['harga_tiket'])
        wd_str = f"Rp {wd:,}".replace(',', '.') if wd > 0 else "Gratis"
        we_str = f"Rp {we:,}".replace(',', '.') if we > 0 else "Gratis"
        tiket_str = f"Weekday: {wd_str} | Weekend: {we_str}" if wd != we else wd_str
        cat_class = {
            "Tempat Bersejarah": "cat-sejarah",
            "Seni & Budaya": "cat-budaya",
            "Wisata Air & Pantai": "cat-air",
            "Gunung & Alam": "cat-gunung"
        }.get(item["kategori"], "cat-taman")
        
        nama_js = item['nama'].replace("'", "\\'")
        lokasi_js = item['lokasi'].replace("'", "\\'")
        desk_js = item['deskripsi'].replace("'", "\\'")
        jam_js = item['jam_operasional'].replace("'", "\\'")
        maps_js = item['rute_maps'].replace("'", "\\'")

        card = f"""
        <div class="col-md-4 mb-4">
            <div class="card card-destination h-100">
                <div class="card-img-wrapper">
                    <img src="{item['gambar']}" alt="{item['nama']}" onerror="this.src='https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80'">
                </div>
                <div class="p-4 d-flex flex-column flex-grow-1">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span class="badge badge-sage px-3 py-1 rounded-pill">⭐ {item['rating']}</span>
                        <span class="cat-badge {cat_class}">{item['kategori']}</span>
                    </div>
                    <h4 class="fw-bold mb-2" style="color: var(--sage-dark);">{item['nama']}</h4>
                    <p class="text-muted small mb-2"><i class="fa-solid fa-location-dot text-danger"></i> {item['lokasi']}</p>
                    <p class="text-secondary small mb-3 flex-grow-1">{item['deskripsi']}</p>
                    
                    <div class="mb-3 p-2 bg-light rounded-3 small">
                        <div><strong>Tiket:</strong> {tiket_str}</div>
                        <div><strong>Jam:</strong> {item['jam_operasional']}</div>
                    </div>

                    <div class="d-flex gap-2">
                        <a href="{item['rute_maps']}" target="_blank" class="btn btn-outline-secondary btn-sm rounded-pill flex-grow-1"><i class="fa-solid fa-map"></i> Google Maps</a>
                        <button onclick="openDetail('{nama_js}', '{lokasi_js}', '{desk_js}', {item.get('harga_weekday', item['harga_tiket'])}, {item.get('harga_weekend', item['harga_tiket'])}, '{jam_js}', '{maps_js}')" class="btn btn-sage btn-sm rounded-pill flex-grow-1"><i class="fa-solid fa-calculator"></i> Detail & Kalkulator</button>
                    </div>
                </div>
            </div>
        </div>
        """
        cards_html += card

    def btn_class(cat):
        return "btn-sage" if active_cat == cat else "btn-outline-success"

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Explor Kalbar - Pesona Wisata Kalimantan Barat</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --sage-dark: #2d6a4f;
            --sage-medium: #40916c;
            --sage-light: #d8f3dc;
            --bg-cream: #f8f9fa;
        }}
        body {{ background-color: var(--bg-cream); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #212529; }}
        .navbar-custom {{ background-color: #ffffff; box-shadow: 0 2px 15px rgba(0,0,0,0.06); }}
        .hero-section {{
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1400&q=80');
            background-size: cover; background-position: center; border-radius: 20px; color: white; padding: 80px 30px; margin-bottom: 30px; text-align: center;
        }}
        .card-destination {{
            border: none; border-radius: 16px; overflow: hidden; transition: transform 0.3s ease, box-shadow 0.3s ease; background: #ffffff; box-shadow: 0 6px 20px rgba(0,0,0,0.06); height: 100%;
        }}
        .card-destination:hover {{ transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0,0,0,0.12); }}
        .card-img-wrapper {{ overflow: hidden; height: 200px; background-color: #e9ecef; }}
        .card-destination img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }}
        .card-destination:hover img {{ transform: scale(1.08); }}
        .btn-sage {{ background-color: var(--sage-dark); color: white; border-radius: 50px; font-weight: 600; padding: 8px 20px; }}
        .btn-sage:hover {{ background-color: #1b4332; color: white; }}
        .badge-sage {{ background-color: var(--sage-light); color: var(--sage-dark); font-weight: 600; }}
        .cat-badge {{ font-size: 0.75rem; padding: 5px 12px; border-radius: 50px; font-weight: 600; }}
        .cat-sejarah {{ background-color: #ffe5d9; color: #bc6c25; }}
        .cat-budaya {{ background-color: #e8dff5; color: #6a4c93; }}
        .cat-air {{ background-color: #d0f4de; color: #073b4c; }}
        .cat-gunung {{ background-color: #cbf3f0; color: #2ec4b6; }}
        .cat-taman {{ background-color: #ffb703; color: #ffffff; }}
    
        /* Animations & Reveal Effects */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .reveal-card {
            animation: fadeInUp 0.6s ease forwards;
            opacity: 0;
        }
        .card-destination {
            border: none; border-radius: 16px; overflow: hidden; 
            transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.4s cubic-bezier(0.165, 0.84, 0.44, 1); 
            background: #ffffff; box-shadow: 0 6px 20px rgba(0,0,0,0.06); height: 100%;
        }
        .card-destination:hover { 
            transform: translateY(-10px) scale(1.01); 
            box-shadow: 0 20px 35px rgba(45,106,79,0.15); 
        }
        .card-img-wrapper img {
            transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
        }
        .card-destination:hover img {
            transform: scale(1.1);
        }
        .fa-heart.fa-solid {
            animation: pulseHeart 0.3s ease;
        }
        @keyframes pulseHeart {
            0% { transform: scale(1); }
            50% { transform: scale(1.3); }
            100% { transform: scale(1); }
        }

    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-custom sticky-top py-3">
        <div class="container">
            <a class="navbar-brand fw-bold fs-4" href="/" style="color: var(--sage-dark);"><i class="fa-solid fa-tree"></i> EXPLOR KALBAR</a>
            <div class="d-flex align-items-center gap-3">
                <span class="badge bg-success px-3 py-2 rounded-pill"><i class="fa-solid fa-user-check"></i> Live Publik Mode (21 Destinasi)</span>
            </div>
        </div>
    </nav>

    <div class="container my-4">
        <div class="hero-section">
            <h1 class="fw-bold display-5 mb-3">Jelajahi Pesona Wisata Kalimantan Barat</h1>
            <p class="lead mb-4 col-md-8 mx-auto">Temukan 21 destinasi wisata terbaik Kalbar lengkap dengan foto asli, informasi tiket, jam operasional, ulasan, dan kalkulator estimasi anggaran perjalanan.</p>
        </div>

        <!-- Filter Kategori -->
        <div class="row mb-4 text-center">
            <div class="col-12">
                <div class="d-flex flex-wrap justify-content-center gap-2">
                    <a href="/?kategori=Semua" class="btn {btn_class('Semua')} rounded-pill px-4">Semua (21)</a>
                    <a href="/?kategori=Tempat Bersejarah" class="btn {btn_class('Tempat Bersejarah')} rounded-pill px-3">🏛️ Bersejarah</a>
                    <a href="/?kategori=Seni & Budaya" class="btn {btn_class('Seni & Budaya')} rounded-pill px-3">🎨 Seni & Budaya</a>
                    <a href="/?kategori=Wisata Air & Pantai" class="btn {btn_class('Wisata Air & Pantai')} rounded-pill px-3">🌊 Air & Pantai</a>
                    <a href="/?kategori=Gunung & Alam" class="btn {btn_class('Gunung & Alam')} rounded-pill px-3">⛰️ Gunung & Alam</a>
                    <a href="/?kategori=Taman Kota & Rekreasi" class="btn {btn_class('Taman Kota & Rekreasi')} rounded-pill px-3">🌳 Taman & Rekreasi</a>
                </div>
            </div>
        </div>

        <!-- Grid Destinasi -->
        <div class="row">
            {cards_html}
        </div>
    </div>

    <!-- Modal Detail & Kalkulator -->
    <div class="modal fade" id="detailModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 rounded-4 shadow">
          <div class="modal-header bg-success text-white rounded-top-4">
            <h5 class="modal-title fw-bold" id="modalTitle">Detail Destinasi</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            <p id="modalLokasi" class="text-muted small mb-2"></p>
            <p id="modalDeskripsi" class="mb-3"></p>
            <div class="alert alert-success py-2 small">
                <div><strong>Jam Buka:</strong> <span id="modalJam"></span></div>
                <div><strong>Harga Tiket Masuk:</strong> Rp <span id="modalTiket"></span></div>
            </div>

            <hr>
            <h6 class="fw-bold text-success mb-3"><i class="fa-solid fa-calculator"></i> Kalkulator Estimasi Anggaran Wisata</h6>
            <div class="mb-3">
                <label class="form-label small fw-bold">Jumlah Orang (Pengunjung):</label>
                <input type="number" id="calcOrang" class="form-control form-control-sm" value="1" min="1" oninput="hitungBudget()">
            </div>
            <div class="mb-3">
                <label class="form-label small fw-bold">Estimasi Biaya Transportasi & Kuliner (Rp):</label>
                <input type="number" id="calcTambahan" class="form-control form-control-sm" value="50000" step="10000" oninput="hitungBudget()">
            </div>
            <div class="p-3 bg-light rounded-3 text-center">
                <span class="small text-muted">Total Estimasi Biaya Perjalanan:</span>
                <h4 class="fw-bold text-success mb-0" id="totalBudget">Rp 0</h4>
            </div>
          </div>
          <div class="modal-footer border-0">
            <a id="modalMapsBtn" href="#" target="_blank" class="btn btn-outline-success btn-sm rounded-pill"><i class="fa-solid fa-map-location-dot"></i> Buka Rute Google Maps</a>
            <button type="button" class="btn btn-secondary btn-sm rounded-pill" data-bs-dismiss="modal">Tutup</button>
          </div>
        </div>
      </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let currentWd = 0;
        let currentWe = 0;
        function openDetail(nama, lokasi, deskripsi, wd, we, jam, maps) {{
            document.getElementById('modalTitle').innerText = nama;
            document.getElementById('modalLokasi').innerHTML = '<i class="fa-solid fa-location-dot text-danger"></i> ' + lokasi;
            document.getElementById('modalDeskripsi').innerText = deskripsi;
            document.getElementById('modalJam').innerText = jam;
            currentWd = parseInt(wd) || 0;
            currentWe = parseInt(we) || 0;
            document.getElementById('modalTiket').innerHTML = `Weekday: ${currentWd === 0 ? 'Gratis' : 'Rp ' + currentWd.toLocaleString('id-ID')} | Weekend: ${currentWe === 0 ? 'Gratis' : 'Rp ' + currentWe.toLocaleString('id-ID')}`;
            document.getElementById('modalMapsBtn').href = maps;
            
            hitungBudget();
            new bootstrap.Modal(document.getElementById('detailModal')).show();
        }}

        function hitungBudget() {{
            const hari = document.getElementById('calcHari') ? document.getElementById('calcHari').value : 'weekday';
            const harga = hari === 'weekend' ? currentWe : currentWd;
            let orang = parseInt(document.getElementById('calcOrang').value) || 1;
            let tambahan = parseInt(document.getElementById('calcTambahan').value) || 0;
            let total = (harga * orang) + tambahan;
            document.getElementById('totalBudget').innerText = total === 0 ? 'Gratis' : 'Rp ' + total.toLocaleString('id-ID');
        }}
    </script>
</body>
</html>
"""
    return html

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        
        if path == "/" or path == "":
            active_cat = query.get("kategori", ["Semua"])[0]
            html = render_page(active_cat)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            super().do_GET()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
