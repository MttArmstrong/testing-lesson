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
1. Test input
2. Calling the function under test with the test input
3. Compare the output with the expected output
