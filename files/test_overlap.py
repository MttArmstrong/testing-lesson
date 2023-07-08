import overlap_v4 as overlap
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
    assert output[0] == '4.0\t1.0\t0'
    assert output[1] == '1.0\t4.0\t0'
    assert output[2] == '0\t0\t1.0'

def test_read_rectangles_simple(simple_input):
    rectangles = overlap.read_rectangles(simple_input)
    assert rectangles == {
        'a': overlap.Rectangle(0, 0, 2, 2),
        'b': overlap.Rectangle(1, 1, 3, 3),
        'c': overlap.Rectangle(10, 10, 11, 11),
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
    assert coords.x1 == pytest.approx(0.1 + 0.2)
    assert coords.y1 == 0.3
    assert coords.x2 == 1.0
    assert coords.y2 == 1.0

def test_read_rectangles_not_equal_coords():
    lines = ['a 1 2 3 4']
    rectangles = overlap.read_rectangles(lines)
    assert rectangles == {'a': overlap.Rectangle(1, 2, 3, 4)}

def test_read_rectangles_fix_order_of_coords():
    lines = ['a 3 4 1 2']
    rectangles = overlap.read_rectangles(lines)
    assert rectangles == {'a': overlap.Rectangle(1, 2, 3, 4)}

def test_read_rectangles_incorrect_number_of_coords_raise_error():
    with pytest.raises(ValueError) as error:
        overlap.read_rectangles(['a 1'])
    assert "Incorrect number of coordinates for " in str(error)

    with pytest.raises(ValueError) as error:
        overlap.read_rectangles(['a'])
    assert "Incorrect number of coordinates for " in str(error)

def test_rectangle_overlap():
    rectangles = {
        'a': overlap.Rectangle(0, 0, 2, 2),
        'b': overlap.Rectangle(1, 1, 3, 3),
        'c': overlap.Rectangle(10, 10, 11, 11),
    }

    assert rectangles['a'].overlap(rectangles['a']) == overlap.Rectangle(0, 0, 2, 2)
    assert rectangles['a'].overlap(rectangles['b']) == overlap.Rectangle(1, 1, 2, 2)
    assert rectangles['b'].overlap(rectangles['a']) == overlap.Rectangle(1, 1, 2, 2)
    assert rectangles['a'].overlap(rectangles['c']) is None


def rotate_rectangle(rectangle):
    if rectangle is None:
        return None
    return rectangle.rotate()

def test_rotate_rectangle():
    rectangle = overlap.Rectangle(1, 2, 3, 3)

    rectangle = rectangle.rotate()
    assert rectangle == overlap.Rectangle(2, -3, 3, -1)

    rectangle = rectangle.rotate()
    assert rectangle == overlap.Rectangle(-3, -3, -1, -2)

    rectangle = rectangle.rotate()
    assert rectangle == overlap.Rectangle(-3, 1, -2, 3)

    rectangle = rectangle.rotate()
    assert rectangle == overlap.Rectangle(1, 2, 3, 3)

rectangle_strs = ['''
┌───┐  
│  ┌┼─┐
└──┼┘ │
   └──┘''','''
┌──┬──┐
│  │  │
└──┴──┘''','''
┌──────┐
│ ┌──┐ │
└─┼──┼─┘
  └──┘''','''
┌─┐  
└─┼─┐
  └─┘''','''
┌─┐  
└─┘ ┌─┐
    └─┘''','''
┌──────┐
│  ┌─┐ │
│  └─┘ │
└──────┘''',
                  ]
@pytest.mark.parametrize(
    "rectangle_2,rectangle_str,result",
    [
        (overlap.Rectangle(0, 0, 2, 3), rectangle_strs[0], overlap.Rectangle(0, 0, 1, 1)),
        (overlap.Rectangle(1, -1, 2, 1), rectangle_strs[1], None),
        (overlap.Rectangle(0, -2, 0.5, 0), rectangle_strs[2], overlap.Rectangle(0, -1, 0.5, 0)),
        (overlap.Rectangle(1, 1, 2, 2), rectangle_strs[3], None),
        (overlap.Rectangle(2, 2, 3, 3), rectangle_strs[4], None),
        (overlap.Rectangle(0, 0, 0.5, 0.5), rectangle_strs[5], overlap.Rectangle(0, 0, 0.5, 0.5)),
    ])
def test_rectangles_overlap_permutations(rectangle_2, rectangle_str, result):
    rectangle_1 = overlap.Rectangle(-1, -1, 1, 1)

    for i in range(4):
        assert rectangle_1.overlap(rectangle_2) == result, (
            f"Failed {rectangle_1}.overlap({rectangle_2}) "
            f"on rotation {i}. {rectangle_str}")

        assert rectangle_2.overlap(rectangle_1) == result, (
            f"Failed {rectangle_2}.overlap({rectangle_1}) "
            f"on rotation {i}. {rectangle_str}")

        rectangle_2 = rotate_rectangle(rectangle_2)
        result = rotate_rectangle(result)


def test_create_rectangle_named_parameters():
    assert overlap.Rectangle(1.1, 4, 2, 3) == overlap.Rectangle(1.1, 3, 2, 4)
    assert overlap.Rectangle(x1=1.1, x2=2, y1=4, y2=3) == overlap.Rectangle(1.1, 3, 2, 4)


def test_create_rectangle_from_list():
    assert overlap.Rectangle.from_list([1.1, 4, 2, 3]) == overlap.Rectangle(1.1, 3, 2, 4)


def test_create_rectangle_from_list_wrong_number_of_args():
    with pytest.raises(ValueError) as error:
        overlap.Rectangle.from_list([1.1, 4, 2])
    assert "Incorrect number of coordinates " in str(error)
    with pytest.raises(ValueError) as error:
        overlap.Rectangle.from_list([1.1, 4, 2, 2, 2])
    assert "Incorrect number of coordinates " in str(error)


def test_rectangle_area():
    assert overlap.Rectangle(0, 0, 1, 1).area() == 1
    assert overlap.Rectangle(0, 0, 1, 2).area() == 2
    assert overlap.Rectangle(0, 1, 2, 2).area() == 2
    assert overlap.Rectangle(0, 0, 0, 0).area() == 0
    assert overlap.Rectangle(0, 0, 0.3, 0.3).area() == 0.09
    assert overlap.Rectangle(0.1, 0, 0.4, 0.3).area() == pytest.approx(0.09)
