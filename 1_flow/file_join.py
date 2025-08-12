# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import os
import glob
import pandas as pd
import sys
import subprocess

#=============================================
#　CSVファイルのIDカラム名（必要に応じて変更してください）
#=============================================
ID = 'id'

#=============================================
# 現在の作業ディレクトリ（スクリプトのあるディレクトリなど）を取得
#=============================================
current_dpath = os.getcwd()
parent_dpath = os.path.dirname(current_dpath)

#=============================================
# Inputデータフォルダパス
#=============================================
INPUT_DNAME = "2_data"
input_dpath = os.path.join(parent_dpath, INPUT_DNAME)

#=============================================
# 出力先のフォルダパス
#=============================================
OUTPUT_DNAME = "3_output"
output_dpath = os.path.join(parent_dpath, OUTPUT_DNAME)
os.makedirs(output_dpath, exist_ok=True)

#=============================================
# 保存名
#=============================================
save_name = "結合.csv"
save_path = os.path.join(output_dpath, save_name)

#=============================================
# 出力先フォルダの前回処理ファイルを削除
#=============================================
for f in os.listdir(output_dpath):
    file_path = os.path.join(output_dpath, f)
    if os.path.isfile(file_path):
        os.remove(file_path)

#=============================================
# ファイルリスト取得
#=============================================
csv_files = glob.glob(os.path.join(input_dpath, "*.csv"))

if not csv_files:
    print("❌ CSVファイルが見つかりません。処理を終了します。")
    sys.exit(1)

#=============================================
# CSV読み込み & 結合
#=============================================
data_list = []
for file in csv_files:
    try:
        df = pd.read_csv(file, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file, encoding="cp932")
    data_list.append(df)

data_df = pd.concat(data_list, axis=0, ignore_index=True)

#=============================================
# 重複IDチェック
#=============================================
if data_df[ID].duplicated().any():
    dup_ids = data_df.loc[data_df["id"].duplicated(), ID].unique()
    print(f"❌ 重複したIDが見つかりました: {list(dup_ids)}")
    print("処理を中止します。")
    sys.exit(1)

#=============================================
# CSV保存
#=============================================
data_df.to_csv(save_path, encoding="cp932", index=False)

#=============================================
# 保存フォルダを開く（OS別対応）
#=============================================
if sys.platform.startswith('win'):
    os.startfile(output_dpath)
elif sys.platform.startswith('darwin'):
    subprocess.run(['open', output_dpath])
else:
    subprocess.run(['xdg-open', output_dpath])


print("処理完了👍")
