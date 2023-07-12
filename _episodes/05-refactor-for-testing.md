---
title: "Refactoring for Testing"
teaching: 20
exercises: 40
questions:
- "Why are long methods hard to test?"
objectives:
- "Learn some key refactoring methods to change code safely."
- "Modify the overlap script to support a Rectangle object."
keypoints:
- "Testing long methods is difficult since you can't pinpoint a few lines of logic."
- "Testable code is also good code!"
- "Changing code without tests can be dangerous.  Work slowly and carefully making only the simplest changes first."
- "Write tests with an adversarial viewpoint."
- "Keep tests DRY, fixtures and parameter can help."
---
# Monolithic Main Methods

One of the smelliest code smells that new developers make is having a single
main method which spans several hundred (thousand?) lines.  Even if the code
is perfect, long methods are an anti-pattern because they require a reader of
the code to have exceptionally good working memory to understand the method.
It also becomes impossible to reuse part of the code elsewhere.

Consider the following two sections of code:
```python
if user is not None and user in database and database[user]['type'] == 'admin':
    # do admin work

#### vs ####
def user_is_admin(user, database):
    return user is not None and user in database and database[user]['type'] == 'admin'

if user_is_admin(user, database):
    # do admin work
```

The second version puts less stress on the reader because when they see the
function called `user_is_admin` they can treat it like a black box until they
are interested in the internals.  But we are here to talk about testing!

Consider writing a test for the first version, where all the logic of what
makes a user an admin is in the if statement.  To even get to this line of code
you will have to set up your system and possibly mock or replace other function
calls.  As a separate function, your test becomes a unit test, exercising a
small piece of code.  Here is a possible pytest:
```python
def test_user_is_admin():
    user = None
    database = {}
    assert user_is_admin(user, database) is False, "None user is not an admin"

    user = "Jim"
    database = {}
    assert user_is_admin(user, database) is False, "User not in database"

    database = {"Jim": {"type": "regular"}}
    assert user_is_admin(user, database) is False, "User is not an admin"

    database = {"Jim": {"type": "admin"}}
    assert user_is_admin(user, database) is True, "User is an admin"
```

A surprising benefit of TDD and testing is that having to write code with tests
makes your code better!  It's just too hard to write tests for bad code; if you
*have* to write a test then it's easier to just write better code.

# Safe Refactoring and TDD
## Reading in Rectangles
Now back to our overlap code.  You have inherited a monolithic main method,
how do you go about breaking it up?  Some IDEs have functions for extracting
a method or attribute but we are following TDD and need to write a failing test
first.  Let's start with the first portion of our existing main method, reading
in the `dict`:

### Red
```python
# overlap.py

def main(infile, outfile):
    # build rectangle struct
    dict = {}
    for line in infile:
        name, *coords = line.split()
        dict[name] = [int(c) for c in coords]
...
```
We have a design decision to make.  Should we extract the entire for loop
or just the inside?  The current code works with an open file,  but any iterable
could do (say a list of strings).  Your decision should be informed by what
is useful *and* what is easy to test.  Having a function to convert a string
to a rectangle could be handy, but for now we will take the entire for loop.

```python
# test_overlap.py
def test_read_rectangles_simple(simple_input):
    rectangles = overlap.read_rectangles(simple_input)
    assert rectangles == {
        'a': [0, 0, 2, 2],
        'b': [1, 1, 3, 3],
        'c': [10, 10, 11, 11],
    }
```

Which fails because we don't have a method named `read_rectangles`.  Note that
we have already decided on a name for the function, its arguments and return
values without touching our source code.

### Green
Now we can pull out the function and replace that for loop with a function
call.

{: .challenge}
> ## Fix the code
>
> Change the overlap file to make the above test pass.
>>
> > ## Solution
>> ```python
>>def main(infile, outfile):
>>    dict = read_rectangles(infile)
>>    ...
>>
>>
>>def read_rectangles(infile):
>>    result = {}
>>    for line in infile:
>>        name, *coords = line.split()
>>        result[name] = [int(c) for c in coords]
>>    return result
>>
>> ```
>> When you start refactoring like this go slow and in parts.  Make the function
>> first and when the `test_read_rectangles` passes replace the code in the main
>> method.  Your end to end test should still pass and tell you if something is
>> wrong.  Note we can remove the comment because the function name is self documenting.
> {: .solution}
{: .challenge}

### Refactor
With read rectangles pulled out, let's rename our `dict` to rectangles.  Since
the argument to our function can be any iterable of strings, we can also rename
it to `rectangles` and add a type annotation to show what we expect as input.
Now is also the time to add a doc string.  Make changes step-wise and run your
tests frequently.
```python
from collections.abc import Iterable

def main(infile, outfile):
    rectangles = read_rectangles(infile)
    ...


def read_rectangles(rectangles: Iterable[str]) -> dict[str, list[float]]:
    result = {}
    for rectangle in rectangles:
        name, *coords = rectangle.split()
        result[name] = [int(c) for c in coords]
    return result
```

Note our return value is a list of floats, ints are implied by that and we
may want to support floats later (hint, we do!).

## Test like an enemy
With a small, testable method in place, we can start adding features and get
creative.  Often you will take the mindset of an adversary of a codebase.  This
is generally easier with someone else's code because you can think "I bet they
didn't think of this" instead of "why didn't I think of this", but being self
deprecating gets easier with practice.

Think of all the ways the overlap code could break, all the things that aren't tested,
and how you would expect them to be handled.  Remember users aren't perfect so
expect non-optimal inputs.  It's better to fail early (and descriptively) than
several lines or modules away.

{: .challenge}
> ### Red-Green-Refactor the `read_rectangles`
> Pick one of the following and work through a red-green-refactor cycle to address
> it.  Work on more as time permits.  Remember to keep each phase short and run
> pytest often.  Stop adding code once a test starts passing.
 - How to handle empty input?
 - Non-numeric X and Y coordinates?
 - X and Y coordinates that are floats?
 - X and Y coordinates not equal?  (how are we not testing this!)
 - X and Y coordinates are not in increasing order?
 - Incorrect number of coordinates supplied?
 - Any others you can think of?
>
> Often there isn't one right answer.  When the user gives an empty file, should
> that be an empty result or throw an error?  The answer may not matter, but
> formalizing it as a test forces you to answer and document such questions.
> Look up `pytest.raises` for how to test if an exception is thrown.
>> ## Solution
>> Here is one set of tests and passing code.  You may have chosen different
>> behavior for some changes.
>> ```python
>> # test_overlap.py
>>def test_read_rectangles_empty_input_empty_output():
>>    rectangles = overlap.read_rectangles([])
>>    assert rectangles == {}
>>
>>def test_read_rectangles_non_numeric_coord_raise_error():
>>    with pytest.raises(ValueError) as error:
>>        overlap.read_rectangles(['a a a a a'])
>>    assert "Non numeric value provided as input for 'a a a a a'" in str(error)
>>
>>def test_read_rectangles_accepts_floats():
>>    lines = ['a 0.3 0.3 1.0 1.0']
>>    rectangles = overlap.read_rectangles(lines)
>>    coords = rectangles['a']
>>    # Note that 0.3 != 0.1 + 0.2 due to floating point error, use pytest.approx
>>    assert coords[0] == pytest.approx(0.1 + 0.2)
>>    assert coords[1] == 0.3
>>    assert coords[2] == 1.0
>>    assert coords[3] == 1.0
>>
>>def test_read_rectangles_not_equal_coords():
>>    lines = ['a 1 2 3 4']
>>    rectangles = overlap.read_rectangles(lines)
>>    assert rectangles == {'a': [1, 2, 3, 4]}
>>
>>def test_read_rectangles_fix_order_of_coords():
>>    lines = ['a 3 4 1 2']
>>    rectangles = overlap.read_rectangles(lines)
>>    assert rectangles == {'a': [1, 2, 3, 4]}
>>
>>def test_read_rectangles_incorrect_number_of_coords_raise_error():
>>    with pytest.raises(ValueError) as error:
>>        overlap.read_rectangles(['a 1'])
>>    assert "Incorrect number of coordinates for 'a 1'" in str(error)
>>
>>    with pytest.raises(ValueError) as error:
>>        overlap.read_rectangles(['a'])
>>    assert "Incorrect number of coordinates for 'a'" in str(error)
>> ```
>> ```python
>># overlap.py
>>def read_rectangles(rectangles: Iterable[str]) -> dict[str, list[float]]:
>>    result = {}
>>    for rectangle in rectangles:
>>        name, *coords = rectangle.split()
>>        try:
>>            value = [float(c) for c in coords]
>>        except ValueError:
>>            raise ValueError(f"Non numeric value provided as input for '{rectangle}'")
>>
>>        if len(value) != 4:
>>            raise ValueError(f"Incorrect number of coordinates for '{rectangle}'")
>>
>>        # make sure x1 <= x2, value = [x1, y1, x2, y2]
>>        value[0], value[2] = min(value[0], value[2]), max(value[0], value[2])
>>        value[1], value[3] = min(value[1], value[3]), max(value[1], value[3])
>>        result[name] = value
>>    return result
>> ```
>> Notice how the test code is much longer than the source code, this is
>> typical for well-tested code.
> {: .solution}
{: .challenge}

A good question is, do we need to update our end-to-end test to cover all these
pathological cases?  The answer is no (for most).  We already know our `read_rectangles`
will handle the incorrect number of coordinates by throwing an informative error
so it would be redundant to see if the main method has the same behavior.  However,
it would be useful to document what happens if an empty input file is supplied.
Maybe you want `read_rectangles` to return an empty dict but the main method should
warn the user or fail.

The decision not to test something in multiple places is more important than
being efficient with our time writing tests.  Say we want to change the message
printed for one of the improper input cases.  If the same function is tested
multiple places we need to update multiple tests that are effectively covering
the same feature.  Remember that tests are code and should be kept DRY.  Tests that
are hard to change don't get run and code eventually degrades back to a legacy version.

## Testing testing for overlap
We have arrived to the largest needed refactoring, the overlap code.  This is the
internals of the nested for loop.
```python
...
for blue_name, blue_coords in rectangles.items():
    # check if rects overlap
    result = '1'

    red_lo_x, red_lo_y, red_hi_x, red_hi_y = red_coords
    blue_lo_x, blue_lo_y, blue_hi_x, blue_hi_y = blue_coords

    if (red_lo_x >= blue_hi_x) or (red_hi_x <= blue_lo_x) or \
            (red_lo_y >= blue_hi_x) or (red_hi_y <= blue_lo_y):
        result = '0'
...
```
Like before, we want to write a failing test first and extract this method.
When that is in place we can start getting creative to test more interesting
cases.  Finally, to support our original goal (reporting the percent overlap)
we will change our return type to another rectangle.

{: .challenge}
> ### Red-Green-Refactor `rects_overlap`
> Extract the inner for loop code.  The signature should be:
>```python
>def rects_overlap(red, blue) -> bool: ...
>```
>> ## Solution
>> For testing, I'm using the simple input, when parsed from `read_rectangles`.
>> Notice that if we had used `read_rectangles` to do the parsing we would add a
>> dependency between that function and this one.  If we change (break) `read_rectangles`
>> this would break too even though nothing is wrong with `rects_overlap`.
>> However, uncoupling them completely doesn't capture how they interact in code.
>> Consider the drawbacks before deciding what to use.
>> ```python
>> # test_overlap.py
>>def test_rects_overlap():
>>    rectangles = {
>>        'a': [0, 0, 2, 2],
>>        'b': [1, 1, 3, 3],
>>        'c': [10, 10, 11, 11],
>>    }
>>
>>    assert overlap.rects_overlap(rectangles['a'], rectangles['a']) is True
>>    assert overlap.rects_overlap(rectangles['a'], rectangles['b']) is True
>>    assert overlap.rects_overlap(rectangles['b'], rectangles['a']) is True
>>    assert overlap.rects_overlap(rectangles['a'], rectangles['c']) is False
>> ```
>> ```python
>># overlap.py
>>def main(infile, outfile):
>>    rectangles = read_rectangles(infile)
>>
>>    for red_name, red_coords in rectangles.items():
>>        output_line = []
>>        for blue_name, blue_coords in rectangles.items():
>>            result = '1' if rects_overlap(red_coords, blue_coords) else '0'
>>
>>            output_line.append(result)
>>        outfile.write('\t'.join(output_line) + '\n')
>>
>>...
>>def rects_overlap(red, blue) -> bool:
>>    red_lo_x, red_lo_y, red_hi_x, red_hi_y = red
>>    blue_lo_x, blue_lo_y, blue_hi_x, blue_hi_y = blue
>>
>>    if (red_lo_x >= blue_hi_x) or (red_hi_x <= blue_lo_x) or \
>>            (red_lo_y >= blue_hi_x) or (red_hi_y <= blue_lo_y):
>>        return False
>>
>>    return True
>> ```
> {: .solution}
{: .challenge}

Now we can really put the function through it's paces.  Here are some
rectangles to guide your testing:
```

     ┌───┐     ┌──┬──┐   ┌──────┐    ┌─┐    
     │  ┌┼─┐   │  │  │   │ ┌──┐ │    └─┼─┐  
     └──┼┘ │   └──┴──┘   └─┼──┼─┘      └─┘  
        └──┘               └──┘             
```
For each, consider swapping the red and blue labels and rotating 90 degrees.
Rotating a coordinate 90 degrees clockwise is simply swapping x and y while
negating the new y value.  If you thought the rotation function would be useful
elsewhere, you could add it to your script, but for now we will keep it in our
pytest code.  First, write some failing unit tests of our new helper function:
```python
# test_overlap.py
def test_rotate_rectangle():
    rectangle = [1, 2, 3, 3]

    rectangle = rotate_rectangle(rectangle)
    assert rectangle == [2, -3, 3, -1]

    rectangle = rotate_rectangle(rectangle)
    assert rectangle == [-3, -3, -1, -2]

    rectangle = rotate_rectangle(rectangle)
    assert rectangle == [-3, 1, -2, 3]

    rectangle = rotate_rectangle(rectangle)
    assert rectangle == [1, 2, 3, 3]
```
Writing out the different permutations was challenging (for me, at least),
probably related to having unnamed attributes for our rectangle as a list of
numbers...  Then you need to produce the correct rectangle where `x1 <= x2`.
```python
# test_overlap.py
def rotate_rectangle(rectangle):
    x1, y1, x2, y2 = rectangle
    x1, y1 = y1, -x1
    x2, y2 = y2, -x2

    # make sure x1 <= x2, value = [x1, y1, x2, y2]
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)

    return [x1, y1, x2, y2]
```
Notice this is *still* in our test file.  We don't want it in our project and
it's just a helper for our tests, we could use it elsewhere in later tests.
Since the function is non-trivial we also have it tested.  For helper functions
that mutate or wrap inputs, you *could* have them non-tested but beware the
simple helper function may evolve into something more complex!

{: .challenge}
> ### Test the first overlap orientation
> Start with the first type of overlap (over corners).  Set one rectangle to
> `(-1, -1, 1, 1)` and place the second rectangle.  Transform the second rectangle by
> rotating it around the origin 3 times and test the `rects_overlap` function
> for each overlap and red/blue assignment. Hint: pytest code is still python!
>> ## Solution
>> With our `rotate_rectangle` function in hand, the test function needs to test
>> `rects_overlap` twice (swapping arguments each time) then rotate the second
>> rectangle.  Note the choice of centering the first rectangle on the origin
>> makes it rotationally invariant.  Here is a test function, notice that the
>> assert statements have a clear message as it would otherwise be difficult to
>> tell when a test failed.
>> ```python
>>def test_rects_overlap_permutations():
>>    rectangle_1 = [-1, -1, 1, 1]
>>    rectangle_2 = [0, 0, 2, 3]
>>    result = True
>>
>>    for i in range(4):
>>        assert overlap.rects_overlap(rectangle_1, rectangle_2) == result, (
>>            f"Failed rects_overlap({rectangle_1}, {rectangle_2}) "
>>            f"on rotation {i}")
>>
>>        assert overlap.rects_overlap(rectangle_2, rectangle_1) == result, (
>>            f"Failed rects_overlap({rectangle_2}, {rectangle_1}) "
>>            f"on rotation {i}")
>>
>>        rectangle_2 = rotate_rectangle(rectangle_2)
>> ```
>> I declare the result to simplify parameterize introduced next.
> {: .solution}
{: .challenge}

We have `test_rects_overlap_permutations` written for one rectangle. You may
be tempted to copy and paste the function multiple times and declare a different
`rectangle_2` and result for each orientation we came up with above.  To avoid
code duplication, you could make our test a helper function, but pytest has
a better builtin option, `parameterize`.

## `pytest.mark.parametrize`
Parametrizing a test function allows you to easily repeat its execution with
different input values.  Using parameters cuts down on duplication and can
vastly increase the input space you can explore by nesting parameters.

Let's work on testing the following function:
```python
def square_sometimes(value, condition):
    if condition:
        raise ValueError()
    return value ** 2
```
Fully testing this function requires testing a variety of `value`s and ensuring
when `condition is True` the function instead raises an error.  Here are a few
tests showing how you could write multiple test functions:
```python
def test_square_sometimes_number_false():
    assert square_sometimes(4, False) == 16

def test_square_sometimes_number_true():
    with pytest.raises(ValueError):
        square_sometimes(4, True)

def test_square_sometimes_list_false():
    assert square_sometimes([1, 1], False) == [1, 1, 1, 1]

def test_square_sometimes_list_true():
    with pytest.raises(ValueError):
        square_sometimes([1, 1], True)
...
```

Hopefully that code duplication is making your skin crawl!  Maybe instead you
write a helper function to check the value of condition:
```python
def square_sometimes_test_helper(value, condition, output):
    if condition:
        with pytest.raises(ValueError):
            square_sometimes(value, condition)
    else:
        assert square_sometimes(value, condition) == output
```

Then you can replace some of your tests with the helper calls:
```python
def test_square_sometimes_number():
    square_sometimes_test_helper(4, False, 16)
    square_sometimes_test_helper(4, True, 16)

def test_square_sometimes_list():
    square_sometimes_test_helper([1, 1], False, [1, 1, 1, 1])
    square_sometimes_test_helper([1, 1], True, [1, 1, 1, 1])
...
```

You could imagine wrapping the helper calls in a loop and you'd basically have
a parametrized test.  Using `pytest.mark.parametrize` you'd instead have:
```python
@pytest.mark.parametrize(
    'value,output',
    [
        (4, 16),
        ([1,1], [1,1,1,1]),
        ('asdf', 'asdfasdf'),
    ]
)
@pytest.mark.paramterize('condition', [True, False])
def test_square_sometimes(value, condition, output):
    if condition:
        with pytest.raises(ValueError):
            square_sometimes(value, condition)
    else:
        assert square_sometimes(value, condition) == output
```

pytest will generate the cross product of all nested parameters, here producing
6 tests.  Notice how there is no code duplication and if you come up with another
test input, you just have to add it to the 'value,output' list; testing each
condition will automatically happen.  Compared with coding the loops yourself,
pytest generates better error reporting on what set of parameters failed.  Like
most of pytest, there is a lot more we aren't covering like mixing parameters
and fixtures.

Here is the parameterized version of `test_rects_overlap_permutations`.  I
added the unicode rectangle images because I already made them above and it
seemed like a shame to not reuse.  Normally I wouldn't spend time making them
and instead use a text descriptor, e.g. "Corners overlap".
```python
rectangle_strs = ['''
┌───┐  
│  ┌┼─┐
└──┼┘ │
   └──┘''','''
┌──┬──┐
│  │  │
└──┴──┘''','''
┌──────┐
│ ┌──┐ │
└─┼──┼─┘
  └──┘''','''
┌─┐  
└─┼─┐
  └─┘''','''
┌─┐  
└─┘ ┌─┐
    └─┘''','''
┌──────┐
│  ┌─┐ │
│  └─┘ │
└──────┘''',
                  ]
@pytest.mark.parametrize(
    "rectangle_2,rectangle_str,result",
    [
        ([0, 0, 2, 3], rectangle_strs[0], True),
        ([1, -1, 2, 1], rectangle_strs[1], False),
        ([0, -2, 0.5, 0], rectangle_strs[2], True),
        ([1, 1, 2, 2], rectangle_strs[3], False),
        ([2, 2, 3, 3], rectangle_strs[4], False),
        ([0, 0, 0.5, 0.5], rectangle_strs[5], True),
    ])
def test_rects_overlap_permutations(rectangle_2, rectangle_str, result):
    rectangle_1 = [-1, -1, 1, 1]

    for i in range(4):
        assert overlap.rects_overlap(rectangle_1, rectangle_2) == result, (
            f"Failed rects_overlap({rectangle_1}, {rectangle_2}) "
            f"on rotation {i}. {rectangle_str}")

        assert overlap.rects_overlap(rectangle_2, rectangle_1) == result, (
            f"Failed rects_overlap({rectangle_2}, {rectangle_1}) "
            f"on rotation {i}. {rectangle_str}")

        rectangle_2 = rotate_rectangle(rectangle_2)
```
Now failed tests will also show the image along with information to recreate
any failures.  Running the above should fail... Time to get back to green.

Note that with parameterize, each set of parameters will be run, e.g. failing
on the second rectangle will not affect the running on the third rectangle.

{: .challenge}
> ### Fix the code
> Work on the source code for `rects_overlap` until all the code passes.
> Hint: try `pytest --pdb test_overlap.py` which launches pdb at the site of the
> first assertion error.
>> ## Solution
>> Only one set of rectangles is failing and it's on the first rotation.  That
>> should indicate our tests are working properly and perhaps there is a more
>> subtle bug hiding in our code.  Hopefully it didn't take too long to see there
>> is a copy paste error in the if statement.
>> ```python
>>    if (red_lo_x >= blue_hi_x) or (red_hi_x <= blue_lo_x) or \
>>            (red_lo_y >= blue_hi_x) or (red_hi_y <= blue_lo_y):
>>                               # ^ should be y!
>> ```
>> Notice that all our other tests didn't exercise this condition.  If we weren't
>> rotating each case we would have also missed this.  At least the fix is easy.
> {: .solution}
{: .challenge}

In contrast to the last implementation change we made (removing the trailing
tab character) this bug fix is more serious.  You have revealed an error in
code that was previously published!  Were this a real example, you should open
an issue with the original code and consider rerunning any dependent analyses
to see if results fundamentally change.  It may be by chance that branch of
code never actually ran and it didn't matter if it were wrong.  Maybe only 1%
of cases were miscalled. That would require just a new version to patch the
issue.  Larger changes in the results may necessitate a revision or retraction
of the original publication.

{% include links.md %}

