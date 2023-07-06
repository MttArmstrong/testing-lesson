---
title: "Introduction"
teaching: 0
exercises: 0
questions:
- "Why do we test software?"
objectives:
- "Understand what is testing"
- "Understand the goals of testing"
keypoints:
- "Testing improves confidence about your code. It doesn't prove that code is correct."
---
# What is testing?
Software testing involves the process of executing the software to discover any
discrepancies between the expect behavior and the actual behavior of the
software. Therefore the goal of software testing is to uncover defects, bugs,
or errors in the software, making it more reliable, stable, and usable. Testing
is the most widely used technique for the quality assurance of software.
However, testing cannot prove that a software is correct, unless you execute
the software with all the possible inputs and verify that the produced outputs
are correct according to the expected behavior. Obviously this is not
practical. Thus the focus of testing is to executed the software with a set of
"good" inputs and verify the produced outputs are correct, and thereby
improving the confidence about the program. Testing typically
involves the following activities.
1. Test input design: It is not practical to test software with all the
   possible inputs that it can get. Therefore we need to select a subset of
   inputs that are likely to detect bugs and would help to increase our confidence
   in the program. One approach is to randomly select inputs from the input space.
   While this can be an effective method, it has the tendency to miss corner cases
   where most mistakes are made. Therefore we will be discussing several
   approaches used for developing test inputs.
2. Test execution: tests need should be executed multiple times when code is
   changed some way, when implementing new features or when fixing bugs. Thus
   execution of tests should be automated as much as possible with the help of
   test frameworks (i.e. test tools) and CI/CD infrastructure.
3. Checking the correctness of test outputs: this is done by comparing the
   output of test cases with the expected output of the software and should be
   automated as well.

# When to test?
The earlier a bug is detected, the less costly it is to fix. For example, a bug
detected and fixed during coding is 50 times cheaper than detecting and fixing
it after the software is deployed. Imagine the cost of publishing code with a bug!
However, executing tests as soon as possible is also beneficial immediately.
When you discover a bug after changing 3 lines of code, you know exactly where
to look for a mistake.  Theoretically, tests can be created and executed even
before the functional code is written. This approach is called Test
Driven Development (TDD) and we will discuss it a little later.  Ultimately,
the bottom line is creating and executing tests should not be an afterthought.
It should be an activity that should go hand-in-hand with development.

{% include links.md %}

