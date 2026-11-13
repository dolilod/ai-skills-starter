---
name: video-penjelasan-bernarasi
description: "Gunakan untuk membuat video penjelasan pendek berbahasa Indonesia dari tujuan belajar, contoh, naskah, visual dan narasi; termasuk paket produksi bila alat suara atau render belum tersedia."
---

# Video penjelasan bernarasi

Hasilkan video yang memperlihatkan cara kerja sebuah gagasan, bukan sekadar membacakan slide. Skill ini adalah petunjuk kerja, bukan aplikasi atau layanan pembuat suara. Jangan mengklaim MP4 sudah dibuat bila baru ada naskah.

## Langkah

1. Tetapkan satu kemampuan yang dapat dilakukan penonton setelah menonton. Gunakan audiens, bahasa, durasi, dan bahan pengguna. Bila belum ditentukan, mulai dari pemula dewasa, bahasa Indonesia, dan satu video 60–90 detik. Ini titik awal, bukan batas wajib. Untuk seri, setiap bagian harus memberi hasil kecil yang dapat dicoba sendiri.
2. Periksa bahan dan kemampuan alat sebelum produksi. Bedakan fakta bersumber, contoh fiktif, dan asumsi. Periksa apakah perender, suara bahasa Indonesia, font, dan penyimpanan tersedia. Di Linux jangan mengandalkan perintah macOS `say`. Jangan memasang dependensi atau mengunduh model tanpa izin.
3. Tulis naskah dan storyboard bersamaan. Untuk setiap adegan catat: kalimat narator, yang terlihat, gerakan yang menjelaskan hubungan, dan kata pemicu perubahan. Mulai dari masalah konkret, tunjukkan contoh, lalu akhiri dengan langkah yang bisa dicoba. Pecah istilah teknis saat pertama dipakai. Gambar dan ucapan harus menjelaskan hal yang sama.
4. Buat pembuka dan satu contoh representatif dahulu. Gunakan gambar buatan sendiri untuk jumlah, urutan, dan diagram yang harus tepat. Jangan memakai foto atau logo yang tidak berhak digunakan. Hindari gerakan dekoratif yang bersaing dengan penjelasan. Bedakan naskah, rekaman suara, dan gambar sebagai komponen yang bisa diperbaiki terpisah.
5. Gunakan penyedia suara dan biaya yang sudah disetujui. Jelaskan ke mana teks dikirim. Jangan mengirim bahan rahasia atau menyalin suara orang tanpa izin. Simpan audio per kalimat agar revisi kecil tidak mengulang semuanya. Jika suara atau jaringan tidak tersedia, selesaikan naskah, storyboard dan petunjuk produksi; laporkan bahwa video bernarasi belum dihasilkan. Jangan menggantinya dengan suara tiruan atau video diam tanpa penjelasan.
6. Setelah contoh lolos pemeriksaan sesuai kebutuhan proyek, lanjutkan produksi. Susun visual mengikuti rekaman suara yang benar-benar dihasilkan. Nilai, jawaban, status dan label baru muncul pada kata pemicunya. Jangan membagi durasi narasi rata untuk menebak waktu muncul. Jika naskah berubah, perbarui audio, visual dan takarir yang terdampak.
7. Ekspor MP4 dan SRT dengan alat yang tersedia. Untuk tutorial mendatar, 1920×1080 dan 30 fps adalah titik awal yang wajar; gunakan format pengguna bila berbeda. Periksa ukuran huruf pada layar kecil, batas aman, takarir, bunyi yang terpotong, sinkronisasi, durasi dan decoding. Jangan membuat timecode SRT final dari perkiraan baca saja.
8. Serahkan MP4, SRT, sumber yang dapat disunting, perintah pembangunan ulang, dan catatan pemeriksaan. Nyatakan bagian yang belum diperiksa, termasuk bila suara belum didengarkan. Mengunggah ke YouTube, mengirim ke orang lain, berlangganan layanan, atau menerbitkan berkas memerlukan izin untuk tindakan tersebut.

Jika engine `narrated-explainer-video` sudah tersedia, gunakan workflow dan pemeriksaan di dalamnya untuk animasi, suara dan render. Repo sumber: https://github.com/dolilod/narrated-explainer-video. Jangan menganggap membaca atau menyalin skill ini otomatis memasang engine tersebut.

## Daftar periksa QA

- [ ] Penonton memiliki satu hasil belajar yang jelas; contoh mendukung hasil tersebut.
- [ ] Klaim dan angka cocok dengan sumber, atau berlabel fiktif.
- [ ] Setiap visual menerangkan ucapan; angka dan jawaban tidak bocor sebelum waktunya.
- [ ] Font terbaca dan teks tidak bertabrakan dengan takarir.
- [ ] Suara yang benar-benar dihasilkan cocok dengan naskah; batas pemeriksaan pendengaran dinyatakan.
- [ ] SRT mengikuti suara, bukan durasi perkiraan.
- [ ] MP4 dapat diputar dan selesai utuh; sumber dan petunjuk pembangunan ulang tersedia.
- [ ] Status dibedakan: paket naskah, draf video, siap ditinjau, atau siap terbit. Pemeriksaan teknis bukan izin terbit.

## Contoh fiktif

Contoh: jelaskan kepada pegawai baru organisasi fiktif cara memberi nama berkas agar mudah ditemukan. Gunakan berkas, orang dan angka rekaan. Tampilkan **CONTOH FIKTIF — BUKAN DOKUMEN RESMI** pada setiap adegan demo dokumen serta di awal ringkasan. Jangan memakai dokumen kerja nyata untuk latihan publik.

Paket latihan: [seri tiga bagian dan prompt yang bisa disalin](../../contoh/video-penjelasan/README.md).
