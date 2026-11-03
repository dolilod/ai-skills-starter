---
name: model-keuangan-sederhana
description: "Gunakan untuk membuat model kelayakan Excel sederhana berbasis penggerak dan menguji asumsi, dengan arus kas proyek dan ekuitas terpisah; bukan untuk audit atau persetujuan investasi."
---

# Model keuangan sederhana

Bangun workbook yang menjawab pertanyaan kelayakan tertentu, bukan tabel angka tempel. Semua hasil adalah proyeksi bersyarat, bukan jaminan atau rekomendasi investasi.

## Definisi arus kas

Gunakan tanda positif untuk penerimaan dan negatif untuk pengeluaran. Definisikan modal kerja operasi neto sebagai aset operasi lancar nonkas dikurangi kewajiban operasi lancar; **kenaikan** modal kerja adalah penggunaan kas. Catat cakupan posnya agar tidak menghitung ganda.

- **Arus kas proyek tanpa pendanaan (unlevered project cash flow):** `EBIT − pajak tunai proyek tanpa bunga + penyusutan/amortisasi − capex − perubahan modal kerja operasi neto`. Sertakan nilai terminal atau pelepasan hanya jika tersedia dasar dan waktunya. Arus kas ini **tidak** memasukkan bunga, pencairan pinjaman, atau pembayaran pokok.
- **Arus kas pemegang saham (equity cash flow):** `EBIT − bunga kas − pajak tunai dengan pendanaan + penyusutan/amortisasi − capex − perubahan modal kerja operasi neto + pencairan pinjaman − pembayaran pokok`. Perhitungkan komponen nonkas lain atau perbedaan kas yang relevan bila didukung input, dan ungkapkan penyesuaiannya. Dengan kata lain, arus kas ekuitas berbeda dari arus kas proyek karena bunga kas, perubahan pajak akibat pendanaan, dan arus utang tersebut.
- Pajak proyek dan pajak dengan pendanaan dihitung terpisah dari asumsi atau sumber yang berlaku. Jangan otomatis mengasumsikan rugi menghasilkan pengembalian pajak, bunga dapat dikurangkan, atau rugi dapat dikompensasikan; jika perlakuannya belum diketahui dan material, tandai hasil terkait belum dapat dihitung. Jangan mencampur pajak tanpa bunga dengan arus kas setelah bunga.
- Untuk NPV arus kas periodik, arus kas awal pada waktu nol ditambahkan langsung ke NPV arus kas setelah waktu nol. Gunakan tingkat diskonto proyek untuk arus kas proyek dan tingkat diskonto ekuitas untuk arus kas ekuitas; dasar setiap tingkat harus dinyatakan. IRR memakai seluruh arus kas termasuk waktu nol. Jika tidak ada solusi yang layak atau ada kemungkinan lebih dari satu IRR, nyatakan keterbatasannya, bukan memilih angka secara diam-diam.

## Langkah

1. Tetapkan keputusan yang didukung, mata uang, satuan, horizon, tanggal awal dan periodisitas. Daftar sumber atau asumsi untuk volume/harga, biaya, investasi, penyusutan, modal kerja, pajak, pendanaan dan tingkat diskonto; pisahkan data bersumber dari asumsi pengguna. Tandai data yang hilang, jangan menggantinya dengan angka dugaan atau nol.
2. Susun rantai penggerak yang relevan dengan kasus, misalnya volume × harga untuk pendapatan dan volume × biaya per unit untuk biaya variabel. Pastikan satuan dan waktu konsisten. Tentukan jadwal capex serta penyusutan, dan jadwal utang/bunga/pokok sesuai masukan, termasuk waktu pencairan dan dasar perhitungan bunga.
3. Buat `.xlsx` dengan sheet `Ringkasan`, `Asumsi`, `Driver`, `Model`, `Arus Kas` dan `Cek`, menggunakan alat yang tersedia. Nilai asumsi berasal dari sumber atau input yang ditandai; hasil turunan dan proyeksi memakai formula yang terhubung. Tampilkan arus kas proyek dan ekuitas secara terpisah, termasuk arus kas awal, dan hitung NPV/IRR masing-masing hanya jika input memadai.
4. Cek secara mandiri beberapa input penting sampai sumber, satu periode operasi, arus kas awal, rumus NPV dan saldo utang. Pastikan saldo utang akhir = saldo awal + pencairan − pokok, tanpa saldo negatif yang tidak dijelaskan, dan arus pendanaan tidak masuk arus kas proyek. Periksa rumus, rentang, tanda, unit, dan galat spreadsheet.
5. Jika mesin spreadsheet tersedia, hitung ulang dan periksa nilai hasil workbook. Jika tidak, nyatakan bahwa nilai tersimpan/cached belum diverifikasi; pemeriksaan rumus dan hitungan terpisah bukan bukti Excel sudah dikalkulasi. Bila `.xlsx` tidak dapat dibuat, tampilkan struktur dan perhitungan yang mungkin sebagai teks serta katakan berkas belum dibuat.
6. Serahkan workbook, sumber, asumsi dan keterbatasan, serta alasan hasil yang belum bisa dihitung. Keputusan, pengujian asumsi, tarif pajak dan validasi profesional tetap tanggung jawab manusia.

## Daftar periksa QA

- [ ] Setiap input dan asumsi material memiliki sumber, satuan, periode dan status yang jelas.
- [ ] Penggerak, pendapatan, biaya dan modal kerja terhubung dengan formula, bukan proyeksi tempel.
- [ ] Arus kas proyek mengecualikan bunga dan seluruh arus utang; arus kas ekuitas memasukkannya dan memakai pajak dengan pendanaan.
- [ ] Waktu nol, jadwal utang, tingkat diskonto, rumus NPV/IRR, dan hasil hitung ulang terpisah sesuai definisi.
- [ ] Hasil tidak dapat dihitung dan status kalkulasi workbook diungkap tanpa mengklaim verifikasi yang belum dilakukan.

## Contoh fiktif

Untuk demo, semua organisasi, orang, sumber, asumsi dan angka harus fiktif. Tampilkan **CONTOH FIKTIF — BUKAN DOKUMEN RESMI** pada setiap sheet atau halaman keluaran dan di awal ringkasan demo. Jangan memakai model atau angka nyata untuk latihan publik.
