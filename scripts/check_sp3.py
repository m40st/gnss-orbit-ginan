import gzip
import sys
from collections import Counter

if len(sys.argv) < 2:
    print("使い方: python check_sp3.py <SP3ファイル(.gz可)>")
    sys.exit(1)

path = sys.argv[1]
opener = gzip.open if path.endswith(".gz") else open

sats = set()
with opener(path, "rt", errors="replace") as f:
    for line in f:
        if line.startswith("P"):      # SP3の位置レコード（例: PG01 ...）
            sats.add(line[1:4])       # 衛星ID（例: G01, J02）

print("システム別の衛星数:", dict(sorted(Counter(s[0] for s in sats).items())))
qzss = sorted(s for s in sats if s.startswith("J"))
print("QZSS（J）の衛星:", qzss if qzss else "なし")
