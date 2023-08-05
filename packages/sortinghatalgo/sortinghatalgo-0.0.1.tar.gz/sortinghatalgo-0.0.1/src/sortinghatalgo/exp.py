from sklearn.model_selection import train_test_split
from scipy import stats
import pandas as pd
import numpy as np
import ast
import sys
import re
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
        if len(list) > 1: #Allows recursion on list to break after split gets to 1.
            mid = len(list)//2 #Find the middle index position of the list
            left = list[:mid] #Separate the left side of list
            right = list[mid:] #separte the right side of list
            self.merge_sort(left) # Recursively sort left list until only one is left
            self.merge_sort(right) # Recursively sort right list until only one is left
            a = 0 # Left indexer
            b = 0 # Right indexer
            c = 0 # List indexer
            while a < len(left) and b < len(right):
                if left[a] < right[b]: # If first value on left is less than first value on right
                    list[c] = list[a] # Set the first value of the list equal to the first value on left
                    a+=1 # Add one to the index position on the left and repeat the process
                else: # If the right is greater than the left
                    list[c] = right[b] # Set the first value of the list to the first value on the right
                    b+=1 # Add one to the index position on the right and repeat the process
                c+=1 # Add one to index position of list for next iteration

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


class helper_functions:
    def __init__(self):
        # self.df = df
        pass
        
    def null_count(self, df):
        return df.isna().sum().sum()

    def tts(self, frac, df):
        split_df = train_test_split(df, train_size = frac)
        return split_df

    def randomize(self, seed, df):
        return df.sample(frac = 1, random_state = seed)

    def list_2_series(self,list_2_series, df):
        ser = pd.Series(list_2_series)
        df['list'] = df.append(ser, ignore_index = True)
        return df

    def random_phrase(self):
        adj = ['Awesome', 'Shiny', 'Impressive', 'Portable', 'Improved']
        noun = ['Anvil', 'Catapult','Disguise', 'Mousetrap', 'Sword']
        return f"{adj[np.random.randint(0, len(adj))]} {noun[np.random.randint(0, len(noun))]}"

    def random_float(self, min_val, max_val):
        return np.random.uniform(min_val, max_val)

    def random_bowling_score(self):
        return np.random.randint(0,300)

    def silly_tuple(self):
        return tuple((self.random_phrase(), self.random_float(1.0, 5.0), self.random_bowling_score()))

    def silly_tuple_list(self, num_tuples=1):
        return [self.silly_tuple() for num in range(num_tuples)]
    
    def abbr_2_state(self, state_series : pd.Series, abbr_2_state : bool =True):
        with open('state.txt') as f:
            data = f.read()
        state_dict = ast.literal_eval(data)

        if abbr_2_state == False:
            state_dict = dict(map(reversed, state_dict.items()))
            state_series = state_series.map(state_dict)
            return state_series

        else:
            state_series = state_series.map(state_dict)
            return state_series
    
    def split_dates(date_series : pd.Series):
        date_series = pd.to_datetime(date_series)
        return pd.DataFrame(data = {
            'Day' : date_series.dt.day,
            'Month' : date_series.dt.month,
            'Year': date_series.dt.year})
    
    def rm_outlier(self, df):
        return df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
    
    def factors(self, num):
        """
        Input: Single positive integer
        Output: All factors of num in range of 1 -> num
        """
        if num > 0 and num.is_integer():
            for i in range(1, num+1):
                if num % i == 0:
                    print(i)
    
    def multi_table(self, num):
        """
        Input: Single positive integer
        Output : Multiplication table from 1-10
        """
        for i in range(1, 11):
            print(f'{num} x {i} = {num*i:.2f}') # :.2f adds 2 zeros at the end
    
    def cel_fah_conversion(self, f):
        return ((f - 32) * (5/9))
    
    def fah_cel_conversion(self, c):
        return (c * (9/5) + 32)

    def quadratic_formula(self, a, b, c):
        """
        Input: a: int,
               b: int,
               c: int
        Output: x1 and x2 from a quadratic equation
        Magic: Calculates the +- values of a quadratic equation. 
        """
        base = (b**2 - 4 * a * c)**0.5
        x1 = (-b + base)/(2 * a)
        x2 = (-b - base)/(2 * a)
        return x1, x2
