sample_programs = [

    """
// 基本的な計算プログラム

    int main() {
        int a = 10;
        int b = 20;
        int sum = a + b;
        printf("Sum: %d\\n", sum);
        return 0;
    }""",
            
    """
// ループを使ったプログラム

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
            
    """
// 配列を使ったプログラム

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