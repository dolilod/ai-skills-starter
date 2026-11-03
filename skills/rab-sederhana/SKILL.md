---
name: rab-sederhana
description: "Gunakan untuk menyusun draf RAB dari BOQ dan bukti harga yang disediakan, termasuk hitung ulang mandiri; bukan untuk menetapkan spesifikasi, HPS, atau menyetujui pengadaan."
---

# RAB sederhana

Ubah daftar kuantitas pekerjaan (*bill of quantities* atau BOQ) dan bukti harga menjadi draf anggaran yang terlacak. Beri label **DRAF — UNTUK REVIU, BUKAN PERSETUJUAN**. Reviu mandiri tidak menggantikan pemeriksaan independen oleh manusia.

## Langkah

1. Daftar setiap item BOQ dengan identitas, uraian, spesifikasi, kuantitas, satuan dan sumbernya. Daftar bukti harga dengan sumber atau tautan, tanggal, mata uang, satuan, syarat pajak dan pengiriman. Catat konflik, informasi hilang, dan harga yang hanya indikatif.
2. Cocokkan spesifikasi dan satuan antara BOQ dan harga. Konversi hanya dengan faktor dan kurs yang bersumber; catat rumusnya. Jika kuantitas, harga atau faktor wajib hilang, statusnya **belum dapat dihitung**, bukan nol. Jangan menganggap komponen yang tidak disebut sudah termasuk.
3. Hitung setiap baris dari kuantitas × harga per satuan yang sebanding. Pisahkan biaya tambahan, pajak, overhead atau kontinjensi hanya jika dasar dan tarifnya diberikan atau bersumber; cegah hitung ganda. Tampilkan subtotal per kelompok dan jumlah item yang sudah dihitung dari seluruh item. Bila ada item atau komponen yang belum diketahui, beri label **subtotal parsial**, bukan total lengkap.
4. Jika tersedia alat pembuat spreadsheet, buat `.xlsx` dengan sheet `Sumber`, `BOQ`, `RAB` dan `Cek`: masukan dapat ditelusuri, hitungan memakai formula yang terhubung ke masukan, dan status baris kosong tetap terlihat. Jika tidak dapat membuat berkas, tampilkan tabel dan rumus dalam teks, serta nyatakan bahwa Excel belum dibuat.
5. Hitung ulang nilai baris dan subtotal secara mandiri; cocokkan dengan rumus, jumlah baris berharga, dan komponen yang tertunda. Gunakan mesin spreadsheet untuk menghitung ulang workbook jika tersedia. Jika tidak, jelaskan bahwa nilai tersimpan/cached belum diverifikasi meskipun rumus dan hitungan terpisah diperiksa.
6. Serahkan draf, cakupan perhitungan, daftar celah, asumsi dan status pemeriksaan. Penetapan spesifikasi, harga resmi, pajak dan keputusan pengadaan tetap memerlukan pihak berwenang.

## Daftar periksa QA

- [ ] Setiap baris mengarah ke BOQ dan bukti harga; spesifikasi dan satuan sebanding.
- [ ] Faktor konversi dan semua parameter punya sumber; yang hilang tidak diam-diam menjadi nol.
- [ ] Harga termasuk/belum termasuk pajak dan pengiriman dinyatakan atau ditandai belum diketahui.
- [ ] Baris, subtotal dan jumlah item dicek ulang; tidak ada biaya ganda.
- [ ] Total parsial dan komponen tertunda jelas; status kalkulasi Excel diungkap.

## Contoh fiktif

Untuk demo, gunakan hanya BOQ, sumber harga, organisasi, orang dan angka fiktif. Tampilkan **CONTOH FIKTIF — BUKAN DOKUMEN RESMI** pada setiap sheet atau halaman keluaran dan di awal ringkasan demo. Jangan memakai harga atau dokumen nyata untuk latihan publik.
