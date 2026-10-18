import os
from pathlib import Path
import urllib.request

BASE_DIR = Path(__file__).resolve().parent
TARGET_DIR = BASE_DIR / "data" / "raw"
TARGET_DIR.mkdir(parents=True, exist_ok=True)

# URL PDF Publik yang jauh lebih stabil
DATASET_URLS = {
    "first_aid_workbook.pdf": (
        "https://www.sja.org.uk/globalassets/documents/mini-first-aid/mini-first-aid-workbook.pdf"
    ),
    "sample_pdf.pdf": (
        "https://raw.githubusercontent.com/mozilla/pdf.js/master/web/compressed.tracemonkey-pldi-09.pdf"
    ),
}

# Teks cadangan materi pertolongan pertama jika internet mati/gagal download
FALLBACK_TEXT = """
PANDUAN PERTOLONGAN PERTAMA PADA KECELAKAAN (P3K)

1. PENANGANAN LUKA BAKAR RINGAN
- Siram bagian yang terbakar dengan air mengalir bersih selama minimal 10-20 menit.
- Jangan gunakan es batu, mentega, atau pasta gigi pada luka bakar.
- Tutup luka dengan kain kasa steril yang tidak lengket.
- Jika timbul lepuhan, jangan dipecahkan sendiri.

2. PENANGANAN LUKA PERDARAHAN
- Tekan area luka secara langsung menggunakan kain bersih atau kasa steril.
- Posisikan bagian tubuh yang terluka lebih tinggi dari jantung jika memungkinkan.
- Jangan melepas kain yang sudah basah oleh darah, tambahkan kain baru di atasnya.
- Segera cari bantuan medis jika darah tidak berhenti dalam 10 menit.

3. PENANGANAN PINGSAN
- Baringkan korban di tempat yang aman dan sejuk.
- Longgarkan pakaian yang ketat (kerah baju, ikat pinggang).
- Angkat kaki korban sekitar 20-30 cm lebih tinggi dari dada.
- Jangan berikan makanan atau minuman saat korban belum sadar sepenuhnya.
"""


def create_fallback_file():
  """Membuat file panduan lokal jika unduhan dari internet gagal."""
  file_path = TARGET_DIR / "panduan_p3k_dasar.txt"
  if not file_path.exists():
    with open(file_path, "w", encoding="utf-8") as f:
      f.write(FALLBACK_TEXT.strip())
    print(
        "📝 [FALLBACK] Berhasil membuat file materi 'panduan_p3k_dasar.txt' di"
        " folder data/raw/"
    )


def download_pdfs():
  print("=" * 60)
  print("🩺 MENGUNDUH DATASET KESEHATAN & PERTOLONGAN PERTAMA")
  print("=" * 60)

  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  download_success = False

  for filename, url in DATASET_URLS.items():
    file_path = TARGET_DIR / filename

    if file_path.exists():
      print(f"⏩ [SKIPPED] {filename} sudah ada.")
      download_success = True
      continue

    print(f"⏳ [DOWNLOADING] {filename}...")
    try:
      req = urllib.request.Request(url, headers=headers)
      with (
          urllib.request.urlopen(req, timeout=15) as response,
          open(file_path, "wb") as out_file,
      ):
        out_file.write(response.read())
      print(f"✅ [SUCCESS] Berhasil disimpan ke {file_path}")
      download_success = True
    except Exception as e:
      print(f"❌ [FAILED] Gagal mengunduh {filename}: {e}")

  # Jika semua download gagal/internet offline, buat file cadangan lokal
  if not download_success and not os.listdir(TARGET_DIR):
    print("\n⚠️ Menggunakan data cadangan lokal karena unduhan gagal...")
    create_fallback_file()
  else:
    create_fallback_file()

  print("\n🎉 Proses siap! Data tersimpan di folder 'data/raw/'.")
  print(
      "Silakan jalankan 'python3 -m streamlit run app.py' lalu klik 'Indeks"
      " Ulang Dokumen PDF'."
  )


if __name__ == "__main__":
  download_pdfs()