# Polygon_width
В данном репозитории находится решение задачи "Ширина выпуклого многоугольника".
## Формулировка задачи
Дано направление n. Проводятся две опорные прямые перпендикулярные n.
Расстояние между ними обозначим w(n). Требуется найти минимум (точку
минимума) w по всем направлениям.
## Формат входных данных
txt-файл, содержащий вершины выпуклого многоугольника следующего формата:
- Разделитель между координатами - символ ","
- Разделитель после каждой точки - символ ";"
- Точки указываются в порядке против часовой стрелки
- Пример содержимого входного файла:
```
3,1;4,3;4,4;2,5;1,4;1,2;
```
## Формат выходных данных
txt-файл, две пары точек на отдельных строках, каждая пара точек задает прямую:
- Разделитель между координатами - символ ","
- Разделитель после каждой точки - символ ";"
- Пример выходного файла:
```
4.0,4.0;4.0,3.0;
1.0,2.0;1.0,4.0;
```
## Алгоритмическая сложность
Алгоритмическая сложность - O(N), где  N - количество точек 
