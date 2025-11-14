#!/usr/bin/env python3
"""Тестирование обработки ошибок конфигурации"""

import csv
import os
from main import ConfigManager, Config


def test_error_cases():
    """Тестирование различных ошибочных сценариев"""
    
    test_cases = [
        {
            'name': 'Некорректный URL',
            'data': [
                ['parameter', 'value'],
                ['package_name', 'test'],
                ['repository_url', 'invalid_url'],
                ['use_test_repository', 'false'],
                ['package_version', '1.0.0'],
                ['output_filename', 'test.png'],
                ['max_depth', '2'],
                ['filter_substring', '']
            ],
            'expected_error': 'URL репозитория должен начинаться с http:// или https://'
        },
        {
            'name': 'Некорректная глубина',
            'data': [
                ['parameter', 'value'],
                ['package_name', 'test'],
                ['repository_url', 'https://github.com/test/test'],
                ['use_test_repository', 'false'],
                ['package_version', '1.0.0'],
                ['output_filename', 'test.png'],
                ['max_depth', 'invalid'],
                ['filter_substring', '']
            ],
            'expected_error': 'Максимальная глубина должна быть целым числом'
        },
        {
            'name': 'Пустое имя пакета',
            'data': [
                ['parameter', 'value'],
                ['package_name', ''],
                ['repository_url', 'https://github.com/test/test'],
                ['use_test_repository', 'false'],
                ['package_version', '1.0.0'],
                ['output_filename', 'test.png'],
                ['max_depth', '2'],
                ['filter_substring', '']
            ],
            'expected_error': 'Имя пакета не может быть пустым'
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        filename = f"test_config_{i}.csv"
        
        # Создание тестового конфигурационного файла
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(test_case['data'])
        
        try:
            config = ConfigManager.load_config(filename)
            config.validate()
            print(f"Тест '{test_case['name']}': Ожидалась ошибка, но валидация прошла успешно")
        except ValueError as e:
            if test_case['expected_error'] in str(e):
                print(f"Тест '{test_case['name']}': Ошибка обработана корректно")
            else:
                print(f"Тест '{test_case['name']}': Неожиданное сообщение об ошибке: {e}")
        except Exception as e:
            print(f"Тест '{test_case['name']}': Неожиданная ошибка: {e}")
        finally:
            # Удаление тестового файла
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == "__main__":
    print("Тестирование обработки ошибок конфигурации\n")
    test_error_cases()
