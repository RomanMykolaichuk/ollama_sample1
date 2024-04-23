import os
import subprocess
import yaml

# Функція для ініціалізації ollama проекту
def init_ollama_project(project_name):
    # Створення проекту за допомогою ollama
    subprocess.run(['ollama', 'init', project_name], check=True)
    # Зміна директорії на створений проект
    os.chdir(project_name)
    print(f"Проект {project_name} успішно створено і перейшли в каталог {project_name}")

# Функція для конфігурації налаштувань
def configure_project_settings(config_file, settings):
    # Завантаження конфігураційного файлу
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    
    # Оновлення конфігураційних параметрів
    config.update(settings)
    
    # Запис змінених налаштувань у файл
    with open(config_file, 'w') as file:
        yaml.safe_dump(config, file, default_flow_style=False)
    
    print(f"Налаштування для {config_file} оновлено")

# Назва проекту
project_name = 'sample1'
# Файл конфігурації
config_file = 'config.yaml'
# Нові налаштування, які потрібно застосувати
new_settings = {
    'project_name': 'Sample Project',
    'project_description': 'Sample Project Description',
    'project_author': 'Roman Mykolaichuk',
    'project_author_email': '',
    'project_version': '0.1.0',    
    'project_license': 'MIT',
}

# Ініціалізація проекту
init_ollama_project(project_name)
# Конфігурація налаштувань
configure_project_settings(config_file, new_settings)
