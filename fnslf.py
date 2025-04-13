# # finder non system linux folders
# import os

# # Массив системных файлов и директорий, которые нужно игнорировать
# SYSTEM_ITEMS = {
#     '.bashrc', '.bash_profile', '.bash_logout', '.bash_history',
#     '.profile', '.gitignore', '.gitmodules', '.gitkeep',
#     '.svn', '.hg', '.bzr', '.DS_Store', '.localized',
#     '.npmignore', '.dockerignore', '.env', '.venv',
#     '.viminfo', '.vimrc', '.editorconfig', '.tmux.conf',
#     '.zshrc', '.zshenv', '.zprofile', '.zlogin', '.zlogout',
#     '.ssh', '.gnupg', '.pki', '.cache', '.config',
#     '.local', '.mozilla', '.thunderbird', '.kde', '.gnome',
#     '.gnome2', '.gconf', '.gconfd', '.kde4', '.kde5',
#     '.swp', '.swo', '.swn', '.un~', '.netrwhist',
#     # Системные директории
#     '/proc', '/sys', '/dev', '/run', '/tmp',
#     '/var', '/etc', '/usr', '/lib', '/lib64',
#     '/bin', '/sbin', '/boot'
# }

# def is_system_path(path):
#     # Проверяем, является ли путь системным
#     path_parts = path.split(os.sep)
#     for part in path_parts:
#         if part in SYSTEM_ITEMS:
#             return True
#     return False

# def scan_system(start_path='/'):
#     hidden_non_system = []
#     for root, dirs, files in os.walk(start_path):
#         # Пропускаем системные директории
#         if is_system_path(root):
#             continue
        
#         # Проверяем все элементы в директории
#         for item in files + dirs:
#             if item.startswith('.'):
#                 full_path = os.path.join(root, item)
#                 if not is_system_path(full_path):
#                     hidden_non_system.append(full_path)
    
#     return hidden_non_system

# if __name__ == "__main__":
#     print("Поиск скрытых несистемных файлов по всей системе...")
#     try:
#         hidden_files = scan_system()
#         if hidden_files:
#             print("Найдены скрытые несистемные файлы:")
#             for file in hidden_files:
#                 print(file)
#         else:
#             print("Скрытых несистемных файлов не найдено.")
#     except PermissionError:
#         print("Ошибка: Нет прав доступа к некоторым директориям.")
#     except KeyboardInterrupt:
#         print("\nСканирование прервано пользователем.")
import os
import fnmatch

def is_hidden(filepath):
    filename = os.path.basename(filepath)
    return filename.startswith('.') and filename not in ('.', '..')

def scan_system_hidden(start_path='/', keywords=['flag{', 'CTF']):
    for root, dirs, files in os.walk(start_path, followlinks=False, onerror=lambda e: None):
        all_entries = dirs + files
        for entry in all_entries:
            full_path = os.path.join(root, entry)
            
            # Проверка на скрытый файл/папку
            if not is_hidden(full_path):
                continue
                
            try:
                # Проверка подозрительных имен
                suspicious_name = any(
                    fnmatch.fnmatch(entry, pattern) 
                    for pattern in ['*.flag*', '*secret*', '*.pass*']
                )
                
                # Проверка содержимого файлов
                content_match = False
                if os.path.isfile(full_path):
                    with open(full_path, 'r', errors='ignore') as f:
                        content = f.read(4096)  # Читаем первые 4KB
                        content_match = any(kw in content for kw in keywords)
                
                # Проверка прав доступа (например, world-writable)
                strange_perms = (
                    os.stat(full_path).st_mode & 0o777 in {0o777, 0o666}
                )
                
                if any([suspicious_name, content_match, strange_perms]):
                    print(f"[!] Найдено: {full_path}")
                    print(f"    Тип: {'Файл' if os.path.isfile(full_path) else 'Папка'}")
                    if content_match:
                        print("    Содержит ключевые слова")
                    if strange_perms:
                        print(f"    Подозрительные права: {oct(os.stat(full_path).st_mode)[-3:]}")

            except PermissionError:
                continue
            except Exception as e:
                print(f"Ошибка при обработке {full_path}: {str(e)}")
                continue

if __name__ == "__main__":
    print("Начинаем сканирование...")
    scan_system_hidden()
    print("Сканирование завершено.")