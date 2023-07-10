---
title: "Testing Big Changes"
teaching: 20
exercises: 30
questions:
- "What does it mean if you have to change a lot of tests while adding features?"
- "What are the advantages of testing an interface?"
objectives:
- "Add a `Rectangle` class"
- "Learn how to use TDD when making large changes to code"
keypoints:
- "Changing a lot of test code for minor features can indicate your tests are not DRY and heavily coupled."
- "Testing a module's interface focuses tests on what a user would typically observe.  You don't have to change as many tests when internal change."
---

# Making big changes
With this fairly simple example, we have fully tested our codebase.  You
can rest easy knowing the code is working as well as you've tested it.  We have
made a few changes to what the legacy code used to do and even found a bug.
Still, our code functions basically the same as it did (perhaps more correct).
How does testing help when we need to add features and really change code?

The answer depends on how well you tested the interface vs the implementation.
If your tests are full of duplication, you will have to change *a lot* of the
test code.  Now you would want to make a commit of this version of the code and
get ready to shake things up.  Even if it seems like you are spending a lot of
time messing with the tests, at the end once everything passes you should
have the same confidence in your code.

## Testing the interface vs the implementation
Consider a database object that performs a query and then can return a result
as separate function calls.  This is not the best design but it is a useful example
```python
class MyDB():
    self._result: list
...
    def query(self, something):
        ...
        self._result = result
    def get_result(self):
        return list(self._result)
```
When you call `query` the result is saved in the `_result` attribute of the
instance.  When you get the result, a copy is returned as a list.

Consider the following two tests for query:
```python
def test_query_1():
    my_db = MyDB()
    my_db.query('something')
    assert my_db._result == ['a result']

def test_query_2():
    my_db = MyDB()
    my_db.query('something')
    assert my_db.get_result() == ['a result']
```
Currently, they do the same thing.  One could argue the first option is better
because it only tests the query function while the second is also exercising
`get_result`.  By convention, the underscore in front of the attribute in python
means it is private and you shouldn't really access it.  Since "private" is
kind of meaningless in python, a better description is that it is an implementation
detail which could change.  Even if it weren't private, the first test is testing
internal implementation (calling `query` sets the `result` attribute) while the
second is testing the interface (call `query` first and `get_result` will give
you the result as a list).

Think about what happens if the `_result` attribute is changed from a list to
a set, or dictionary.  This is valid since no one should really use `_result`
outside of the class, but in terms of testing, `test_query_1` would break while
`test_query_2` still passes, *even if the code is correct*.  This is annoying
because you have to change a lot of test code but it is also dangerous.  Tests
that fail for correct code encourage you to run tests less often and can cause
code and tests to diverge.  **Where possible, test to the interface**.

## Returning a new rectangle
Back to our rectangles, let's change our `rects_overlap` to return a new rectangle
when the arguments overlap, and None when they do not.

### Red
We will start with the basic `test_rects_overlap`
```python
# test_overlap.py

def test_rects_overlap():
    rectangles = {
        'a': [0, 0, 2, 2],
        'b': [1, 1, 3, 3],
        'c': [10, 10, 11, 11],
    }

    assert overlap.rects_overlap(rectangles['a'], rectangles['a']) == [0, 0, 2, 2]
    assert overlap.rects_overlap(rectangles['a'], rectangles['b']) == [1, 1, 2, 2]
    assert overlap.rects_overlap(rectangles['b'], rectangles['a']) == [1, 1, 2, 2]
    assert overlap.rects_overlap(rectangles['a'], rectangles['c']) is None
```
We are failing since the first call returns True instead of our list.

### Green
Simple enough, instead of False we should return None and instead of True we
need to make a new rectangle with the smaller of the coordinates.
```python
# overlap.py
def rects_overlap(red, blue) -> list[float] | None:
    red_lo_x, red_lo_y, red_hi_x, red_hi_y = red
    blue_lo_x, blue_lo_y, blue_hi_x, blue_hi_y = blue

    if (red_lo_x >= blue_hi_x) or (red_hi_x <= blue_lo_x) or \
            (red_lo_y >= blue_hi_y) or (red_hi_y <= blue_lo_y):
        return None

    x1 = max(red_lo_x, blue_lo_x)
    x2 = min(red_hi_x, blue_hi_x)
    y1 = max(red_lo_y, blue_lo_y)
    y2 = min(red_hi_y, blue_hi_y)
    return [x1, y1, x2, y2]
```
We are passing the new `test_rects_overlap` but failing another 6 tests!  That's
because many tests are still testing the old behavior.  If you have kept tests
DRY and not tested the implementation, this should be quick to fix, otherwise
take the opportunity to refactor your tests!

For us, the `test_rects_overlap_permutation` will accept a rectangle as the result.
On each loop iteration, we need to rotate the result rectangle.  Since `None` is
a valid rectangle now, `rotate_rectangle` needs to handle it appropriately.
Here is the finished test method:
```python
@pytest.mark.parametrize(
    "rectangle_2,rectangle_str,result",
    [
    ([0, 0, 2, 3], rectangle_strs[0], [0, 0, 1, 1]),
    ([1, -1, 2, 1], rectangle_strs[1], None),
    ([0, -2, 0.5, 0], rectangle_strs[2], [0, -1, 0.5, 0]),
    ([1, 1, 2, 2], rectangle_strs[3], None),
    ([2, 2, 3, 3], rectangle_strs[4], None),
    ([0, 0, 0.5, 0.5], rectangle_strs[5], [0, 0, 0.5, 0.5]),
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
        result = rotate_rectangle(result)
```

### Refactor
Since our tests are fairly small and not too coupled to the implementation
we don't have to change anything.  If you *had* written the permutation function
as 48 separate tests, it would make sense to refactor that while updating
the return values!

### End-to-end test?
You may be surprised our end to end test is still passing.  This is a feature of
python more than any design of our system.  The line
```python
result = '1' if rects_overlap(red_coords, blue_coords) else '0'
```
works properly because `None` evaluates as False while a non-empty list evaluates
as True in a boolean context.

Take a minute to reflect on this change.  Creating a new rectangle is non-trivial,
it would be easy to mix up a min or max or introduce a copy/paste error.  Since
we have tests, we can be confident we made this change correctly.  With our
end-to-end test we further know that our main method is behaving exactly the same
as well.

## A `Rectangle` Object
Any decent OOP developer would be pulling their hair over using a list of 4
numbers as a rectangle when you could have a full object hierarchy!  We have
another design decision before we really dig into the changes, how much should
we support the old format of a rectangle as a list of numbers?  Coming from
strict, static typing you may be inclined to say "not at all" but python gains
power from its duck typing.

Consider adding support for comparing a rectangle to a list of numbers. 
If you support lists fully we can maintain the same tests.  However, a user
may not expect a list to equal a rectangle and could cause problems with other code.
Since we want to focus on writing tests instead of advanced python we will try
to replace everything with rectangles.  In real applications you may want to
transiently add support for comparisons to lists so the tests pass to confirm
any other logic is sound.  After the tests are converted to rectangles you
would alter your `__eq__` method to only compare with other rectangles.

Without getting carried away, we want our rectangles to support
- Construction from a list of numbers or with named arguments
- Comparison with other rectangles, primarily for testing
- Calculation of area
- An overlap function with a signature like `def overlap(self, other: Rectangle) -> Rectangle`.

Afterwards, our main loop code will change from
```python
result = '1' if rects_overlap(red_coords, blue_coords) else '0'
# to
overlap_area = red_rectangle.overlap(blue_rectangle).area()
```
We will also need to change code in our `read_rectangles` and `rects_overlap`
functions as well as `main`.  

{: .challenge}
> ### Order of Operations
> Should we start with converting our existing tests or making new tests for
> the rectangle object?
>> ## Solution
>> It's better to work from bottom up, e.g. test creating a rectangle before
>> touching `read_rectangles`.
>>
>> Imaging a red, green, refactor cycle where you start with updating `read_rectangles`
>> to return a (yet unimplemented) Rectangle object.  First change your tests to
>> expect a Rectangle to get them failing.  The problem is to get them passing
>> you need to add code to create a rectangle and test for equality.  It's possible
>> but then you don't have unit tests for those functions.  Furthermore, that
>> breaks with the idea that TDD cycles should be short; you have to add a
>> lot of code to get things passing!
> {: .solution}
{: .challenge}

### TDD: Creating Rectangles
Starting with a new test, we will simply check that a new rectangle can be
created from named arguments.
```python
# test_overlap.py
def test_create_rectangle_named_parameters():
    assert overlap.Rectangle(x1=1.1, x2=2, y1=4, y2=3)
```
Fails because there is no Rectangle object yet.  To get green, we are going
to use a python dataclass:
```python
# overlap.py
from dataclasses import dataclass

@dataclass
class Rectangle:
    x1: float
    y1: float
    x2: float
    y2: float
```
The `dataclass` produces a default `__init__` and `__eq__`.

How about rectangles from lists?
```python
# test_overlap.py
def test_create_rectangle_from_list():
    assert overlap.Rectangle.from_list([1.1, 4, 2, 3])
```
Here we are using the order of parameters matching the existing implementation.
The code uses a bit of advanced python but should be clear:

```python
# overlap.py
class Rectangle:
    # ...
    @classmethod
    def from_list(cls, coordinates: list[float]):
        x1, y1, x2, y2 = coordinates
        return cls(x1=x1, y1=y1, x2=x2, y2=y2)
```

And let's add a test for the incorrect number of values in the list:
```python
# test_overlap.py
def test_create_rectangle_from_list_wrong_number_of_args():
    with pytest.raises(ValueError) as error:
        overlap.Rectangle.from_list([1.1, 4, 2])
    assert "Incorrect number of coordinates " in str(error)
    with pytest.raises(ValueError) as error:
        overlap.Rectangle.from_list([1.1, 4, 2, 2, 2])
    assert "Incorrect number of coordinates " in str(error)
```
And update the code.
```python
# overlap.py
class Rectangle:
    # ...
    @classmethod
    def from_list(cls, coordinates: list[float]):
        if len(coordinates) != 4:
            raise ValueError(f"Incorrect number of coordinates for '{coordinates}'")
        x1, y1, x2, y2 = coordinates
        return cls(x1=x1, y1=y1, x2=x2, y2=y2)
```
Notice that we now have some code duplication since we use the same check in 
`read_rectangles`.  But we can't remove it until we start using the Rectangle
there.

### TDD: Testing equality
Instead of checking our rectangles are just not None, let's see if they are
what we expect:

```python
# test_overlap.py
def test_create_rectangle_named_parameters():
    assert overlap.Rectangle(1.1, 4, 2, 3) == overlap.Rectangle(1.1, 3, 2, 4)
    assert overlap.Rectangle(x1=1.1, x2=2, y1=4, y2=3) == overlap.Rectangle(1.1, 3, 2, 4)


def test_create_rectangle_from_list():
    assert overlap.Rectangle.from_list([1.1, 4, 2, 3]) == overlap.Rectangle(1.1, 3, 2, 4)
```
Here we use unnamed parameters during initialization to check for equality. 
The order of attributes in the dataclass determines the order of assignment.
Since that's fairly brittle, consider adding `kw_only` for production code.

This fails not because of an issue with `__eq__` but the `__init__`, we aren't
ensuring our expected ordering of `x1 <= x2`.  You could overwrite `__init__`
but instead we will use a `__post_init__` to valid the attributes.
```python
# overlap.py
@dataclass
class Rectangle:
    x1: float
    y1: float
    x2: float
    y2: float

    def __post_init__(self):
        self.x1, self.x2 = min(self.x1, self.x2), max(self.x1, self.x2)
        self.y1, self.y2 = min(self.y1, self.y2), max(self.y1, self.y2)
```
Note this also fixes the issue with `from_list` as it calls `__init__` as well.
If we later decide to add an attribute like `color` the `__init__` method would
update and our `__post_init__` would function as intended.

### TDD: Calculate Area
For area we can come up with a few simple tests:
```python
# test_overlap.py
def test_rectangle_area():
    assert overlap.Rectangle(0, 0, 1, 1).area() == 1
    assert overlap.Rectangle(0, 0, 1, 2).area() == 2
    assert overlap.Rectangle(0, 1, 2, 2).area() == 2
    assert overlap.Rectangle(0, 0, 0, 0).area() == 0
    assert overlap.Rectangle(0, 0, 0.3, 0.3).area() == 0.09
    assert overlap.Rectangle(0.1, 0, 0.4, 0.3).area() == 0.09
```
The code shouldn't be too surprising:
```python
# overlap.py
@dataclass
class Rectangle:
    ...

    def area(self):
        return (self.x2-self.x1) * (self.y2-self.y1)
```
But you may be surprised that the last assert is failing, even though the second
to last is passing.  Again we are struck by the limits of floating point precision.

{: .challenge}
> ### Fix the tests
> Fix the issue of floating point comparison.  Hint, look up `pytest.approx`.
>> ## Solution
>> ```python
>>    assert overlap.Rectangle(0.1, 0, 0.4, 0.3).area() == pytest.approx(0.09)
>> ```
>> To be thorough, you should approximate the line above as well.  While it
>> doesn't fail here, a different machine may have different precision.
> {: .solution}
{: .challenge}

### TDD: Overlap
Now we have the challenge of replacing the `rects_overlap` function with
a Rectangle method with the following signature `def overlap(self, other: Rectangle) -> Rectangle`.

> ### Red, green, refactor
> Perform an iteration of TDD to add the `overlap` method to `Rectangle`.  Hint,
> start with only the `test_rects_overlap` test for now.
>> ## Solution
>> ### Red
>> ```python
>> # test_overlap.py
>> def test_rectangle_overlap():
>>     rectangles = {
>>         'a': overlap.Rectangle(0, 0, 2, 2),
>>         'b': overlap.Rectangle(1, 1, 3, 3),
>>         'c': overlap.Rectangle(10, 10, 11, 11),
>>     }
>> 
>>     assert rectangles['a'].overlap(rectangles['a']) == overlap.Rectangle(0, 0, 2, 2)
>>     assert rectangles['a'].overlap(rectangles['b']) == overlap.Rectangle(1, 1, 2, 2)
>>     assert rectangles['b'].overlap(rectangles['a']) == overlap.Rectangle(1, 1, 2, 2)
>>     assert rectangles['a'].overlap(rectangles['c']) is None
>> ```
>> ### Green
>> You can copy most of the current code to the new method with changes to variable names.
>> ```python
>> # overlap.py
>> class Rectangle:
>>     ...
>> 
>>     def overlap(self, other):
>>         if (self.x1 >= other.x2) or \
>>                 (self.x2 <= other.x1) or \
>>                 (self.y1 >= other.y2) or \
>>                 (self.y2 <= other.y1):
>>             return None
>> 
>>         return Rectangle(
>>             x1=max(self.x1, other.x1),
>>             y1=max(self.y1, other.y1),
>>             x2=min(self.x2, other.x2),
>>             y2=min(self.y2, other.y2),
>>         )
>> ```
>> This was after refactoring to get rid of extra variables.  Since we can use
>> named arguments for new rectangles, we don't have to set `x1` separately for
>> clarity.
>> ### Refactor
>> While it's tempting to go forth and replace all `rects_overlap` calls now,
>> we need to work on some other tests first.
> {: .solution}
{: .challenge}

Wrapping up the overlap tests, we need to work on `rotate_rectangle` and the
overlap permutations function.  I think it makes sense to move our rotate
function to `Rectangle` now.  While we don't use it in our main method, the class
is becoming general enough to be used outside our current script.

```python
# test_overlap.py
def test_rotate_rectangle():
    rectangle = overlap.Rectangle(1, 2, 3, 3)

    rectangle = rectangle.rotate()
    assert rectangle == overlap.Rectangle(2, -3, 3, -1)

    rectangle = rectangle.rotate()
    assert rectangle == overlap.Rectangle(-3, -3, -1, -2)

    rectangle = rectangle.rotate()
    assert rectangle == overlap.Rectangle(-3, 1, -2, 3)

    rectangle = rectangle.rotate()
    assert rectangle == overlap.Rectangle(1, 2, 3, 3)
```
The special case when `Rectangle` is None is not handled anymore since you
can't call the method `rotate` on a None object.

```python
# overlap.py
class Rectangle:
    ...

    def rotate(self):
        return Rectangle(
            x1=self.y1,
            y1=-self.x1,
            x2=self.y2,
            y2=-self.x2,
        )
```
That is *much* cleaner than the last version.  Now to handle our `None` rectangles,
we will keep our `rotate_rectangle` helper function in the test code to wrap our
method dispatch and modify our test:
```python
# test_overlap.py
def rotate_rectangle(rectangle):
    if rectangle is None:
        return None
    return rectangle.rotate()

...
@pytest.mark.parametrize(
    "rectangle_2,rectangle_str,result",
    [
        (overlap.Rectangle(0, 0, 2, 3), rectangle_strs[0], overlap.Rectangle(0, 0, 1, 1)),
        (overlap.Rectangle(1, -1, 2, 1), rectangle_strs[1], None),
        (overlap.Rectangle(0, -2, 0.5, 0), rectangle_strs[2], overlap.Rectangle(0, -1, 0.5, 0)),
        (overlap.Rectangle(1, 1, 2, 2), rectangle_strs[3], None),
        (overlap.Rectangle(2, 2, 3, 3), rectangle_strs[4], None),
        (overlap.Rectangle(0, 0, 0.5, 0.5), rectangle_strs[5], overlap.Rectangle(0, 0, 0.5, 0.5)),
    ])
def test_rectangles_overlap_permutations(rectangle_2, rectangle_str, result):
    rectangle_1 = overlap.Rectangle(-1, -1, 1, 1)

    for i in range(4):
        assert rectangle_1.overlap(rectangle_2) == result, (
            f"Failed {rectangle_1}.overlap({rectangle_2}) "
            f"on rotation {i}. {rectangle_str}")

        assert rectangle_2.overlap(rectangle_1) == result, (
            f"Failed {rectangle_2}.overlap({rectangle_1}) "
            f"on rotation {i}. {rectangle_str}")

        rectangle_2 = rotate_rectangle(rectangle_2)
        result = rotate_rectangle(result)
```
And we can almost get rid of `rects_overlap` entirely.  It's not in our tests,
but we do use it in our main script.  The last function to change is `read_rectangles`.

### TDD: Read rectangles

> ### Red, green, refactor
> Perform an iteration of TDD to make the `read_rectangles` function return `Rectangle`s.
>> ## Solution
>> ### Red
>> It's best to start with the simple method then clean up failures on refactor.
>> ```python
>> # test_overlap.py
>> def test_read_rectangles_simple(simple_input):
>>     rectangles = overlap.read_rectangles(simple_input)
>>     assert rectangles == {
>>         'a': overlap.Rectangle(0, 0, 2, 2),
>>         'b': overlap.Rectangle(1, 1, 3, 3),
>>         'c': overlap.Rectangle(10, 10, 11, 11),
>>     }
>> ```
>> ### Green(ish)
>> The original code dealing with coordinate ordering and number of coordinates
>> can be removed as that's now handled by `Rectangle`.
>> ```python
>> # overlap.py
>> def read_rectangles(rectangles: Iterable[str]) -> dict[str, Rectangle]:
>>     result = {}
>>     for rectangle in rectangles:
>>         name, *coords = rectangle.split()
>>         try:
>>             value = [float(c) for c in coords]
>>         except ValueError:
>>             raise ValueError(f"Non numeric value provided as input for '{rectangle}'")
>> 
>>         result[name] = Rectangle.from_list(value)
>> 
>>     return result
>> ```
>> This is not a real green since other tests are failing, but at least
>> `test_read_rectangles_simple` is passing.
>> ### Refactor
>> You have to touch a lot of test code to get everything passing.  Afterwards
>> you can finally remove `rects_overlap`.
> {: .solution}
{: .challenge}

### TDD: Area of overlap
Recall we set out to do all this in order to output the area of the overlap of
a rectangle, instead of just `1` when rectangles overlap.  That change will
only affect our end to end test.  It may be prudent to extract the line
```python
result = '1' if red_rect.overlap(blue_rect) else '0'
```
into a separate function to exercise it more fully, but for now we will leave it.

> ### Red, green, refactor
> Perform an iteration of TDD to make the `main` function output the area of overlap.
>> ## Solution
>> ### Red
>> Our simple rectangles aren't the best for testing, but we are at least confident
>> our `area` method is well tested elsewhere.
>> ```python
>> # test_overlap.py
>> def test_end_to_end(simple_input):
>>     # initialize a StringIO with a string to read from
>>     infile = simple_input
>>     # this holds our output
>>     outfile = StringIO()
>>     # call the function
>>     overlap.main(infile, outfile)
>>     output = outfile.getvalue().split('\n')
>>     assert output[0] == '4.0\t1.0\t0'
>>     assert output[1] == '1.0\t4.0\t0'
>>     assert output[2] == '0\t0\t1.0'
>> ```
>> ### Green
>> ```python
>> # overlap.py
>> def main(infile, outfile):
>>     rectangles = read_rectangles(infile)
>> 
>>     for red_name, red_rect in rectangles.items():
>>         output_line = []
>>         for blue_name, blue_rect in rectangles.items():
>>             overlap = red_rect.overlap(blue_rect)
>>             result = str(overlap.area()) if overlap else '0'
>> 
>>             output_line.append(result)
>>         outfile.write('\t'.join(output_line) + '\n')
>> ```
>> ### Refactor
>> You may consider changing the formatting of the floats, but otherwise we are done!
> {: .solution}
{: .challenge}

## Big Conclusions
Take a breath, we are out of the deep end of rectangles for now.  At this point,
you may think TDD has slowed you down; sometimes a simple change of code required
touching a lot of test code just to have the same performance and functionality.
If that's your impression, consider the following:
- *Make new mistakes.* Nothing is worse than finding the same bug twice.  It is
  hard to appreciate preventing regressions on simple problems like we used here,
  but the overlap and rotate functions are close.  Once you've put in the time
  to write a test and are confident in the results, it is easier to make changes
  touching that code because the previous tests should still pass.  Without tests
  you may forget a negative sign or make a typo when refactoring and not notice
  until production.  Don't spend your time making the same mistakes, go forth
  and make new mistakes!
- *Go far, not fast.* There is a proverb "If you want to go fast, go alone. If
  you want to go far, go together."  The translation to testing breaks down
  because frequently having tests makes your work go much faster.  You are
  investing in code upfront with tests to limit debugging time later.
- *Work with a safety net.* Moving to a problem of larger complexity, working on
  legacy code can feel unsettling.  The entire system is too large and opaque to
  be sure everything works so you are left with an uneasy feeling that maybe a
  change you made introduced a bug.  With tests, you can sleep soundly knowing
  all your tests passed.  There may be bugs, but they are new bugs.

As you move into open source projects or work with multiple collaborators,
fully tested codebases make sure the quality of the project won't degrade as
long as tests are informative, fast, and fun to write.

{% include links.md %}

