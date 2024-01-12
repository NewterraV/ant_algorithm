from PIL import Image
import numpy as np

"""
Описано 2 метода:
 - **generate_path** - генерирует точки и возвращает словарь с 
координатами черных пикселей в ключах. Более быстрый алгоритм, но в размере 
поля указанном в задаче, проигрывает второму в использовании RAM. 
Однако при увеличении поля выиграет и в RAM
 - **generate_path__numpy** - генерирует точки и возвращает NumPy массив в 
виде матрицы. в случае задачки меньше использует RAM, но с увеличением поля 
проигрывает первому.
"""


def generate_path_numpy(x=512, y=512, size=1024):
    """Метод генерирует массив с указанием цвета пикселей"""

    arr = np.ones((size, size))
    directions = ["y+", "x+", "y-", "x-"]
    direction = 0

    while 0 < x < size and 0 < y < size - 1:
        # перемещение
        if directions[direction] == "y+":
            y += 1
        elif directions[direction] == "y-":
            y -= 1
        elif directions[direction] == "x+":
            x += 1
        elif directions[direction] == "x-":
            x -= 1
        # Смена цвета
        if arr[y, x] == 1:
            arr[y, x] = 0
            direction += 1
        else:
            arr[y, x] = 1
            direction -= 1
        # зацикливание списка направлений
        if direction == 4:
            direction = 0
        elif direction == -4:
            direction = 0
    count = np.sum(arr == 0)
    return (arr * 255), count


def generate_path(x=512, y=512, size=1024):
    """Метод генерирует словарь с указанием координат черных пикселей"""
    pixel_colors = {}
    directions = ["y+", "x+", "y-", "x-"]
    direction = 0

    while 0 < x < size and 0 < y < size:
        # перемещение
        if directions[direction] == "y+":
            y += 1
        elif directions[direction] == "y-":
            y -= 1
        elif directions[direction] == "x+":
            x += 1
        elif directions[direction] == "x-":
            x -= 1
        # Смена цвета
        pixel_color = pixel_colors.get(f"{x}_{y}")
        if pixel_color is None:
            pixel_colors[f"{x}_{y}"] = 1
            direction += 1
        else:
            del pixel_colors[f"{x}_{y}"]
            direction -= 1
        # зацикливание списка направлений
        if direction == 4:
            direction = 0
        elif direction == -4:
            direction = 0
    return pixel_colors


def save_img(arr, path=None):
    """Метод сохраняет картинку на основе полученного типа данных"""
    if type(arr) is dict:
        with Image.new(size=(1024, 1024), color=255, mode="L") as img:
            for key in arr.keys():
                x, y = key.split("_")
                img.putpixel((int(x), int(y)), 0)
            img.save(path)
    #             img.show()
    else:
        with Image.fromarray(arr) as img:
            img.convert("L").save(path)


if __name__ == "__main__":
    # Вариант с массивом
    matrix = generate_path_numpy(512, 512, 1024)
    save_img(matrix[0], "img.png")
    print(matrix[1])

    # Вариант со словарем
    black_pixels = generate_path(512, 512, 1024)
    save_img(black_pixels, "img.png")
    print(len(black_pixels))
