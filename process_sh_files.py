import os
from pathlib import Path
import subprocess
import sys

def find_sh_files(directory):
    """
    Recursively find all .sh files in the given directory and its subdirectories.

    :param directory: The root directory to start the search.
    :return: A list of Path objects representing .sh files.
    """
    p = Path(directory)
    sh_files = list(p.rglob('*.sh'))  # rglob searches recursively
    return sh_files

def add_shebang(file_path):
    """
    Add a shebang line to the .sh file if it doesn't already have one.

    :param file_path: Path object of the .sh file.
    :return: Boolean indicating whether a shebang was added.
    """
    shebang = "#!/bin/bash\n"
    try:
        with file_path.open('r', encoding='utf-8') as f:
            lines = f.readlines()

        if not lines:
            # Empty file, add shebang
            lines = [shebang]
            added = True
        elif lines[0].startswith('#!'):
            # Shebang already exists
            added = False
        else:
            # Insert shebang at the top
            lines.insert(0, shebang)
            added = True

        if added:
            with file_path.open('w', encoding='utf-8', newline='\n') as f:
                f.writelines(lines)
            print(f"Added shebang to: {file_path}")
        else:
            print(f"Shebang already exists in: {file_path}")

        return added

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def git_add_chmod(file_path):
    """
    Run the git command to add the file with executable permissions.

    :param file_path: Path object of the .sh file.
    :return: Boolean indicating whether the git command was successful.
    """
    try:
        # Construct the git add command
        # Using subprocess.run for better control and error handling
        result = subprocess.run(
            ['git', 'add', '--chmod=+x', str(file_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Ran git add --chmod=+x on: {file_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git command failed for {file_path}: {e.stderr.strip()}")
        return False
    except FileNotFoundError:
        print("Git is not installed or not found in PATH.")
        sys.exit(1)

def main():
    # Define the directory to search
    search_dir = r"C:\Users\Mark\Documents\GitHub\charts"  # <-- Replace this with your desired directory

    # Alternatively, set it relative to the script's location:
    # search_dir = Path(__file__).parent / "relative\\path\\to\\search"

    # Create a Path object
    p = Path(search_dir)

    # Check if the provided directory exists
    if not p.is_dir():
        print(f"Error: '{search_dir}' is not a valid directory.")
        sys.exit(1)

    # Find .sh files
    sh_files = find_sh_files(search_dir)

    # Check if any .sh files were found
    if not sh_files:
        print(f"No .sh files found in '{search_dir}'.")
        sys.exit(0)

    print(f"Found {len(sh_files)} .sh file(s) in '{search_dir}':\n")

    # Track the number of modifications
    shebang_added_count = 0
    git_add_success_count = 0

    for file in sh_files:
        print(f"Processing: {file.resolve()}")

        # Step 1: Add shebang if necessary
        if add_shebang(file):
            shebang_added_count += 1

        # Step 2: Run git add --chmod=+x
        if git_add_chmod(file):
            git_add_success_count += 1

    # Summary
    print("\nProcessing Complete.")
    print(f"Shebang added to {shebang_added_count} file(s).")
    print(f"Git add --chmod=+x succeeded for {git_add_success_count} file(s).")

    # Optionally, you can commit the changes automatically
    # Uncomment the following lines if you want to commit
    """
    commit_message = "Add shebang and set execute permissions for .sh files"
    try:
        subprocess.run(
            ['git', 'commit', '-m', commit_message],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Committed changes to Git repository.")
    except subprocess.CalledProcessError as e:
        print(f"Git commit failed: {e.stderr.strip()}")
    """

if __name__ == "__main__":
    main()
