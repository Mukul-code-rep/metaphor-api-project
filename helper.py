import re


def partition(array: list, low: int, high: int, modify: bool = False) -> int:
    """
        Choose the rightmost element as the pivot, place the pivot at its correct
        position in the sorted array, and place all smaller elements to the left
        and larger elements to the right.

        Args:
            array (list): The list to be sorted.
            low (int): Starting index of the partition.
            high (int): Ending index of the partition.
            modify (bool, optional): If True, the array contains tuples. Defaults to False.

        Returns:
            int: Index of the pivot element.
    """
    if modify:
        pivot = array[high][0]
    else:
        pivot = array[high]
    i = low - 1

    for j in range(low, high):
        if modify:
            elem = array[j][0]
        else:
            elem = array[j]
        if elem <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    return i + 1


def quick_sort(array: list, low: int, high: int, modify: bool = False) -> None:
    """
        Sort the array using the QuickSort algorithm.

        Args:
            array (list): The list to be sorted.
            low (int): Starting index of the array.
            high (int): Ending index of the array.
            modify (bool, optional): If True, the array contains tuples. Defaults to False.
    """
    if low < high:
        pi = partition(array, low, high, modify)
        quick_sort(array, low, pi - 1, modify)
        quick_sort(array, pi + 1, high, modify)


def binary_search(array: list[str], target: str) -> int:
    """
        Perform binary search on a sorted array to find the target.

        Args:
            array (list[str]): The sorted list to be searched.
            target (str): The target string to be searched.

        Returns:
            int: 0 if the target is found, -1 otherwise.
    """
    start, stop = 0, len(array)-1

    while start <= stop:
        middle = (start + stop) // 2
        if re.search(f"^{array[middle]}", target):
            return 0
        elif array[middle] < target:
            start = middle + 1
        else:
            stop = middle - 1

    return -1
