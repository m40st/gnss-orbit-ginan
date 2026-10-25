#!/bin/bash
# fit_sp3_pseudoobs.yaml の実行に必要なGinanの入力ファイルだけを取得する。
# 取得先: Ginan公式の配布元(Amazon S3)のみ。
#
# 使い方:
#   bash get_ginan_inputs.sh check   # 存在とサイズの確認だけ(ダウンロードしない)
#   bash get_ginan_inputs.sh get     # ダウンロードして解凍する

SERVER="https://peanpod.s3.ap-southeast-2.amazonaws.com/aux/products"
DEST="/data/ginan_work/products"

FILES=(
  "boxwing.yaml"
  "igs20.atx"
  "igs96p02.erp"
  "brdm1990.19p"
  "IGS1R03SNX_20191950000_07D_07D_CRD.SNX"
  "IGS2R03FIN_20191980000_01D_05M_ORB.SP3"
  "IGS2R03FIN_20191990000_01D_05M_ORB.SP3"
  "IGS2R03FIN_20192000000_01D_05M_ORB.SP3"
  "tables/EGM2008.gfc"
  "tables/DE436.1950.2050"
  "tables/fes2014b_Cnm-Snm.dat"
  "tables/igs_satellite_metadata_2203_plus.snx"
  "tables/sat_yaw_bias_rate.snx"
  "tables/qzss_yaw_modes.snx"
  "tables/bds_yaw_modes.snx"
)

MODE="$1"
if [ "$MODE" != "check" ] && [ "$MODE" != "get" ]; then
  echo "使い方: bash $0 check | get"
  exit 1
fi

total=0
for f in "${FILES[@]}"; do
  url="$SERVER/$f.gz"
  if [ "$MODE" = "check" ]; then
    # ヘッダーだけ取得してサイズを確認(本体は取得しない)
    size=$(curl -sI -L "$url" | tr -d '\r' | awk 'tolower($1)=="content-length:" {print $2}' | tail -1)
    code=$(curl -s -o /dev/null -I -L -w "%{http_code}" "$url")
    echo "$code  ${size:-?} bytes  $f"
    [ -n "$size" ] && total=$((total + size))
  else
    mkdir -p "$DEST/$(dirname "$f")"
    if [ -f "$DEST/$f" ]; then
      echo "スキップ(既に存在): $f"
      continue
    fi
    echo "取得: $f"
    if curl -fL --retry 3 -o "$DEST/$f.gz" "$url"; then
      gzip -d "$DEST/$f.gz"
    else
      echo "  失敗: $f"
      rm -f "$DEST/$f.gz"
    fi
  fi
done

if [ "$MODE" = "check" ]; then
  echo "合計(圧縮時): $((total / 1024 / 1024)) MB 程度"
fi
