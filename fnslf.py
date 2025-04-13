#!/usr/bin/env python3
import os
import fnmatch
from datetime import datetime

# Определяем системные директории для исключения
SYSTEM_DIRS = {'/proc', '/sys', '/dev', '/run', '/tmp', '/snap', '/usr', '/var', '/.var', '/etc', '/root'}

def is_hidden(filepath):
    return os.path.basename(filepath).startswith('.') and not filepath.endswith(('/', '/.', '/..'))

def is_system_path(path):
    return any(path.startswith(sd) for sd in SYSTEM_DIRS)

def scan_hidden():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting recursive scan from / ...")
    
    for root, dirs, files in os.walk('/', followlinks=False):
        try:
            # Фильтруем системные директории
            dirs[:] = [d for d in dirs if not is_system_path(os.path.join(root, d))]
            
            # Объединяем файлы и директории
            entries = dirs + files
            
            for entry in entries:
                full_path = os.path.join(root, entry)
                
                # Пропускаем не скрытые файлы
                if not is_hidden(full_path):
                    continue
                
                # Выводим ВСЕ скрытые несистемные файлы
                if not is_system_path(full_path):
                    print(f"[Basic Scan] Hidden entry: {full_path}")
                
                # Проверка на флаги только в несистемных путях
                if is_system_path(full_path):
                    continue
                
                try:
                    # Поиск флагов в содержимом
                    if os.path.isfile(full_path):
                        with open(full_path, 'rb') as f:
                            content = f.read(4096).decode('utf-8', errors='ignore')
                            if 'flag{' in content:
                                print(f"\n[!] FLAG FOUND: {full_path}")
                                print(f"    Content snippet: {content[:100].strip()}\n")
                                
                    # Проверка подозрительных разрешений
                    st = os.stat(full_path)
                    if st.st_mode & 0o777 in {0o777, 0o666}:
                        print(f"[!] Strange permissions {oct(st.st_mode)[-3:]} on: {full_path}")
                        
                except UnicodeDecodeError:
                    continue
                except PermissionError:
                    print(f"[x] Access denied: {full_path}")
                except Exception as e:
                    print(f"[x] Error checking {full_path}: {str(e)}")
                    
        except Exception as e:
            print(f"[x] Directory error: {str(e)}")
            continue

if __name__ == "__main__":
    try:
        scan_hidden()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    finally:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Scan completed")