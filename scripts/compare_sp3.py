"""2つのSP3ファイルの軌道を比較し、位置差の3D RMSを出す。

使い方:
    python compare_sp3.py <推定SP3> <基準SP3> [衛星システム文字: G J E R ...]

例:
    python compare_sp3.py baseline_M.sp3 IGS2R03FIN_20191990000_01D_05M_ORB.SP3 G

・.gz のままでも読める
・同じ衛星・同じ時刻の位置だけを比べる(共通エポックのみ)
・SP3の座標はkm。表示はm
・SP3のフレーム(ECEFか慣性系か)が違うと意味のない差になるので、
  ヘッダーの座標系表記も表示する
"""
import gzip
import math
import sys
from collections import defaultdict


def read_sp3(path):
    """{衛星ID: {エポック(文字列): (x, y, z)[m]}} とヘッダー1行目を返す。"""
    opener = gzip.open if path.endswith(".gz") else open
    data = defaultdict(dict)
    header = ""
    epoch = None
    with opener(path, "rt", errors="replace") as f:
        for i, line in enumerate(f):
            if i == 0:
                header = line.rstrip()
            if line.startswith("*"):
                epoch = line[1:].split()
                epoch = " ".join(epoch[:6])
            elif line.startswith("P") and epoch is not None:
                sat = line[1:4]
                try:
                    x = float(line[4:18]) * 1000.0
                    y = float(line[18:32]) * 1000.0
                    z = float(line[32:46]) * 1000.0
                except ValueError:
                    continue
                # 欠測値(0.000000 や 999999.999999)は除外
                if (x == 0 and y == 0 and z == 0) or abs(x) > 9.0e8:
                    continue
                data[sat][epoch] = (x, y, z)
    return data, header


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    path_a, path_b = sys.argv[1], sys.argv[2]
    systems = set(sys.argv[3:])  # 空なら全システム

    a, head_a = read_sp3(path_a)
    b, head_b = read_sp3(path_b)
    print("推定  :", head_a)
    print("基準  :", head_b)

    per_sat = {}
    all_sq = []
    epochs_used = set()
    for sat in sorted(a):
        if systems and sat[0] not in systems:
            continue
        if sat not in b:
            continue
        common = sorted(set(a[sat]) & set(b[sat]))
        if not common:
            continue
        sq = []
        for e in common:
            dx = a[sat][e][0] - b[sat][e][0]
            dy = a[sat][e][1] - b[sat][e][1]
            dz = a[sat][e][2] - b[sat][e][2]
            sq.append(dx * dx + dy * dy + dz * dz)
            epochs_used.add(e)
        per_sat[sat] = (math.sqrt(sum(sq) / len(sq)), len(sq))
        all_sq.extend(sq)

    if not all_sq:
        print("共通の衛星・時刻がありませんでした。日付やシステム指定を確認してください。")
        sys.exit(1)

    print()
    print(f"共通エポック数: {len(epochs_used)}  /  比較した衛星数: {len(per_sat)}")
    print(f"全体の3D RMS : {math.sqrt(sum(all_sq) / len(all_sq)):.3f} m")
    print()
    print("衛星ごとの3D RMS [m]（エポック数）")
    for sat, (rms, n) in sorted(per_sat.items()):
        print(f"  {sat}  {rms:10.3f}  ({n})")


if __name__ == "__main__":
    main()
