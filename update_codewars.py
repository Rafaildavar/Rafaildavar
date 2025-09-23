#!/usr/bin/env python3
"""
Скрипт для обновления статистики CodeWars в README.md
"""

import requests
from bs4 import BeautifulSoup
import re
import sys

def get_codewars_stats(username):
    """Получает статистику пользователя с CodeWars"""
    url = f"https://www.codewars.com/users/{username}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Извлекаем данные из HTML
        page_text = response.text
        
        # Ищем ранг
        rank_match = re.search(r'Rank.*?(\d+)\s*kyu', page_text)
        rank = rank_match.group(1) if rank_match else "7"
        
        # Ищем honor
        honor_match = re.search(r'Honor.*?(\d+)', page_text)
        honor = honor_match.group(1) if honor_match else "76"
        
        # Ищем количество решенных задач
        completed_match = re.search(r'Total Completed Kata.*?(\d+)', page_text)
        completed = completed_match.group(1) if completed_match else "13"
        
        return {
            'rank': rank,
            'honor': honor,
            'completed': completed
        }
        
    except Exception as e:
        print(f"Ошибка при получении данных с CodeWars: {e}")
        return None

def update_readme(stats):
    """Обновляет README.md с новой статистикой"""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Обновляем статистику
        content = re.sub(
            r'(\*\*Ранг\*\*: )\d+ kyu',
            f'\\g<1>{stats["rank"]} kyu',
            content
        )
        
        content = re.sub(
            r'(\*\*Honor\*\*: )\d+',
            f'\\g<1>{stats["honor"]}',
            content
        )
        
        content = re.sub(
            r'(\*\*Решено задач\*\*: )\d+',
            f'\\g<1>{stats["completed"]}',
            content
        )
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Статистика обновлена: {stats['rank']} kyu, {stats['honor']} honor, {stats['completed']} задач")
        return True
        
    except Exception as e:
        print(f"Ошибка при обновлении README: {e}")
        return False

if __name__ == "__main__":
    username = "remi_hr"
    stats = get_codewars_stats(username)
    
    if stats:
        success = update_readme(stats)
        if success:
            print("🎉 README успешно обновлен!")
        else:
            sys.exit(1)
    else:
        print("❌ Не удалось получить статистику")
        sys.exit(1)
