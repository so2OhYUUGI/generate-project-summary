# Generate Project Summary 
このPythonスクリプトは、プロジェクトのフォルダ構造を走査し、ファイルとその内容のMarkdown表現を作成することでプロジェクトのサマリーを生成します。プロジェクトの構造とファイルの内容を1つのMarkdownファイルにまとめて文書化するのに便利な方法を提供します。

## 特徴
- プロジェクトのフォルダ構造のMarkdownサマリーを生成します。
- 各ファイルの内容をサマリーに含めます。
- `.gitignore`と`.summaryignore`ファイルを使用して、特定のファイルとフォルダを除外できます。
- UTF-8とShift-JISのエンコーディングを試すことで、ファイルのエンコーディングの問題を処理します。
- 生成されたサマリーを`<project_name>_project_summary.txt`という名前のファイルに保存します。
- ローカルディレクトリまたはZIPファイルからプロジェクトサマリーを生成できます。
- ZIPファイルを選択して自動的に展開し、サマリー生成後にクリーンアップします。

## 使用方法
1. リポジトリをクローンするか、`generate_project_summary.py`スクリプトをダウンロードします。
2. ターミナルまたはコマンドプロンプトを開き、スクリプトを含むディレクトリに移動します。
3. `python generate_project_summary.py`コマンドを使用してスクリプトを実行します。
4. ローカルディレクトリを使用するか、ZIPファイルを使用するかを選択します。
   - ローカルディレクトリを選択した場合：プロジェクトディレクトリのパスを入力します。パスが指定されない場合、現在のディレクトリがデフォルトとして使用されます。
   - ZIPファイルを選択した場合：`zip_files`フォルダ内の利用可能なZIPファイルのリストから選択します。
5. スクリプトはプロジェクトのサマリーを生成し、`summaries`フォルダ内に`<project_name>_project_summary.txt`という名前のファイルに保存します。

## ZIPファイルの使用
1. スクリプトと同じディレクトリに`zip_files`フォルダを作成します。
2. 分析したいプロジェクトのZIPファイルを`zip_files`フォルダに配置します。
3. スクリプトを実行し、ZIPファイルオプションを選択します。
4. 利用可能なZIPファイルのリストから目的のファイルを選択します。
5. スクリプトは自動的にZIPファイルを展開し、サマリーを生成し、作業が完了したら一時ファイルをクリーンアップします。

## ファイルとフォルダの除外
プロジェクトのルートディレクトリに`.gitignore`と`.summaryignore`ファイルを作成することで、プロジェクトのサマリーから特定のファイルとフォルダを除外できます。これらのファイルには、除外したいパターンやファイル/フォルダ名を1行に1つずつ記述します。

- `.gitignore`ファイルは、Gitなどのバージョンコントロールシステムからファイルとフォルダを除外するためによく使用されます。
- `.summaryignore`ファイルはこのスクリプト専用で、プロジェクトのサマリーから追加のファイルとフォルダを除外できます。

## 依存関係
このスクリプトは外部の依存関係を必要としません。Pythonの組み込みの`os`、`fnmatch`、`zipfile`、`shutil`モジュールを使用します。

## 貢献
貢献は大歓迎です！問題を見つけたり、改善のための提案がある場合は、GitHubリポジトリでissueを開いたり、プルリクエストを送信してください。

## ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。

---

This Python script generates a project summary by walking through the project's folder structure and creating a Markdown representation of the files and their contents. It provides a convenient way to document your project's structure and file contents in a single Markdown file.

## Features
- Generates a Markdown summary of the project's folder structure.
- Includes the contents of each file in the summary.
- Supports excluding specific files and folders using `.gitignore` and `.summaryignore` files.
- Handles encoding issues by attempting to decode files using UTF-8 and Shift-JIS encodings.
- Saves the generated summary to a file named `<project_name>_project_summary.txt`.
- Can generate project summaries from either local directories or ZIP files.
- Automatically extracts selected ZIP files and cleans up after summary generation.

## Usage
1. Clone the repository or download the `generate_project_summary.py` script.
2. Open a terminal or command prompt and navigate to the directory containing the script.
3. Run the script using the command: `python generate_project_summary.py`.
4. Choose whether to use a local directory or a ZIP file.
   - If using a local directory: Enter the path to your project directory when prompted. If no path is provided, the current directory will be used as the default.
   - If using a ZIP file: Select from a list of available ZIP files in the `zip_files` folder.
5. The script will generate a project summary and save it to a file named `<project_name>_project_summary.txt` in the `summaries` folder.

## Using ZIP Files
1. Create a `zip_files` folder in the same directory as the script.
2. Place ZIP files of the projects you want to analyze in the `zip_files` folder.
3. Run the script and choose the ZIP file option.
4. Select the desired file from the list of available ZIP files.
5. The script will automatically extract the ZIP file, generate the summary, and clean up temporary files when finished.

## Ignoring Files and Folders
You can exclude specific files and folders from the project summary by creating `.gitignore` and `.summaryignore` files in your project's root directory. These files should contain patterns or file/folder names that you want to exclude, one per line.

- The `.gitignore` file is commonly used to exclude files and folders from version control systems like Git.
- The `.summaryignore` file is specific to this script and allows you to exclude additional files and folders from the project summary.

## Dependencies
This script does not require any external dependencies. It uses Python's built-in `os`, `fnmatch`, `zipfile`, and `shutil` modules.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License
This project is licensed under the MIT License.