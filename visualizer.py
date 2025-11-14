#!/usr/bin/env python3
"""
Этап 3: Визуализация графа зависимостей
"""

import os


class SimpleVisualizer:
    """Упрощенный визуализатор графа зависимостей"""
    
    def generate_text_graph(self, package_name, dependencies, max_depth=1):
        """
        Генерация текстового представления графа
        """
        lines = []
        lines.append(f"Граф зависимостей для: {package_name}")
        lines.append("=" * 50)
        lines.append(f"📦 {package_name}")
        
        for dep in dependencies:
            optional_flag = " (опциональная)" if dep.is_optional else ""
            lines.append(f"    └── 📦 {dep.name} {dep.version}{optional_flag}")
        
        lines.append("=" * 50)
        lines.append(f"Всего зависимостей: {len(dependencies)}")
        
        return '\n'.join(lines)
    
    def save_graph(self, graph_text, filename):
        """
        Сохранение графа в текстовый файл
        """
        txt_filename = filename.replace('.png', '.txt')
        with open(txt_filename, 'w', encoding='utf-8') as file:
            file.write(graph_text)
        print(f"Текстовый граф сохранен: {txt_filename}")


def main_stage_3():
    """Основная функция этапа 3"""
    print("Инструмент визуализации графа зависимостей - Этап 3")
    print("Визуализация графа зависимостей\n")
    
    try:
        from config_manager import ConfigManager
        from data_collector import main_stage_2
        
        config = ConfigManager.load_config()
        config.validate()
        
        dependencies = main_stage_2()
        
        if not dependencies:
            print("Нет зависимостей для визуализации")
            return
        
        visualizer = SimpleVisualizer()
        graph_text = visualizer.generate_text_graph(
            config.package_name, 
            dependencies, 
            max_depth=config.max_depth
        )
        
        print("Текстовое представление графа:")
        print(graph_text)
        
        visualizer.save_graph(graph_text, config.output_filename)
        
        print("\n✅ Этап 3 завершен успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка на этапе 3: {e}")


def demonstrate_multiple_packages():
    """
    Демонстрация визуализации для трех различных пакетов
    """
    test_packages = [
        {'name': 'serde', 'version': '1.0.200'},
        {'name': 'tokio', 'version': '1.0.0'},
        {'name': 'reqwest', 'version': '0.11.0'}
    ]
    
    visualizer = SimpleVisualizer()
    
    for pkg in test_packages:
        print(f"\n{'='*50}")
        print(f"ДЕМОНСТРАЦИЯ ДЛЯ ПАКЕТА: {pkg['name']}")
        print(f"{'='*50}")
        
        try:
            from data_collector import CargoDataCollector
            collector = CargoDataCollector()
            
            class TempConfig:
                package_name = pkg['name']
                filter_substring = ""
            
            config = TempConfig()
            dependencies = collector.get_direct_dependencies(config)
            
            graph_text = visualizer.generate_text_graph(pkg['name'], dependencies)
            print(graph_text)
            
            filename = f"{pkg['name']}_dependencies.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(graph_text)
            print(f"Файл сохранен: {filename}")
                
        except Exception as e:
            print(f"Ошибка для пакета {pkg['name']}: {e}")


if __name__ == "__main__":
    main_stage_3()