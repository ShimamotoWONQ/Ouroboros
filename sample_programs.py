#!/usr/bin/env python3
"""
Sample Programs for Ouroboros
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class ProgramCategory(Enum):
    BASIC = "Basic Programming"
    CONTROL_FLOW = "Control Flow"
    FUNCTIONS = "Functions"
    ARRAYS = "Arrays"
    STRINGS = "String Processing"
    MEMORY = "Memory Management"
    ALGORITHMS = "Mathematical Algorithms"
    ADVANCED = "Advanced Features"

@dataclass
class SampleProgram:
    id: str
    title: str
    description: str
    category: ProgramCategory
    difficulty: int  # 1-5 scale
    code: str
    expected_output: Optional[str] = None
    notes: Optional[str] = None

class SampleProgramManager:
    def __init__(self):
        self.programs: List[SampleProgram] = []
        self._load_programs()
    
    def _load_programs(self):
        """Load all sample programs"""
        
        # Basic Programming
        self.programs.extend([
            SampleProgram(
                id="basic_hello",
                title="Hello World",
                description="Basic printf output",
                category=ProgramCategory.BASIC,
                difficulty=1,
                code='''

int main() {
    printf("Hello, World!\\n");
    return 0;
}''',
                expected_output="Hello, World!\n"
            ),
            
            SampleProgram(
                id="basic_variables",
                title="Variable Declaration and Operations",
                description="Basic variable operations and arithmetic",
                category=ProgramCategory.BASIC,
                difficulty=1,
                code='''int main() {
    int x = 5;
    int y = x * 2;
    printf("x = %d, y = %d\\n", x, y);
    
    int a = 10, b = 20, c;
    c = a + b;
    printf("a = %d, b = %d, c = %d\\n", a, b, c);
    
    return 0;
}''',
                expected_output="x = 5, y = 10\na = 10, b = 20, c = 30\n"
            ),
        ])
        
        # Control Flow
        self.programs.extend([
            SampleProgram(
                id="control_if_else",
                title="Conditional Statements",
                description="if-else statements and logical operators",
                category=ProgramCategory.CONTROL_FLOW,
                difficulty=2,
                code='''int main() {
    int x = 15;
    
    if (x > 10) {
        printf("x is greater than 10\\n");
    } else {
        printf("x is not greater than 10\\n");
    }
    
    char c = 'A';
    if (c >= 'A' && c <= 'Z') {
        printf("'%c' is uppercase\\n", c);
    }
    
    return 0;
}''',
                expected_output="x is greater than 10\n'A' is uppercase\n"
            ),
            
            SampleProgram(
                id="control_for_loop",
                title="For Loop",
                description="Basic for loop implementation",
                category=ProgramCategory.CONTROL_FLOW,
                difficulty=2,
                code='''int main() {
    for(int i = 0; i < 5; i++) {
        printf("i = %d\\n", i);
    }
    return 0;
}''',
                expected_output="i = 0\ni = 1\ni = 2\ni = 3\ni = 4\n"
            ),
            
            SampleProgram(
                id="control_while_loop",
                title="While Loop",
                description="While loop with counter",
                category=ProgramCategory.CONTROL_FLOW,
                difficulty=2,
                code='''int main() {
    int count = 0;
    while (count < 3) {
        printf("Count: %d\\n", count);
        count++;
    }
    return 0;
}''',
                expected_output="Count: 0\nCount: 1\nCount: 2\n"
            ),
        ])
        
        # Functions
        self.programs.extend([
            SampleProgram(
                id="func_basic",
                title="Function Definition and Call",
                description="Basic function definition and calling",
                category=ProgramCategory.FUNCTIONS,
                difficulty=2,
                code='''int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(10, 20);
    printf("Sum: %d\\n", result);
    return 0;
}''',
                expected_output="Sum: 30\n"
            ),
            
            SampleProgram(
                id="func_fibonacci",
                title="Recursive Fibonacci",
                description="Fibonacci sequence using recursion",
                category=ProgramCategory.FUNCTIONS,
                difficulty=4,
                code='''int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    for (int i = 0; i < 8; i++) {
        printf("fibonacci(%d) = %d\\n", i, fibonacci(i));
    }
    return 0;
}''',
                expected_output="fibonacci(0) = 0\nfibonacci(1) = 1\nfibonacci(2) = 1\nfibonacci(3) = 2\nfibonacci(4) = 3\nfibonacci(5) = 5\nfibonacci(6) = 8\nfibonacci(7) = 13\n"
            ),
            
            SampleProgram(
                id="func_factorial",
                title="Factorial Function",
                description="Recursive factorial calculation",
                category=ProgramCategory.FUNCTIONS,
                difficulty=3,
                code='''int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int num = 5;
    printf("Factorial of %d: %d\\n", num, factorial(num));
    return 0;
}''',
                expected_output="Factorial of 5: 120\n"
            ),
        ])
        
        # Arrays
        self.programs.extend([
            SampleProgram(
                id="array_basic",
                title="Array Operations",
                description="Basic array declaration and manipulation",
                category=ProgramCategory.ARRAYS,
                difficulty=2,
                code='''int main() {
    int arr[5] = {10, 20, 30, 40, 50};
    
    printf("Array elements:\\n");
    for (int i = 0; i < 5; i++) {
        printf("arr[%d] = %d\\n", i, arr[i]);
    }
    
    return 0;
}''',
                expected_output="Array elements:\narr[0] = 10\narr[1] = 20\narr[2] = 30\narr[3] = 40\narr[4] = 50\n"
            ),
            
            SampleProgram(
                id="array_bubble_sort",
                title="Bubble Sort Algorithm",
                description="Sorting array using bubble sort",
                category=ProgramCategory.ARRAYS,
                difficulty=4,
                code='''int main() {
    int arr[6] = {64, 34, 25, 12, 22, 11};
    int n = 6;
    
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
}''',
                expected_output="Original array: 64 34 25 12 22 11 \nSorted array: 11 12 22 25 34 64 \n"
            ),
            
            SampleProgram(
                id="array_2d_matrix",
                title="2D Array Matrix",
                description="Two-dimensional array operations",
                category=ProgramCategory.ARRAYS,
                difficulty=3,
                code='''int main() {
    int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    
    printf("Matrix:\\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\\n");
    }
    
    printf("Diagonal elements: ");
    for (int i = 0; i < 3; i++) {
        printf("%d ", matrix[i][i]);
    }
    printf("\\n");
    
    return 0;
}''',
                expected_output="Matrix:\n1 2 3 \n4 5 6 \n7 8 9 \nDiagonal elements: 1 5 9 \n"
            ),
        ])
        
        # String Processing
        self.programs.extend([
            SampleProgram(
                id="string_basic",
                title="String Operations",
                description="Basic string manipulation",
                category=ProgramCategory.STRINGS,
                difficulty=2,
                code='''int main() {
    char str[] = "Hello World";
    int len = strlen(str);
    
    printf("String: %s\\n", str);
    printf("Length: %d\\n", len);
    
    return 0;
}''',
                expected_output="String: Hello World\nLength: 11\n"
            ),
            
            SampleProgram(
                id="string_vowel_count",
                title="Vowel Counter",
                description="Count vowels and consonants in a string",
                category=ProgramCategory.STRINGS,
                difficulty=3,
                code='''int main() {
    char str[] = "Hello World";
    int len = strlen(str);
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
    
    printf("String: %s\\n", str);
    printf("Vowels: %d, Consonants: %d\\n", vowels, consonants);
    
    return 0;
}''',
                expected_output="String: Hello World\nVowels: 3, Consonants: 7\n"
            ),
        ])
        
        # Memory Management
        self.programs.extend([
            SampleProgram(
                id="memory_malloc_basic",
                title="Dynamic Memory Allocation",
                description="Basic malloc and free operations",
                category=ProgramCategory.MEMORY,
                difficulty=4,
                code='''int main() {
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
}''',
                expected_output="Allocated array:\nptr[0] = 10\nptr[1] = 20\nptr[2] = 30\nptr[3] = 40\nMemory freed successfully\n",
                notes="Demonstrates dynamic memory allocation simulation"
            ),
            
            SampleProgram(
                id="memory_realloc",
                title="Memory Reallocation",
                description="Dynamic array expansion with realloc",
                category=ProgramCategory.MEMORY,
                difficulty=5,
                code='''int main() {
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
}''',
                expected_output="Original array:\narr[0] = 1\narr[1] = 2\narr[2] = 3\nExtended array:\narr[0] = 1\narr[1] = 2\narr[2] = 3\narr[3] = 4\narr[4] = 5\nExtended array freed\n"
            ),
        ])
        
        # Mathematical Algorithms
        self.programs.extend([
            SampleProgram(
                id="math_prime_check",
                title="Prime Number Detection",
                description="Check if numbers are prime",
                category=ProgramCategory.ALGORITHMS,
                difficulty=3,
                code='''int isPrime(int n) {
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
    printf("Prime numbers up to 20:\\n");
    for (int i = 2; i <= 20; i++) {
        if (isPrime(i)) {
            printf("%d ", i);
        }
    }
    printf("\\n");
    
    return 0;
}''',
                expected_output="Prime numbers up to 20:\n2 3 5 7 11 13 17 19 \n"
            ),
            
            SampleProgram(
                id="math_gcd",
                title="Greatest Common Divisor",
                description="Calculate GCD using Euclidean algorithm",
                category=ProgramCategory.ALGORITHMS,
                difficulty=3,
                code='''int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main() {
    int a = 48, b = 18;
    printf("GCD(%d, %d) = %d\\n", a, b, gcd(a, b));
    
    a = 56; b = 98;
    printf("GCD(%d, %d) = %d\\n", a, b, gcd(a, b));
    
    return 0;
}''',
                expected_output="GCD(48, 18) = 6\nGCD(56, 98) = 14\n"
            ),
        ])
        
        # Advanced Features
        self.programs.extend([
            SampleProgram(
                id="advanced_compound_ops",
                title="Compound Assignment Operators",
                description="Demonstration of +=, -=, *=, /= operators",
                category=ProgramCategory.ADVANCED,
                difficulty=2,
                code='''int main() {
    int x = 10;
    printf("Initial x: %d\\n", x);
    
    x += 5;
    printf("x += 5: %d\\n", x);
    
    x *= 2;
    printf("x *= 2: %d\\n", x);
    
    x /= 3;
    printf("x /= 3: %d\\n", x);
    
    x -= 2;
    printf("x -= 2: %d\\n", x);
    
    return 0;
}''',
                expected_output="Initial x: 10\nx += 5: 15\nx *= 2: 30\nx /= 3: 10\nx -= 2: 8\n"
            ),
            
            SampleProgram(
                id="advanced_complex_logic",
                title="Complex Logical Operations",
                description="Complex conditional expressions and character analysis",
                category=ProgramCategory.ADVANCED,
                difficulty=3,
                code='''int main() {
    char c = 'E';
    
    printf("Analyzing character: '%c'\\n", c);
    
    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
        printf("'%c' is a letter\\n", c);
        
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' ||
            c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U') {
            printf("'%c' is a vowel\\n", c);
        } else {
            printf("'%c' is a consonant\\n", c);
        }
    } else {
        printf("'%c' is not a letter\\n", c);
    }
    
    return 0;
}''',
                expected_output="Analyzing character: 'E'\n'E' is a letter\n'E' is a vowel\n"
            ),
        ])
    
    def get_all_programs(self) -> List[SampleProgram]:
        """Get all sample programs"""
        return self.programs
    
    def get_programs_by_category(self, category: ProgramCategory) -> List[SampleProgram]:
        """Get programs filtered by category"""
        return [p for p in self.programs if p.category == category]
    
    def get_programs_by_difficulty(self, difficulty: int) -> List[SampleProgram]:
        """Get programs filtered by difficulty level"""
        return [p for p in self.programs if p.difficulty == difficulty]
    
    def get_program_by_id(self, program_id: str) -> Optional[SampleProgram]:
        """Get a specific program by ID"""
        for program in self.programs:
            if program.id == program_id:
                return program
        return None
    
    def get_categories(self) -> List[ProgramCategory]:
        """Get all available categories"""
        return list(set(p.category for p in self.programs))
    
    def get_difficulty_levels(self) -> List[int]:
        """Get all available difficulty levels"""
        return sorted(list(set(p.difficulty for p in self.programs)))
    
    def search_programs(self, keyword: str) -> List[SampleProgram]:
        """Search programs by keyword in title or description"""
        keyword = keyword.lower()
        return [p for p in self.programs 
                if keyword in p.title.lower() or keyword in p.description.lower()]
    
    def get_program_count(self) -> int:
        """Get total number of programs"""
        return len(self.programs)
    
    def get_program_count_by_category(self) -> Dict[ProgramCategory, int]:
        """Get program count grouped by category"""
        count_dict = {}
        for category in self.get_categories():
            count_dict[category] = len(self.get_programs_by_category(category))
        return count_dict

# For backward compatibility with existing code
sample_programs = []

def initialize_sample_programs():
    """Initialize the legacy sample_programs list for backward compatibility"""
    global sample_programs
    manager = SampleProgramManager()
    sample_programs = [program.code for program in manager.get_all_programs()]

# Initialize on import
initialize_sample_programs()