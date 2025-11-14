#!/usr/bin/env python3
"""
Менеджер конфигурации для инструмента визуализации зависимостей
Этап 1: Минимальный прототип с конфигурацией
"""

import csv
import os
import sys
from dataclasses import dataclass


@dataclass
class Config:
    """Класс для хранения конфигурационных параметров"""
    package_name: str = ""
    repository_url: str = ""
    use_test_repository: bool = False
    package_version: str = ""
    output_filename: str = "dependencies.png"
    max_depth: int = 1
    filter_substring: str = ""

    def validate(self):
        """Валидация конфигурационных параметров"""
        errors = []
        
        if not self.package_name:
            errors.append("Имя пакета не может быть пустым")
        
        if not self.repository_url:
            errors.append("URL репозитория не может быть пустым")
        elif not (self.repository_url.startswith('http://') or 
                 self.repository_url.startswith('https://')):
            errors.append("URL репозитория должен начинаться с http:// или https://")
        
        try:
            self.max_depth = int(self.max_depth)
            if self.max_depth < 1 or self.max_depth > 10:
                errors.append("Максимальная глубина должна быть от 1 до 10")
        except ValueError:
            errors.append("Максимальная глубина должна быть целым числом")
        
        if not self.output_filename.endswith('.png'):
            errors.append("Имя выходного файла должно иметь расширение .png")
        
        if errors:
            raise ValueError("Ошибки конфигурации:\n- " + "\n- ".join(errors))


class ConfigManager:
    """Менеджер для работы с конфигурационными файлами"""
    
    @staticmethod
    def load_config(filename="config.csv"):
        """
        Загрузка конфигурации из CSV файла
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Конфигурационный файл '{filename}' не найден")
        
        config = Config()
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    parameter = row['parameter'].strip()
                    value = row['value'].strip()
                    
                    if parameter == 'package_name':
                        config.package_name = value
                    elif parameter == 'repository_url':
                        config.repository_url = value
                    elif parameter == 'use_test_repository':
                        config.use_test_repository = value.lower() == 'true'
                    elif parameter == 'package_version':
                        config.package_version = value
                    elif parameter == 'output_filename':
                        config.output_filename = value
                    elif parameter == 'max_depth':
                        config.max_depth = value
                    elif parameter == 'filter_substring':
                        config.filter_substring = value
        
        except Exception as e:
            raise ValueError(f"Ошибка чтения конфигурационного файла: {e}")
        
        return config
    
    @staticmethod
    def create_default_config(filename="config.csv"):
        """Создание конфигурационного файла по умолчанию"""
        default_config = [
            ['parameter', 'value'],
            ['package_name', 'serde'],
            ['repository_url', 'https://github.com/serde-rs/serde'],
            ['use_test_repository', 'false'],
            ['package_version', '1.0.200'],
            ['output_filename', 'dependencies_graph.png'],
            ['max_depth', '2'],
            ['filter_substring', '']
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(default_config)
        
        print(f"Создан конфигурационный файл по умолчанию: {filename}")


def print_config(config):
    """Вывод конфигурационных параметров в формате ключ-значение"""
    print("=" * 50)
    print("НАСТРОЙКИ ПОЛЬЗОВАТЕЛЯ")
    print("=" * 50)
    print(f"Имя анализируемого пакета: {config.package_name}")
    print(f"URL-адрес репозитория: {config.repository_url}")
    print(f"Режим работы с тестовым репозиторием: {config.use_test_repository}")
    print(f"Версия пакета: {config.package_version}")
    print(f"Имя сгенерированного файла: {config.output_filename}")
    print(f"Максимальная глубина анализа: {config.max_depth}")
    print(f"Подстрока для фильтрации: '{config.filter_substring}'")
    print("=" * 50)


def main_stage_1():
    """Основная функция этапа 1"""
    print("Инструмент визуализации графа зависимостей - Этап 1")
    print("Минимальный прототип с конфигурацией\n")
    
    if not os.path.exists("config.csv"):
        print("Конфигурационный файл не найден. Создаю файл по умолчанию...")
        ConfigManager.create_default_config()
    
    try:
        config = ConfigManager.load_config()
        config.validate()
        print_config(config)
        print("\n✅ Конфигурация успешно загружена и проверена!")
        print("Этап 1 завершен успешно.")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main_stage_1()