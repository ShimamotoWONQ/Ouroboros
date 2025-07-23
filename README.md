# Ouroboros

### - C language interpreter written in Python written in C. -

Ouroborosは、Python で実装された C 言語用インタプリタです  
つまり、C 言語のコードをコンパイルすることなく、ランタイムで逐次的に解析し、実行します  
ちなみに、Pythonの標準実装である CPython は C 言語で実装された Python 用インタプリタです  


## 🚀 Quick Start

### Requirements
- Python 3.7+

### Touch Off
```bash
# ルートディレクトリに移動
cd Ouroboros

# デモ起動用ファイルを実行
python run.py
```
! 今後、画面にはたくさんの情報が表示されます
! 見やすさの為に、ターミナルのサイズを大きくすることを推奨します

## 📖 User Guide

### Menu

`run.py` を実行すると、以下のメニューが表示されます

```
- 20 Sample Programs Available -

1. Execute All Sample Programs
2. Execute Specific Sample Program  
3. Execute C file
4. Execute in Interactive Mode
5. Exit

Please select (1-5):
```

終了するには `5` を入力するか、 `Ctrl + C` を押下してください

> ### `1` Execute All Sample Programs

全てのサンプルプログラムを順番に実行します  
次のサンプルプログラムに進むには `Enter` を押下してください  
中断するには `Ctrl + C` を押下してください  


> ### `2` Execute Specific Program

利用可能なサンプルプログラム一覧が表示されます  
番号を選択して実行できます  


> ### `3` Execute C File

.C ファイルを実行できます  
サンプルとして、ルート直下に `HelloWorld.c` を用意してあります  
`HelloWorld.c` と入力して実行してみてください  


> ### `4` Interactive Mode

直接 C 言語を入力・実行できます  
入力したコードを実行するには `Enter` を２回押下してください  
中断するには `Ctrl + C` を押下してください  

## ✨ Features

- **変数** ... `int`, `float`, `char` 型の宣言と演算 
- **制御** ... `if-else`, `for`, `while` 文  
- **関数** ... 定義、呼び出し、再帰  
- **出力** ... `printf` でのフォーマット出力に対応
- **配列** ... 1次元・2次元配列の操作  
- **文字列関数** ... `strlen`, `strcpy`, `strcmp`  
- **メモリ管理** ... `malloc`, `free`, `realloc` (シミュレーション)

## 🚧 Limitations

- `struct`, `union` は未サポート
- `File I/O` は未サポート
- プリプロセッサは未サポート
- ポインタ操作は基本的な機能のみサポート
