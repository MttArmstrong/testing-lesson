---
title: "Test Driven Development"
teaching: 0
exercises: 0
questions:
- "Why should you write tests first?"
- "What are the 3 phases of TDD"
objectives:
- "Start running tests with pytest."
- "Replace the end-to-end test with a pytest version."
keypoints:
- "Writing tests first ensures you *have* tests and that they are working"
- "Making code testable forces better style"
- "It is much faster to work with code under test"
---
# Test Driven Development
Test Driven Development (or TDD) has a history in agile development but put simply
you're going to write tests *before* you write code (or nearly the same time).  This
is in contrast to the historical "waterfall" development cycle where tests were
developed after code was written e.g. on a separate day or business quarter.

You don't have to be a TDD purist as long as your code ends up having tests.  Some
say TDD makes code less buggy, though that may not be strictly true.  Still, TDD
provides at least three major benefits:

- It greatly informs the *design*, making for more maintainable,
 legible and generally pretty code

- It ensures that tests will *exist* in the first place (b/c
 you are writing them first).  Remember, everyone dislikes
 writing tests, so you should hack yourself to get them done.

- It makes writing tests A LOT more fun and enjoyable. That's
 because writing tests when there's no code yet is a huge
 puzzle that feels more like problem-solving (which is what
 programmers like) than clerical work or bookkeeping (which
 programmers generally despise).

Often times when you write tests with existing code, you anchor your expectations
based on what the code does, instead of brain storming on what a user could do
to break your system.

## Red, green, refactor

The basic cycle of work with TDD is called red, green, refactor:
- Start by writing a failing test.  This is the red phase since your test runner
will show a failure, usually with a red color.  Only when you having a failing
test can you add a feature.
- Add only as much code to make the test pass (green).  You want to work on the code base
only until your tests are passing, then stop!  This is often difficult if you
are struck by inspiration but try to slow down and add a note to come back to.
Maybe you identified the next test to write!
- Look over your code *and tests* and see if anything should be refactored.  At
this point your test suite is passing and you can really get creative.  If a change
causes something to break you can easily undo it and get back to safety.  Also,
having this as a separate step allows you to focus on testing and writing code
in the other phases.  Remember, tests are code too and benefit from the same
design considerations.

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

Note that two tests were found.  Passing test are marked with a green `.` while
failures are `F` and exceptions are `E`.


## Importing overlap.py, red-green-refactor

Getting back to the overlap script, let's start with a failing test.

### Red
You may be surprised how easy it is to fail:
```python
# test_overlap.py

import overlap_v0 as overlap  # change version as needed

def test_import():
    pass
```
When you run pytest, you get an error due to the line opening `sys.argv[1]` when
we aren't providing an input file.  Note how brittle the original design is,
if we wanted to use part of the file somewhere else we aren't able to since
the file expects to be called as the main method.  If you wanted to change
command line parsers or use some part in a notebook, you would quickly run into
problems.


### Green
Maybe you are thinking about how to pull file IO out of this function, but to
start we do the least amount possible to pass our test (which is really just
importing):
```python
# overlap.py

import sys

def main():
    # read input file
    infile = open(sys.argv[1], 'r')
    outfile = open(sys.argv[2], 'w')
    # ...

if __name__ == "__main__":
    main()
```

Now pytest should fail on `test_failure.py`.  You can limit which tests are
run by listing the test files or subdirectories as arguments.

```bash
$ pytest test_overlap.py
========================================== test session starts ===========================================
platform linux -- Python 3.9.16, pytest-7.3.1, pluggy-1.0.0
rootdir: ~/projects/testing-lesson/files
plugins: anyio-3.6.2
collected 1 item

test_overlap.py .                                                                                  [100%]

=========================================== 1 passed in 0.01s ============================================
```
You can be extra thorough and see if `end-to-end.sh` still passes.

### Refactor
At this point, our pytest function is just making sure we can import the code.
But our end-to-end test makes sure the entire function is working as expected
(albeit for a small, simple input).  How about we move the file IO into the main
guard.

{: .challenge}
> ## Refactor
>
> Change file IO to occur in the guard clause.  Your new main method should look
> like `def main(infile, outfile)`.
>>
> > ## Solution
>> ```python
>>def main(infile, outfile):
>>    ...
>>
>>if __name__ == "__main__":
>>    with open(sys.argv[1], encoding='utf-8') as infile, \
>>            open(sys.argv[2], 'w', encoding='utf-8') as outfile:
>>        main(infile, outfile)
>> ```
> > That addresses the context manager and encoding of files. Continue to run
> > your tests to see your changes are ok!
> {: .solution}
{: .challenge}

## End-to-end testing with pytest

We have a lot to address, but it would be nice to integrate our end to end test
with pytest so we can just run one command.  The problem is our main method deals
with files.  Reading and writing to a file system can be several orders of magnitude
slower than working in main memory.  We want our tests to be fast so we can run
them all the time.  The nice thing about python's duck typing is the infile and
outfile variables don't have to be open files on disk, they can be in memory files.
In python, this is accomplished with a StringIO object from the io library.

A StringIO object acts just like an open file.  You can read and iterate from
it just like an opened text file and you can write to it.  When you want to 
read the contents, use the function `getvalue` to get a string representation.

### Red
Let's write a test that will pass in two StringIO objects, one with the file to
read and one for the output.
```python
# test_overlap.py
import overlap_v1 as overlap
from io import StringIO

def test_end_to_end():
    ## ARRANGE
    # initialize a StringIO with a string to read from
    infile = StringIO(
        'a	0	0	2	2\n'
        'b	1	1	3	3\n'
        'c	10	10	11	11'
    )
    # this holds our output
    outfile = StringIO()

    ## ACT
    # call the function
    overlap.main(infile, outfile)

    ## ASSERT
    output = outfile.getvalue().split('\n')
    assert output[0].split() == '1 1 0'.split()
    assert output[1].split() == '1 1 0'.split()
    assert output[2].split() == '0 0 1'.split()
```
Since this is the first non-trivial test, let's spend a moment going over it.
Like before we import our module and make our test function start with `test_`.
The actual name of the function is for your benefit only so don't be worried if
it is too long.  You won't have to type it so be descriptive!  Next we have the
three steps in all tests: Arrange-Act-Assert (aka Given-When-Then)

- Arrange: Set up the system in a particular way to test the feature you want.
Consider edge cases, mocking databases or files, building helper objects, etc.
- Act: Call the code you want to test
- Assert: Confirm the observable outputs are what you expect.  Notice that the
outputs here read like the actual output file.

Again, pytest uses plain assert statements to test results.

But we have a problem, our test passes!  This is partially because we are replacing
an existing test, but the problem is how can you be sure you are testing what you
think?  Maybe you are importing a different version of code, maybe pytest isn't
finding your test, etc.  Often a test that passes which should fail is more
worrisome than a test which fails that should be passing.

Notice the splits in the assert section, they normalize the output so any
whitespace will be accepted.  Let's replace those with explicit white space
(tabs) and see if we can go red:
```python
    assert output[0] == '1\t1\t0'
    assert output[1] == '1\t1\t0'
    assert output[2] == '0\t0\t1'
```
Since `split('\n')` strips off the newline at the end of each line.  Now we
fail (yay!) and it's due to something we have wanted to change anyways.  The
pytest output says
```bash
E       AssertionError: assert '1\t1\t0\t' == '1\t1\t0'
```
that is, we have an extra tab at the end of our lines.

### Green

{: .challenge}
> ## Fix the code
>
> Change the overlap file to make the above test pass.  Hint, change when and
> where you write a tab to the file.
>>
> > ## Solution
>> There are a few options here.  I'm opting for building a list and using
>> `join` for the heavy lifting.
>> ```python
>>    for red_name, red_coords in dict.items():
>>        output_line = []
>>        for blue_name, blue_coords in dict.items():
>>            # check if rects overlap
>>            result = '1'
>>
>>            red_lo_x, red_lo_y, red_hi_x, red_hi_y = red_coords
>>            blue_lo_x, blue_lo_y, blue_hi_x, blue_hi_y = blue_coords
>>
>>            if (red_lo_x >= blue_hi_x) or (red_hi_x <= blue_lo_x) or \
>>                    (red_lo_y >= blue_hi_x) or (red_hi_y <= blue_lo_y):
>>                result = '0'
>>
>>            output_line.append(result)
>>        outfile.write('\t'.join(output_line) + '\n')
>> ```
> {: .solution}
{: .challenge}

Once you get the test passing you will notice that the `end-to-end.sh` will no
longer pass!  One of the reasons to test code is to find (and prevent) bugs.
When you work on legacy code, sometimes you will find bugs in published code and
the questions can get more problematic.  Is the change something that will alter
published results?  Was the previous version wrong or just not what you prefer?
You may decide to keep a bug if it was a valid answer!  In this case we will keep
the change and not have a tab followed by a newline.

### Refactor
Let's focus this round of refactoring on our test code and introduce some nice
pytest features.  First, it seems like we will want to use our simple input
file in other tests.  Instead of copying and pasting it around, let's extract it
as a *fixture*.  Pytest fixtures can do a lot, but for now we just need an object
built for some tests:
```python
# test_overlap.py
import overlap_v1 as overlap
from io import StringIO
import pytest

@pytest.fixture()
def simple_input():
    return StringIO(
        'a	0	0	2	2\n'
        'b	1	1	3	3\n'
        'c	10	10	11	11'
    )

def test_end_to_end(simple_input):
    # initialize a StringIO with a string to read from
    infile = simple_input
    ...
```
We start by importing pytest so we can use the `@pytest.fixture()` decorator.
This decorates a function and makes its return value available to any function
that uses it as an input argument.  Next we can replace our `infile` definition
by assigning it to `simple_input`.

For this code, the end-to-end test runs quickly, but what if it took several
minutes?  Ideally we could run our fast tests all the time and occasionally run
everything.  The simplest way to achieve this with pytest is to mark the function
as slow and invoke pytest with `pytest -m "not slow"`:

```python
# test_overlap.py
@pytest.mark.slow()
def test_end_to_end(simple_input):
    ...
```

```bash
pytest -m "not slow" test_overlap.py
========================================== test session starts ===========================================
platform linux -- Python 3.9.16, pytest-7.3.1, pluggy-1.0.0
rootdir: ~/projects/testing-lesson/files
plugins: anyio-3.6.2
collected 1 item / 1 deselected / 0 selected
```

Note that the one test was deselected and not run.  You can (and should) formalize
this mark as described in the warning that will pop up!

{% include links.md %}

