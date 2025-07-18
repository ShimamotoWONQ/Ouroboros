# メモリ管理機能のテストコード

# 例1: 基本的なmalloc/free
code1 = """
int main() {
    int *ptr = malloc(4 * sizeof(int));
    if (ptr != 0) {
        ptr[0] = 10;
        ptr[1] = 20;
        ptr[2] = 30;
        ptr[3] = 40;
        
        printf("Allocated array:\\n");
        for (int i = 0; i < 4; i++) {
            printf("ptr[%d] = %d\\n", i, ptr[i]);
        }
        
        free(ptr);
        printf("Memory freed successfully\\n");
    }
    return 0;
}
"""

# 例2: 動的文字列処理
code2 = """
int main() {
    char *str = malloc(20);
    if (str != 0) {
        strcpy(str, "Hello, World!");
        printf("String: %s\\n", str);
        printf("Length: %d\\n", strlen(str));
        
        free(str);
        printf("String memory freed\\n");
    }
    return 0;
}
"""

# 例3: realloc による動的配列の拡張
code3 = """
int main() {
    int *arr = malloc(3 * sizeof(int));
    if (arr != 0) {
        arr[0] = 1;
        arr[1] = 2;
        arr[2] = 3;
        
        printf("Original array:\\n");
        for (int i = 0; i < 3; i++) {
            printf("arr[%d] = %d\\n", i, arr[i]);
        }
        
        arr = realloc(arr, 5 * sizeof(int));
        if (arr != 0) {
            arr[3] = 4;
            arr[4] = 5;
            
            printf("Extended array:\\n");
            for (int i = 0; i < 5; i++) {
                printf("arr[%d] = %d\\n", i, arr[i]);
            }
            
            free(arr);
            printf("Extended array freed\\n");
        }
    }
    return 0;
}
"""

# 例4: 複数のメモリ確保と解放
code4 = """
int main() {
    int *ptr1 = malloc(10 * sizeof(int));
    int *ptr2 = malloc(5 * sizeof(int));
    char *ptr3 = malloc(50);
    
    printf("Memory addresses:\\n");
    printf("ptr1: %p\\n", ptr1);
    printf("ptr2: %p\\n", ptr2);
    printf("ptr3: %p\\n", ptr3);
    
    if (ptr1 != 0) {
        for (int i = 0; i < 10; i++) {
            ptr1[i] = i * i;
        }
        printf("ptr1 data: ");
        for (int i = 0; i < 10; i++) {
            printf("%d ", ptr1[i]);
        }
        printf("\\n");
    }
    
    if (ptr2 != 0) {
        for (int i = 0; i < 5; i++) {
            ptr2[i] = i + 100;
        }
        printf("ptr2 data: ");
        for (int i = 0; i < 5; i++) {
            printf("%d ", ptr2[i]);
        }
        printf("\\n");
    }
    
    if (ptr3 != 0) {
        strcpy(ptr3, "Dynamic string allocation test");
        printf("ptr3 string: %s\\n", ptr3);
    }
    
    free(ptr1);
    free(ptr2);
    free(ptr3);
    
    printf("All memory freed\\n");
    return 0;
}
"""

# 例5: メモリ再利用のテスト
code5 = """
int main() {
    printf("=== Memory Reuse Test ===\\n");
    
    int *ptr1 = malloc(8 * sizeof(int));
    printf("First allocation: %p\\n", ptr1);
    free(ptr1);
    
    int *ptr2 = malloc(8 * sizeof(int));
    printf("Second allocation: %p\\n", ptr2);
    free(ptr2);
    
    char *ptr3 = malloc(32);
    printf("Third allocation: %p\\n", ptr3);
    free(ptr3);
    
    return 0;
}
"""

# 例6: エラーハンドリングのテスト
code6 = """
int main() {
    printf("=== Error Handling Test ===\\n");
    
    int *ptr = malloc(10 * sizeof(int));
    if (ptr != 0) {
        printf("Malloc successful: %p\\n", ptr);
        ptr[0] = 42;
        printf("Value stored: %d\\n", ptr[0]);
        
        free(ptr);
        printf("Memory freed\\n");
    }
    
    return 0;
}
"""

# 実行
from ouroboros import run_code

print("=== Test 1: Basic malloc/free ===")
run_code(code1)

print("\\n=== Test 2: Dynamic string processing ===")
run_code(code2)

print("\\n=== Test 3: realloc test ===")
run_code(code3)

print("\\n=== Test 4: Multiple allocations ===")
run_code(code4)

print("\\n=== Test 5: Memory reuse test ===")
run_code(code5)

print("\\n=== Test 6: Error handling test ===")
run_code(code6)

# メモリ使用状況のデバッグ出力
print("\\n=== Memory Manager Debug Info ===")
try:
    from ouroboros.interpreter import OuroborosInterpreter
    interpreter = OuroborosInterpreter()
    print(interpreter.memory_manager.debug_dump())
except Exception as e:
    print(f"Debug info not available: {e}")