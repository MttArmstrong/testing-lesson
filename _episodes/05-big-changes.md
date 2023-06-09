---
title: "Introduction"
teaching: 0
exercises: 0
questions:
- "Key question (FIXME)"
objectives:
- "First learning objective. (FIXME)"
keypoints:
- "First key point. Brief Answer to questions. (FIXME)"
---

# Making big changes
With this fairly simple example, we have basically tested our codebase fully.  You
can rest easy knowing the code is working as well as you've tested it.  We have
made a few changes to what the legacy code used to do and even found a bug.
Still, our code functions basically the same as it did (perhaps more correct).
How does testing help when we need to add features and really change code?

The answer depends on how well you tested the interface vs the implementation.
If your tests are full of duplication, you will have to change *a lot* of the
test code.  Now you would want to make a commit of this version of the code and
get ready to shake things up.  Even if it seems like you are spending a lot of
time messing with the tests, at the end once everything is passes you should
have the same confidence your code is working.

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
numbers as a rectangle when you could have a full object hierarchy!


{% include links.md %}

