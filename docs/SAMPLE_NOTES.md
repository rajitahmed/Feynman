Recursion – CS notes (week 4)

What it is
- A function that calls itself to solve a problem
- Breaks a big problem into smaller versions of the SAME problem
- Every recursive function needs 2 parts:
  1. Base case → the simplest version, answered directly, no more calls
  2. Recursive case → function calls itself on a smaller input
- No base case (or input never gets smaller) = infinite recursion → stack overflow error

How it works
- Each call gets added to the call stack (its own copy of the variables)
- Calls keep stacking up until one hits the base case
- Then the answers "unwind": each call returns its result to the one that called it
- Results get combined on the way back up

Example: factorial
- 5! = 5 × 4 × 3 × 2 × 1
- factorial(n) = n × factorial(n - 1)
- base case: factorial(1) = 1
- factorial(3) → 3 × factorial(2) → 3 × 2 × factorial(1) → 3 × 2 × 1 = 6

  def factorial(n):
      if n <= 1:
          return 1
      return n * factorial(n - 1)

Other examples
- Walking a folder tree: a folder contains files AND other folders → open each folder the same way
- Fibonacci: fib(n) = fib(n-1) + fib(n-2), base cases fib(0)=0, fib(1)=1 (slow without memoization!!)
- Binary search, merge sort, tree traversal

Recursion vs loops
- Anything recursive can be written with a loop (and vice versa)
- Recursion is cleaner when the problem is naturally "made of smaller copies of itself" (trees, nested stuff)
- Loops are usually faster + use less memory (no call stack buildup)
- Python has a recursion limit (~1000 calls by default)

Why use it
- Shorter, more readable code for tree/nested problems
- Matches how the problem is defined (e.g. math definitions like factorial)
- Downside: harder to debug, can be slow if it repeats work (fib)
