---
title: "Working with Legacy Code"
teaching: 0
exercises: 0
questions:
- "What is legacy code?"
- "Why should you test legacy code before changing it?"
objectives:
- "Understand the sample legacy code"
- "Set up an end-to-end test"
- "Use TDD to begin refactoring"
keypoints:
- "Legacy code is code without tests. It's extremely challenging to change code that doesn't have tests."
- "At the very least you should have an end-to-end test when starting to change code."
- "Try to add tests before making changes, work in small steps."
- "Having tests pass doesn't mean your code is correct."
---
# Meet the legacy code project

Imagine you are joining a new lab and have inherited a script from
another grad student or published paper.  It takes in a file with coordinates
of rectangles and produces a matrix where the value at index `i,j == 1` if rectangle
`i` overlaps with rectangle `j`, and 0 otherwise.  Here is the starting script

```python
import sys


# read input file
infile = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], 'w')

# build rectangle struct
dict = {}
for line in infile:
    name, *coords = line.split()
    dict[name] = [int(c) for c in coords]

for red_name, red_coords in dict.items():
    for blue_name, blue_coords in dict.items():
        # check if rects overlap
        result = '1'

        red_lo_x, red_lo_y, red_hi_x, red_hi_y = red
        blue_lo_x, blue_lo_y, blue_hi_x, blue_hi_y = blue

        if (red_lo_x >= blue_hi_x) or (red_hi_x <= blue_lo_x) or \
                (red_lo_y >= blue_hi_x) or (red_hi_y <= blue_lo_y):
            result = '0'

        outfile.write(result + '\t')
    outfile.write('\n')

infile.close()
outfile.close()
```

{: .challenge}
> ## Critique the published version
>
> The code above is certainly not perfect.  Name 3 issues with the code and (to
> be nice) 1 good thing.  
> Consider if the problems will affect testing or can
> be addressed with testing.
>>
> > ## Solution
> > Starting with good things:
> > 1. Variable names are fairly clear and properly formatted
> > 2. Comments are used properly
> > 3. Runs without errors
> > 4. Dependencies are handled (no dependencies)
> >
> > And some of the issues:
> > 1. Unable to import
> > 2. No encoding specified on open
> > 3. Redundant execution in main loop
> > 4. Several assumptions made without checking or asserting correctness (hi vs. low, int coords)
> > 5. Shadowing `dict` keywords
> > 6. Trailing tab on the end of each output line
> > 7. Not using context managers for file io
> > And likely many more!
> {: .solution}
{: .challenge}

Now your advisor wants you to take this code, make it run twice as fast and
instead of just saying if there is overlap, output the percent the two areas
overlap!  You think you need to introduce a `Rectangle` object, but how can you
make changes without adding to this pile of code?

# A simple end-to-end test

The first step to making legacy code into tested code is to add a test.

> Legacy code has many negative connotations.  Here we are using it as defined
> by Micheal Feathers in [Working Effectively with Legacy Code](https://learning.oreilly.com/library/view/working-effectively-with/0131177052/).
> "To me, legacy code is simply code without tests."  All the other bad features
> of legacy code stem from a lack of testing.

Often the best test to write first is an end-to-end or integration test.  These
kinds of tests exercise an entire codebase with some "representative" input and
ensure the correct output is produced.  You probably use a test like this, even
if you don't have it automated or formalized.  End-to-end tests ensure the code
is working in its entirety and giving the same output.  They are often not
ideal since with non-trivial systems they can take significant time or
resources to run and verify.  It is also difficult to test many corner
cases without testing smaller parts of a codebase.

Like all tests, passing does not verify correctness just that the tests are not
failing.  Still, it is reassuring that some larger refactoring isn't breaking
published code!  Let's start with this simple input file (the header is just
for display here):
```input.txt
#name	x1	y1	x2	y2
a	0	0	2	2
b	1	1	3	3
c	10	10	11	11
```
Clearly rectangles a and b overlap while c is far away.  As output, we expect
the following matrix:
```output.txt
1	1	0	
1	1	0	
0	0	1	
```

{: .challenge}
> ## Critique the sample input
>
> What are some issues with the sample input?  Is the result still useful?
>>
> > ## Solution
> > The input doesn't test rectangles where `x != y` or really challenge more
> > interesting cases (overlap at a point, a line, overlap exactly, etc).
> > 
> > The result can still be useful *if it fails*.  Knowing something that was
> > working has stopped working can notify you an error is present.  However,
> > having this test pass doesn't make your code correct!
> {: .solution}
{: .challenge}

Given the `input.txt` and `output.txt` files, how can we test the function?
You may be used to doing this manually, with the following commands:
```bash
# run the command
python overlap_v0.py input.txt new_output.txt
# view the result
cat new_output.txt
# compare the outputs
cmp output.txt new_output.txt
```

On every change to the file, you can press the up arrow or `Ctrl+p` to recall
a command and rerun it.  Bonus points if you are using multiple terminal sessions
or a multiplexer.  A better setup is to formalize this test with a script you
can repeatedly run.  Tools like [entr](https://github.com/eradman/entr) or your
text editor can automatically run the test when your files change.  Here is a
simple end-to-end test of the initial script:
```bash
#!/bin/bash

# run the command
python overlap_v0.py input.txt new_output.txt
# compare the outputs
cmp output.txt new_output.txt && echo 'passes'
```
When cmp is successful (no difference between files) `passes` will be echoed to
the terminal.  When it fails the byte and line number that differs will be
printed.  This script can be run with CI and should act as the final step to
ensure your outputs are as expected.  Think of tests like a funnel: you want to
run quick tests frequently to catch most bugs early, on every file write. Slower
tests can run prior to a git commit to catch the bugs that escaped the first round.
Finally, the slowest, most thorough tests run via CI/CD on a PR and should
catch a minority of bugs.  We will run our end to end test after making major changes.

You can also add more test files to this script but we want to move to a better
testing framework ASAP!

{% include links.md %}

