from ouroboros import run_code, Logger
from sample_programs import SampleProgramManager, ProgramCategory

def load_c_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        Logger.error(f"File '{filename}' not found")
        return ""
    except Exception as e:
        Logger.error(f"File reading error: {e}")
        return ""

def show_sample_programs(manager: SampleProgramManager):
    """Display all available sample programs with enhanced information"""
    Logger.header("📝 Available Sample Programs")
    
    programs = manager.get_all_programs()
    for i, program in enumerate(programs, 1):
        difficulty_stars = "⭐" * program.difficulty
        category_emoji = {
            ProgramCategory.BASIC: "🔤",
            ProgramCategory.CONTROL_FLOW: "🔄",
            ProgramCategory.FUNCTIONS: "⚙️",
            ProgramCategory.ARRAYS: "📊",
            ProgramCategory.STRINGS: "📝",
            ProgramCategory.MEMORY: "🧠",
            ProgramCategory.ALGORITHMS: "🧮",
            ProgramCategory.ADVANCED: "🚀"
        }.get(program.category, "📋")
        
        Logger.print(f"{i:2d}. {category_emoji} {program.title}")
        Logger.print(f"     {difficulty_stars} | {program.category.value} | {program.description}")

def run_selected_program(manager: SampleProgramManager, program_index: int):
    """Execute the program at the specified index"""
    programs = manager.get_all_programs()
    
    if 1 <= program_index <= len(programs):
        program = programs[program_index - 1]
        
        Logger.section_start(f"{program.title} Execution")
        Logger.print(f"📋 Category: {program.category.value}")
        Logger.print(f"⭐ Difficulty: {'⭐' * program.difficulty}")
        Logger.print(f"📄 Description: {program.description}")
        
        if program.notes:
            Logger.print(f"📝 Notes: {program.notes}")
        
        Logger.divider("📄 Source Code:")
        Logger.print(program.code)
        Logger.divider()
        
        Logger.divider("🚀 Execution Result:")
        try:
            results = run_code(program.code)
            if results:
                Logger.info(f"Program exit code: {results[-1]}")
        except Exception as e:
            Logger.error(f"Execution error: {e}")
        Logger.divider()
        
        if program.expected_output:
            Logger.divider("📋 Expected Output:")
            Logger.print(program.expected_output.replace('\\n', '\n'))
            Logger.divider()
        
        Logger.section_end(f"{program.title} Completed")
    else:
        Logger.error("Invalid program number")

def run_all_programs(manager: SampleProgramManager):
    """Execute all sample programs sequentially"""
    programs = manager.get_all_programs()
    Logger.header(f"🔄 Execute All Sample Programs ({len(programs)} total)")
    
    for i, program in enumerate(programs, 1):
        Logger.section_start(f"{i}/{len(programs)}: {program.title}")
        Logger.print(f"📋 {program.category.value} | ⭐{'⭐' * (program.difficulty-1)}")
        Logger.print("📄 Source Code:")
        Logger.print(program.code)
        Logger.marker()
        
        Logger.print("🚀 Execution Result:")
        try:
            results = run_code(program.code)
            if results:
                Logger.info(f"Exit code: {results[-1]}")
        except Exception as e:
            Logger.error(f"Execution error: {e}")
        
        Logger.section_end(f"{program.title} Completed")
        
        # Confirm before proceeding to next program
        if i < len(programs):
            input("\nPress Enter to continue to the next program...")

def interactive_mode():
    """Execute C code in interactive mode"""
    Logger.header("💻 Interactive Mode")
    Logger.print("Enter C language code")
    Logger.print("For multi-line input, end input with an empty line")
    Logger.print("Type 'exit' to quit interactive mode")
    
    while True:
        try:
            Logger.print("\nouroboros> ", end="")
            lines = []
            
            while True:
                line = input()
                if line.strip().lower() == 'exit':
                    return
                if not line.strip() and lines:  # Empty line ends input
                    break
                lines.append(line)
            
            if lines:
                code = '\n'.join(lines)
                Logger.divider("🚀 Execution Result:")
                try:
                    results = run_code(code)
                    if results:
                        Logger.info(f"Result: {results[-1]}")
                except Exception as e:
                    Logger.error(f"Execution error: {e}")
                Logger.divider()
                    
        except KeyboardInterrupt:
            Logger.info("\nExiting interactive mode")
            break
        except Exception as e:
            Logger.error(f"Error: {e}")

def load_and_run_file():
    """Load and execute a file"""
    Logger.header("📁 File Execution Mode")
    filename = input("Enter C file name to execute: ").strip()
    
    if not filename:
        Logger.error("No filename entered")
        return
    
    code = load_c_file(filename)
    if code:
        Logger.print(f"📄 File '{filename}' loaded")
        Logger.divider("Source Code:")
        Logger.print(code)
        Logger.divider()
        
        Logger.divider("🚀 Execution Result:")
        try:
            results = run_code(code)
            if results:
                Logger.info(f"Program exit code: {results[-1]}")
        except Exception as e:
            Logger.error(f"Execution error: {e}")
        Logger.divider()

def show_program_details(manager: SampleProgramManager, program_index: int):
    """Display details of the specified program"""
    programs = manager.get_all_programs()
    
    if 1 <= program_index <= len(programs):
        program = programs[program_index - 1]
        
        Logger.header(f"📋 {program.title} - Details")
        Logger.print(f"🆔 ID: {program.id}")
        Logger.print(f"📂 Category: {program.category.value}")
        Logger.print(f"⭐ Difficulty: {'⭐' * program.difficulty} ({program.difficulty}/5)")
        Logger.print(f"📝 Description: {program.description}")
        
        if program.notes:
            Logger.print(f"📄 Notes: {program.notes}")
        
        Logger.divider("Source Code:")
        Logger.print(program.code)
        Logger.divider()
        
        if program.expected_output:
            Logger.divider("📋 Expected Output:")
            Logger.print(program.expected_output.replace('\\n', '\n'))
            Logger.divider()
        
        # Display code statistics
        lines = program.code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        Logger.print(f"\n📊 Code Statistics:")
        Logger.print(f"   Total lines: {len(lines)}")
        Logger.print(f"   Non-empty lines: {len(non_empty_lines)}")
        Logger.print(f"   Characters: {len(program.code)}")
        
        input("\nPress Enter to return...")
    else:
        Logger.error("Invalid program number")

def main():
    # Initialize the sample program manager
    manager = SampleProgramManager()
    Logger.title()
    
    while True:
        Logger.print(f"📚 {manager.get_program_count()} Sample Programs Available")
        Logger.print("")
        Logger.print("1. Execute All Sample Programs")
        Logger.print("2. Execute Specific Sample Program")
        Logger.print("3. Execute C file")
        Logger.print("4. Execute in Interactive Mode")
        Logger.print("5. Exit")
        
        choice = input("\nPlease select (1-5): ").strip()
        
        if choice == "1":
            confirm = input("Execute all sample programs? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                run_all_programs(manager)
                input("\nPress Enter to return...")
            else:
                Logger.info("Cancelled")

        elif choice == "2":
            show_sample_programs(manager)
            try:
                program_num = int(input(f"\nSelect program number to execute (1-{manager.get_program_count()}): "))
                run_selected_program(manager, program_num)
                input("\nPress Enter to return...")
            except ValueError:
                Logger.error("Invalid number")
                input("\nPress Enter to return...")

        elif choice == "3":
            load_and_run_file()    

        elif choice == "4":
            interactive_mode()
            
        elif choice == "5":
            Logger.info("Exiting Ouroboros...")
            break
            
        else:
            Logger.error("Invalid selection (please enter a number 1-5)")
            input("\nPress Enter to return...")

if __name__ == "__main__":
    main()