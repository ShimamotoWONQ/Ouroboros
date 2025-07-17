# 例1: 変数と計算
code1 = """
int x = 5;
int y = x * 2;
printf("Result: %d\\n", y);
"""

# 例2: for文
code2 = """
int main() {
    for(int i = 0; i < 5; i++) {
        printf("i = %d\\n", i);
    }
    return 0;
}
"""

# 例3: 関数定義
code3 = """
int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(10, 20);
    printf("Sum: %d\\n", result);
    return 0;
}
"""

# 実行
from ouroboros import run_code
run_code(code1)
run_code(code2)
run_code(code3)