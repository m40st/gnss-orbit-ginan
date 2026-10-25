# gnss-orbit-ginan

Ginan（Geoscience Australia製のオープンソースGNSS解析ツール）で、GNSS衛星の軌道を精密暦（SP3）に当てはめ、力学モデルの設定（極潮汐など）が精度に与える影響を調べる実験記録。準天頂衛星QZSS/みちびきの処理は調査中。

## 目的

- Ginanで精密暦（SP3）への軌道の当てはめを行い、精度を定量的に評価する。QZSSへの適用を目指す。
- パラメータが軌道の当てはめに与える影響を、仮説をもとに検証する。
- 手順・設定・結果を再現可能な形で公開し、日本語の記事としてまとめる。

## 概要と方式

Ginanの付属設定（`fit_sp3_pseudoobs.yaml`）を使い、精密暦（SP3）を擬似観測として、力学モデルで軌道を当てはめる。観測データRINEXから軌道を推定する方式ではない。

評価指標：推定SP3と基準SP3の位置差の3D RMS（共通の衛星・時刻のみ）。基準暦同士の差、すなわち基準の不確かさの目安）は、今後評価する予定。

## 結果（GPS、2019年7月17〜19日、IGS最終暦への当てはめ）

| 条件 | 17日 | 18日 | 19日 |
|---|---|---|---|
| 基準（極潮汐あり） | 0.007 m | 0.030 m | 0.078 m |
| 極潮汐なし | 0.007 m | 0.030 m | 0.078 m |
| 2つの推定軌道の差 | 0.001 m | 0.002 m | 未確認 |

数値は、推定SP3と基準SP3の位置差の3D RMS。詳細は [docs/experiment_log.md](docs/experiment_log.md)。

- 仮説：衛星の力モデルのうち、極潮汐を考慮しないと、基準暦との当てはめ誤差が増える。期間が長くなるほど差が広がる。
- 結果：軌道は1〜2 mm動くが、当てはめ誤差には現れなかった（3日間）。3日間の実験なので、長期の影響は検証できていない。
- 注意：この設定は経験的パラメータを有効にしており、小さな力モデルの違いを吸収している可能性がある（仮説・未検証）。

## 基準暦

### これまでの実験で使った基準

IGS REPRO3 最終暦（IGS2R03FIN、GPS、2019年7月17〜19日）を使用した。Ginan付属のサンプル設定が、この暦への3日間の当てはめを例にしているため（Ginanの `exampleConfigs/README.md`、[7]）。

### QZSSで使う基準（計画）

| プロダクト | QZSS | 位置づけ |
|---|---|---|
| JGX MGN Final | 含む | 主基準。当面は試験提供のため、取得日を記録する |
| JGX OPS | 含まない | QZSSの基準には使わない |
| 他のMGEX解析センターの暦（CODEなど） | 取得時に確認 | 副基準の候補（未使用） |

### 確認した事実

- JGXは、国土地理院（GSI）とJAXAが共同で運営するIGS解析センターで、2023年12月から運用されている [1][2]。
- JGXには2種類のプロダクトがある。OPSはGPS・GLONASS・Galileoを対象とし、IGSに提出している公式プロダクトと同一。MGNはQZSSを含むMulti-GNSSプロダクトで、当面は試験提供とされている [3][8]。
- JGXの解析にはJAXAのMADOCAが使われている。QZSSとBeiDouを含むFinal暦は、JAXAがMGEXに提供しているとされている [4]。
- QZSSの精密暦をIGSの公式プロダクトにすることは、JGXチームの今後の優先課題とされている [5]。そのため、IGSの合成暦にはQZSSが含まれないと理解している（IGSのプロダクト一覧では未確認）。
- 自分で確認：`JGX0MGNFIN_20262830000_01D_05M_ORB.SP3.gz`（2026年第283日）に、QZSSの J02・J03・J04・J07 が含まれる。第281・282日も同様。取得日は、第283日が2026年10月20日、第281・282日が10月22日。

### 基準の不確かさ

基準暦そのものにも誤差がある。文献では、MGEXの解析センター間のQZSS（傾斜軌道）の軌道の一致は、3Dで11〜16 cm程度とされている [6]。この値より小さい差は、基準の不確かさと区別できない可能性がある。

### 未評価の点

- JGX MGNの座標系はIGS20系（SP3のヘッダーに `IGc20` と表記）で、Ginanの出力は `igb14` 表記。この差が評価に与える影響は未評価。

### 参考文献

1. JGX Product Performance（IGS Workshop 2026ポスター）: https://files.igs.org/pub/resource/pubs/workshop/2026/IGS2026_Sy_P101_Miyahara.pdf
2. 国土地理院「日本初！国際GNSS事業の解析センターに認定」（2023年12月4日）: https://www.gsi.go.jp/denshi/denshi65011.html
3. GNSS精密暦提供サービス（JGX）: https://jgxnet.gsi.go.jp/ja/top/
4. Overview of MADOCA（IGS Workshop 2026ポスター）: https://files.igs.org/pub/resource/pubs/workshop/2026/IGS2026_Sy_P104_Imada.pdf
5. JPGU 2026 U06-05「Japanese Precise Orbit Determination for GNSS satellites…」: https://pub.confit.atlas.jp/ja/event/jpgu2026/presentation/U06-05
6. Precise Orbit and Clock Products of Galileo, BDS and QZSS from MGEX Since 2018: Comparison and PPP Validation, Remote Sensing 12(9), 2020: https://doi.org/10.3390/rs12091415
7. Ginan（Geoscience Australia）: https://github.com/GeoscienceAustralia/ginan
8. 国土地理院「GNSS精密暦の提供を開始」（2024年3月28日）: https://www.gsi.go.jp/denshi/denshi65013.html

## 現状

- 環境：Ginan v4.1.2（Docker）
- QZSS対応：GinanのREADMEでは「Development ongoing」と記載。対応範囲は検証で確認する。
- 進捗：極潮汐の実験（GPS）は完了。JGX MGN最終暦（2026年10月8〜10日）を入力にした実行も行ったが、JGXとの差の評価は未実施。QZSSは内部では処理されているが（`orbit_ics`、TRACEに記録）、SP3に出力されない。原因は調査中。

## ロードマップ

| 段階 | 内容 | 状態 |
|---|---|---|
| 1 | 基準暦の確定、Ginanの動作確認、データ取得 | 完了 |
| 2 | GPSの当てはめと評価（極潮汐の実験） | 完了 |
| 3 | QZSSがSP3に出力されない原因の調査（Ginanへの質問を含む） | 進行中 |
| 4 | 重力場の次数（`egm_degree`）の実験（GPS） | 未着手 |
| 5 | 記事① 再現手順 | 未着手 |
| 6 | QZSSでのパラメータ実験（3が解決した場合） | 未定 |
| 7 | 記事② パラメータの影響 | 未着手 |

## ディレクトリ構成

- `scripts/`：SP3の確認・比較、Ginanの入力ファイルの取得、診断用のスクリプト
- `configs/`：Ginanの設定ファイル（付属の設定をコピーして変更したもの）
- `docs/`：実験ログ

## データの扱い

- 精密暦（SP3）や、Ginanの入力データは、このリポジトリに含めない。各提供元の利用条件に従って、取得する。
- JGXのデータは、手で、必要な日だけをダウンロードしている。過度な通信を避けるため、クローラーや大量のダウンロードは行わない（JGXサイトの注意書きに従う）。
- JGXのデータをコマンドラインで取得する場合はトークンが必要。トークンはリポジトリに含めず、環境変数や `.env` で管理し、`.gitignore` で除外する。
- JGXのプロダクトは、解析設定の変更や再解析で更新されることがある。使用したファイルと取得日は [docs/experiment_log.md](docs/experiment_log.md) に記録する。

## 出典・ライセンス

- 出典：GNSS精密暦提供サービス（https://jgxnet.gsi.go.jp/ja/top/）。国土地理院とJAXAの連携により得られた成果。
- 本リポジトリの結果は、上記のJGX MGN最終暦を入力として、筆者が編集・加工して作成したものであり、国土地理院およびJAXAが作成したものではない。
- JGX MGN最終暦のDOI：https://doi.org/10.57499/GSI_GNSS_2025_006
- Ginan：Geoscience Australia、Apache License 2.0。`configs/` の設定は、Ginan付属の設定を元に、一部を変更したもの。
- 本リポジトリのスクリプトのライセンス：未定（決まったら記載する）。
