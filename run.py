from src.ouroboros import OuroborosInterpreter

def load_c_file(filename: str) -> str:
    """C言語ファイルを読み込み"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return ""
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def main():
    print("🐍 Ouroboros - Enhanced C Language Interpreter")
    print("C言語で書かれたコードをPythonで実行します")
    print("-" * 60)
    
    interpreter = OuroborosInterpreter()
    
    # より本格的なサンプルプログラム
    sample_programs = [
        """// 基本的な計算プログラム

int main() {
    int a = 10;
    int b = 20;
    int sum = a + b;
    printf("Sum: %d\\n", sum);
    return 0;
}""",
        
        """// ループを使ったプログラム

int main() {
    int i;
    int factorial = 1;
    int n = 5;
    
    for(i = 1; i <= n; i++) {
        factorial *= i;
    }
    
    printf("Factorial of %d is %d\\n", n, factorial);
    return 0;
}""",
        
        """// 配列を使ったプログラム

int main() {
    int numbers[5];
    int i = 0;
    int sum = 0;
    
    // 配列に値を代入
    for(i = 0; i < 5; i++) {
        numbers[i] = (i + 1) * 10;
    }
    
    // 合計を計算
    for(i = 0; i < 5; i++) {
        sum += numbers[i];
        printf("numbers[%d] = %d\\n", i, numbers[i]);
    }
    
    printf("Total sum: %d\\n", sum);
    return 0;
}"""
    ]
    
    print("\n📝 サンプルC言語プログラム:")
    for i, program in enumerate(sample_programs, 1):
        print(f"\n--- Sample {i} ---")
        print(program)
        print(f"\n🚀 実行結果:")
        try:
            # 新しいインタープリターインスタンスで実行
            test_interpreter = OuroborosInterpreter()
            results = test_interpreter.interpret(program)
            if results:
                print(results)
                print(f"Program returned: {results[-1]}")
        except Exception as e:
            print(f"エラー: {e}")
        
        print("-" * 40)
    
    print("\n" + "="*60)
    print("対話モードまたはファイル実行モード:")
    print("- C言語コードを直接入力")
    print("- 'load filename.c' でファイルを読み込み")
    print("- 'exit' で終了")
    
    while True:
        try:
            line = input("ouroboros> ").strip()
            if line.lower() in ('exit', 'quit'):
                break
            if not line:
                continue
            
            # ファイル読み込みコマンド
            if line.startswith('load '):
                filename = line[5:].strip()
                code = load_c_file(filename)
                if code:
                    print(f"Loading {filename}...")
                    print("🚀 実行結果:")
                    results = interpreter.interpret(code)
                    if results:
                        print(f"Program returned: {results[-1]}")
                continue
            
            # 直接コード実行
            results = interpreter.interpret(line)
            if results:
                for result in results:
                    print(f"=> {result}")
                    
        except KeyboardInterrupt:
            print("\n終了します...")
            break
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    main()