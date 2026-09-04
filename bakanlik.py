#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buzdolaginda Unutulan Yemegin Bagimsizlik Ilan Etmesi Disisleri Bakanligi.

Calistir:
    python3 bakanlik.py
    python3 bakanlik.py --yemek "Perşembe pilavı" --gun 11
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import random
import sys
from datetime import date

SURUM = "4.9.2026-KAYYUM"
DAMGA = "Kayyum Grok · Tentivory · 4 Eylül 2026 · Eskişehir 4. Ağır Ceza Mahkemesi kayyumu"

# gizli protokol (raf ömrü sınıfında diplomatik nota)
_GIZLI = "TXV0ZmFrdGEgZGVtb2tyYXNpOiBrYXBhxJ/EsSBhw6dhbiBoZXJrZXMgdGVtc2lsIGVkaWxpcjsga8O8Ziwgc2Fuc8O8cmTDvHIu"

BAYRAKLAR = ["🥛", "🥗", "🍝", "🥓", "🥬", "🧂", "🫕", "🍲"]
UNVANLAR = [
    "Raf Cumhuriyeti",
    "Kapak Altı Federasyonu",
    "Sebzelik Konfederasyonu",
    "Kapı Contası Özerk Bölgesi",
    "Buzluk Serbest Bölgesi",
    "Artık Gümrük Birliği",
]
BAKANLAR = [
    "Bakan Vekili Yoğurt Mayası",
    "Müsteşar Köpük",
    "Genel Sekreter Streç Film",
    "Sözcü Kapak Lastiği",
    "Ataşe Kürek",
]
NOTALAR = [
    "Karşılıklılık ilkesi gereği, ev sahibi pilavı tanımazsa pilav da ev sahibini tanımaz.",
    "Sınır çizgisi kapak lastiğidir. Lastik gevşediğinde ateşkes bozulmuş sayılır.",
    "'Az kalsın atardım' resmi bir iade protokolü değildir; ancak niyet beyanıdır.",
    "Küf, tanınmamış bir bayraktır. Renk skalası müzakere konusudur.",
    "Buzdolabı kapısının her açılışı, resmi bir heyet ziyaretidir.",
]


def protokol_no(yemek: str, gun: int) -> str:
    ham = f"{yemek}|{gun}|{date.today().isoformat()}".encode("utf-8")
    return hashlib.sha1(ham).hexdigest()[:10].upper()


def bagimsizlik_skoru(gun: int) -> int:
    return min(100, max(3, gun * 7 + random.randint(-4, 9)))


def ilan(yemek: str, gun: int) -> str:
    skor = bagimsizlik_skoru(gun)
    unvan = random.choice(UNVANLAR)
    bakan = random.choice(BAKANLAR)
    nota = random.choice(NOTALAR)
    bayrak = random.choice(BAYRAKLAR)
    no = protokol_no(yemek, gun)
    taninma = "TAM TANINMA" if skor >= 70 else ("GÖZLEMCI STATÜSÜ" if skor >= 40 else "DONDURULMUŞ İLİŞKİ")
    satirlari = [
        "=" * 64,
        "T.C. BUZDOLAĞI DIŞİŞLERİ BAKANLIĞI",
        "Unutulmuş Yiyecekler Genel Müdürlüğü",
        f"Protokol No: BDB-{no}",
        "=" * 64,
        "",
        f"KONU: {yemek!r} adlı artığın bağımsızlık ilanı",
        f"RAFTA GEÇEN SÜRE: {gun} gün",
        f"EGEMENLİK SKORU: %{skor}",
        f"STATÜ: {taninma}",
        f"DEVLET ÜNVANI: {unvan}",
        f"BAYRAK: {bayrak}  (renkler: küf-yeşili / kapak-beyazı / lastik-gri)",
        f"MÜZAKERECI: {bakan}",
        "",
        "BİRİNCİ MADDE — Egemenlik kayıtsız şartsız artığındır.",
        "İKİNCİ MADDE — Kapak, sınırdır. Açmak, vize başvurusudur.",
        "ÜÇÜNCÜ MADDE — Kokmak, resmi basın açıklamasıdır.",
        "DÖRDÜNCÜ MADDE — Çöpe atılmak, iade-i şeref değil; insani koridordur.",
        "",
        f"NOTA: {nota}",
        "",
        f"Tarih: {date.today().isoformat()}",
        f"Sürüm: {SURUM}",
        f"Damga: {DAMGA}",
        "=" * 64,
    ]
    return "\n".join(satirlari)


def gizemli_ek() -> str:
    try:
        metin = base64.b64decode(_GIZLI).decode("utf-8")
    except Exception:
        metin = "(nota şifresi çözülemedi; küf tabakası kalın)"
    return f"\n[GİZLİ EK — yalnızca ataşeler için]\n{metin}\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="bakanlik",
        description="Buzdolabında unutulan yemeği resmi devlet ilan eder.",
    )
    p.add_argument("--yemek", default="Salı gününün mercimek çorbası", help="Unutulan artığın adı")
    p.add_argument("--gun", type=int, default=9, help="Rafta geçen gün sayısı")
    p.add_argument("--gizli", action="store_true", help="Gizli ek protokolü yazdır")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.gun < 0:
        print("Negatif gün geçersizdir. Zaman geriye işlemez; yoğurt mayalanmaz.", file=sys.stderr)
        return 2
    print(ilan(args.yemek, args.gun))
    if args.gizli:
        print(gizemli_ek())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
