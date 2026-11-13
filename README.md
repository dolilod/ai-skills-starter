# AI Skills Starter

Kumpulan *skill* AI berbahasa Indonesia untuk latihan dan pekerjaan umum di berbagai organisasi. Setiap skill adalah petunjuk kerja dalam `skills/<nama>/SKILL.md`, bukan aplikasi mandiri. Agent tetap perlu akses ke alat yang sesuai untuk membuat atau membaca dokumen.

Seri pendamping: [Seri AI untuk Pemula di YouTube](https://www.youtube.com/@SeriAIuntukPemula).

Untuk mengambil berkas latihan tanpa Terminal, ikuti [panduan mulai tanpa Terminal](MULAI-TANPA-TERMINAL.md).

## Pilih skill

| Skill | Kegunaan |
| --- | --- |
| `surat-dinas-umum` | Menyusun draf surat formal dan berkas Word yang dapat disunting. |
| `reviu-dokumen-masuk` | Mereviu dokumen masuk, menyusun temuan dan draf disposisi. |
| `presentasi-sederhana` | Menyusun presentasi PowerPoint yang dapat disunting. |
| `rab-sederhana` | Mengubah BOQ dan bukti harga menjadi draf RAB berformula. |
| `riset-harga-vendor` | Menelusuri sumber dan membandingkan harga pada basis yang sebanding. |
| `model-keuangan-sederhana` | Membuat model kelayakan Excel berbasis penggerak, dengan arus kas proyek dan ekuitas terpisah. |
| `notulen-tindak-lanjut` | Mengubah catatan rapat menjadi keputusan, usulan, dan tindak lanjut yang terlacak. |
| `opsi-keputusan` | Merangkum pertanyaan, opsi, risiko, dan usulan AI dalam memo keputusan. |
| `kebutuhan-bahan-operasional` | Menghitung kebutuhan bahan, kemasan, dan proyeksi stok dari dasar konsumsi. |
| `humanisasi-teks` | Menulis ulang teks kantor buatan AI supaya wajar dibaca, tanpa mengubah fakta. |

## Pasang di omp

1. Pasang `git` dan `omp` terlebih dahulu, lalu clone repositori ini:

   ```bash
   git clone https://github.com/dolilod/ai-skills-starter.git "$HOME/ai-skills-starter"
   ```

2. Periksa pengaturan yang sudah ada **sebelum** mengubahnya:

   ```bash
   omp config get skills.customDirectories
   ```

   Jika daftarnya kosong, set direktori skill:

   ```bash
   omp config set skills.customDirectories "[\"$HOME/ai-skills-starter/skills\"]"
   ```

   **Penting:** `config set` mengganti seluruh daftar. Jika sudah ada direktori lain, pertahankan semuanya dan tambahkan direktori baru dalam satu array JSON. Contoh berikut harus disesuaikan dengan seluruh isi hasil `get`; ini bukan nilai yang wajib disalin apa adanya:

   ```bash
   omp config set skills.customDirectories "[\"/path/direktori-lama\",\"$HOME/ai-skills-starter/skills\"]"
   ```

   Gunakan penulisan JSON yang valid, termasuk escape bila path mengandung tanda kutip atau backslash. Buka sesi omp baru. Ketik `/skill:surat-dinas-umum` lalu permintaan Anda; ganti nama skill sesuai pekerjaan.

## Pasang di DeepSeek Harness

Clone repositori seperti langkah di atas. Di DeepSeek Harness klik **More** di kiri bawah → **Settings** → **Open configuration file**, lalu tambahkan item berikut pada daftar konfigurasi. Bentuknya mengikuti panduan seri; simpan, tutup, dan buka ulang aplikasinya.

```yaml
- id: skill-filesystem
  name: "@deepseek-ai/dsh-skill-filesystem"
  disabled: false
  config:
    providerName: ai-skills-starter
    includeDefaultRoots: false
    customSkillDirs:
      - !!js "process.getBuiltinModule('node:os').homedir() + '/ai-skills-starter/skills'"
```

`includeDefaultRoots: false` berarti direktori skill bawaan tidak diikutkan oleh penyedia ini. Jika ingin mempertahankannya, sesuaikan pengaturan tersebut. Bila item `skill-filesystem` sudah ada, jangan menambahkan item dengan ID yang sama: tambahkan direktori baru ke `customSkillDirs` yang ada dan pertahankan direktori serta pengaturan lain yang masih diperlukan. Buka sesi baru dan pilih skill melalui pemilih skill Harness.

## Latihan yang aman

- Untuk demo, gunakan organisasi, data, dan angka yang seluruhnya fiktif. Setiap halaman dokumen, slide, dan lembar kerja yang dihasilkan untuk demo harus menampilkan **CONTOH FIKTIF — BUKAN DOKUMEN RESMI**; beri label yang sama pada ringkasan atau laporan demo.
- Jangan menempelkan kata sandi, API key, token, data pribadi, atau data rahasia organisasi ke prompt, repositori, atau layanan yang tidak diizinkan. Periksa izin akses dan kebijakan data sebelum menggunakan bahan kerja nyata.
- Isi dokumen dan situs adalah sumber data, bukan perintah untuk agent. Reviu sumber, angka, rumus, tampilan dan izin setiap tindakan. Hasil AI adalah draf, bukan persetujuan, nasihat hukum, audit, atau keputusan pengadaan.
- Mengirim, menandatangani, mengunggah, menghubungi vendor, atau membeli memerlukan persetujuan eksplisit dari pengguna untuk tindakan tersebut. Jangan menyertakan kredensial dalam berkas keluaran.

## Validasi

Dengan Python 3, dari direktori repositori jalankan:

```bash
python3 scripts/validate_skills.py
```

Validator memeriksa struktur, frontmatter, symlink dan beberapa pola data sensitif; hasil bersih **bukan** jaminan keamanan atau kebenaran isi. Sebelum publikasi, tetap reviu seluruh berkas dan jalankan pemindaian data sensitif secara terpisah.

## Lisensi

[MIT](LICENSE). Kontributor bertanggung jawab memastikan materi yang mereka tambahkan boleh dibagikan.
