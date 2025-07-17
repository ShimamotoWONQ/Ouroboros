#!/usr/bin/env python3

from ouroboros import run_code

# 1. 再帰関数 - フィボナッチ数列
fibonacci_code = """
int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    for (int i = 0; i < 10; i++) {
        printf("fibonacci(%d) = %d\\n", i, fibonacci(i));
    }
    return 0;
}
"""

# 2. 配列操作とバブルソート
bubble_sort_code = """
int main() {
    int arr[8] = {64, 34, 25, 12, 22, 11, 90, 88};
    int n = 8;
    
    printf("Original array: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\\n");
    
    // Bubble sort
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
    
    printf("Sorted array: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\\n");
    
    return 0;
}
"""

# 3. 複数の関数と複合演算子
complex_functions_code = """
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int power(int base, int exp) {
    int result = 1;
    for (int i = 0; i < exp; i++) {
        result *= base;
    }
    return result;
}

int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main() {
    int num = 5;
    printf("Factorial of %d: %d\\n", num, factorial(num));
    
    int base = 2, exp = 8;
    printf("%d^%d = %d\\n", base, exp, power(base, exp));
    
    int a = 48, b = 18;
    printf("GCD(%d, %d) = %d\\n", a, b, gcd(a, b));
    
    // 複合演算子のテスト
    int x = 10;
    x += 5;
    printf("x += 5: %d\\n", x);
    x *= 2;
    printf("x *= 2: %d\\n", x);
    x /= 3;
    printf("x /= 3: %d\\n", x);
    
    return 0;
}
"""

# 4. ネストした制御構造
nested_control_code = """
int main() {
    int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    
    // 2次元配列の処理（簡略化）
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (i == j) {
                printf("Diagonal element [%d][%d] = %d\\n", i, j, matrix[i][j]);
            } else if (i < j) {
                printf("Upper triangle [%d][%d] = %d\\n", i, j, matrix[i][j]);
            } else {
                printf("Lower triangle [%d][%d] = %d\\n", i, j, matrix[i][j]);
            }
        }
    }
    
    return 0;
}
"""

# 5. 文字列処理（単純化）
string_processing_code = """
int main() {
    char str[] = "Hello World";
    int len = strlen(str);
    
    printf("String: %s\\n", str);
    printf("Length: %d\\n", len);
    
    // 文字列を逆順に出力
    printf("Reversed: ");
    for (int i = len - 1; i >= 0; i--) {
        printf("%c", str[i]);
    }
    printf("\\n");
    
    // 文字数をカウント
    int vowels = 0, consonants = 0;
    for (int i = 0; i < len; i++) {
        char c = str[i];
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' ||
            c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U') {
            vowels++;
        } else if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
            consonants++;
        }
    }
    
    printf("Vowels: %d, Consonants: %d\\n", vowels, consonants);
    
    return 0;
}
"""

# 6. 数学的アルゴリズム
math_algorithms_code = """
int isPrime(int n) {
    if (n <= 1) return 0;
    if (n <= 3) return 1;
    if (n % 2 == 0 || n % 3 == 0) return 0;
    
    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) {
            return 0;
        }
    }
    return 1;
}

int main() {
    printf("Prime numbers up to 50:\\n");
    for (int i = 2; i <= 50; i++) {
        if (isPrime(i)) {
            printf("%d ", i);
        }
    }
    printf("\\n");
    
    // パスカルの三角形（最初の6行）
    printf("\\nPascal's Triangle:\\n");
    for (int i = 0; i < 6; i++) {
        int val = 1;
        for (int j = 0; j <= i; j++) {
            printf("%d ", val);
            val = val * (i - j) / (j + 1);
        }
        printf("\\n");
    }
    
    return 0;
}
"""

# テスト実行
test_cases = [
    ("フィボナッチ数列", fibonacci_code),
    ("バブルソート", bubble_sort_code),
    ("複数関数と複合演算子", complex_functions_code),
    ("ネストした制御構造", nested_control_code),
    ("文字列処理", string_processing_code),
    ("数学的アルゴリズム", math_algorithms_code)
]

def run_tests():
    for name, code in test_cases:
        print(f"\n{'='*50}")
        print(f"Testing: {name}")
        print('='*50)
        try:
            run_code(code)
            print(f"✓ {name} - SUCCESS")
        except Exception as e:
            print(f"✗ {name} - FAILED: {e}")

if __name__ == "__main__":
    run_tests()