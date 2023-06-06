import overlap_v2 as overlap
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

def test_read_rectangles_simple(simple_input):
    rectangles = overlap.read_rectangles(simple_input)
    assert rectangles == {
        'a': [0, 0, 2, 2],
        'b': [1, 1, 3, 3],
        'c': [10, 10, 11, 11],
    }

def test_read_rectangles_empty_input_empty_output():
    rectangles = overlap.read_rectangles([])
    assert rectangles == {}

def test_read_rectangles_non_numeric_coord_raise_error():
    with pytest.raises(ValueError) as error:
        overlap.read_rectangles(['a a a a a'])
    assert "Non numeric value provided as input for 'a a a a a'" in str(error)

def test_read_rectangles_accepts_floats():
    lines = ['a 0.3 0.3 1.0 1.0']
    rectangles = overlap.read_rectangles(lines)
    coords = rectangles['a']
    # Note that 0.3 != 0.1 + 0.2 due to floating point error, use pytest.approx
    assert coords[0] == pytest.approx(0.1 + 0.2)
    assert coords[1] == 0.3
    assert coords[2] == 1.0
    assert coords[3] == 1.0

def test_read_rectangles_not_equal_coords():
    lines = ['a 1 2 3 4']
    rectangles = overlap.read_rectangles(lines)
    assert rectangles == {'a': [1, 2, 3, 4]}

def test_read_rectangles_fix_order_of_coords():
    lines = ['a 3 4 1 2']
    rectangles = overlap.read_rectangles(lines)
    assert rectangles == {'a': [1, 2, 3, 4]}

def test_read_rectangles_incorrect_number_of_coords_raise_error():
    with pytest.raises(ValueError) as error:
        overlap.read_rectangles(['a 1'])
    assert "Incorrect number of coordinates for 'a 1'" in str(error)
