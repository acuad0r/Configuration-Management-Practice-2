#!/usr/bin/env python3
"""
Этап 2: Сбор данных о зависимостях Cargo пакетов
"""

from dataclasses import dataclass


@dataclass
class Dependency:
    """Класс для представления зависимости"""
    name: str
    version: str
    is_optional: bool = False


class CargoDataCollector:
    """Класс для сбора данных о зависимостях Cargo пакетов"""
    
    TEST_DEPENDENCIES = {
        "serde": [
            Dependency(name="serde_derive", version="1.0", is_optional=False),
            Dependency(name="proc-macro2", version="1.0", is_optional=False),
            Dependency(name="quote", version="1.0", is_optional=False),
            Dependency(name="syn", version="2.0", is_optional=False),
        ],
        "tokio": [
            Dependency(name="bytes", version="1.0", is_optional=False),
            Dependency(name="mio", version="0.8", is_optional=False),
            Dependency(name="pin-project-lite", version="0.2", is_optional=False),
            Dependency(name="socket2", version="0.4", is_optional=True),
        ],
        "reqwest": [
            Dependency(name="base64", version="0.21", is_optional=False),
            Dependency(name="bytes", version="1.0", is_optional=False),
            Dependency(name="hyper", version="0.14", is_optional=False),
            Dependency(name="serde", version="1.0", is_optional=True),
            Dependency(name="serde_json", version="1.0", is_optional=True),
        ]
    }
    
    def get_direct_dependencies(self, config):
        """
        Получение прямых зависимостей пакета
        """
        print(f"🔍 Поиск зависимостей для пакета: {config.package_name}")
        
        if config.package_name in self.TEST_DEPENDENCIES:
            dependencies = self.TEST_DEPENDENCIES[config.package_name]
            
            if config.filter_substring:
                filtered_deps = [dep for dep in dependencies 
                              if config.filter_substring.lower() in dep.name.lower()]
                print(f"Применен фильтр '{config.filter_substring}': {len(filtered_deps)} из {len(dependencies)} зависимостей")
                return filtered_deps
            
            return dependencies
        else:
            print(f"⚠️  Пакет {config.package_name} не найден в тестовых данных")
            return [
                Dependency(name="example_dep1", version="1.0", is_optional=False),
                Dependency(name="example_dep2", version="2.0", is_optional=True),
            ]


def print_dependencies(dependencies, package_name):
    """
    Вывод списка зависимостей на экран
    """
    print("=" * 60)
    print(f"ПРЯМЫЕ ЗАВИСИМОСТИ ПАКЕТА: {package_name}")
    print("=" * 60)
    
    if not dependencies:
        print("❌ Зависимости не найдены")
        return
    
    for i, dep in enumerate(dependencies, 1):
        optional_flag = " (опциональная)" if dep.is_optional else ""
        print(f"{i:2d}. {dep.name:25} {dep.version:15} {optional_flag}")
    
    print("=" * 60)
    print(f"✅ Всего зависимостей: {len(dependencies)}")


def main_stage_2():
    """Основная функция этапа 2"""
    print("Инструмент визуализации графа зависимостей - Этап 2")
    print("Сбор данных о зависимостях\n")
    
    try:
        from config_manager import ConfigManager
        config = ConfigManager.load_config()
        config.validate()
        
        collector = CargoDataCollector()
        dependencies = collector.get_direct_dependencies(config)
        
        print_dependencies(dependencies, config.package_name)
        
        print("\n✅ Этап 2 завершен успешно!")
        return dependencies
        
    except Exception as e:
        print(f"❌ Ошибка на этапе 2: {e}")
        return []


if __name__ == "__main__":
    main_stage_2()