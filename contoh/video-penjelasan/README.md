# Latihan: membuat video penjelasan dengan AI

**CONTOH FIKTIF — BUKAN DOKUMEN RESMI**

Paket ini mendampingi skill [video-penjelasan-bernarasi](../../skills/video-penjelasan-bernarasi/SKILL.md). Fokusnya pemula yang ingin membuat video pendek yang benar-benar menjelaskan sesuatu.

## Tiga bagian

1. **Dari topik menjadi tujuan belajar.** Ubah permintaan umum menjadi tujuan, contoh, dan prompt yang dapat dikerjakan.
2. **Pasangkan ucapan dengan gambar.** Pecah naskah menjadi adegan dan tentukan kapan gambar berubah mengikuti narator.
3. **Periksa sebelum dibagikan.** Periksa isi, suara, takarir dan berkas. Ubah bagian yang salah tanpa mengulang semuanya.

Semua bagian memakai contoh fiktif yang sama: memberi nama berkas `2026-10-01_laporan-v01.pdf` agar bisa dicari. Tidak ada data organisasi nyata. Durasi sasaran sekitar satu menit per bagian, tetapi durasi akhir mengikuti rekaman suara dan jeda yang diperiksa.

## Berkas

- [prompt-siap-salin.md](prompt-siap-salin.md): prompt latihan, dapat ditempel ke AI yang memiliki alat yang sesuai.
- [seri.json](seri.json): naskah lengkap, aksi visual, teks layar, dan kata pemicu per adegan. Waktu akhir belum ditentukan.
- [naskah-storyboard.md](naskah-storyboard.md): versi yang mudah dibaca tanpa alat pengembang.

## Mulai tanpa Terminal

1. Buka tautan skill di atas. Klik **Raw**, lalu salin isinya ke berkas bernama `SKILL.md` dalam folder `video-penjelasan-bernarasi`.
2. Jika aplikasi Anda mendukung folder skill, ikuti cara pemuatan skill aplikasi tersebut. Jika tidak, tempel instruksi skill dan prompt latihan dalam percakapan yang sama. Ini memberi petunjuk, bukan menambahkan alat baru.
3. Salin prompt latihan. Minta AI memeriksa alat yang tersedia dahulu. Jangan menempelkan kata sandi, kunci API, atau dokumen rahasia.
4. Tinjau pembuka dan satu contoh sebelum meminta semua bagian dirender. Jika alat suara belum tersedia, hasil pertama yang benar adalah paket naskah, bukan klaim bahwa video sudah selesai.

## Status paket

Paket berisi **naskah dan storyboard**, bukan MP4 bernarasi atau takarir final. Jangan memakai perkiraan durasi sebagai timecode SRT. Suara, sinkronisasi, durasi aktual dan hasil video harus diperiksa setelah produksi. Publikasi ke saluran mana pun adalah tindakan terpisah.

## Alur produksi yang dapat diteruskan

Gunakan engine [narrated-explainer-video](https://github.com/dolilod/narrated-explainer-video) atau alat video lain yang sudah tersedia dan disetujui. Pertahankan naskah sebagai sumber tunggal. Simpan audio per kalimat, bangun urutan visual dari waktu audio, lalu ekspor MP4 dan SRT. Ubah satu bagian dahulu saat memperbaiki kesalahan. Jangan memasang ulang paket yang sudah tersedia.
