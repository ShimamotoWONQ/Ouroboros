# メモリ管理機能のテストコード
from ouroboros import run_code

# 例1: 基本的なmalloc/free
code1 = """
int main() {
    int *ptr = (int*)malloc(4 * sizeof(int));
    if (ptr != NULL) {
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
    char *str = (char*)malloc(20);
    if (str != NULL) {
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
    int *arr = (int*)malloc(3 * sizeof(int));
    if (arr != NULL) {
        arr[0] = 1;
        arr[1] = 2;
        arr[2] = 3;
        
        printf("Original array:\\n");
        for (int i = 0; i < 3; i++) {
            printf("arr[%d] = %d\\n", i, arr[i]);
        }
        
        // 配列を5要素に拡張
        arr = (int*)realloc(arr, 5 * sizeof(int));
        if (arr != NULL) {
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
    int *ptr1 = (int*)malloc(10 * sizeof(int));
    int *ptr2 = (int*)malloc(5 * sizeof(int));
    char *ptr3 = (char*)malloc(50);
    
    printf("Memory addresses:\\n");
    printf("ptr1: %p\\n", ptr1);
    printf("ptr2: %p\\n", ptr2);
    printf("ptr3: %p\\n", ptr3);
    
    if (ptr1 != NULL) {
        for (int i = 0; i < 10; i++) {
            ptr1[i] = i * i;
        }
        printf("ptr1 data: ");
        for (int i = 0; i < 10; i++) {
            printf("%d ", ptr1[i]);
        }
        printf("\\n");
    }
    
    if (ptr2 != NULL) {
        for (int i = 0; i < 5; i++) {
            ptr2[i] = i + 100;
        }
        printf("ptr2 data: ");
        for (int i = 0; i < 5; i++) {
            printf("%d ", ptr2[i]);
        }
        printf("\\n");
    }
    
    if (ptr3 != NULL) {
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
    
    // 最初の確保と解放
    int *ptr1 = (int*)malloc(8 * sizeof(int));
    printf("First allocation: %p\\n", ptr1);
    free(ptr1);
    
    // 同じサイズで再確保（同じアドレスが再利用される可能性）
    int *ptr2 = (int*)malloc(8 * sizeof(int));
    printf("Second allocation: %p\\n", ptr2);
    free(ptr2);
    
    // 異なるサイズで確保
    char *ptr3 = (char*)malloc(32);
    printf("Third allocation: %p\\n", ptr3);
    free(ptr3);
    
    return 0;
}
"""

# 例6: エラーハンドリングのテスト
code6 = """
int main() {
    printf("=== Error Handling Test ===\\n");
    
    // 正常なmalloc
    int *ptr = (int*)malloc(10 * sizeof(int));
    if (ptr != NULL) {
        printf("Malloc successful: %p\\n", ptr);
        ptr[0] = 42;
        printf("Value stored: %d\\n", ptr[0]);
        
        // 正常なfree
        free(ptr);
        printf("Memory freed\\n");
        
        // 二重解放のテスト（エラーが発生するはず）
        printf("Attempting double free...\\n");
        // free(ptr);  // これはエラーになる
    }
    
    return 0;
}
"""

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