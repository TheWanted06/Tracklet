import os
import shutil

def remove_path(path):
    if os.path.isdir(path):
        print(f"Removing directory: {path}")
        shutil.rmtree(path)
    elif os.path.isfile(path):
        print(f"Removing file: {path}")
        os.remove(path)

def clean_project(root_dir="."):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Remove __pycache__ folders
        if "__pycache__" in dirnames:
            remove_path(os.path.join(dirpath, "__pycache__"))
            dirnames.remove("__pycache__")

        # Remove *.egg-info folders
        egginfo_dirs = [d for d in dirnames if d.endswith(".egg-info")]
        for d in egginfo_dirs:
            remove_path(os.path.join(dirpath, d))
            dirnames.remove(d)

        # Remove build and dist folders
        for folder in ["build", "dist", ".tox", ".cache", "htmlcov", ".ipynb_checkpoints"]:
            if folder in dirnames:
                remove_path(os.path.join(dirpath, folder))
                dirnames.remove(folder)

        # Remove byte-compiled files
        for filename in filenames:
            if filename.endswith((".pyc", ".pyo")) or filename.endswith(".log"):
                remove_path(os.path.join(dirpath, filename))

        # Remove coverage files
        coverage_files = [".coverage", ".coverage.*", "coverage.xml", "nosetests.xml"]
        for cov_file in coverage_files:
            cov_path = os.path.join(dirpath, cov_file)
            if os.path.exists(cov_path):
                remove_path(cov_path)

if __name__ == "__main__":
    clean_project()

