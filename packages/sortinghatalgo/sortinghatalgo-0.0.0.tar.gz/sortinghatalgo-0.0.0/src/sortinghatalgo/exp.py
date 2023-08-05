class Sorting_Algo:    
    def __init__(self):
        pass
    def bubble_sort(self,list: list):
        """
        Simplist and slowest algorithm used for sorting. Should be used for smaller datasets due to it's BigO Notation.\n
        Designed so that the highest value in the list bubbles its way to the top as the algo iterates through.\n
        Has an outer loop(passes) and an inner loop where the remaining unsorted elements are sorted.\n
        Time/Space Complexity is at worst O(n^2).
        """
        last_idx = len(list)-1 #Last element index position
        for pass_number in range(last_idx, 0, -1): #Passes through each element of the list, from the back
            for idx in range(pass_number):
                if list[idx] > list[idx+1]:
                    list[idx], list[idx+1] = list[idx+1], list[idx]
        return list

    def merge_sort(self, list: list):
        """

        """
        if len(list) > 1:
            mid = len(list)//2
            left = list[:mid]
            right = list[mid:]
            self.merge_sort(left)
            self.merge_sort(right)
            a = 0
            b = 0
            c = 0
            while a < len(left) and b < len(right):
                if left[a] < right[b]:
                    list[c] = list[a]
                    a+=1
                else:
                    list[c] = right[b]
                    b+=1
                c+=1

            while a < len(left):
                list[c]=left[a]
                a+=1
                c+=1
            while b < len(right):
                list[c] = right[b]
                b+=1
                c+=1
        return list

    def insertion_sort(self, list: list):
        """
        Inserts data points into the list by sorting the list and inserting where it belongs.
        Starts with two data points and sorts them, then takes the next value and sorts it until reaching the end.
        Can be used on smaller data structures, but would not be recommended for larger structures
        At best, if a list is already sorted, O(n), worst case is O(n^2)
        """
        for i in range(1, len(list)): # Used to iterate through the entire list
            j = i-1 #Selects first element of the list
            next_element = list[i] #Selects second element of the list
            while (list[j] > next_element) and (j >=0):
                list[j+1] = list[j]
                j = j-1
            list[j+1] = next_element
        return list

    def shell_sort(self, list):
        """

        """
        dist = len(list) // 2
        while dist > 0:
            for i in range(dist, len(list)):
                temp = list[i]
                j = i
                while j >= dist and list[j-dist] > temp:
                    list[j] = list[j-dist]
                    j = j-dist
                list[j] = temp
            dist = dist//2
        return list

    def selection_sort(self, list: list):
        """

        """
        for fill_slot in range(len(list) - 1, 0, -1): #Starts from the back of the list
            max_index=0
            for location in range(1, fill_slot+1):
                if list[location] > list[max_index]:
                    max_index = location
            list[fill_slot], list[max_index] = list[max_index], list[fill_slot]
        return list