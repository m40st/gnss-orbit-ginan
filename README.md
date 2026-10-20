# QZSS-orbit-ginan
Geoscience Australia のオープンソースGNSS解析ツールGinanを用いて準天頂衛星システム(QZSS/みちびき)の軌道を推定し、MGEXproduct(CODE)および JGX MGN productの精密暦と比較・評価する。

## 目的
・GinanによるQZSS軌道推定を再現し、精度を定量的に評価する。

・パラメータが軌道推定に与える影響を仮説をもとに検証する。

・手順・設定・結果を再現可能な形で公開し、日本語の記事としてまとめる。

### 基準暦
主基準　JGX MGN FINAL　─QZSSを含む。当面は試験提供のため取得日を記録。

副基準　MGEX(COD) 　─QZSSの収録は取得時に確認。

JGX の OPS プロダクト（IGS に提出している公式プロダクトと同一）は GPS・GLONASS・Galileo のみで、QZSS は含まれない。
IGS の合成暦は QZSS を含まないため、QZSS の基準としては使わない。
確認済み：JGX0MGNFIN_20262830000_01D_05M_ORB.SP3.gz（2026年第283日）に QZSS の衛星 J02・J03・J04・J07 が含まれる。

#### 現状
・環境:Ginan v4.1.2(Docker)

・QZSS対応：GinanのREADMEでは「Development ongoing」と記載。対応範囲は検証で確認。

・進捗：基準暦の確定

##### ロードマップ

1	基準暦の確定、Ginan 動作確認、データ取得	
2	1日分（2026年第283日）の軌道推定と基準暦との比較をスクリプト/図化する
3	評価指標の決定、1週間分への拡張
4	記事① 再現手順を記事にする
5–6	仮説を立ててパラメータ実験を行う。
7	結果を解釈する。
8	記事② パラメータの影響を記事にする。

**評価指標**

・基準値との差を3DRMSの値で確認。

・基準暦同士の差

**注意**

JGX のデータをコマンドラインで取得する場合はトークンが必要。トークンはリポジトリに含めず、環境変数や .env で管理し、.gitignore で除外する。

**参考**

Ginan: https://github.com/GeoscienceAustralia/ginan

Ginan ドキュメント: https://geoscienceaustralia.github.io/ginan/

JGX: https://jgxnet.gsi.go.jp/ja/top/


