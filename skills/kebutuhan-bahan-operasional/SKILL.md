---
name: kebutuhan-bahan-operasional
description: "Gunakan untuk menghitung kebutuhan bahan operasional dari laju konsumsi, periode, cadangan, stok dan ukuran kemasan yang diberikan; bukan untuk menetapkan dosis, harga, atau melakukan pembelian."
---

# Kebutuhan bahan operasional

Hitung kebutuhan per bahan dan periode berdasarkan masukan yang dapat ditelusuri. Keluaran adalah **rencana untuk reviu**, bukan pesanan atau penetapan standar konsumsi.

## Langkah

1. Untuk setiap bahan, catat sumber dan satuan **laju konsumsi**, **lama periode**, **target cadangan di akhir periode**, **stok awal yang dapat digunakan**, dan **isi per kemasan**. Gunakan laju konsumsi yang diberikan atau disetujui pengguna; riwayat pembelian saja bukan bukti laju pemakaian. Stok harus tersedia untuk kebutuhan periode tersebut; catat stok rusak, kedaluwarsa, teralokasi untuk keperluan lain, atau kedatangan yang belum pasti secara terpisah dan jangan menghitungnya sebagai stok tersedia. Hindari pengurangan ganda bila saldo sumber sudah mengecualikannya.
2. Samakan satuan laju, periode, stok, cadangan dan kemasan. Konversi hanya menggunakan faktor yang tersedia dan bersumber. Jika laju atau periode belum diketahui, tandai **pemakaian belum dapat dihitung**; jika cadangan, stok atau kemasan belum diketahui, tandai bagian yang bergantung padanya **belum dapat dihitung**. Data yang tidak diketahui bukan nol; nilai nol digunakan hanya jika dinyatakan atau dihitung dari data yang lengkap.
3. Untuk setiap baris dengan input lengkap, tampilkan rumus dan hasilnya dalam satuan yang sama:
   - `pemakaian = laju konsumsi × lama periode`.
   - `kebutuhan bersih = maksimum(0, pemakaian + target cadangan − stok awal tersedia)`.
   - `jumlah kemasan = pembulatan ke atas(kebutuhan bersih ÷ isi per kemasan)`; isi per kemasan harus lebih besar dari nol. Jika kebutuhan bersih nol, jumlah kemasan juga nol.
   - `jumlah bahan yang direncanakan = jumlah kemasan × isi per kemasan`.
4. Periksa neraca akhir dengan rumus `stok akhir proyeksi = stok awal tersedia + jumlah bahan yang tiba dalam periode − pemakaian`. Cadangan adalah target untuk dibandingkan dengan stok akhir, bukan pemakaian yang dikurangkan dari stok fisik. Jika seluruh jumlah yang direncanakan **belum terbukti tiba dalam periode**, tampilkan neraca dengan label **skenario: seluruh jumlah rencana tiba dalam periode**, bukan sebagai kedatangan pasti; catat pula risiko kekurangan bila waktunya tidak diketahui. Nilai neraca negatif berarti kekurangan, bukan stok fisik negatif. Bandingkan stok akhir proyeksi dengan target cadangan dan jelaskan apakah target tercapai.
5. Sajikan tabel per bahan dengan sumber tiap input, satuan dan periode, rumus serta hasil pemakaian, kebutuhan bersih, jumlah kemasan, jumlah bahan, stok akhir dan status pemeriksaan. Jika data penting kurang, tampilkan hasil yang memang dapat dihitung dan daftar data yang dibutuhkan, tanpa menyebutnya rencana lengkap. Tinjau waktu kedatangan dan keterbatasan data bersama manusia; jangan mengubah laju/dosis atau membuat pesanan tanpa persetujuan dan kewenangan yang sesuai.

## Daftar periksa QA

- [ ] Setiap input memiliki sumber, satuan dan periode; laju konsumsi tidak direka.
- [ ] Satuan konsisten; faktor konversi bersumber dan isi kemasan lebih besar dari nol.
- [ ] Kebutuhan bersih dan pembulatan kemasan dihitung per baris; tidak ada pemesanan saat kebutuhan bersih nol.
- [ ] Neraca stok akhir dihitung ulang, target cadangan tidak dikurangkan sebagai pemakaian, dan kekurangan terlihat.
- [ ] Kedatangan yang belum pasti dan input kosong tidak diperlakukan sebagai fakta atau nol.

## Contoh fiktif

Untuk demo, gunakan hanya organisasi, orang, bahan, sumber dan angka yang fiktif. Tampilkan **CONTOH FIKTIF — BUKAN DOKUMEN RESMI** pada setiap halaman atau sheet keluaran dan di awal ringkasan demo. Jangan memakai data operasi atau stok nyata untuk latihan publik.
