---
title: "Test framework"
teaching: 15
exercises: 15
questions:
- "What is a test framework?"
- "How to write test cases using a test frmework?"
objectives:
- "Start running tests with pytest."
keypoints:
- "A test framework simplifies adding tests to your project."
- "Choose a framework that doesn't get in your way and makes testing fun."
- "Coverage tools are useful to identify which parts of the code are executed with tests"
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

## Writing actual test cases

Let's understand writing a test case using the following function that 
is supposed to compute `x + 1` given `x`. Note the very obvious bug.

```python
# sample_calc.py
def func(x):
    return x - 1
```
A typical test case consits of the following components:
1. A test input.
2. A call to the function under test with the test input.
3. A statement to compare the output with the expected output.

Following is a simple test case written to test `func(x)`. Note that we have
given a descriptive name to show what function is tested and and with what type
of input. This is a good practice to increase the readability of tests. You
shouldn't have to explicitly call the test functions, so don't worry if the
names are longer than you would normally use. The test input here is 3 and the
expected output is 4. The assert statement checks the equality of the two.

```python
#test_sample_calc.py
import sample_calc as sc

def test_func_for_positive_int():
    input_value = 3                     # 1. test input
    func_output = sc.func(input_value)  # 2. call function
    assert func_output == 4             # 3. compare output with expected
```
When the test is executed it is going to fail due to the bug in `func`.
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
> ## Improve the code
> Modify `func` and `test_sample_calc.py`:
  1. Fix the bug in the code.
  2. Add two tests test with a negative number and zero. 
>
>>
> > ## Solution
> > 1. Clearly `func` should return `x + 1` instead of `x - 1`
> > 2. Here are some additional assert statements to test more values.
> > ```python
> > assert sc.func(0) == 1
> > assert sc.func(-1) == 0
> > assert sc.func(-3) == -2
> > assert sc.func(10) == 11
> > ```
> > How you organize those calls is a matter of style.  You could have one
> > `test_` function for each or group them into a single `test_func_hard_inputs`.
> > Pytest code is just python code, so you could set up a loop or use the
> > `pytest.parameterize` decorator to call the same code with different inputs.
> {: .solution}
{: .challenge}


We will cover more features of pytest as we need them.  Now that we know how to
use the pytest framework, we can use it with our legacy code base!

# What is code (test) coverage

The term *code coverage* or *coverage* is used to refer to the code constructs
such as statements and branches executed by your test cases. 

Note: It is not recommended to create test cases to simply to cover the code.
This can lead to creating useless test cases and a false sense of security.
Rather, coverage should be used to learn about which parts of the code are not
executed by a test case and use that information to augment test cases to check
the respective functionality of the code.  In open source projects, assuring
high coverage can force contributors to test their new code.

We will be using [Coverage.py](https://coverage.readthedocs.io/en/7.2.7/#) to
calculate the coverage of the test cases that we computed above. Follow the
instructions [here](https://coverage.readthedocs.io/en/7.2.7/install.html) to
install Coverage.py.

Now let's use Coverage.py to check the coverage of the tests we created for
`func(x)`, To run your tests using pytest under coverage you need to use the
`coverage run` command:
```bash
$ coverage run -m pytest test_sample_calc.py 
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
E        +  where 2 = <function func at 0x7fab8ca2be50>(3)
E        +    where <function func at 0x7fab8ca2be50> = sc.func

test_sample_calc.py:4: AssertionError
=========================== short test summary info ============================
FAILED test_sample_calc.py::test_answer - assert 2 == 4
============================== 1 failed in 0.31s ===============================
```
To get a report of the coverage use the command `coverage report`:
```bash
$ coverage report
Name                  Stmts   Miss  Cover
-----------------------------------------
sample_calc.py            2      0   100%
test_sample_calc.py       3      0   100%
-----------------------------------------
TOTAL                     5      0   100%
```
Note the statement coverage of sample_calc.py which is 100% right now.  We can
also specifically check for the executed branches using the `--branch` flag
with the `coverage run` command. You can use the `--module` flag with the
`coverage report` command to see which statements are missed with the test
cases if there is any and update the test cases accordingly.
