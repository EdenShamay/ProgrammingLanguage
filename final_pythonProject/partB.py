# question 1 :
from functools import reduce


def fibonacci(count):
    fib_list = [0, 1]

    any(map(lambda _: fib_list.append(sum(fib_list[-2:])),
            range(2, count)))

    return fib_list[:count]


print("----------Question 1 Result: ---------- \n")
print(fibonacci(10))
print(fibonacci(5))
#print("---------------------------------------- \n")

# question 2 :

concat_strings = lambda word_list: reduce(lambda word1, word2: word1 + ' ' + word2, word_list)
print("----------Question 2 Result: ---------- \n")
words = ["Afeka", "College", "Of", "Engineering"]
print(concat_strings(words))
#print("---------------------------------------- \n")

# question 3 :

cumulative_sum_of_squares_of_even = lambda lst: list(map(lambda sub_lst: reduce(lambda x, y: x + y, map(lambda num: num ** 2, filter(lambda num: num % 2 == 0, sub_lst)), 0), lst))

lists_of_numbers1 = [[1, 2, 3], [6], [7, 8, 9, 10, 11, 12]] # [2^2 , 6^2, 8^2+10^2+12^2]
lists_of_no_numbers = [] #empty []

print("----------Question 3 Result: ---------- \n")
print(cumulative_sum_of_squares_of_even(lists_of_numbers1))
print(cumulative_sum_of_squares_of_even(lists_of_no_numbers))
#print("---------------------------------------- \n")

# question 4:

print("----------Question 4 Result: ---------- \n")

def cumulative_operation(op):
    return lambda seq: reduce(op, seq)


factorial = cumulative_operation(lambda x, y: x * y)


def exponentiation(seq):
    # Helper function to compute power
    def exp(base, exp):
        return base ** exp


    def power_reduce(x, y):
        return exp(x, y)

    return reduce(lambda acc, elem: exp(elem, acc), reversed(seq))



factorial_input = range(1, 5)
print(f"Factorial of 4 is : {factorial(factorial_input)}")  # 24


exponentiation_input = [2, 2, 4]
print(f"Exponentiation 2^(2^4) is : {exponentiation(exponentiation_input)}")

print("---------------------------------------- \n")
# question 5:

print("----------Question 5 Result: ---------- \n")
tuple = [1, 2, 3, 4] # 2^2 + 4^2
sum_squared = reduce(lambda a, x: a + x, map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, tuple)))
print(sum_squared)
#print("---------------------------------------- \n")

# question 6:
print("----------Question 6 Result: ---------- \n")
palindromes = lambda lists: list(
    map(lambda sublist: reduce(lambda a, x: a + 1 if x == x[::-1] else a, sublist, 0), lists))

my_palindrome_list = [['pop', 'cook', 'eden'], ['wow', 'mom', 'dad', 'civic', 'lol']] # [1 ,5 ]
no_palindrome_list = [] #empty []

result = palindromes(my_palindrome_list)
result2 = palindromes(no_palindrome_list)
print(result)
print(result2)
#print("---------------------------------------- \n")

# question 7:
print("----------Question 7 Result: ---------- \n")
print("\n"
      "In lazy evaluation,\n"
      "values are not computed until they are actually needed.\n"
      "In contrast, in this program, all values are calculated in advance,\n"
      "even if they are never used. With lazy evaluation, however,\n"
      "values are computed only when they are required,\n"
      "leading to more efficient resource management.\n")


#print("---------------------------------------- \n")
# question 8:
sort_primes_descending = lambda num_list: sorted(
    [num for num in num_list if all(num % divisor != 0 for divisor in range(2, int(num**0.5) + 1)) and num > 1],
    reverse=True)

numbers = [1, 2, 3, 19, 5, 7, 23]


print("----------Question 8 Result: ---------- \n")
print(sort_primes_descending(numbers))  # [23 ,19 ,7 ,5 ,3 ,2 ]
#print("--------------------------------------- \n")






