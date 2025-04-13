# finder non system linux folders
import os

# Массив системных файлов и директорий, которые нужно игнорировать
SYSTEM_ITEMS = {
    '.bashrc', '.bash_profile', '.bash_logout', '.bash_history',
    '.profile', '.gitignore', '.gitmodules', '.gitkeep',
    '.svn', '.hg', '.bzr', '.DS_Store', '.localized',
    '.npmignore', '.dockerignore', '.env', '.venv',
    '.viminfo', '.vimrc', '.editorconfig', '.tmux.conf',
    '.zshrc', '.zshenv', '.zprofile', '.zlogin', '.zlogout',
    '.ssh', '.gnupg', '.pki', '.cache', '.config',
    '.local', '.mozilla', '.thunderbird', '.kde', '.gnome',
    '.gnome2', '.gconf', '.gconfd', '.kde4', '.kde5',
    '.swp', '.swo', '.swn', '.un~', '.netrwhist',
    # Системные директории
    '/proc', '/sys', '/dev', '/run', '/tmp',
    '/var', '/etc', '/usr', '/lib', '/lib64',
    '/bin', '/sbin', '/boot', '/root', '/home'
}

def is_system_path(path):
    # Проверяем, является ли путь системным
    path_parts = path.split(os.sep)
    for part in path_parts:
        if part in SYSTEM_ITEMS:
            return True
    return False

def scan_system(start_path='/'):
    hidden_non_system = []
    for root, dirs, files in os.walk(start_path):
        # Пропускаем системные директории
        if is_system_path(root):
            continue
        
        # Проверяем все элементы в директории
        for item in files + dirs:
            if item.startswith('.'):
                full_path = os.path.join(root, item)
                if not is_system_path(full_path):
                    hidden_non_system.append(full_path)
    
    return hidden_non_system

if __name__ == "__main__":
    print("Поиск скрытых несистемных файлов по всей системе...")
    try:
        hidden_files = scan_system()
        if hidden_files:
            print("Найдены скрытые несистемные файлы:")
            for file in hidden_files:
                print(file)
        else:
            print("Скрытых несистемных файлов не найдено.")
    except PermissionError:
        print("Ошибка: Нет прав доступа к некоторым директориям.")
    except KeyboardInterrupt:
        print("\nСканирование прервано пользователем.")
