import ast
import pkg_resources
import os

def extract_imports_from_file(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)

    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module.split('.')[0])

    return imports

def get_installed_packages():
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    return installed_packages

def generate_requirements(imports):
    installed_packages = get_installed_packages()
    requirements = [pkg for pkg in imports if pkg.lower() in installed_packages]
    
    # Handle known package mappings (customize this as needed)
    package_mappings = {
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'sklearn': 'scikit-learn',
    }

    for i, pkg in enumerate(requirements):
        if pkg in package_mappings:
            requirements[i] = package_mappings[pkg]

    return requirements

def write_requirements_file(requirements, output_path='requirements.txt'):
    with open(output_path, 'w') as file:
        for pkg in requirements:
            file.write(pkg + '\n')

if __name__ == '__main__':
    # Replace 'your_script.py' with the path to your Python file
    python_file_path = r'backend\app.py'
    if not os.path.isfile(python_file_path):
        print(f"File {python_file_path} does not exist.")
        exit(1)

    imports = extract_imports_from_file(python_file_path)
    requirements = generate_requirements(imports)
    write_requirements_file(requirements)

    print(f"requirements.txt generated with {len(requirements)} packages.")
