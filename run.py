from ouroboros import run_code, Logger
from sample_programs import sample_programs

def load_c_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        Logger.error(f"File '{filename}' not found.")
        return ""
    except Exception as e:
        Logger.error(f"Error reading file: {e}")
        return ""

def main():
    Logger.title()
    Logger.divider()
    
    Logger.header("📝 C言語プログラムのサンプル:")
    for i, program in enumerate(sample_programs, 1):
        Logger.section_start(f"Sample No.{i}")
        try:
            Logger.print(program)
            Logger.marker()
            run_code(program)
        except Exception as e:
            Logger.error(f"{e}")
        
    # print("対話モードまたはファイル実行モード:")
    # print("- C言語コードを直接入力")
    # print("- 'load filename.c' でファイルを読み込み")
    # print("- 'exit' で終了")
    
    # while True:
    #     try:
    #         line = input("ouroboros> ").strip()
    #         if line.lower() in ('exit', 'quit'):
    #             break
    #         if not line:
    #             continue
            
    #         if line.startswith('load '):
    #             filename = line[5:].strip()
    #             code = load_c_file(filename)
    #             if code:
    #                 print(f"Loading {filename}...")
    #                 print("Result:")
    #                 results = run_code(code)
    #                 if results:
    #                     print(f"Program returned: {results[-1]}")
    #             continue
            
    #         run_code(line)
                    
    #     except KeyboardInterrupt:
    #         Logger.info("See you, or me!")
    #         break
    #     except Exception as e:
    #         Logger.error(f"{e}")

if __name__ == "__main__":
    main()