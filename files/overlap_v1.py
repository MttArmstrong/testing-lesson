import sys


def main(infile, outfile):
    # build rectangle struct
    dict = {}
    for line in infile:
        name, *coords = line.split()
        dict[name] = [int(c) for c in coords]

    for red_name, red_coords in dict.items():
        output_line = []
        for blue_name, blue_coords in dict.items():
            # check if rects overlap
            result = '1'

            red_lo_x, red_lo_y, red_hi_x, red_hi_y = red_coords
            blue_lo_x, blue_lo_y, blue_hi_x, blue_hi_y = blue_coords

            if (red_lo_x >= blue_hi_x) or (red_hi_x <= blue_lo_x) or \
                    (red_lo_y >= blue_hi_x) or (red_hi_y <= blue_lo_y):
                result = '0'

            output_line.append(result)
        outfile.write('\t'.join(output_line) + '\n')


if __name__ == "__main__":
    with open(sys.argv[1], encoding='utf-8') as infile, \
            open(sys.argv[2], 'w', encoding='utf-8') as outfile:
        main(infile, outfile)
