import os
import fnmatch
import zipfile
import shutil
from pathlib import Path

def is_binary(file_path):
    with open(file_path, 'rb') as file:
        return b'\0' in file.read(1024)

def read_file_contents(file_path):
    encodings = ['utf-8', 'shift_jis']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                print(f'Reading file: {file_path}')
                return file.read()
        except UnicodeDecodeError:
            pass
    return ''

def is_ignored(path, project_dir, gitignore_patterns, summaryignore_patterns, additional_ignore_patterns):
    relative_path = os.path.relpath(path, project_dir)
    for pattern in gitignore_patterns + summaryignore_patterns + additional_ignore_patterns:
        pattern = f"*{pattern}*"
        if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(f'{os.sep}{relative_path}', pattern):
            return True
    return False

def generate_project_summary(project_dir, project_name):
    summary = f'# {project_name}\n\n## Directory Structure\n\n'

    gitignore_patterns = read_gitignore(project_dir)
    print(f"gitignore_patterns: {gitignore_patterns}")
    summaryignore_patterns = read_summaryignore(project_dir)
    print(f"summaryignore_patterns: {summaryignore_patterns}")
    additional_ignore_patterns = ['generate_project_summary.py','.summaryignore', f'{project_name}_project_summary.txt', '.git']

    file_contents_section = "\n## File Contents\n\n"

    def traverse_directory(root, level):
        nonlocal summary, file_contents_section
        indent = '  ' * level
        relative_path = os.path.relpath(root, project_dir)
        if not is_ignored(relative_path, project_dir, gitignore_patterns, summaryignore_patterns, additional_ignore_patterns):
            summary += f'{indent}- {os.path.basename(root)}/\n'

            subindent = '  ' * (level + 1)
            for item in os.listdir(root):
                item_path = os.path.join(root, item)
                if os.path.isdir(item_path):
                    if not is_ignored(item_path, project_dir, gitignore_patterns, summaryignore_patterns, additional_ignore_patterns):
                        traverse_directory(item_path, level + 1)
                else:
                    if not is_ignored(item_path, project_dir, gitignore_patterns, summaryignore_patterns, additional_ignore_patterns):
                        if not is_binary(item_path):
                            summary += f'{subindent}- {item}\n'
                            content = read_file_contents(item_path)
                            if content.strip():
                                relative_file_path = os.path.relpath(item_path, project_dir)
                                file_contents_section += f'### {relative_file_path}\n\n```\n{content}\n```\n\n'
                        else:
                            summary += f'{subindent}- {item} (binary file)\n'

    traverse_directory(project_dir, 0)

    # サマリーファイルを保存するサブフォルダを作成
    summaries_folder = os.path.join(os.path.dirname(__file__), 'summaries')
    os.makedirs(summaries_folder, exist_ok=True)

    # サマリーファイルをサブフォルダに保存
    summary_file_path = os.path.join(summaries_folder, f'{project_name}_project_summary.txt')
    with open(summary_file_path, 'w', encoding='utf-8') as file:
        file.write(summary + file_contents_section)

    print(f"Project summary has been saved to: {summary_file_path}")

def read_gitignore(project_dir):
    gitignore_path = os.path.join(project_dir, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as file:
            patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            expanded_patterns = []
            for pattern in patterns:
                expanded_patterns.append(pattern)
                if '/' in pattern:
                    expanded_patterns.append(pattern.replace('/', '\\'))
                if '\\' in pattern:
                    expanded_patterns.append(pattern.replace('\\', '/'))
            return expanded_patterns
    return []

def read_summaryignore(project_dir):
    summaryignore_patterns = []
    
    # プロジェクトディレクトリ内の .summaryignore を読み込む
    project_summaryignore = os.path.join(project_dir, '.summaryignore')
    if os.path.exists(project_summaryignore):
        summaryignore_patterns.extend(read_ignore_file(project_summaryignore))
    
    # スクリプトが存在するディレクトリ内の .summaryignore を読み込む
    script_dir_summaryignore = os.path.join(Path(__file__).parent, '.summaryignore')
    if os.path.exists(script_dir_summaryignore):
        summaryignore_patterns.extend(read_ignore_file(script_dir_summaryignore))
    
    return list(set(summaryignore_patterns))  # 重複を除去

def read_ignore_file(file_path):
    with open(file_path, 'r') as file:
        patterns = [line.strip() for line in file if line.strip() and not line.startswith('#')]
        expanded_patterns = []
        for pattern in patterns:
            expanded_patterns.append(pattern)
            if '/' in pattern:
                expanded_patterns.append(pattern.replace('/', '\\'))
            if '\\' in pattern:
                expanded_patterns.append(pattern.replace('\\', '/'))
        return expanded_patterns

def list_zip_files(folder):
    return [f for f in os.listdir(folder) if f.endswith('.zip')]

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def remove_folder(folder):
    shutil.rmtree(folder)

def main():
    history = []  # 履歴を保持するリスト
    history_file = 'history.txt'
    
    # 履歴ファイルが存在すれば、履歴を読み込む
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            history = [line.strip() for line in file]

    # 選択肢を表示
    choice = input("Choose an option:\n1. Use a directory or view past directories\n2. Use a ZIP file\nEnter your choice (1 or 2): ")

    if choice == '1':
        # フォルダパスの入力または履歴からの選択
        if history:
            print("Past directories:")
            for i, path in enumerate(history, 1):
                print(f"{i}. {path}")

        user_input = input('Enter the project directory path or select a number from history (leave blank for current directory): ')

        if user_input.isdigit():
            try:
                history_choice = int(user_input) - 1
                if history_choice < 0 or history_choice >= len(history):
                    print("Invalid choice.")
                    return
                project_directory = history[history_choice]
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                return
        else:
            project_directory = user_input.strip()
            if not project_directory:
                project_directory = os.getcwd()

            if not os.path.isdir(project_directory):
                print("Directory does not exist.")
                return

            # 履歴に追加し、履歴ファイルに保存
            if project_directory not in history:
                history.append(project_directory)
                with open(history_file, 'a') as file:
                    file.write(project_directory + '\n')

        project_name = os.path.basename(project_directory)
        generate_project_summary(project_directory, project_name)
        
    elif choice == '2':
        zip_folder = os.path.join(os.path.dirname(__file__), 'zip_files')
        os.makedirs(zip_folder, exist_ok=True)
        
        zip_files = list_zip_files(zip_folder)
        if not zip_files:
            print("No ZIP files found in the zip_files folder.")
            return

        print("Available ZIP files:")
        for i, file in enumerate(zip_files, 1):
            print(f"{i}. {file}")

        try:
            zip_choice = int(input("Enter the number of the ZIP file you want to use: ")) - 1
            if zip_choice < 0 or zip_choice >= len(zip_files):
                print("Invalid choice.")
                return

            selected_zip = os.path.join(zip_folder, zip_files[zip_choice])
            extract_folder = os.path.join(zip_folder, 'extracted')
            os.makedirs(extract_folder, exist_ok=True)

            extract_zip(selected_zip, extract_folder)

            # ZIPファイル名からプロジェクト名を取得
            project_name = os.path.splitext(zip_files[zip_choice])[0]
            generate_project_summary(extract_folder, project_name)
            remove_folder(extract_folder)

        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
