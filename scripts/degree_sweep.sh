#!/bin/bash
# egm_degree（重力場の次数）を変えて、同じ当てはめを繰り返す。
# 入力: IGS REPRO3 最終暦（GPS、2019年7月17〜19日）。基準は fit_baseline.yaml（egm_degree: 15）。
#
# 使い方（コンテナの中で）:
#   bash /data/ginan_work/degree_sweep.sh 2 4 8 12
# 1つの次数につき、約5分かかる。
#
# 出力: /data/ginan_work/outputs_baseline/deg<次数>_20190717.sp3 など（":" を含まない名前）

set -e

CONF=/data/ginan_work/configs
OUT=/data/ginan_work/outputs_baseline
BASE=$CONF/fit_baseline.yaml

if [ "$#" -lt 1 ]; then
  echo "使い方: bash $0 <次数> [<次数> ...]   例: bash $0 2 4 8 12"
  exit 1
fi

if [ ! -f "$BASE" ]; then
  echo "基準の設定が見つかりません: $BASE"
  exit 1
fi

cd /ginan/exampleConfigs

for DEG in "$@"; do
  NAME=fit_deg${DEG}
  echo "=============================="
  echo "次数 $DEG の設定を作ります: $NAME"

  cp "$BASE" "$CONF/$NAME.yaml"
  sed -i "s/egm_degree: 15/egm_degree: ${DEG}/" "$CONF/$NAME.yaml"
  sed -i "s/config_description: fit_sp3_pseudoobs_/config_description: ${NAME}_/" "$CONF/$NAME.yaml"

  echo "基準との差分（egm_degree と config_description の2か所だけのはず）:"
  diff "$BASE" "$CONF/$NAME.yaml" || true

  N=$(diff "$BASE" "$CONF/$NAME.yaml" | grep -c '^>' || true)
  if [ "$N" -ne 2 ]; then
    echo "差分が2行ではありません（$N 行）。中断します。"
    exit 1
  fi

  echo "実行します（約5分）"
  pea --config "$CONF/$NAME.yaml" > "/data/ginan_work/${NAME}_run.log" 2>&1

  for D in 17 18 19; do
    SRC="outputs/${NAME}_HEAD/${NAME}_HEAD_2019-07-${D}_00:00_M.sp3"
    if [ ! -f "$SRC" ]; then
      echo "出力が見つかりません: $SRC"
      exit 1
    fi
    cp "$SRC" "$OUT/deg${DEG}_201907${D}.sp3"
  done
  echo "次数 $DEG: 完了"
done

echo "=============================="
echo "すべて完了しました。保存先: $OUT"
ls -l "$OUT" | grep deg
