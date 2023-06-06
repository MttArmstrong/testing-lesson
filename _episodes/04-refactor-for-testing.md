---
title: "Refactoring for Testing"
teaching: 0
exercises: 0
questions:
- "Why are long methods hard to test?"
objectives:
- "Learn some key refactoring methods to change code safely."
- "Modify the overlap script to support a Rectangle object."
keypoints:
- "Testable code is also good code!"
- "Changing code without tests can be dangerous.  Work slowly and carefully making only the simplest changes first."
- "Write tests with an adversarial viewpoint."
---
# Monolithic Main Methods

One of the smelliest code smells that new developers make is having a single
main method which spans several hundred (thousand?) lines.  Even if the code
is perfect, long methods are an anti-pattern because they require a reader of
the code to have exceptionally good working memory to understand the method.

Consider the following two codes:
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
how do you go about breaking it up?  Some IDEs have function for extracting
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
we have already decided on a name for the function, it's arguments and return
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
>> first and when the test_read_rectangles passes replace the code in the main
>> method.  Your end to end test should still pass and tell you if something is
>> wrong.  Note we can remove the comment because the function name is self documenting
> {: .solution}
{: .challenge}

### Refactor
With read rectangles pulled out, let's rename our `dict` to rectangles.  Since
the argument to our function can be any iterable of strings, we can also rename
it to `rectangles` and add a type annotation to show what we expect as input.
Now is also the time to add a doc string.  Make changes step-wise and run your
tests frequently.
```python
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
did think of this" instead of "why didn't I think of this", but it gets easier
with practice.

Think of all the ways this code could break, all the things that aren't tested,
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
> Look up `pytest.raises` for how to test an exception is thrown.
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
>> Notice how the test code is much longer than the actual source code, this is
>> typical for well-tested code
> {: .solution}
{: .challenge}

A good question is, do we need to update our end-to-end test to cover all these
pathological cases?  The answer is no (for most).  We already know our `read_rectangles`
will handle the incorrect number of coordinates by throwing an informative error
so it would be redundant to see if the main method has the same behavior.  However,
it would be useful to document what happens if an empty input file is supplied.

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
>>    assert rects_overlap(rectangles['a'], rectangles['a']) is True
>>    assert rects_overlap(rectangles['a'], rectangles['b']) is True
>>    assert rects_overlap(rectangles['b'], rectangles['a']) is True
>>    assert rects_overlap(rectangles['a'], rectangles['c']) is False
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
   ------        ---------       -------    ---                                
   |    |        |       |       |  |  |    | |                              
   |  ------     | ----- |       |  |  |    -----                          
   |  | |  |     | |   | |       -------      | |                                
   ------  |     --|---|--                    ---                            
      |    |       |   |                                                      
      ------       -----                                                      
```
For each, consider swapping the red and blue labels and rotating 90 degrees.

{% include links.md %}

