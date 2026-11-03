# -*- coding: utf-8 -*-
"""
CONTOH FIKTIF — BUKAN DOKUMEN RESMI

Latihan CAD: bordes baja 1500 x 1200 mm dengan railing pipa OD 50 mm
pada satu sisi panjang 1500 mm. Skrip ini dijalankan sepenuhnya headless
dengan freecadcmd dan menghasilkan:

  1. Model 3D  : bordes_baja_1500x1200_railing.FCStd
  2. Ekspor     : bordes_baja_1500x1200_railing.step
  3. Gambar 2D  : gambar_kerja_bordes_baja_1500x1200.dxf
                  (denah + tampak depan, berdimensi, kertas A2 1:10)
  4. Material   : DAFTAR_MATERIAL_DAN_ASUMSI.md
  5. Pratinjau  : pratinjau_gambar_kerja.png (alat bantu verifikasi)

Cara menjalankan (dari folder ini):

  /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd buat_bordes_railing.py

Catatan: skrip tidak membuka GUI, tidak mengubah preferensi global FreeCAD,
tidak menginstal paket, dan tidak mengakses jaringan. DXF ditulis langsung
sebagai DXF R12 (AC1009) oleh skrip ini karena library DXF opsional FreeCAD
tidak terpasang.
"""

import datetime
import math
import os
import sys

# ---------------------------------------------------------------------------
# Konstanta proyek
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("MPLCONFIGDIR", os.path.join(BASE_DIR, ".cache", "matplotlib"))

import FreeCAD as App
import Part
import Draft
import Import

LABEL = "CONTOH FIKTIF — BUKAN DOKUMEN RESMI"
PROJECT = "Bordes Baja 1500 × 1200 mm dengan Railing Pipa Ø50 mm"
STEEL_DENSITY = 7850.0  # kg/m3 (baja)

FONTS = [
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]

OUT = {
    "fcstd": os.path.join(BASE_DIR, "bordes_baja_1500x1200_railing.FCStd"),
    "step": os.path.join(BASE_DIR, "bordes_baja_1500x1200_railing.step"),
    "dxf": os.path.join(BASE_DIR, "gambar_kerja_bordes_baja_1500x1200.dxf"),
    "md": os.path.join(BASE_DIR, "DAFTAR_MATERIAL_DAN_ASUMSI.md"),
    "png": os.path.join(BASE_DIR, "pratinjau_gambar_kerja.png"),
}

# Parameter desain (semua mm)
P = {
    "plate_l": 1500.0,      # panjang bordes (sisi dengan railing)
    "plate_w": 1200.0,      # lebar bordes
    "plate_t": 10.0,        # tebal pelat bordes
    "post_inset": 50.0,     # as tiang dari tepi pelat (arah y dan x ujung)
    "post_spacing_max": 1000.0,
    "rail_h": 1000.0,       # tinggi railing dari permukaan atas pelat
    "pipe_od": 50.0,
    "pipe_wall": 3.0,
    "mid_rail_h": 500.0,    # as mid rail dari permukaan atas pelat
    "base_plate": 100.0,
    "base_t": 10.0,
    "bolt_d": 12.0,
    "bolt_len_model": 30.0,
    "bolt_pitch": 60.0,
    "bolt_count_per_post": 4,
    "density": STEEL_DENSITY,
}


def v(x, y, z=0.0):
    return App.Vector(float(x), float(y), float(z))


def fmt_id(value, decimals=1):
    """Format angka dengan pemisah ribuan titik dan desimal koma."""
    s = f"{value:,.{decimals}f}"
    return s.replace(",", "~").replace(".", ",").replace("~", ".")


def compute_layout():
    """Hitung tata letak tiang, rail, dan ketinggian."""
    L = P["plate_l"]
    inset = P["post_inset"]
    n = 2
    while (L - 2.0 * inset) / (n - 1) > P["post_spacing_max"]:
        n += 1
    spacing = (L - 2.0 * inset) / (n - 1)
    post_x = [inset + i * spacing for i in range(n)]

    plate_top = P["plate_t"]
    base_top = plate_top + P["base_t"]
    rail_top = plate_top + P["rail_h"]
    top_rail_z = rail_top - P["pipe_od"] / 2.0
    post_top = top_rail_z - P["pipe_od"] / 2.0
    post_len = post_top - base_top
    mid_z = plate_top + P["mid_rail_h"]

    mid_rails = []
    for i in range(n - 1):
        x1 = post_x[i] + P["pipe_od"] / 2.0
        x2 = post_x[i + 1] - P["pipe_od"] / 2.0
        mid_rails.append((x1, x2, x2 - x1))

    bolts = []
    for x in post_x:
        for dx in (-P["bolt_pitch"] / 2.0, P["bolt_pitch"] / 2.0):
            for dy in (-P["bolt_pitch"] / 2.0, P["bolt_pitch"] / 2.0):
                bolts.append((x + dx, inset + dy))

    return {
        "post_count": n,
        "post_spacing": spacing,
        "post_x": post_x,
        "post_y": inset,
        "post_len": post_len,
        "post_top": post_top,
        "base_top": base_top,
        "plate_top": plate_top,
        "rail_top": rail_top,
        "top_rail_z": top_rail_z,
        "top_rail_len": L,
        "mid_z": mid_z,
        "mid_rails": mid_rails,
        "mid_total": sum(r[2] for r in mid_rails),
        "bolts": bolts,
        "pipe_total": n * post_len + L + sum(r[2] for r in mid_rails),
    }


# ---------------------------------------------------------------------------
# Model 3D
# ---------------------------------------------------------------------------
def make_pipe(od, wall, length, p0, axis):
    outer = Part.makeCylinder(od / 2.0, length, p0, axis)
    inner = Part.makeCylinder(od / 2.0 - wall, length, p0, axis)
    return outer.cut(inner)


def build_model(lay):
    doc = App.newDocument("BordesBaja")
    doc.Label = LABEL
    doc.Comment = "Latihan CAD fiktif: " + PROJECT + ". " + LABEL
    doc.addProperty("App::PropertyString", "LabelWajib", "Metadata")
    doc.LabelWajib = LABEL

    g_bordes = doc.addObject("App::DocumentObjectGroup", "Grup_Bordes")
    g_bordes.Label = "01 — Bordes"
    g_railing = doc.addObject("App::DocumentObjectGroup", "Grup_Railing")
    g_railing.Label = "02 — Railing"
    g_anotasi = doc.addObject("App::DocumentObjectGroup", "Grup_Anotasi")
    g_anotasi.Label = "03 — Anotasi"

    def add_part(name, label, shape, group):
        obj = doc.addObject("Part::Feature", name)
        obj.Label = label
        obj.Shape = shape
        group.addObject(obj)
        return obj

    L, W, T = P["plate_l"], P["plate_w"], P["plate_t"]
    od, wall = P["pipe_od"], P["pipe_wall"]
    y_post = lay["post_y"]

    # Pelat bordes + lubang baut angkur (Ø14)
    plate = Part.makeBox(L, W, T)
    hole_cutters = [
        Part.makeCylinder(7.0, T + 2.0, v(bx, by, -1.0), v(0, 0, 1))
        for bx, by in lay["bolts"]
    ]
    plate = plate.cut(Part.makeCompound(hole_cutters))
    plate_obj = add_part("Pelat_Bordes", "Pelat bordes 1500 x 1200 x 10", plate, g_bordes)

    # Tiang pipa
    post_objs = []
    for i, x in enumerate(lay["post_x"], start=1):
        shp = make_pipe(od, wall, lay["post_len"], v(x, y_post, lay["base_top"]), v(0, 0, 1))
        post_objs.append(
            add_part(f"Tiang_{i}", f"Tiang pipa OD50 - {i}", shp, g_railing)
        )

    # Top rail
    top_rail = make_pipe(od, wall, lay["top_rail_len"], v(0, y_post, lay["top_rail_z"]), v(1, 0, 0))
    top_rail_obj = add_part("Top_Rail", "Top rail pipa OD50 L1500", top_rail, g_railing)

    # Mid rail (2 segmen di antara tiang)
    mid_objs = []
    for i, (x1, x2, length) in enumerate(lay["mid_rails"], start=1):
        shp = make_pipe(od, wall, length, v(x1, y_post, lay["mid_z"]), v(1, 0, 0))
        mid_objs.append(
            add_part(f"Mid_Rail_{i}", f"Mid rail pipa OD50 L{length:.0f} - {i}", shp, g_railing)
        )

    # Base plate + lubang baut Ø14
    base_objs = []
    for i, x in enumerate(lay["post_x"], start=1):
        bp = Part.makeBox(P["base_plate"], P["base_plate"], P["base_t"],
                          v(x - P["base_plate"] / 2.0, y_post - P["base_plate"] / 2.0, lay["plate_top"]))
        cutters = []
        for bx, by in lay["bolts"]:
            if abs(bx - x) <= P["bolt_pitch"] / 2.0 + 0.01:
                cutters.append(Part.makeCylinder(7.0, P["base_t"] + 4.0, v(bx, by, lay["plate_top"] - 1.0)))
        bp = bp.cut(Part.makeCompound(cutters))
        base_objs.append(
            add_part(f"Base_Plate_{i}", f"Base plate 100x100x10 - {i}", bp, g_railing)
        )

    # Baut angkur (disederhanakan, Ø12 x 30)
    bolt_shapes = [
        Part.makeCylinder(P["bolt_d"] / 2.0, P["bolt_len_model"], v(bx, by, 0.0), v(0, 0, 1))
        for bx, by in lay["bolts"]
    ]
    bolts_obj = add_part(
        "Baut_Angkur", f"Baut angkur M12 - {len(bolt_shapes)} bh",
        Part.makeCompound(bolt_shapes), g_railing,
    )

    # Label wajib sebagai teks 3D + teks anotasi 2D
    font_path = next((p for p in FONTS if os.path.exists(p)), None)
    if not font_path:
        raise RuntimeError("Font TTF tidak ditemukan untuk label 3D.")
    label_shape = Draft.makeShapeString(LABEL, font_path, 40.0, 0.0)
    label_shape.Label = LABEL
    label_shape.Placement.Base = App.Vector(0.0, -220.0, 0.0)
    g_anotasi.addObject(label_shape)

    label_text = Draft.make_text(
        [LABEL],
        placement=App.Placement(App.Vector(0.0, -320.0, 0.0), App.Rotation()),
    )
    label_text.Label = "Label wajib (2D)"
    g_anotasi.addObject(label_text)

    doc.recompute()

    all_parts = [plate_obj] + post_objs + [top_rail_obj] + mid_objs + base_objs + [bolts_obj]
    return {
        "doc": doc,
        "plate": plate_obj,
        "posts": post_objs,
        "top_rail": top_rail_obj,
        "mid_rails": mid_objs,
        "base_plates": base_objs,
        "bolts": bolts_obj,
        "label_shape": label_shape,
        "parts": all_parts,
        "font_path": font_path,
    }


def save_and_export(model, lay):
    doc = model["doc"]
    for path in (OUT["fcstd"], OUT["step"]):
        if os.path.exists(path):
            os.remove(path)
    doc.saveAs(OUT["fcstd"])
    # saveAs() menimpa Label dokumen dengan nama berkas; set ulang lalu simpan
    # agar Label dokumen di dalam Document.xml tetap label wajib.
    doc.Label = LABEL
    doc.Comment = "Latihan CAD fiktif: " + PROJECT + ". " + LABEL
    doc.save()
    Import.export(model["parts"] + [model["label_shape"]], OUT["step"])
    return {
        "fcstd_size": os.path.getsize(OUT["fcstd"]),
        "step_size": os.path.getsize(OUT["step"]),
    }


# ---------------------------------------------------------------------------
# Penulis DXF R12 (AC1009)
# ---------------------------------------------------------------------------
def _round(value):
    s = f"{float(value):.4f}".rstrip("0").rstrip(".")
    if s in ("", "-0"):
        s = "0"
    return s


def rec(code, value):
    return f"{code}\n{value}\n"


def LINE(p1, p2, layer="VIEW", ltype=None, color=None):
    return {"t": "LINE", "p1": (float(p1[0]), float(p1[1])),
            "p2": (float(p2[0]), float(p2[1])), "layer": layer,
            "ltype": ltype, "color": color}


def CIRCLE(center, radius, layer="VIEW", ltype=None):
    return {"t": "CIRCLE", "c": (float(center[0]), float(center[1])),
            "r": float(radius), "layer": layer, "ltype": ltype}


def SOLID(points, layer="DIM"):
    return {"t": "SOLID", "pts": [(float(p[0]), float(p[1])) for p in points], "layer": layer}


def TEXT(pos, height, value, layer="TEXT", rot=0.0, hjust=0, vjust=0, style="ARIAL", color=None):
    return {"t": "TEXT", "p": (float(pos[0]), float(pos[1])), "h": float(height),
            "txt": value, "layer": layer, "rot": float(rot),
            "hjust": int(hjust), "vjust": int(vjust), "style": style, "color": color}


class DxfWriter:
    """DXF R12 minimal tetapi lengkap: layer, linetype, dimstyle, blok dimensi."""

    LAYERS = [
        ("0", 7, "CONTINUOUS"),
        ("BORDER", 7, "CONTINUOUS"),
        ("VIEW", 7, "CONTINUOUS"),
        ("HIDDEN", 8, "HIDDEN"),
        ("CENTER", 6, "CENTER"),
        ("DIM", 5, "CONTINUOUS"),
        ("TEXT", 7, "CONTINUOUS"),
        ("TITLE", 7, "CONTINUOUS"),
        ("LABEL", 1, "CONTINUOUS"),
        ("NOTE", 7, "CONTINUOUS"),
    ]

    def __init__(self, width=594.0, height=420.0):
        self.width = width
        self.height = height
        self.items = []
        self.blocks = {}
        self.dim_n = 0

    # -- entity helpers -----------------------------------------------------
    def line(self, p1, p2, layer="VIEW", ltype=None):
        self.items.append(LINE(p1, p2, layer, ltype))

    def rect(self, x1, y1, x2, y2, layer="VIEW", ltype=None):
        self.line((x1, y1), (x2, y1), layer, ltype)
        self.line((x2, y1), (x2, y2), layer, ltype)
        self.line((x2, y2), (x1, y2), layer, ltype)
        self.line((x1, y2), (x1, y1), layer, ltype)

    def circle(self, center, radius, layer="VIEW", ltype=None):
        self.items.append(CIRCLE(center, radius, layer, ltype))

    def solid(self, points, layer="DIM"):
        self.items.append(SOLID(points, layer))

    def text(self, pos, height, value, layer="TEXT", rot=0.0, hjust=0, vjust=0, style="ARIAL"):
        self.items.append(TEXT(pos, height, value, layer, rot, hjust, vjust, style))

    def _dim_arrow_h(self, tip, direction, size=2.5, half=0.9):
        """Panah horizontal; direction +1 = menghadap +x."""
        x, y = tip
        base_x = x - direction * size
        return SOLID([(x, y), (base_x, y - half), (base_x, y + half)])

    def _dim_arrow_v(self, tip, direction, size=2.5, half=0.9):
        """Panah vertikal; direction +1 = menghadap +y."""
        x, y = tip
        base_y = y - direction * size
        return SOLID([(x, y), (x - half, base_y), (x + half, base_y)])

    def dim_h(self, x1, x2, y_ref, y_dim, value):
        self.dim_n += 1
        name = f"*D{self.dim_n}"
        sgn = 1.0 if y_dim > y_ref else -1.0
        items = []
        for x in (x1, x2):
            items.append(LINE((x, y_ref + sgn * 1.0), (x, y_dim + sgn * 1.5), "DIM"))
        items.append(LINE((x1, y_dim), (x2, y_dim), "DIM"))
        items.append(self._dim_arrow_h((x1, y_dim), -1.0))
        items.append(self._dim_arrow_h((x2, y_dim), +1.0))
        ty = y_dim + 1.0
        items.append(TEXT(((x1 + x2) / 2.0, ty), 3.5, value, "DIM", 0.0, 1, 0))
        self.blocks[name] = items
        self.items.append({
            "t": "DIMENSION", "layer": "DIM", "block": name,
            "dp": ((x1 + x2) / 2.0, y_dim), "tp": ((x1 + x2) / 2.0, ty + 1.75),
            "p1": (float(x1), float(y_ref)), "p2": (float(x2), float(y_ref)),
            "angle": 0.0, "text": value,
        })

    def dim_v(self, x_ref, y1, y2, x_dim, value):
        self.dim_n += 1
        name = f"*D{self.dim_n}"
        sgn = 1.0 if x_dim > x_ref else -1.0
        items = []
        for y in (y1, y2):
            items.append(LINE((x_ref + sgn * 1.0, y), (x_dim + sgn * 1.5, y), "DIM"))
        items.append(LINE((x_dim, y1), (x_dim, y2), "DIM"))
        items.append(self._dim_arrow_v((x_dim, y1), -1.0))
        items.append(self._dim_arrow_v((x_dim, y2), +1.0))
        if x_dim < x_ref:
            tx = x_dim - 1.0
        else:
            tx = x_dim + 4.5
        ty = (y1 + y2) / 2.0
        items.append(TEXT((tx, ty), 3.5, value, "DIM", 90.0, 1, 0))
        mid_tx = tx - 1.75 if x_dim < x_ref else tx + 1.75
        self.blocks[name] = items
        self.items.append({
            "t": "DIMENSION", "layer": "DIM", "block": name,
            "dp": (x_dim, ty), "tp": (mid_tx, ty),
            "p1": (float(x_ref), float(y1)), "p2": (float(x_ref), float(y2)),
            "angle": 90.0, "text": value,
        })

    def leader(self, tip, elbow, text_pos, value, height=2.8, layer="TEXT"):
        """Leader polyline + panah terbuka (LINE) + teks (rata kiri, baseline)."""
        self.line(text_pos, elbow, layer)
        self.line(elbow, tip, layer)
        dx = tip[0] - elbow[0]
        dy = tip[1] - elbow[1]
        ln = math.hypot(dx, dy) or 1.0
        ux, uy = dx / ln, dy / ln
        bx, by = tip[0] - ux * 2.0, tip[1] - uy * 2.0
        px, py = -uy * 0.7, ux * 0.7
        self.line((bx + px, by + py), tip, layer)
        self.line((bx - px, by - py), tip, layer)
        self.text(text_pos, height, value, layer, 0.0, 0, 0)

    # -- serialization ------------------------------------------------------
    def _ser(self, e):
        t = e["t"]
        layer = e["layer"]
        if t == "LINE":
            s = rec(0, "LINE") + rec(8, layer)
            if e.get("ltype"):
                s += rec(6, e["ltype"])
            if e.get("color"):
                s += rec(62, e["color"])
            s += rec(10, _round(e["p1"][0])) + rec(20, _round(e["p1"][1])) + rec(30, 0.0)
            s += rec(11, _round(e["p2"][0])) + rec(21, _round(e["p2"][1])) + rec(31, 0.0)
            return s
        if t == "CIRCLE":
            s = rec(0, "CIRCLE") + rec(8, layer)
            if e.get("ltype"):
                s += rec(6, e["ltype"])
            s += rec(10, _round(e["c"][0])) + rec(20, _round(e["c"][1])) + rec(30, 0.0)
            s += rec(40, _round(e["r"]))
            return s
        if t == "SOLID":
            s = rec(0, "SOLID") + rec(8, layer)
            pts = list(e["pts"]) + [e["pts"][-1]]
            for i in range(4):
                s += rec(10 + i, _round(pts[i][0])) + rec(20 + i, _round(pts[i][1])) + rec(30 + i, 0.0)
            return s
        if t == "TEXT":
            s = rec(0, "TEXT") + rec(8, layer)
            if e.get("color"):
                s += rec(62, e["color"])
            x, y = e["p"]
            s += rec(10, _round(x)) + rec(20, _round(y)) + rec(30, 0.0)
            s += rec(40, _round(e["h"])) + rec(1, e["txt"]) + rec(50, _round(e["rot"]))
            s += rec(7, e["style"]) + rec(72, e["hjust"]) + rec(73, e["vjust"])
            s += rec(11, _round(x)) + rec(21, _round(y)) + rec(31, 0.0)
            return s
        if t == "DIMENSION":
            s = rec(0, "DIMENSION") + rec(8, e["layer"]) + rec(2, e["block"])
            s += rec(10, _round(e["dp"][0])) + rec(20, _round(e["dp"][1])) + rec(30, 0.0)
            s += rec(11, _round(e["tp"][0])) + rec(21, _round(e["tp"][1])) + rec(31, 0.0)
            s += rec(70, 0) + rec(1, e["text"]) + rec(3, "STANDARD")
            s += rec(13, _round(e["p1"][0])) + rec(23, _round(e["p1"][1])) + rec(33, 0.0)
            s += rec(14, _round(e["p2"][0])) + rec(24, _round(e["p2"][1])) + rec(34, 0.0)
            s += rec(50, _round(e["angle"]))
            return s
        raise ValueError(t)

    def save(self, path):
        out = []
        out.append(rec(0, "SECTION") + rec(2, "HEADER"))
        out.append(rec(9, "$ACADVER") + rec(1, "AC1009"))
        out.append(rec(9, "$DWGCODEPAGE") + rec(3, "ANSI_1252"))
        out.append(rec(9, "$INSBASE") + rec(10, 0.0) + rec(20, 0.0) + rec(30, 0.0))
        out.append(rec(9, "$EXTMIN") + rec(10, 0.0) + rec(20, 0.0) + rec(30, 0.0))
        out.append(rec(9, "$EXTMAX") + rec(10, _round(self.width)) + rec(20, _round(self.height)) + rec(30, 0.0))
        out.append(rec(9, "$LIMMIN") + rec(10, 0.0) + rec(20, 0.0))
        out.append(rec(9, "$LIMMAX") + rec(10, _round(self.width)) + rec(20, _round(self.height)))
        out.append(rec(9, "$TEXTSIZE") + rec(40, 3.5))
        out.append(rec(9, "$LTSCALE") + rec(40, 1.0))
        out.append(rec(9, "$DIMSTYLE") + rec(2, "STANDARD"))
        out.append(rec(9, "$CLAYER") + rec(8, "0"))
        out.append(rec(9, "$LUNITS") + rec(70, 2))
        out.append(rec(9, "$LUPREC") + rec(70, 2))
        out.append(rec(9, "$MEASUREMENT") + rec(70, 1))
        out.append(rec(0, "ENDSEC"))

        out.append(rec(0, "SECTION") + rec(2, "TABLES"))
        out.append(rec(0, "TABLE") + rec(2, "LTYPE") + rec(70, 4))
        out.append(rec(0, "LTYPE") + rec(2, "CONTINUOUS") + rec(70, 0) + rec(3, "Solid line") +
                   rec(72, 65) + rec(73, 0) + rec(40, 0.0))
        out.append(rec(0, "LTYPE") + rec(2, "DASHED") + rec(70, 0) + rec(3, "Dashed __ __") +
                   rec(72, 65) + rec(73, 2) + rec(40, 4.5) + rec(49, 3.0) + rec(74, 0) + rec(49, -1.5))
        out.append(rec(0, "LTYPE") + rec(2, "CENTER") + rec(70, 0) + rec(3, "Center ____ _ ____") +
                   rec(72, 65) + rec(73, 4) + rec(40, 22.225) + rec(49, 12.7) + rec(74, 0) +
                   rec(49, -3.175) + rec(74, 0) + rec(49, 3.175) + rec(74, 0) + rec(49, -3.175))
        out.append(rec(0, "LTYPE") + rec(2, "HIDDEN") + rec(70, 0) + rec(3, "Hidden __ __ __") +
                   rec(72, 65) + rec(73, 2) + rec(40, 4.5) + rec(49, 3.0) + rec(74, 0) + rec(49, -1.5))
        out.append(rec(0, "ENDTAB"))

        out.append(rec(0, "TABLE") + rec(2, "LAYER") + rec(70, len(self.LAYERS)))
        for name, color, ltype in self.LAYERS:
            out.append(rec(0, "LAYER") + rec(2, name) + rec(70, 0) + rec(62, color) + rec(6, ltype))
        out.append(rec(0, "ENDTAB"))

        out.append(rec(0, "TABLE") + rec(2, "STYLE") + rec(70, 2))
        out.append(rec(0, "STYLE") + rec(2, "STANDARD") + rec(70, 0) + rec(40, 0.0) + rec(41, 1.0) +
                   rec(50, 0.0) + rec(71, 0) + rec(42, 2.5) + rec(3, "txt") + rec(4, ""))
        out.append(rec(0, "STYLE") + rec(2, "ARIAL") + rec(70, 0) + rec(40, 0.0) + rec(41, 1.0) +
                   rec(50, 0.0) + rec(71, 0) + rec(42, 2.5) + rec(3, "arial.ttf") + rec(4, ""))
        out.append(rec(0, "ENDTAB"))

        out.append(rec(0, "TABLE") + rec(2, "DIMSTYLE") + rec(70, 1))
        out.append(rec(0, "DIMSTYLE") + rec(2, "STANDARD") + rec(70, 0) +
                   rec(40, 1.0) + rec(41, 2.5) + rec(42, 1.0) + rec(43, 3.75) + rec(44, 1.25) +
                   rec(140, 3.5) + rec(141, 2.5) + rec(144, 10.0) + rec(147, 1) +
                   rec(73, 0) + rec(74, 0) + rec(77, 1) + rec(78, 8))
        out.append(rec(0, "ENDTAB"))
        out.append(rec(0, "ENDSEC"))

        out.append(rec(0, "SECTION") + rec(2, "BLOCKS"))
        for name, items in self.blocks.items():
            out.append(rec(0, "BLOCK") + rec(8, "0") + rec(2, name) + rec(70, 0) +
                       rec(10, 0.0) + rec(20, 0.0) + rec(30, 0.0) + rec(3, name) + rec(1, ""))
            for item in items:
                out.append(self._ser(item))
            out.append(rec(0, "ENDBLK") + rec(8, "0"))
        out.append(rec(0, "ENDSEC"))

        out.append(rec(0, "SECTION") + rec(2, "ENTITIES"))
        for item in self.items:
            out.append(self._ser(item))
        out.append(rec(0, "ENDSEC"))
        out.append(rec(0, "EOF"))

        with open(path, "w", encoding="cp1252", newline="\n") as fh:
            fh.write("".join(out))


# ---------------------------------------------------------------------------
# Tata letak gambar kerja (A2, skala 1:10)
# ---------------------------------------------------------------------------
SHEET_W, SHEET_H = 594.0, 420.0
SCALE = 0.1
PLAN_X, PLAN_Y = 70.0, 95.0
ELEV_X, ELEV_Y = 70.0, 255.0
NOTES_X1, NOTES_Y1, NOTES_X2, NOTES_Y2 = 404.0, 70.0, 584.0, 380.0


def sx(x):
    return PLAN_X + x * SCALE


def sy_plan(y):
    return PLAN_Y + y * SCALE


def sz(z):
    return ELEV_Y + z * SCALE


def build_drawing(lay, masses):
    dxf = DxfWriter(SHEET_W, SHEET_H)
    date_str = datetime.date.today().isoformat()

    # --- bingkai & banner --------------------------------------------------
    dxf.rect(10, 10, 584, 410, "BORDER")
    dxf.rect(25, 386, 574, 406, "BORDER")
    dxf.text((299.5, 392.5), 9.0, LABEL, "LABEL", hjust=1)
    dxf.line((25, 389.5), (574, 389.5), "LABEL")

    # --- TAMPAK DEPAN (ELEVASI) -------------------------------------------
    L = P["plate_l"]
    T = P["plate_t"]
    od = P["pipe_od"]
    y_post = lay["post_y"]

    # pelat bordes
    dxf.rect(sx(0), sz(0), sx(L), sz(T), "VIEW")
    # base plate
    for x in lay["post_x"]:
        dxf.rect(sx(x - P["base_plate"] / 2.0), sz(T),
                 sx(x + P["base_plate"] / 2.0), sz(T + P["base_t"]), "VIEW")
    # tiang
    for x in lay["post_x"]:
        dxf.rect(sx(x - od / 2.0), sz(lay["base_top"]),
                 sx(x + od / 2.0), sz(lay["post_top"]), "VIEW")
        dxf.line((sx(x), sz(0) - 2.0), (sx(x), sz(lay["rail_top"]) + 2.0), "CENTER", "CENTER")
    # top rail
    dxf.rect(sx(0), sz(lay["top_rail_z"] - od / 2.0),
             sx(L), sz(lay["top_rail_z"] + od / 2.0), "VIEW")
    # mid rail
    for x1, x2, _ in lay["mid_rails"]:
        dxf.rect(sx(x1), sz(lay["mid_z"] - od / 2.0),
                 sx(x2), sz(lay["mid_z"] + od / 2.0), "VIEW")

    dxf.text((PLAN_X, 246.0), 4.0, "TAMPAK DEPAN (ELEVASI) — SKALA 1:10", "TEXT")

    # dimensi elevasi
    dxf.dim_v(ELEV_X, sz(T), sz(lay["rail_top"]), 44.0, f"{P['rail_h']:.0f}")
    dxf.dim_v(ELEV_X, sz(T), sz(lay["mid_z"]), 58.0, f"{P['mid_rail_h']:.0f}")
    dxf.dim_h(sx(0), sx(L), sz(lay["rail_top"]), 368.0, f"{L:.0f}")

    # label komponen
    dxf.leader((219.0, 353.5), (232.0, 350.0), (240.0, 350.0), "TOP RAIL — PIPA Ø50 × 3,0")
    dxf.leader((216.0, 330.0), (232.0, 326.0), (240.0, 326.0), "TIANG — PIPA Ø50 (3 bh)")
    dxf.leader((210.0, 306.0), (232.0, 302.0), (240.0, 302.0), "MID RAIL — PIPA Ø50")
    dxf.leader((218.0, 256.5), (232.0, 252.0), (240.0, 252.0), "PELAT BORDES t = 10 mm")

    # --- DENAH (PLAN) ------------------------------------------------------
    W = P["plate_w"]
    dxf.rect(sx(0), sy_plan(0), sx(L), sy_plan(W), "VIEW")

    # top rail band + centerline
    y1 = sy_plan(y_post - od / 2.0)
    y2 = sy_plan(y_post + od / 2.0)
    dxf.line((sx(0), y1), (sx(L), y1), "VIEW")
    dxf.line((sx(0), y2), (sx(L), y2), "VIEW")
    dxf.line((sx(0), sy_plan(y_post)), (sx(L), sy_plan(y_post)), "CENTER", "CENTER")

    # base plate + tiang
    for x in lay["post_x"]:
        bp = P["base_plate"]
        dxf.rect(sx(x - bp / 2.0), sy_plan(y_post - bp / 2.0),
                 sx(x + bp / 2.0), sy_plan(y_post + bp / 2.0), "VIEW")
        dxf.circle((sx(x), sy_plan(y_post)), od / 2.0 * SCALE, "VIEW")
        # tanda pusat
        dxf.line((sx(x) - 3.0, sy_plan(y_post)), (sx(x) + 3.0, sy_plan(y_post)), "CENTER", "CENTER")
        dxf.line((sx(x), sy_plan(y_post) - 3.0), (sx(x), sy_plan(y_post) + 3.0), "CENTER", "CENTER")

    dxf.text((PLAN_X, 222.0), 4.0, "DENAH (PLAN) — SKALA 1:10", "TEXT")
    dxf.text((sx(L / 2.0), sy_plan(700.0)), 3.2,
             "PELAT BORDES 1500 × 1200 × 10", "TEXT", hjust=1)
    dxf.text((sx(L / 2.0), sy_plan(420.0)), 2.8,
             "RAILING PIPA Ø50 PADA SATU SISI PANJANG (SISI BAWAH GAMBAR)",
             "TEXT", hjust=1)

    # dimensi denah
    for a, b in zip(lay["post_x"][:-1], lay["post_x"][1:]):
        dxf.dim_h(sx(a), sx(b), sy_plan(y_post), 82.0, f"{lay['post_spacing']:.0f}")
    dxf.dim_h(sx(0), sx(L), sy_plan(0), 68.0, f"{L:.0f}")
    dxf.dim_v(sx(0), sy_plan(0), sy_plan(W), 55.0, f"{W:.0f}")

    # keterangan denah
    dxf.leader((219.5, sy_plan(y_post)), (232.0, 96.0), (240.0, 96.0),
               "BASE PLATE 100 × 100 × 10 + 4 × M12")
    dxf.text((240.0, 75.0), 2.8, "AS RAILING & TIANG = 50 mm DARI TEPI PELAT", "TEXT")

    # --- TITLE BLOCK -------------------------------------------------------
    dxf.rect(404, 10, 584, 55, "BORDER")
    dxf.line((404, 46), (584, 46), "BORDER")
    dxf.line((404, 36), (584, 36), "BORDER")
    dxf.line((404, 26), (584, 26), "BORDER")
    dxf.line((404, 18), (584, 18), "BORDER")
    dxf.line((494, 18), (494, 36), "BORDER")
    dxf.line((494, 10), (494, 18), "BORDER")

    dxf.text((494.0, 48.2), 4.4, LABEL, "LABEL", hjust=1)
    dxf.text((410.0, 39.0), 4.2, "BORDES BAJA 1500 × 1200 + RAILING PIPA Ø50", "TITLE")
    dxf.text((410.0, 29.3), 3.2, "GAMBAR KERJA — DENAH & TAMPAK DEPAN", "TITLE")
    dxf.text((500.0, 29.3), 3.2, "SKALA 1:10", "TITLE")
    dxf.text((410.0, 20.8), 2.8, "DIGAMBAR: LATIHAN CAD (FIKTIF)", "TITLE")
    dxf.text((500.0, 20.8), 2.8, f"TANGGAL: {date_str}", "TITLE")
    dxf.text((410.0, 13.0), 2.6, "SATUAN: mm  |  KERTAS: A2  |  PROYEKSI EROPA  |  LEMBAR 1/1", "TITLE")

    # --- PANEL CATATAN & ASUMSI -------------------------------------------
    dxf.rect(NOTES_X1, NOTES_Y1, NOTES_X2, NOTES_Y2, "BORDER")
    dxf.text((410.0, 370.0), 4.0, "CATATAN & ASUMSI DESAIN", "TITLE")
    dxf.line((410.0, 367.5), (578.0, 367.5), "BORDER")

    notes = [
        "1. Semua dimensi dalam mm. Skala gambar 1:10, kertas A2.",
        "2. Bordes: pelat baja 1500 × 1200 × 10 mm (1 lembar).",
        "   Permukaan atas pelat = elevasi acuan ±0,00.",
        "3. Railing pada satu sisi panjang 1500 mm; as tiang",
        "   dan as rail 50 mm dari tepi pelat.",
        "4. Tinggi railing 1000 mm dari permukaan atas pelat",
        "   sampai sisi atas top rail.",
        "5. Pipa baja OD 50 mm, tebal dinding 3,0 mm.",
        "6. Tiang 3 bh, panjang 940 mm, jarak as 700 mm",
        "   (persyaratan maksimum 1000 mm terpenuhi).",
        "7. Top rail 1500 mm; mid rail 2 × 650 mm.",
        "8. Base plate 100 × 100 × 10 mm (3 bh), baut angkur",
        "   M12 × 100 (12 bh), pola 60 × 60 mm.",
        "9. Las fillet 4 mm tidak dimodelkan; baut angkur",
        "   disederhanakan sebagai silinder Ø12.",
        "10. Struktur penumpu, pondasi, dan sambungan ke",
        "    struktur utama di luar lingkup latihan ini.",
        "11. Tanpa perhitungan struktur/angin/seismik;",
        "    model fiktif, bukan untuk konstruksi.",
    ]
    ty = 360.0
    for line in notes:
        dxf.text((410.0, ty), 2.7, line, "NOTE")
        ty -= 4.2

    ty -= 4.0
    dxf.text((410.0, ty), 4.0, "KEBUTUHAN MATERIAL (RINGKAS)", "TITLE")
    dxf.line((410.0, ty - 2.5), (578.0, ty - 2.5), "BORDER")
    ty -= 10.0

    mat_lines = [
        f"Pelat bordes 1500×1200×10 : 1 lbr — {fmt_id(masses['plate'], 1)} kg",
        f"Pipa Ø50×3,0 total {fmt_id(lay['pipe_total'] / 1000.0, 2)} m — {fmt_id(masses['pipe'], 1)} kg",
        f"   Tiang 3 × 940 mm = 2.820 mm",
        f"   Top rail 1 × 1.500 mm = 1.500 mm",
        f"   Mid rail 2 × 650 mm = 1.300 mm",
        f"Base plate 100×100×10 : 3 bh — {fmt_id(masses['base'], 1)} kg",
        "Baut angkur M12×100 : 12 bh",
        "Cat dasar + finish : ± 0,9 m² (railing)",
    ]
    for line in mat_lines:
        dxf.text((410.0, ty), 2.7, line, "NOTE")
        ty -= 4.2

    # --- rekap data desain -------------------------------------------------
    dxf.rect(410.0, 164.0, 578.0, 226.0, "BORDER")
    dxf.text((414.0, 217.5), 3.6, "REKAP DATA DESAIN", "TITLE")
    dxf.line((410.0, 213.5), (578.0, 213.5), "BORDER")
    dxf.line((500.0, 164.0), (500.0, 213.5), "BORDER")

    data_rows = [
        ("Tinggi railing (permukaan pelat ke top rail)", "1000 mm"),
        ("Jarak antar tiang (as), maks. 1000 mm", f"{lay['post_spacing']:.0f} mm — OK"),
        ("Jumlah tiang / base plate", f"{lay['post_count']} bh / {lay['post_count']} bh"),
        ("Panjang pipa Ø50 × 3,0 total", f"{fmt_id(lay['pipe_total'] / 1000.0, 2)} m"),
        ("Berat baja total (tanpa baut angkur)", f"{fmt_id(masses['total'], 1)} kg"),
        ("Dimensi bordes (P × L × t)", "1500 × 1200 × 10 mm"),
        ("Kertas / skala / proyeksi", "A2 / 1:10 / Eropa"),
    ]
    ry = 207.0
    for label, value in data_rows:
        dxf.text((414.0, ry), 2.5, label, "NOTE")
        dxf.text((504.0, ry), 2.5, value, "NOTE")
        ry -= 6.0

    # --- legenda garis -----------------------------------------------------
    dxf.rect(410.0, 108.0, 578.0, 160.0, "BORDER")
    dxf.text((414.0, 151.5), 3.4, "LEGENDA GARIS", "TITLE")
    dxf.line((410.0, 148.5), (578.0, 148.5), "BORDER")
    dxf.line((414.0, 140.0), (434.0, 140.0), "VIEW")
    dxf.text((439.0, 140.0), 2.5, "Garis benda / tepi terlihat", "NOTE")
    dxf.line((414.0, 131.0), (434.0, 131.0), "CENTER", "CENTER")
    dxf.text((439.0, 131.0), 2.5, "Garis sumbu (centerline)", "NOTE")
    dxf.line((414.0, 122.0), (434.0, 122.0), "DIM")
    dxf.text((439.0, 122.0), 2.5, "Garis dimensi & teks ukuran", "NOTE")

    dxf.text((410.0, 94.0), 2.6,
             "Berat dihitung dengan densitas baja 7.850 kg/m³.", "NOTE")
    dxf.text((410.0, 86.0), 2.6,
             "Label wajib: " + LABEL, "LABEL")

    return dxf


# ---------------------------------------------------------------------------
# Pratinjau PNG (matplotlib, opsional)
# ---------------------------------------------------------------------------
LAYER_COLORS = {
    "0": "#111111", "BORDER": "#000000", "VIEW": "#111111", "HIDDEN": "#777777",
    "CENTER": "#b000b0", "DIM": "#1f44c8", "TEXT": "#111111", "TITLE": "#000000",
    "LABEL": "#b00000", "NOTE": "#111111",
}


def render_preview(dxf, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Polygon
    from matplotlib.lines import Line2D

    mm = 1.0 / 25.4
    fig = plt.figure(figsize=(SHEET_W * mm, SHEET_H * mm), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, SHEET_W)
    ax.set_ylim(0, SHEET_H)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")

    style_map = {"CONTINUOUS": "-", "DASHED": (0, (4, 2)), "HIDDEN": (0, (4, 2)),
                 "CENTER": (0, (8, 2, 2, 2))}
    layer_ltype = {name: lt for name, _, lt in DxfWriter.LAYERS}

    def draw(item, block=False):
        t = item["t"]
        layer = item["layer"]
        color = LAYER_COLORS.get(layer, "#111111") if layer != "0" else "#1f44c8"
        if t == "LINE":
            lt = style_map.get(item.get("ltype") or layer_ltype.get(layer, "CONTINUOUS"), "-")
            lw = 1.5 if layer == "BORDER" else 0.8
            ax.add_line(Line2D([item["p1"][0], item["p2"][0]], [item["p1"][1], item["p2"][1]],
                               color=color, linewidth=lw, linestyle=lt, solid_capstyle="butt"))
        elif t == "CIRCLE":
            ax.add_patch(Circle(item["c"], item["r"], fill=False, edgecolor=color, linewidth=0.8))
        elif t == "SOLID":
            ax.add_patch(Polygon(item["pts"], closed=True, facecolor=color, edgecolor=color, linewidth=0.2))
        elif t == "TEXT":
            fs = item["h"] * 72.0 / 25.4
            ha = {0: "left", 1: "center", 2: "right"}[item["hjust"]]
            va = {0: "baseline", 1: "bottom", 2: "middle", 3: "top"}[item["vjust"]]
            ax.text(item["p"][0], item["p"][1], item["txt"], fontsize=fs, color=color,
                    ha=ha, va=va, rotation=item["rot"], rotation_mode="anchor",
                    family="DejaVu Sans")

    for item in dxf.items:
        if item["t"] == "DIMENSION":
            continue
        draw(item)

    for items in dxf.blocks.values():
        for item in items:
            draw(item, block=True)

    fig.savefig(path, dpi=150, facecolor="white", bbox_inches=None, pad_inches=0)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Daftar material & asumsi
# ---------------------------------------------------------------------------
def write_material_doc(lay, masses):
    pipe_total_m = lay["pipe_total"] / 1000.0
    pipe_order_m = math.ceil(pipe_total_m * 1.05 * 100.0) / 100.0
    date_str = datetime.date.today().isoformat()

    md = f"""# {LABEL}

> **{LABEL}** — dokumen latihan fiktif. Bukan dokumen resmi, bukan untuk fabrikasi, konstruksi, atau verifikasi struktur.

## Ringkasan proyek

| Item | Nilai |
|---|---|
| Proyek | {PROJECT} |
| Tanggal | {date_str} |
| Satuan | milimeter (mm) |
| Skala gambar | 1:10, kertas A2 |
| Proyeksi | Eropa (first angle) |
| Tinggi railing | 1000 mm dari permukaan atas pelat |
| Pipa railing | baja OD 50 mm, tebal dinding 3,0 mm |
| Jarak antar tiang (as) | {fmt_id(lay['post_spacing'], 0)} mm (maksimum 1000 mm) |
| Jumlah tiang | {lay['post_count']} bh |
| Panjang pipa total | {fmt_id(pipe_total_m, 2)} m |

## 1. Daftar kebutuhan material

| No | Komponen | Spesifikasi | Jumlah | Dimensi / panjang | Volume (m³) | Berat (kg) |
|---:|---|---|---:|---|---:|---:|
| 1 | Pelat bordes | Baja, t = 10 mm | 1 lbr | 1500 × 1200 mm | {fmt_id(masses['plate_v'], 4)} | {fmt_id(masses['plate'], 1)} |
| 2 | Tiang railing | Pipa baja OD 50 × 3,0 mm | {lay['post_count']} bh | {fmt_id(lay['post_len'], 0)} mm/tiang | {fmt_id(masses['post_v'], 4)} | {fmt_id(masses['post'], 1)} |
| 3 | Top rail | Pipa baja OD 50 × 3,0 mm | 1 bh | 1500 mm | {fmt_id(masses['top_v'], 4)} | {fmt_id(masses['top'], 1)} |
| 4 | Mid rail | Pipa baja OD 50 × 3,0 mm | {len(lay['mid_rails'])} bh | 650 mm/bh | {fmt_id(masses['mid_v'], 4)} | {fmt_id(masses['mid'], 1)} |
| 5 | Base plate | Baja, t = 10 mm, 4 lubang Ø14 | {lay['post_count']} bh | 100 × 100 mm | {fmt_id(masses['base_v'], 4)} | {fmt_id(masses['base'], 1)} |
| 6 | Baut angkur | M12 × 100 (disederhanakan) | {len(lay['bolts'])} bh | Ø12, pola 60 × 60 mm | — | — |
| 7 | Cat dasar + finish | Sistem cat baja | ± 0,9 m² | — | — | — |

**Total berat baja (tanpa baut angkur dan cat): {fmt_id(masses['total'], 1)} kg.**

### 1.1 Rekap pipa Ø50 × 3,0 mm

| Segmen | Jumlah | Panjang satuan | Total |
|---|---:|---:|---:|
| Tiang (post) | {lay['post_count']} | 940 mm | 2.820 mm |
| Top rail | 1 | 1.500 mm | 1.500 mm |
| Mid rail | {len(lay['mid_rails'])} | 650 mm | 1.300 mm |
| **Total** | | | **{fmt_id(lay['pipe_total'], 0)} mm = {fmt_id(pipe_total_m, 2)} m** |

- Berat pipa dihitung dari volume geometri (pipa berongga) × 7.850 kg/m³: **{fmt_id(masses['pipe'], 1)} kg**.
- Kebutuhan order dengan allowance 5%: **{fmt_id(pipe_order_m, 2)} m**.
- Asumsi batang pipa standar 6 m: **1 batang** cukup untuk kebutuhan bersih 5,62 m (sisa ± 0,38 m). Dengan allowance 5% (5,91 m) masih di bawah 6 m, tetapi kehilangan potong/kerf belum dihitung.

### 1.2 Pemeriksaan jarak tiang

- Jumlah tiang = {lay['post_count']} bh; bentang = {lay['post_count'] - 1} × {fmt_id(lay['post_spacing'], 0)} mm.
- Jarak antar tiang {fmt_id(lay['post_spacing'], 0)} mm ≤ batas 1000 mm → **memenuhi**.
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
17. **Label wajib** "{LABEL}" dicantumkan pada setiap file output dan pada gambar DXF (banner, title block, dan footer catatan).

## 3. Batasan

- Tidak untuk dipakai sebagai gambar kerja nyata, pemesanan material, atau dasar fabrikasi.
- Tidak ada jaminan kekuatan, stabilitas, defleksi, atau keselamatan.
- Setiap penggunaan nyata memerlukan perencanaan oleh insinyur struktur yang berwenang.

## 4. Cara menjalankan ulang

```bash
cd "{BASE_DIR}"
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

**{LABEL}**
"""
    with open(OUT["md"], "w", encoding="utf-8", newline="\n") as fh:
        fh.write(md)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("LATIHAN CAD — " + LABEL)
    print("=" * 78)

    lay = compute_layout()
    print(f"Tiang: {lay['post_count']} bh, spasi as {lay['post_spacing']:.0f} mm, "
          f"panjang {lay['post_len']:.0f} mm")
    print(f"Pipa total: {lay['pipe_total']:.0f} mm "
          f"(tiang {lay['post_count'] * lay['post_len']:.0f} + top rail "
          f"{lay['top_rail_len']:.0f} + mid rail {lay['mid_total']:.0f})")

    model = build_model(lay)
    doc = model["doc"]
    print(f"Model: {len(model['parts'])} part + label 3D; valid = "
          f"{all(o.Shape.isValid() for o in model['parts'])}")

    sizes = save_and_export(model, lay)
    print(f"FCStd : {OUT['fcstd']} ({sizes['fcstd_size'] / 1024:.1f} KiB)")
    print(f"STEP  : {OUT['step']} ({sizes['step_size'] / 1024:.1f} KiB)")

    # Massa dari volume geometri (mm3 -> m3 -> kg)
    def mass(objs):
        vol = sum(o.Shape.Volume for o in objs)
        return vol, vol / 1e9 * P["density"]

    plate_v, plate_m = mass([model["plate"]])
    post_v, post_m = mass(model["posts"])
    top_v, top_m = mass([model["top_rail"]])
    mid_v, mid_m = mass(model["mid_rails"])
    base_v, base_m = mass(model["base_plates"])
    pipe_v = post_v + top_v + mid_v
    pipe_m = post_m + top_m + mid_m
    masses = {
        "plate_v": plate_v / 1e9, "plate": plate_m,
        "post_v": post_v / 1e9, "post": post_m,
        "top_v": top_v / 1e9, "top": top_m,
        "mid_v": mid_v / 1e9, "mid": mid_m,
        "base_v": base_v / 1e9, "base": base_m,
        "pipe": pipe_m,
        "total": plate_m + pipe_m + base_m,
    }

    dxf = build_drawing(lay, masses)
    dxf.save(OUT["dxf"])
    print(f"DXF   : {OUT['dxf']} ({os.path.getsize(OUT['dxf']) / 1024:.1f} KiB, "
          f"{len(dxf.items)} entity + {len(dxf.blocks)} blok dimensi)")

    write_material_doc(lay, masses)
    print(f"MD    : {OUT['md']} ({os.path.getsize(OUT['md']) / 1024:.1f} KiB)")

    try:
        render_preview(dxf, OUT["png"])
        print(f"PNG   : {OUT['png']} ({os.path.getsize(OUT['png']) / 1024:.1f} KiB)")
    except Exception as exc:  # pratinjau bukan output wajib
        print(f"PERINGATAN: pratinjau PNG gagal dibuat: {exc}")

    print("-" * 78)
    print(f"Pelat {fmt_id(plate_m, 1)} kg | pipa {fmt_id(pipe_m, 1)} kg | "
          f"base plate {fmt_id(base_m, 1)} kg | total {fmt_id(masses['total'], 1)} kg")
    print("Selesai. Semua output memuat label:")
    print("  " + LABEL)
    print("=" * 78)


# freecadcmd mengeksekusi berkas ini dua kali dalam satu proses: sekali
# sebagai modul dan sekali sebagai __main__. Guard pada modul sys mencegah
# model/gambar dibuat dua kali.
if not getattr(sys, "_BORDES_RAILING_MAIN_DONE", False):
    sys._BORDES_RAILING_MAIN_DONE = True
    main()
