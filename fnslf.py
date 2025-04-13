import os
import fnmatch
from datetime import datetime

def is_hidden(filepath):
    filename = os.path.basename(filepath)
    return filename.startswith('.') and filename not in ('.', '..')

def scan_system_hidden(start_path='/', keywords=['flag{', 'CTF']):
    dir_count = 0
    file_count = 0
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Начало сканирования...")
    
    for root, dirs, files in os.walk(start_path, followlinks=False, onerror=lambda e: None):
        dir_count += 1
        all_entries = dirs + files
        
        # Прогресс каждые 100 директорий
        if dir_count % 100 == 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Обработано директорий: {dir_count} | Файлов: {file_count} | Текущая: {root}")
        
        for entry in all_entries:
            file_count += 1
            full_path = os.path.join(root, entry)
            
            if not is_hidden(full_path):
                continue
                
            try:
                # Вывод для отладки подозрительных файлов
                debug_msg = []
                
                # Проверка имени
                suspicious_name = any(fnmatch.fnmatch(entry, p) for p in ['*.flag*', '*secret*'])
                if suspicious_name:
                    debug_msg.append("СОВПАДЕНИЕ ИМЕНИ")
                
                # Проверка содержимого
                content_match = False
                if os.path.isfile(full_path):
                    with open(full_path, 'r', errors='ignore') as f:
                        content = f.read(4096)
                        content_match = any(kw in content for kw in keywords)
                        if content_match:
                            debug_msg.append("СОВПАДЕНИЕ КОНТЕНТА")
                
                # Проверка прав
                strange_perms = os.stat(full_path).st_mode & 0o777 in {0o777, 0o666}
                if strange_perms:
                    debug_msg.append(f"ПОДОЗРИТЕЛЬНЫЕ ПРАВА {oct(os.stat(full_path).st_mode)[-3:]}")
                
                # Если найдены критерии
                if debug_msg:
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Обнаружено: {full_path}")
                    print(f"    Причины: {' | '.join(debug_msg)}")
                
            except PermissionError as pe:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Ошибка доступа: {full_path} ({str(pe)})")
                continue
            except Exception as e:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Критическая ошибка в {full_path}: {str(e)}")
                continue

if __name__ == "__main__":
    scan_system_hidden()
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Сканирование завершено")