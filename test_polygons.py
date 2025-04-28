# does not intersect self

poly1 = [(188, 337), (110, 269), (105, 215), (135, 147), (172, 113), (221, 91), (252, 135), (250, 208), (248, 244), (277, 272), (334, 245), (335, 188), (353, 96), (413, 83), (468, 177), (418, 269), (386, 322), (345, 335), (316, 325), (255, 311), (218, 279), (200, 213), (185, 165), (168, 166), (147, 201), (153, 244), (176, 269), (211, 317), (303, 373), (395, 368), (446, 248), (489, 308), (473, 366), (446, 356), (429, 424), (508, 474), (399, 552), (314, 518), (269, 442), (324, 420), (181, 422), (150, 454), (78, 444), (82, 381), (193, 393)]

poly2 = [(160, 335), (94, 272), (159, 177), (179, 76), (318, 68), (412, 130), (487, 115), (553, 175), (514, 283), (560, 349), (543, 451), (458, 514), (421, 433), (471, 348), (401, 282), (466, 163), (280, 164), (322, 240), (234, 246), (362, 327), (343, 471), (228, 529), (271, 420), (318, 383), (236, 333), (174, 444), (89, 422), (35, 377), (131, 387), (107, 353)]
origin2 = [199.0, 246.0]
# heron area error [493.683665888892, 416.84020183635454]
# origin2 = (0, 0)

#origin = (363, 515) for divide by zero errors
# (274, 331) dvzerror
#(586, 419) dvzerror
# (309, 245) multible socialisable divisions
# (324, 262) some sort of error occurs
# (318, 578) incorrect coloring
# (669, 220) very low error
# (23, 427) incorrect coloring
# (21, 310) incorrect coloring
# [328, 498] incorrect coloring
# [133.0, 515.0] incorrect coloring
# CRITICAL drawing outlines for drawing the polygon is not a proper fix

# [326.0, 274.0] something heron error

# ORIGIN POSITION: [474.0, 420.0]
# c:\Users\teofi\Desktop\polygon program\data_structures.py:34: RuntimeWarning: divide by zero encountered in scalar divide
#   kn = (a[0] - a[1] / r[1] * r[0]) / (r[0] * c[1] / r[1] - c[0])
# c:\Users\teofi\Desktop\polygon program\data_structures.py:34: RuntimeWarning: invalid value encountered in scalar divide
#   kn = (a[0] - a[1] / r[1] * r[0]) / (r[0] * c[1] / r[1] - c[0])

# ORIGIN POSITION: [505.0, 383.0]
# c:\Users\teofi\Desktop\polygon program\data_structures.py:34: RuntimeWarning: divide by zero encountered in scalar divide
#   kn = (a[0] - a[1] / r[1] * r[0]) / (r[0] * c[1] / r[1] - c[0])
# c:\Users\teofi\Desktop\polygon program\data_structures.py:34: RuntimeWarning: invalid value encountered in scalar divide
#   kn = (a[0] - a[1] / r[1] * r[0]) / (r[0] * c[1] / r[1] - c[0])

poly3 = [(208, 271), (319, 134), (511, 204), (326, 410)]
origin3 = (375, 267)
# origin = (375, 267) incorrect generation of bowties 
# 

poly4 = [(153, 327), (185, 150), (376, 96), (490, 197), (437, 388), (254, 425)]
origin4 = (308, 271)

poly5 = [(101, 439), (104, 279), (195, 108), (280, 65), (330, 97), (275, 171), (272, 230), (320, 289), (398, 318), (423, 366), (339, 412), (238, 412), (188, 436)]
origin5 = (451, 456)

poly6 = [[124.0, 462.0], [107.0, 82.0], [165.0, 73.0], [163.0, 430.0], [188.0, 433.0], [184.0, 69.0], [195.0, 69.0], [205.0, 433.0], [232.0, 428.0], [220.0, 75.0], [240.0, 37.0], [257.0, 425.0], [289.0, 423.0], [278.0, 14.0], [314.0, 79.0], [329.0, 422.0], [379.0, 17.0], [354.0, 424.0], [412.0, 135.0], [417.0, 408.0], [455.0, 93.0], [466.0, 401.0], [505.0, 171.0], [499.0, 405.0], [566.0, 22.0], [650.0, 494.0]]
origin6 = [46.0, 334.0]

poly7 = [[192.0, 462.0], [125.0, 122.0], [201.0, 99.0], [191.0, 143.0], [209.0, 521.0], [289.0, 27.0], [281.0, 519.0], [359.0, 14.0], [350.0, 475.0], [384.0, 8.0], [408.0, 480.0], [418.0, 36.0], [438.0, 465.0], [446.0, 8.0], [493.0, 469.0], [491.0, 26.0], [553.0, 538.0], [542.0, 7.0], [595.0, 554.0], [600.0, 13.0], [634.0, 561.0], [652.0, 19.0], [692.0, 547.0], [704.0, 14.0], [760.0, 550.0], [773.0, 28.0], [791.0, 579.0], [97.0, 569.0]]
origin7 = [40.0, 414.0]
#incorrect coloring
#[40.0, 414.0] math domain error sqrt of negative number

poly_presets = {
            1:[poly1, (236, 367)],
            2:[poly2, origin2],#(209, 314)(398, 375) long time origin: (398, 375)
            3:[poly3, origin3],
            4:[poly4, origin4],
            5:[poly5, origin5],
            6:[poly6, origin6],
            7:[poly7, origin7]
        }