from ouroboros import run_code

# 複数変数宣言のテスト
multi_var_test = """
int main() {
    int a = 10, b = 20, c;
    c = a + b;
    printf("a = %d, b = %d, c = %d\\n", a, b, c);
    return 0;
}
"""

# 文字範囲比較のテスト
char_range_test = """
int main() {
    char c = 'A';
    
    if (c >= 'A' && c <= 'Z') {
        printf("'%c' is uppercase\\n", c);
    }
    
    if (c >= 'a' && c <= 'z') {
        printf("'%c' is lowercase\\n", c);
    }
    
    return 0;
}
"""

# 複雑な論理演算子のテスト
complex_logic_test = """
int main() {
    char c = 'e';
    
    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
        printf("'%c' is a letter\\n", c);
        
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
            printf("'%c' is a vowel\\n", c);
        }
    }
    
    return 0;
}
"""

# 複数行条件式のテスト
multiline_condition_test = """
int main() {
    char c = 'A';
    
    if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' ||
        c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U') {
        printf("'%c' is a vowel\\n", c);
    } else if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
        printf("'%c' is a consonant\\n", c);
    }
    
    return 0;
}
"""

print("=== 複数変数宣言テスト ===")
try:
    run_code(multi_var_test)
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== 文字範囲比較テスト ===")
try:
    run_code(char_range_test)
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== 複雑な論理演算子テスト ===")
try:
    run_code(complex_logic_test)
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== 複数行条件式テスト ===")
try:
    run_code(multiline_condition_test)
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")