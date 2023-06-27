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
Software testing involves the process of executing the software to discover any discrepencies between the expect behavior and the actual behavior of the software. Therefore the goal of software testing is to uncover defects, bugs, or errors in the software, making it more reliable, stable, and usable. Testing is the most widely used technique for the quality assuarance of software. However, testing cannot prove that a software is correct, unless you execute the software with all the possible inputs and verify that th produced outputs are correct accoriding to the expected behavior. Obviously this is not practical. Thus the focus of testing is to executed the software with a set of "good" inputs and verify the produced outputs are correct, and there by improving the confidance about the program. Therefore, testing typically involves the following activities.
1. Test input design.
2. Test execution.
3. Checking the correctness of test outputs.

# When to test?
Earlier a bug is detected, it is less costly to fix them. For example, a bug detected and fixed during coding is 50 times cheaper than detecting and fixing it after the software is deployed. Thus, executing tests as soon as possible would be benficial in the long run. Theoritically, tests can be created and executed even before the functional code is written. This is what is acually done in Test Driven Development (TDD) which we discuss little later. Ultimately, the bottom line is creating and executing tests should not be an afterthought. It should be an activity that should go hand-in-hand with development.

{% include links.md %}

