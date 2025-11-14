#!/usr/bin/env python3
"""
Главный файл инструмента визуализации графа зависимостей
Объединяет все три этапа
"""

import sys
from config_manager import ConfigManager, print_config


def main():
    """Главная функция, объединяющая все три этапа"""
    print("=" * 70)
    print("ИНСТРУМЕНТ ВИЗУАЛИЗАЦИИ ГРАФА ЗАВИСИМОСТЕЙ CARGO ПАКЕТОВ")
    print("=" * 70)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        try:
            from visualizer import demonstrate_multiple_packages
            demonstrate_multiple_packages()
            return
        except ImportError as e:
            print(f"Ошибка импорта: {e}")
            return
    
    try:
        # Этап 1: Конфигурация
        print("\n🎯 ЭТАП 1: Конфигурация")
        print("-" * 40)
        
        config = ConfigManager.load_config()
        config.validate()
        print_config(config)
        
        # Этап 2: Сбор данных
        print("\n🎯 ЭТАП 2: Сбор данных о зависимостях")
        print("-" * 40)
        
        from data_collector import main_stage_2
        dependencies = main_stage_2()
        
        # Этап 3: Визуализация
        print("\n🎯 ЭТАП 3: Визуализация графа")
        print("-" * 40)
        
        from visualizer import main_stage_3
        main_stage_3()
        
        print("\n" + "=" * 70)
        print("✅ ВСЕ ЭТАПЫ ЗАВЕРШЕНЫ УСПЕШНО!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()