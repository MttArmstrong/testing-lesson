import overlap_v1 as overlap
from io import StringIO
import pytest

@pytest.fixture()
def simple_input():
    return StringIO(
        'a	0	0	2	2\n'
        'b	1	1	3	3\n'
        'c	10	10	11	11'
    )

@pytest.mark.slow()
def test_end_to_end(simple_input):
    # initialize a StringIO with a string to read from
    infile = simple_input
    # this holds our output
    outfile = StringIO()
    # call the function
    overlap.main(infile, outfile)
    output = outfile.getvalue().split('\n')
    assert output[0] == '1\t1\t0'
    assert output[1] == '1\t1\t0'
    assert output[2] == '0\t0\t1'
