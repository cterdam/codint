import os
import re

import pytest

"""
NOTE
capsys does not read output from shell processes, therefore it always captures
a blank output if we test through running shell commands. Use capfd instead.
"""


def countTests(testDir):
    """
    Count the number of test cases in testDir.

    A valid test case is a pair of files 't[n]-in' and 't[n]-out', no filename
    extension. For instance, 'in5' and 'out5' is a valid test case. In this
    directory, the numbering must start from 1.

    Params:
        (str) testDir: Path of directory containing valid test cases to count.

    Returns:
        (int) The largest numbering found in test files named properly.

    Example1:
        testDir contains: 't1-in', 't1-out', 't2-in', 't2-out'
        Returns: 2
    Example2:
        testDir is empty
        Returns: 0
    """
    testCount = 0
    for fileName in os.listdir(testDir):
        testMatch = re.match(r't(\d+)-(in|out)', fileName)
        if testMatch:
            testID = int(testMatch.group(1))
            if testID > testCount:
                testCount = testID
    return testCount


def tallySols(workDir, pName, exts):
    """
    Count the number of solutions in each extension.

    A valid solution is a file '[pName][n].[ext]', where pName is the name of
    the problem, and ext is a programming language filetype extension. For
    instance, if the problem name is 'traverseBST', then 'traverseBST5.py' is
    a valid solution. If n is 1 then it can be omitted. So 'traverseBST.cpp'
    is also a valid solution.

    Params:
        (str) workDir: Path of directory containing valid solutions to tally
        (str) pName: Name of the problem
        (set) exts: Set of filename extensions (in str) to look for

    Returns:
        (str -> int) extFreq: dictionary where:
            extFreq[k] is the number of solutions found in workDir with
            extension k. Each extension in exts corresponds to an entry in d.

    Example:
        workDir contains: 'hello.c', 'hello.py', 'hello2.py', 'random.cpp'
        pName = 'hello'
        exts = {'c', 'cs', 'py'}
        Returns: {'c':1, 'cs':0, 'py':2}
    """
    extFreq = {s: 0 for s in exts}
    namePattern = '^' + pName + r'(\d*)$'
    # Iterate through all files in wordDir and update count into dict
    for fileName in os.listdir(workDir):
        fileNameSplit = os.path.splitext(fileName)
        thisName = fileNameSplit[0]
        thisExt = fileNameSplit[1].replace('.', '')
        if thisExt in exts:
            nameMatch = re.match(namePattern, thisName)
            if nameMatch:
                thisNumStr = nameMatch.group(1)
                thisNum = 1 if thisNumStr == '' else int(thisNumStr)
                if thisNum > extFreq[thisExt]:
                    extFreq[thisExt] = thisNum
    return extFreq


def readFlags(workDir):
    """
    Reads flags from the problem statement file in the working directory.

    All flags are stored in the 2nd line of the PS file. If there are no
    flags, the 2nd line is empty.

    Params:
        (str) workDir: Path of directory containing the problem statement

    Returns:
        (str*) A set containing all flags read from the problem statement.

    Example1:
        2nd line from workDir/PS.md is: ''
        Returns: set()
    Example2:
        2nd line from workDir/PS.md is: '-anyOrder'
        Returns: {-anyOrder}

    """
    with open(workDir + '/PS.md', 'r') as psFile:
        psFile.readline()
        flagLine = psFile.readline()
        return set(flagLine.split())


@ pytest.fixture(scope='module')
def dirInfo():
    """
    Gathers various info about the current working directory.

    Returns:
        (str) workDir: Path of current working directory, the dir containing
            material for this problem. When this script is a soft link, the
            dir is parent to the link and not its target.
            Example: '/Users/sterdam/cterdam/playground/d0_avgLen'
        (str) testDir: Path of directory containing all tests for this
            problem.
            Example: '/Users/sterdam/cterdam/playground/d0_avgLen/tests'
        (str) pName: Name of this problem, without the difficulty mark.
            Example: 'traverseBST'
        (int) testCount: Number of test cases found in testDir. See countTests
            for definition of valid test cases.
        (str -> int) extFreq: dictionary where:
            extFreq[k] is the number of valid solution files of extension k
            found in workDir. See tallySols for definition of valid solution
            files.
        (str*) flags: Set of flag strings found in the problem statement.
            Example: {-anyOrder}
    """
    workDir = os.path.dirname(os.path.abspath(__file__))
    testDir = workDir + '/tests'
    pName = re.sub(r'^d\d_', '', os.path.basename(workDir))
    testCount = countTests(testDir)
    exts = {'c', 'cs', 'py'}
    extFreq = tallySols(workDir, pName, exts)
    flags = readFlags(workDir)

    yield workDir, testDir, pName, testCount, extFreq, flags

    # Cleanup
    os.system('rm -rf ' + workDir + '/__pycache__')


def genSols(workDir, pName, ext, solCount):
    """
    Gives a generator for all valid solution filepaths with given extension.
    See tallySols for definition of valid solution.

    Params:
        (str) workDir: Path of directory containing all solutions
        (str) pName: Problem name, e.g. 'traverseBST'
        (str) ext: extension without the dot, e.g. 'c' or 'py'
        (int) solCount: The number of solutions to generate

    Returns:
        ( -> str) Generator for all valid solutions filepaths in this format.
    """
    for solNum in range(1, solCount+1):
        numStr = '' if solNum == 1 else str(solNum)
        thisSol = workDir + '/' + pName + numStr + '.' + ext
        yield thisSol


def genTests(testDir, testCount):
    """
    Gives a generator for all valid test cases in this path.
    See countTests for definition of valid test cases.

    Params:
        (str) testDir: Directory containing all test cases
        (int) testCount: The number of solutions to generate

    Returns:
        ( -> (str, str)) Generator for all valid test cases in this path.
    """
    for testNum in range(1, testCount+1):
        thisIn = testDir + '/t' + str(testNum) + '-in'
        thisOut = testDir + '/t' + str(testNum) + '-out'
        yield thisIn, thisOut


def test_simplC(capfd, dirInfo):
    """
    Test all .c solutions for this problem.
    """

    # Skip the test if no .c file is found
    ext = 'c'
    pName = dirInfo[2]
    solCount = dirInfo[4][ext]
    if solCount <= 0:
        pytest.skip('No .' + ext + ' file found for ' + pName)

    # Prepare flags
    flags = dirInfo[5]
    sortOut = ' | sort' if '-anyOrder' in flags else ''

    # For all solutions, run through all tests
    for sol in genSols(dirInfo[0], pName, ext, solCount):
        compileDest = sol.replace('.', '_')
        os.system('gcc ' + sol + ' -o ' + compileDest)
        for thisIn, thisOut in genTests(dirInfo[1], dirInfo[3]):
            capfd.readouterr()
            os.system('cat ' + thisIn + ' | ' + compileDest + sortOut)
            thisSolOut, thisSolErr = capfd.readouterr()
            os.system('cat ' + thisOut + sortOut)
            thisRefOut, thisRefErr = capfd.readouterr()
            assert thisSolOut == thisRefOut
            assert thisSolErr == thisRefErr
        os.system('rm ' + compileDest)


def test_CSharp(capfd, dirInfo):
    ext = 'cs'
    pName = dirInfo[2]
    solCount = dirInfo[4][ext]
    if solCount <= 0:
        pytest.skip('No .' + ext + ' file found for ' + pName)


def test_Python(capfd, dirInfo):
    """
    Test all .py solutions for this problem.
    """

    # Skip the test if no .c file is found
    ext = 'py'
    pName = dirInfo[2]
    solCount = dirInfo[4][ext]
    if solCount <= 0:
        pytest.skip('No .' + ext + ' file found for ' + pName)

    # Prepare flags
    flags = dirInfo[5]
    sortOut = ' | sort' if '-anyOrder' in flags else ''

    # For all solutions, run through all tests
    for sol in genSols(dirInfo[0], pName, ext, solCount):
        for thisIn, thisOut in genTests(dirInfo[1], dirInfo[3]):
            capfd.readouterr()
            os.system('cat ' + thisIn + ' | python3 ' + sol + sortOut)
            thisSolOut, thisSolErr = capfd.readouterr()
            os.system('cat ' + thisOut + sortOut)
            thisRefOut, thisRefErr = capfd.readouterr()
            assert thisSolOut == thisRefOut
            assert thisSolErr == thisRefErr
