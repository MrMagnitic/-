import random


size: int = 10
array: list[int] = [random.randint(0,99) for _ in range(size)]
print(array)



def array_sort_shacker(array: list[int]) -> None:
    size = len(array)
    left = 0
    right = size - 1
    sort = True

    while sort:
        sort = False
        for i in range(left, right):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                sort = True
        right -= 1
        
        if not sort:
            break

        for i in range(right, left, -1):
            if array[i] < array[i - 1]:
                array[i], array[i - 1] = array[i - 1], array[i]
                sort = True
        left += 1 

array_sort_shacker(array)
print(array)
