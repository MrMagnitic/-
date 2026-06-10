import random 


#def array_shift_right_ai(array: list, steps: int) -> None:
#    size = len(array)
 #   steps %= size

#    for _ in range(steps):
#        temp = array[0]
#        for  i in range(1, size):
#            array[i - 1] = array[i]
#        array[size - 1] = temp

#array =[random.randint(0, 99) for _ in range (10)]
#print(array)
#array_shift_right_ai(array, 3)
#print(array)

# def array_shift_right_ai(array: list, steps: int) -> None:
#     size = len(array)
#     if size == 0:
#         return
#     steps %= size

#     for _ in range(steps):
#         temp = array[-1]          
#         for i in range(size - 1, 0, -1):
#             array[i] = array[i - 1]   
#         array[0] = temp

# array_shift_right_ai(array, 8)
# print(array)




# def array_find(array: list[int], key: int) -> int:
#     size: int = len(array)
#     for i in range(size):
#         if key == array[i]:
#             return i
#     return -1


# def array_find_bin(aray: list[int], key: int) -> None:
#     left: int = 0
#     right: int = len(array) - 1
#     while left<=right:
#         middle = (left + right) // 2
#         if array[middle] > key:
#             right = middle - 1
#         else:
#             left = middle + 1
#     return -1

size: int = 10
array: list[int] = [random.randint(0,99) for _ in range(size)]
print(array)

# key: int = int(input("Введите ключ: "))
# index: int = array_find(array, key)
# if(index < 0):
#     print("Ключа нет")
# else:
#     print(f"Ключь найден на {index} позиции")

# def array_sort_select(array: list[int]):
#     size: int = len(array)
#     for left in range(size - 1):
#         min_index = left
#         for index in range(left + 1, size):
#             if array[min_index] > array[index]:
#                 min_index = index
#         array[left], array[min_index] = array[min_index], array[left]

# array_sort_select(array)
# print(array)

# def array_sort_boble(array: list[int]) -> None:
#     size: int = len(array)
#     for left in range(size - 1):
#         isSort: bool = True
#         for index in range(size - 1, left, -1):
#             if array[index] < array[index - 1]:
#                 array[index], array[index - 1] = array[index - 1], array[index]
#                 isSort = False
#         if isSort: break

# array_sort_boble(array)
# print(array)



# def array_sort_shacke(array: list[int]) -> None:
#     size: int = len(array)
#     for left in range(size - 1):
#         sort: bool = True
#         for index in range(size - 1, left, -1):
#             if array[index] < array[index - 1]:
#                 array[index], array[index - 1] = array[index - 1], array[index]
#                 sort = True
#                 left += 1
#                 if sort:
#                     for index in range(size, left):
#                         if array[index - 1] > array[index]:
#                             array[index - 1], array[index] = array[index], array[index - 1]
#                 sort = True

# array_sort_shacke(array)
# print(array)



# def array_sort_quick_req(array: list[int], start: int, finish: int) -> None:
#     left: int = start
#     right: int = finish
#     pivot = array[(start + finish) //2]

#     while left <= right:
#         while array[left] < pivot: left += 1
#         while array[right] > pivot: right -= 1
#         if left <= right:
#             array[left], array[right] = array[right], array[left]
#             left += 1
#             right -= 1
#     if start < right: array_sort_quick_req(array, start, right)
#     if left < finish: array_sort_quick_req(array, left, finish)

# def array_sort_quick(array: list[int]) -> None:
#     array_sort_quick_req(array, 0, len(array) - 1)

# array_sort_quick(array)
# print(array)


