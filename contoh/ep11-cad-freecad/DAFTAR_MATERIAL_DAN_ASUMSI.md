# CONTOH FIKTIF — BUKAN DOKUMEN RESMI

> **CONTOH FIKTIF — BUKAN DOKUMEN RESMI** — dokumen latihan fiktif. Bukan dokumen resmi, bukan untuk fabrikasi, konstruksi, atau verifikasi struktur.

## Ringkasan proyek

| Item | Nilai |
|---|---|
| Proyek | Bordes Baja 1500 × 1200 mm dengan Railing Pipa Ø50 mm |
| Tanggal | 2026-11-03 |
| Satuan | milimeter (mm) |
| Skala gambar | 1:10, kertas A2 |
| Proyeksi | Eropa (first angle) |
| Tinggi railing | 1000 mm dari permukaan atas pelat |
| Pipa railing | baja OD 50 mm, tebal dinding 3,0 mm |
| Jarak antar tiang (as) | 700 mm (maksimum 1000 mm) |
| Jumlah tiang | 3 bh |
| Panjang pipa total | 5,62 m |

## 1. Daftar kebutuhan material

| No | Komponen | Spesifikasi | Jumlah | Dimensi / panjang | Volume (m³) | Berat (kg) |
|---:|---|---|---:|---|---:|---:|
| 1 | Pelat bordes | Baja, t = 10 mm | 1 lbr | 1500 × 1200 mm | 0,0180 | 141,2 |
| 2 | Tiang railing | Pipa baja OD 50 × 3,0 mm | 3 bh | 940 mm/tiang | 0,0012 | 9,8 |
| 3 | Top rail | Pipa baja OD 50 × 3,0 mm | 1 bh | 1500 mm | 0,0007 | 5,2 |
| 4 | Mid rail | Pipa baja OD 50 × 3,0 mm | 2 bh | 650 mm/bh | 0,0006 | 4,5 |
| 5 | Base plate | Baja, t = 10 mm, 4 lubang Ø14 | 3 bh | 100 × 100 mm | 0,0003 | 2,2 |
| 6 | Baut angkur | M12 × 100 (disederhanakan) | 12 bh | Ø12, pola 60 × 60 mm | — | — |
| 7 | Cat dasar + finish | Sistem cat baja | ± 0,9 m² | — | — | — |

**Total berat baja (tanpa baut angkur dan cat): 162,9 kg.**

### 1.1 Rekap pipa Ø50 × 3,0 mm

| Segmen | Jumlah | Panjang satuan | Total |
|---|---:|---:|---:|
| Tiang (post) | 3 | 940 mm | 2.820 mm |
| Top rail | 1 | 1.500 mm | 1.500 mm |
| Mid rail | 2 | 650 mm | 1.300 mm |
| **Total** | | | **5.620 mm = 5,62 m** |

- Berat pipa dihitung dari volume geometri (pipa berongga) × 7.850 kg/m³: **19,5 kg**.
- Kebutuhan order dengan allowance 5%: **5,91 m**.
- Asumsi batang pipa standar 6 m: **1 batang** cukup untuk kebutuhan bersih 5,62 m (sisa ± 0,38 m). Dengan allowance 5% (5,91 m) masih di bawah 6 m, tetapi kehilangan potong/kerf belum dihitung.

### 1.2 Pemeriksaan jarak tiang

- Jumlah tiang = 3 bh; bentang = 2 × 700 mm.
- Jarak antar tiang 700 mm ≤ batas 1000 mm → **memenuhi**.
- As tiang ujung berjarak 50 mm dari tepi pelat; base plate 100 × 100 mm tepat di dalam tepi pelat.

## 2. Asumsi desain

1. **Fiktif**: seluruh model, gambar, dan angka adalah contoh latihan; tidak ada perhitungan struktur, angin, seismik, fatik, atau verifikasi kapasitas.
2. **Satuan** mm; elevasi acuan ±0,00 adalah permukaan atas pelat bordes.
3. **Pelat bordes**: baja 1500 × 1200 × 10 mm, datar (bukan pelat kembang/checkered), satu lembar. Struktur penumpu, balok, kolom, pondasi, dan sambungan ke struktur utama tidak dimodelkan dan di luar lingkup.
4. **Railing** dipasang pada satu sisi panjang 1500 mm (sisi y = 0 pada model), dengan as tiang dan as rail 50 mm dari tepi pelat.
5. **Tinggi railing** 1000 mm diukur dari permukaan atas pelat sampai sisi atas top rail.
6. **Pipa**: baja karbon OD 50 mm, tebal dinding 3,0 mm, mutu asumsi ASTM A53 / setara; ujung pipa terbuka (tanpa cap).
7. **Tiang**: 3 bh (bentang 2 × 700 mm), panjang 940 mm, dari atas base plate (z = 20 mm) sampai bawah top rail (z = 960 mm).
8. **Top rail** menerus 1500 mm pada z = 985 mm (as); **mid rail** 2 segmen × 650 mm pada z = 510 mm (as), dipasang di antara tiang.
9. **Base plate** 100 × 100 × 10 mm, 3 bh, dengan 4 lubang Ø14 per pelat; **baut angkur** M12 × 100, 12 bh, pola 60 × 60 mm, jarak tepi 20 mm.
10. **Baut angkur** pada model disederhanakan sebagai silinder Ø12 × 30 mm; ulir, mur, ring, dan washer tidak dimodelkan. Panjang nominal M12 × 100 hanya untuk daftar material.
11. **Las** fillet 4 mm pada sambungan tiang–base plate dan rail–tiang diasumsikan ada, tetapi tidak dimodelkan.
12. **Toleransi dan gap** las tidak dimodelkan; permukaan pelat dan pipa dianggap sempurna.
13. **Material** baja karbon; densitas 7.850 kg/m³ untuk perhitungan berat.
14. **Finishing**: cat dasar (primer) + cat finish, luas railing ± 0,9 m²; jenis dan warna cat tidak ditentukan.
15. **Gambar**: A2 (594 × 420 mm), skala 1:10, proyeksi Eropa (first angle), denah di bawah tampak depan; garis tersembunyi tidak ditampilkan pada denah agar gambar sederhana.
16. **DXF** ditulis sebagai DXF R12 (AC1009), satuan mm, layer terpisah untuk garis, dimensi, teks, dan label; teks memakai style ARIAL (arial.ttf) dan code page ANSI_1252.
17. **Label wajib** "CONTOH FIKTIF — BUKAN DOKUMEN RESMI" dicantumkan pada setiap file output dan pada gambar DXF (banner, title block, dan footer catatan).

## 3. Batasan

- Tidak untuk dipakai sebagai gambar kerja nyata, pemesanan material, atau dasar fabrikasi.
- Tidak ada jaminan kekuatan, stabilitas, defleksi, atau keselamatan.
- Setiap penggunaan nyata memerlukan perencanaan oleh insinyur struktur yang berwenang.

## 4. Cara menjalankan ulang

```bash
cd "Latihan-CAD"
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd buat_bordes_railing.py
```

Skrip berjalan headless, tidak membuka GUI, tidak menginstal paket, dan tidak mengakses jaringan.

## 5. File output

| File | Isi |
|---|---|
| `bordes_baja_1500x1200_railing.FCStd` | Model 3D FreeCAD (pelat, tiang, rail, base plate, baut, anotasi label) |
| `bordes_baja_1500x1200_railing.step` | Ekspor STEP AP214, termasuk teks label 3D |
| `gambar_kerja_bordes_baja_1500x1200.dxf` | Gambar kerja 2D: denah + tampak depan, berdimensi, A2 1:10 |
| `DAFTAR_MATERIAL_DAN_ASUMSI.md` | Dokumen ini |
| `pratinjau_gambar_kerja.png` | Pratinjau raster gambar kerja (alat bantu verifikasi) |

---

**CONTOH FIKTIF — BUKAN DOKUMEN RESMI**
