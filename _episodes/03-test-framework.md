---
title: "Test framework"
teaching: 0
exercises: 0
questions:
- "What is a test framework?"
- "How to write test cases using a test frmework?"
objectives:
- "Start running tests with pytest."
keypoints:
- 
---
# pytest: A test framework
While it is not practical to test a program with all possible inputs we should
execute multiple tests that exercise different aspects of the program. Thus, to
ease this process we use *test frameworks*. It is simply a software tool or
library that provides a structured and organized environment for designing,
writing, and executing tests. Here we will be using **[pytest](https://docs.pytest.org/en/7.3.x/index.html)**,
which is a widely used testing framework for Python.

Follow the instructions [here](https://docs.pytest.org/en/7.3.x/getting-started.html) to install pytest if
you haven't done so already. We will be using pytest in as our test framework. 

## Test already!
Now let's make sure pytest is set up and ready to test.
> In a larger package the structure should follow what you've already been
> taught, with source code and tests in different directories.  Here we will stick
> in the same folder for simplicity.

Pytest looks for files that start with `test_` and runs any functions in those
files that start with `test_`.  In contrast to `unittest` or other x-unit style
frameworks, pytest has one test statement, `assert` which works exactly like in
normal python code.  Here are some pointless tests:
```python
# test_nothing.py

def test_math():
    assert 2 + 2 == 4

def test_failure():
    assert 0  # zero evaluates to false
```

In the same directory as your test files, run `pytest`:
```bash
$ pytest
========================================== test session starts ==========================================
platform linux -- Python 3.9.16, pytest-7.3.1, pluggy-1.0.0
rootdir: ~/projects/testing-lesson/files
plugins: anyio-3.6.2
collected 2 items

test_nothing.py .F                                                                                [100%]

=============================================== FAILURES ================================================
_____________________________________________ test_failure ______________________________________________

    def test_failure():
    >       assert 0  # zero evaluates to false
    E       assert 0

test_nothing.py:5: AssertionError
======================================== short test summary info ========================================
FAILED test_nothing.py::test_failure - assert 0
====================================== 1 failed, 1 passed in 0.06s ======================================
```

Note that two tests were found.  Passing tests are marked with a green `.` while
failures are `F` and exceptions are `E`.

## Writng working test cases

Let's understand writing a test case using the following fucntion that computes that is supporse to compute x + 1 given x. However, note that it has a very obvious bug.

```python
# sample_calc.py
def func(x):
    return x - 1
```
A typical test case consits of the following components:
1. A test input.
2. A call to the function under test with the test input.
3. A statement to compare the output with the expected output.

Following is a simple test case written to test func(x). Note that we have given a descriptive name to show what function is tested and and with what type of input. This is a good practice to increase the readability of tests. The test input here is 3 and the expected output is 4. The assert statement checks the equality of the two.

```python
#test_sample_calc.py
import sample_calc as sc

def test_func_for_positive_int():
    assert sc.func(3) == 4
```
When the test is executed it is going to fail due to the bug.
```bash
$ pytest test_sample_calc.py 
============================= test session starts ==============================
platform darwin -- Python 3.9.12, pytest-7.1.1, pluggy-1.0.0
rootdir: /Volumes/Data/Work/research/INTERSECT2023/TestingLesson
plugins: anyio-3.5.0
collected 1 item                                                               

test_sample_calc.py F                                                    [100%]

=================================== FAILURES ===================================
_________________________________ test_answer __________________________________

    def test_answer():
>       assert sc.func(3) == 4
E       assert 2 == 4
E        +  where 2 = <function func at 0x7fe290e39160>(3)
E        +    where <function func at 0x7fe290e39160> = sc.func

test_sample_calc.py:4: AssertionError
=========================== short test summary info ============================
FAILED test_sample_calc.py::test_answer - assert 2 == 4
============================== 1 failed in 0.10s ===============================

```

{: .challenge}
1. Fix the bug in the code.
2. Add two tests test with a negative number and zero.

Now that we know how to use the pytest test framework, we can use it with our legacy code base!
