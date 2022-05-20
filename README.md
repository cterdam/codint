# codint

codint is a collection of programming problems with a standardized test
script.

Use this tool to practice for your coding interview. You can also use it to
pick up new programming languages quickly!

## Requirements

- `python3` and `pytest` to run any tests
- The command `gcc` must invoke a C compiler if you want to test C code
  - On macOS, `gcc` invokes clang by default. This also works.

## How to Use

### Getting Started

Clone this repo to a local directory.

Inside this directory, initialize test scripts:

```
bash setup.sh clear && bash setup.sh distribute
```

- The above command sends the `testtemplate.py` in the repo root to each
  problem's subdirectory as a symlink, to make sure they can be recognized by
  pytest.

Now, run `pytest -slv` to run a diagnosis of all existing coding problems and
test exising solutions for each problem.

### Read a problem

`cd` into any of the top-level directories. Inside you will find
subdirectories each named `d[x]_[pName]`, where `[x]` is the difficulty rating
of the problem ([0-2], the lower, the easier), and `[pName]` is the name of the
problem. Each of these contains material for a programming problem.

- For example, `d1_traverseBST` is a valid subdirectory name in this format.

`cd` into one of these. Read `PS.md` for the problem statement.

### Write a solution

Write a solution to the problem as described in the `PS.md` writeup. You can
write in any of the [supported languages](#supported-languages). Your solution
must be a single file. The naming convention is `[pName].[suffix]`, where
`[pName]` is the problem name as inferred from this directory name (without the
difficulty rating), and `[suffix]` is that of your programming language.

- If the problem directory is `d1_traverseBST` and you decide to write C code,
  your solution should be called `traverseBST.c`.

- If a solution already exists, just delete it. It's in the repo, anyways.

- If you write multiple solutions, starting with the second solution you may
  append a number after `pName`. e.g. `traverseBST2.c`, `traverseBST3.c`.
  These will all be recognized by the test script.

  - The numbers are unlimited but they cannot be skipped: Do not write the 3rd
    solution without the 2nd solution.

  - Numbers do not overlap across languages. If you write two solutions in C
    and Python each, they should be called `traverseBST.c`, `traverseBST2.c`,
    `traverseBST.py`, `traverseBST2.py`.

Your solution should read all input from `stdin`. By default any single-line
input will be postfixed with a newline character.

Your solution should write all output to `stdout`. Make sure the end of the output contains a
newline character.

### Test Solutions

In the problem directory, run `pytest -slv` to test all solutions for this
problem following the correct naming convention.

Test cases are located in `d[x]_[pName]/tests/`. The naming convention is
`t[n]-in` and `t[n]-out`, where `[n]` is the test case number, which must be
named in order, starting from 1.

- For example, `t1-in` and `t1-out` together form a complete test case.

- When a solution takes in the contents of `t[n]-in` via `stdin`, it is
  expected to print content equal to `t[n]-out` to `stdout`.

- Unless, if the `PS.md` file of this problem includes a `-anyOrder` flag on
  the second line, that will make the test script ignore line order when
  comparing solutions. In that case a test case will pass as long as each line
  of `t[n]-out` is printed, no matter the order.

The test script will test all solutions it can find in all supported languages
(according to the solution naming convention) against all test cases it can
find (according to the test case naming convention).

If a test case fails, pytest will output these variables:

- `sol` which is the solution being run
- `thisIn` and `thisOut` which is the failing test case
- `thisSolOut` which is the solution's output
- `thisRefOut` which is the solution's output

For compiled languages (such as C), the test script will manage the
compilation and clearance of the compiled executable after testing finishes.

## Current Development

### Supported Languages

- C
- Python3

### Supported Flags

- `-anyOrder`: The test script will ignore line order when testing solutions.
  A test case will pass as long as each line of the correct output is printed,
  no matter the order.

## Contributing

### Adding new test cases for an existing problem

Just create new `t[n]-in` and `t[n]-out` files in the `tests` directory.
Remember that test case numbers cannot be skipped. Do not write the 9th pair
of test case if there's no 8th yet.

It is advisable to put easier test cases first (in smaller numbers) as the
test script tests them in increasing order.

### Adding new programming problems

In an appropriate category directory, create a sub-directory to host the new
problem. Name it `d[x]_[pName]`, as outlined.

- `[x]` is the difficulty rating. Roughly `0` means easy, `1` means medium,
  `2` means hard.

- For `[pName]` follow the `camelCase` naming convention.

In the new problem directory, make sure there is:

- `PS.md`: Reference the format from a `PS.md` from another file.

  - If it's needed to supply any flags, specify them on the second line with a
    space between any two adjacent flag strings, but no space at the start of
    line. Here's an example of a `PS.md` on the second line:

    ```
    -anyOrder -otherFlag -anotherFlag
    ```

  - If no flag is needed, leave the second line blank.

- `tests/`: A directory to host the test cases. This is required for the setup
  script to recognize this directory as a problem directory.

When the directory is prepared, go to the repo's root, and run `bash setup.sh
distribute` to redistribute the test script symlink:

Now run `pytest -slv` and confirm that the new programming problem is included
in all problems.

### Adding support for new programming languages

Study `testtemplate.py` in the repo root directory. Add a new function
`test_languageName(capfd, dirInfo)` in the script. Most components can be
copied over from existing test functions for other languages, other than the
`ext` extension name and the specific compile and cleanup commands.

Existing language-specific test functions in `testtemplate.py` can be renamed
without any consequences.

When this new language's test function is added to `testtemplate.py`, no
change should be needed to update the individual symlinks in problem
directories.

Now run `pytest -slv`. If there is no programming files in that language
extension yet, it should display relevant tests as 'SKIPPED'.

### Adding new flags

Flags are parsed in the `readFlags(workDir)` function in `testtemplate.py`,
and are passed to individual `test_languageName` functions to influence
specific test routines.  Add customized compile/test commands there, or
elsewhere as seen fit.  Be sure to expand every language-specific test
function to account for the new flag.

### Other functionalities to contribute

- List language-specific and problem-specific stats (How many problems are
  solved in this many languages?) Look into `setup.sh`.
