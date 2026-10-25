#!/bin/bash
# fit_jgxboth の出力で、QZSSがどこまで処理されているかを確認する(読み取りのみ)

D=/ginan/exampleConfigs/outputs/fit_jgxboth_HEAD
cd "$D" || { echo "出力フォルダが見つかりません: $D"; exit 1; }

echo "== 1. orbit_ics の最初と最後のファイル =="
first=$(ls orbit_ics | head -1)
last=$(ls orbit_ics | tail -1)
echo "最初: $first"
echo "最後: $last"

echo
echo "== 2. 各ファイルに載っている衛星(最初と最後) =="
for f in "$first" "$last"; do
  echo "-- $f"
  echo "   G の衛星数: $(grep -o 'G[0-9][0-9]' "orbit_ics/$f" | sort -u | wc -l)"
  echo "   J の衛星  : $(grep -o 'J[0-9][0-9]' "orbit_ics/$f" | sort -u | tr '\n' ' ')"
done

echo
echo "== 3. orbit_ics のうち J02 を含むファイルの数 / 全体 =="
echo "J02あり: $(grep -l 'J02' orbit_ics/* | wc -l) / $(ls orbit_ics | wc -l)"
echo "G01あり: $(grep -l 'G01' orbit_ics/* | wc -l) / $(ls orbit_ics | wc -l)"

echo
echo "== 4. Network.TRACE の ORBIT 行(J02 と G01 の行数) =="
echo "J02: $(grep -c 'ORBIT.*J02' fit_jgxboth_HEAD_Network.TRACE)"
echo "G01: $(grep -c 'ORBIT.*G01' fit_jgxboth_HEAD_Network.TRACE)"

echo
echo "== 5. 出力SP3の衛星システム別の位置レコード数(1日目) =="
grep '^P' fit_jgxboth_HEAD_2026-10-08_00:00_M.sp3 | cut -c2 | sort | uniq -c
