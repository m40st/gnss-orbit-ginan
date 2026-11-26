"""重力場の次数（egm_degree）ごとの当てはめ結果を比較する。

使い方（compare_sp3.py と同じフォルダ、Downloads で）:
    python sweep_compare.py

表示する2つの表（GPSのみ、2019年7月17〜19日、単位 mm）:
  表1: 各次数の推定SP3 と IGS最終暦 の 3D RMS（当てはめ誤差）
  表2: 各次数の推定SP3 と 次数15（基準）の推定SP3 の 3D RMS（軌道そのものの違い）

注意: SP3 の位置は 1 mm 単位で書かれているので、1 mm 未満の差は、丸めの影響を受ける。
"""
import math
import os

from compare_sp3 import read_sp3

OUT = r"ginan_work\outputs_baseline"
PRODUCTS = r"ginan_work\products"

DAYS = [("17", "20191980000"), ("18", "20191990000"), ("19", "20192000000")]
DEGREES = [2, 4, 8, 12, 15]   # 15 は基準（ecef_*.sp3）
SYSTEM = "G"

_cache = {}


def load(path):
    if path not in _cache:
        _cache[path] = read_sp3(path)[0]
    return _cache[path]


def est_path(deg, day):
    if deg == 15:
        name = f"ecef_201907{day}.sp3"
    else:
        name = f"deg{deg}_201907{day}.sp3"
    return os.path.join(OUT, name)


def ref_path(code):
    return os.path.join(PRODUCTS, f"IGS2R03FIN_{code}_01D_05M_ORB.SP3")


def rms_mm(path_a, path_b):
    """共通の衛星・時刻の位置差の 3D RMS [mm] と、比べた点の数を返す。"""
    if not (os.path.exists(path_a) and os.path.exists(path_b)):
        return None, 0
    a, b = load(path_a), load(path_b)
    sq = []
    for sat in a:
        if not sat.startswith(SYSTEM) or sat not in b:
            continue
        for epoch in set(a[sat]) & set(b[sat]):
            d = [a[sat][epoch][i] - b[sat][epoch][i] for i in range(3)]
            sq.append(sum(x * x for x in d))
    if not sq:
        return None, 0
    return math.sqrt(sum(sq) / len(sq)) * 1000.0, len(sq)


def table(title, pair_fn):
    print(title)
    print("  次数    17日        18日        19日")
    for deg in DEGREES:
        cells = []
        for day, code in DAYS:
            value, n = pair_fn(deg, day, code)
            cells.append("   (なし)  " if value is None else f"{value:9.2f}   ")
        print(f"  {deg:>3}  " + "".join(cells))
    print()


def vs_igs(deg, day, code):
    return rms_mm(est_path(deg, day), ref_path(code))


def vs_deg15(deg, day, code):
    if deg == 15:
        return 0.0, 0
    return rms_mm(est_path(deg, day), est_path(15, day))


if __name__ == "__main__":
    table("表1: IGS最終暦との3D RMS [mm]（当てはめ誤差）", vs_igs)
    table("表2: 次数15の推定軌道との3D RMS [mm]（軌道そのものの違い）", vs_deg15)
    print("次数2 は pea が異常終了したため、出力がない。")
