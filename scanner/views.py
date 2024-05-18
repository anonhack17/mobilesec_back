import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
import hashlib
import os
import json
from .list import list

def calculate_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def scan_directory(directory_path):
    known_signatures = set(list)
    exploits_found = []

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            print(file_name)
            file_path = os.path.join(root, file_name)
            file_hash = calculate_hash(file_path)
            if file_hash in known_signatures:
                exploits_found.append({"path": file_path, "hash": file_hash})
    return exploits_found

def remove_exploits(exploits):
    for exploit in exploits:
        exploit_file = exploit['path']
        if os.path.exists(exploit_file):
            os.remove(exploit_file)
            print(f"Файл {exploit_file} удален")
        else:
            print(f"Файл {exploit_file} не существует")

def scan_directory_view(request):
    try:
        directory_path = request.GET.get('directory_path')
        if directory_path:
            found_exploits = scan_directory(directory_path)
            return JsonResponse({"exploits": found_exploits})
        else:
            return JsonResponse({"error": "Путь к директории не предоставлен"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Ошибка сервера: {str(e)}"}, status=500)


import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def remove_exploits_view(request):
    if request.method == 'GET':
        # Получаем параметр exploits из строки запроса
        exploits_param = request.GET.get('exploits', '')

        # Разбираем JSON строку в словарь
        try:
            exploits_dict = json.loads(exploits_param)
            print(exploits_dict)
            exploits_list = exploits_dict.get('exploits', [])
            print(exploits_list)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        # Список для хранения удаленных эксплойтов
        removed_exploits = []

        # Перебираем каждый эксплойт из списка
        for exploit in exploits_list:
            exploit_file = exploit.get('path', '').strip()
            if os.path.exists(exploit_file):
                os.remove(exploit_file)
                removed_exploits.append(exploit_file)
                print(f"Файл {exploit_file} удален")
            else:
                print(f"Файл {exploit_file} не существует")

        # Возвращаем ответ с информацией о удаленных эксплойтах и списком эксплойтов
        return JsonResponse({'removed': removed_exploits, 'exploits': exploits_list}, status=200)

    # Если запрос не GET, возвращаем ошибку метода
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def scan_device_view(request):
    try:
        # Выполнение команды ADB для получения списка приложений
        adb_command = "adb shell pm list packages"
        result = subprocess.run(adb_command, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return JsonResponse({"error": "Failed to scan device"}, status=500)

        packages = result.stdout.splitlines()
        return JsonResponse({"packages": packages})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)