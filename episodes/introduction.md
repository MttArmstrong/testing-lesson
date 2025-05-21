---
title: "Introduction"
teaching: 10
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions 

- Why do we test software?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Understand what is testing
- Understand the goals of testing

::::::::::::::::::::::::::::::::::::::::::::::::



# What is testing?

Software testing is the process of executing the software to discover
any discrepancies between the expected behavior and the actual
behavior of the software. Thus, the focus of testing is to execute the
software with a set of "good" inputs and verify the produced outputs
match some expected outputs.

## Anatomy of a test

A software test typically involves the following activities.

1. Designing test inputs: It is not practical to test software with all 
   possible inputs. Therefore we need to select a subset of
   inputs that are likely to detect bugs and would help to increase our confidence
   in the program. One approach is to randomly select inputs from the input space.
   While this can be an effective method, it has the tendency to miss corner cases
   where most mistakes are made. Therefore we will be discussing several
   approaches used for developing test inputs.
2. Test execution: tests need should be executed multiple times when code is
   changed some way, when implementing new features or when fixing bugs. Thus
   execution of tests should be automated as much as possible with the help of
   test frameworks (i.e. test tools) and CI/CD infrastructure.
3. Checking the test outputs: this is done by comparing the output of
   test cases with the expected output of the software and should be
   automated as well.

## Verification vs. validation

Notice that we did *not* define testing as confirming that the
software is *correct* because testing alone cannot prove that software
is correct. Even if you could execute the software with all possible
inputs, all that would do is confirm that the outputs produced agree
with what the tests understand as the expected behavior, i.e. with
the *specifications*.

Software engineering lingo captures this distinction with the
(non-interchangeable) terms "verification" and "validation":

* __Verification :__ does the software do what the specification says
  it should do? In other words, does the output match expectations?
* __Validation :__ are those even the right specs in the first place?
  In other words, do our expectations align with reality or scientific
  ground truth? Or in yet other words, is verified code correct?

On its own, testing is about verification. Validation requires extra
steps: attempts at replication, real-world data/experimentation,
scientific debate and arrival at consensus, etc.

Of course, having a robust (and ideally automated) verification system
in place is what makes validation possible. That's why systematic
testing is the most widely used technique to assure software quality,
to uncover errors, and to make software more reliable, stable, and
usable.

# Why (else) do we test?

When asked this question, most of us instinctively answer "to make
sure the code is correct".  We've just seen that while testing is an
essential component in validation, it doesn't really accomplish this
on its own.  So why else should we test?

* Uncover bugs
* Document bugs
* Document the specifications, more broadly (and more specifically)
* Detect regressions
* Guide the software design
* Circumscribe and focus your coding (avoiding "feature creep")

# When to *run* tests?

The earlier a bug is detected, the less costly it is to fix. For
example, a bug detected and fixed during coding is 50 times cheaper
than detecting and fixing it after the software is deployed. Imagine
the cost of publishing code with a bug!  However, executing tests as
soon as possible is also immediately beneficial.  When you discover a
bug after just having changed 3 lines of code, you know exactly where
to look for a mistake. We will discuss automated methods to run whole
suites of quick tests on a very high cadence.

# When to *write* tests?

Most of us are in the habit of writing tests after the code is
written.  This seems like a no-brainer: after all, how can you test
something that doesn't exist yet? But this thinking is an artifact of
believing that the primary (or only) purpose of testing is to "make
sure the code is correct".

One of the main takeaways of today's lesson --- and also the one that
you will most resist --- is that writing and running a test for code
that doesn't yet exist is precisely what you ought to be doing. This
approach is called Test Driven Development (TDD) and we will discuss
it a little later.







::::::::::::::::::::::::::::::::::::: keypoints 

- Testing improves confidence about your code. It doesn't prove that code is correct.
- Testing is a vehicle for both software design and software documentation.
- Creating and executing tests should not be an afterthought. It should be an activity that goes hand-in-hand with code development.
- Tests are themselves code. Thus, test code should follow the same overarching design principles as functional code (e.g. DRY, modular, reusable, commented, etc).

::::::::::::::::::::::::::::::::::::::::::::::::
