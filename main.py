from functools import reduce


def cmdsq(x):
    return b'\x1B' + bytes(x)


reset_printer = cmdsq(b'@')


def begin_hires_gfx(density, columns):
    n1 = columns  % 256
    n2 = columns // 256
    return cmdsq(b'*' + bytes([density, n1, n2]))


empf_on = cmdsq(b'E')
empf_off = cmdsq(b'F')

italics_on = cmdsq(b'4')
italics_off = cmdsq(b'5')

raster_map1 = [
    "*                      *",
    " *                    * ",
    "  *                  *  ",
    "   *                *   ",
    "    *              *    ",
    "     *            *     ",
    "      *          *      ",
    "       *        *       ",
    "        *      *        ",
    "         *    *         ",
    "          *  *          ",
    "           **           ",
    "           **           ",
    "          *  *          ",
    "         *    *         ",
    "        *      *        ",
    "       *        *       ",
    "      *          *      ",
    "     *            *     ",
    "    *              *    ",
    "   *                *   ",
    "  *                  *  ",
    " *                    * ",
    "*                      *",
]

raster_map2 = [
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
    "*  *  *  *  *  *  *  *  ",
]

raster_map3 = [
    "************************",
    "                        ",
    "************************",
    "                        ",
    "************************",
    "                        ",
    "************************",
    "                        ",
    "************************",
    "                        ",
    "************************",
    "                        ",
    "************************",
    "                        ",
    "************************",
    "                        ",
    "************************",
    "                        ",
    "************************",
    "                        ",
    "************************",
    "                        ",
    "************************",
    "                        ",
]

raster_map4 = [
    "* * * * * * * * * * * * ",
    " * * * * * * * * * * * *",
    "* * * * * * * * * * * * ",
    " * * * * * * * * * * * *",
    "* * * * * * * * * * * * ",
    " * * * * * * * * * * * *",
    "* * * * * * * * * * * * ",
    " * * * * * * * * * * * *",
    "* * * * * * * * * * * * ",
    " * * * * * * * * * * * *",
    "* * * * * * * * * * * * ",
    " * * * * * * * * * * * *",
    "* * * * * * * * * * * * ",
    " * * * * * * * * * * * *",
    "* * * * * * * * * * * * ",
    " * * * * * * * * * * * *",
    "* * * * * * * * * * * * ",
    " * * * * * * * * * * * *",
    "* * * * * * * * * * * * ",
    " * * * * * * * * * * * *",
    "* * * * * * * * * * * * ",
    " * * * * * * * * * * * *",
    "* * * * * * * * * * * * ",
    " * * * * * * * * * * * *",
]

raster_map5 = [
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
    "************************",
]

def get_max(iterable, func):
    return reduce(
        lambda x, y: max(x, y),
        map(lambda x: func(x), iterable),
        0
    )


def encode2raster(raster):
    width = get_max(raster, len)
    height = len(raster)

    raster = [[1 if z == '*' else 0 for z in y] for y in [f"{x:{width}s}" for x in raster]]
    columns = [[0 for y in range(height // 8 + (1 if height % 8 else 0))] for x in range(width)]

    pwr = 7
    for n, line in enumerate(raster):
        octet = n // 8
        wgt = 1 << pwr
        columns = [[wgt * bit + val if i == octet else val for i, val in enumerate(bytes)] for bit, bytes in zip(line, columns)]
        pwr = pwr-1 if pwr > 0 else 7

    return columns


if __name__ == '__main__':
    from pprint import pprint
    # pprint(encode2raster(raster_map))
    data = [
        encode2raster(raster_map1),
        encode2raster(raster_map2),
        encode2raster(raster_map3),
        encode2raster(raster_map4),
        encode2raster(raster_map5),
    ]
    with open("/dev/usb/lp0", "wb") as p:
        p.write(reset_printer)
        densities = (
            (32, b"Single density (24-pin)"),
            (33, b"Double density (24-pin)"),
            (38, b"CRT 3 (24-pin)"),
            (39, b"Triple density (24-pin)"),
            (40, b"Hex density (24-pin)"),
        )
        for dn, title in densities:
            p.write(b'\r\n\r\n')
            pprint(title)
            p.write(title)
            p.write(b'\r\n')
            for pattern in range(5):
                pprint(begin_hires_gfx(dn, 24*20))
                p.write(begin_hires_gfx(dn, 24*20))
                for i in range(20):
                    for col in data[pattern]:
                        pprint(bytes(col))
                        p.write(bytes(col))
                p.write(b'\r\n')
        # p.write(f"\n\n\n\rTEST {empf_on}TEST {italics_on}TEST {empf_off}ТЕСТ {italics_off}TEST".encode("cp866"))
