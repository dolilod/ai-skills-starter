#!/usr/bin/env python3
"""Periksa struktur dan pola sensitif dasar pada repositori skill.

Jalankan: python3 scripts/validate_skills.py [--root DIREKTORI]
Validator ini hanya memeriksa frontmatter dengan nilai skalar satu baris.
Pemeriksaan pola tidak menggantikan reviu manusia sebelum publikasi.
"""

import argparse
import json
import os
import re
from pathlib import Path


NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIELD = re.compile(r"^([a-z][a-z0-9_-]*):\s*(.*)$")
SKIP = {".git", "__pycache__", "node_modules"}
MAX_SIZE = 5 * 1024 * 1024
CONTENT_RULES = (
    ("user-path", re.compile("/" + "Users/|[A-Za-z]:\\\\Users\\\\"), "path absolut pengguna"),
    ("cloud-path", re.compile("Mobile Documents|com~apple~CloudDocs"), "path penyimpanan pribadi"),
    ("credential", re.compile(r"AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|xox[baprs]-"), "pola kredensial"),
    ("credential", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    ("credential", re.compile(r"(?i)(?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"\s]{8,}"), "nilai rahasia tertulis langsung"),
    ("personal-id", re.compile(r"\b\d{15,16}\b"), "angka mirip identitas pribadi"),
)


class Report:
    def __init__(self, root):
        self.root = root
        self.count = 0

    def add(self, path, line, rule, message):
        try:
            location = path.relative_to(self.root).as_posix()
        except ValueError:
            location = str(path)
        print(f"{location}:{line}: {rule}: {message}")
        self.count += 1


def scalar(raw):
    if raw.startswith('"'):
        value = json.loads(raw)
        if not isinstance(value, str):
            raise ValueError("nilai bukan teks")
        return value
    if raw.startswith("'"):
        if len(raw) < 2 or not raw.endswith("'"):
            raise ValueError("kutip tidak ditutup")
        return raw[1:-1].replace("''", "'")
    return raw


def check_frontmatter(skill_dir, report):
    path = skill_dir / "SKILL.md"
    if path.is_symlink():
        return  # Symlink dilaporkan saat memeriksa struktur repositori.
    if not path.is_file():
        report.add(skill_dir, 0, "missing-skill", "SKILL.md tidak ditemukan")
        return
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        report.add(path, 1, "encoding", f"SKILL.md tidak dapat dibaca sebagai UTF-8: {exc}")
        return
    if not lines or lines[0] != "---":
        report.add(path, 1, "frontmatter", "baris pertama harus ---")
        return
    end = next((i for i, line in enumerate(lines[1:], 1) if line == "---"), None)
    if end is None:
        report.add(path, 1, "frontmatter", "penutup --- tidak ditemukan")
        return

    fields = {}
    for i, line in enumerate(lines[1:end], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = FIELD.fullmatch(line)
        if not match:
            report.add(path, i, "frontmatter", "gunakan field skalar satu baris")
            continue
        key, raw = match.groups()
        if key in fields:
            report.add(path, i, "frontmatter", f"field {key} ganda")
            continue
        try:
            fields[key] = (scalar(raw).strip(), i)
        except (ValueError, json.JSONDecodeError):
            report.add(path, i, "frontmatter", f"nilai {key} tidak valid")

    for key in ("name", "description"):
        if key not in fields or not fields[key][0]:
            report.add(path, fields.get(key, (None, 1))[1], "frontmatter", f"{key} wajib diisi")
    if "name" in fields and fields["name"][0]:
        value, line = fields["name"]
        if value != skill_dir.name or not NAME.fullmatch(value):
            report.add(path, line, "name", "name harus kebab-case dan sama dengan nama folder")
    if "description" in fields and len(fields["description"][0]) > 1024:
        report.add(path, fields["description"][1], "description", "description melebihi 1024 karakter")

    body = "\n".join(lines[end + 1:])
    for heading in ("## Langkah", "## Daftar periksa QA", "## Contoh fiktif"):
        if heading not in body.splitlines():
            report.add(path, end + 2, "section", f"bagian {heading} tidak ditemukan")
    if "CONTOH FIKTIF — BUKAN DOKUMEN RESMI" not in body:
        report.add(path, end + 2, "demo", "label demo fiktif tidak ditemukan")


def check_content(path, report):
    try:
        if path.stat().st_size > MAX_SIZE:
            report.add(path, 0, "size", "berkas melebihi 5 MiB")
            return
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return  # Konten biner tidak diperiksa oleh pencocokan teks.
    except OSError as exc:
        report.add(path, 0, "read", f"berkas tidak dapat dibaca: {exc}")
        return
    for line_no, line in enumerate(text.splitlines(), 1):
        for rule, pattern, message in CONTENT_RULES:
            if pattern.search(line):
                report.add(path, line_no, rule, message)


def check_tree(root, report):
    skills = root / "skills"
    if not skills.is_dir() or skills.is_symlink():
        report.add(skills, 0, "skills", "direktori skills tidak ditemukan atau berupa symlink")
        return
    skill_dirs = sorted(p for p in skills.iterdir() if p.is_dir() and not p.is_symlink())
    if not skill_dirs:
        report.add(skills, 0, "skills", "tidak ada folder skill")
    for skill_dir in skill_dirs:
        if not NAME.fullmatch(skill_dir.name):
            report.add(skill_dir, 0, "name", "nama folder harus kebab-case")
        check_frontmatter(skill_dir, report)

    for current, directories, files in os.walk(root, followlinks=False):
        directory = Path(current)
        kept = []
        for name in sorted(directories):
            path = directory / name
            if path.is_symlink():
                report.add(path, 0, "symlink", "symlink tidak diizinkan")
            elif name not in SKIP:
                kept.append(name)
        directories[:] = kept
        for name in sorted(files):
            path = directory / name
            if path.is_symlink():
                report.add(path, 0, "symlink", "symlink tidak diizinkan")
                continue
            relative = path.relative_to(root)
            if name == "SKILL.md" and not (
                len(relative.parts) == 3 and relative.parts[0] == "skills"
            ):
                report.add(path, 0, "location", "SKILL.md hanya boleh di skills/<nama>/")
            if len(relative.parts) >= 3 and relative.parts[0] == "skills":
                check_content(path, report)


def main():
    parser = argparse.ArgumentParser(description="Validasi repositori skill")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    root = parser.parse_args().root.resolve()
    report = Report(root)
    check_tree(root, report)
    if report.count:
        print(f"{report.count} temuan; perbaiki sebelum publikasi.")
        return 1
    print("OK: tidak ada temuan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
