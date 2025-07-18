from ouroboros import run_code

# 複数の論理演算子テスト
logical_test = """
int main() {
    char c = 'a';
    if (c == 'a' || c == 'e') {
        printf("Simple OR works\\n");
    }
    
    if (c == 'a' || c == 'e' || c == 'i') {
        printf("Triple OR works\\n");
    }
    
    return 0;
}
"""

# 2次元配列テスト（単純化）
array_2d_test = """
int main() {
    int matrix[3][3];
    matrix[0][0] = 1;
    matrix[0][1] = 2;
    printf("2D array access: %d %d\\n", matrix[0][0], matrix[0][1]);
    return 0;
}
"""

# printf複数引数テスト
printf_test = """
int main() {
    int a = 10;
    int b = 20;
    printf("a = %d, b = %d\\n", a, b);
    return 0;
}
"""

print("=== 論理演算子テスト ===")
try:
    run_code(logical_test)
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== 2次元配列テスト ===")
try:
    run_code(array_2d_test)
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== printf複数引数テスト ===")
try:
    run_code(printf_test)
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")