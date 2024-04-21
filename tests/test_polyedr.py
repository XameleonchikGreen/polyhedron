import unittest
from unittest.mock import patch, mock_open

from shadow.polyedr import Polyedr


class TestPolyedr(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        fake_file_content = """200.0	45.0	45.0	30.0
8	4	16
-0.5	-0.5	0.5
-0.5	0.5	0.5
0.5	0.5	0.5
0.5	-0.5	0.5
-0.5	-0.5	-0.5
-0.5	0.5	-0.5
0.5	0.5	-0.5
0.5	-0.5	-0.5
4	5    6    2    1
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5"""
        fake_file_path = 'data/holey_box.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

        fake_file_content = """200.0	60.0	-140.0	60.0
8	5	20
-0.5	-0.5	0.5
-0.5	0.5	0.5
0.5	0.5	0.5
0.5	-0.5	0.5
-0.5	-0.5	-0.5
-0.5	0.5	-0.5
0.5	0.5	-0.5
0.5	-0.5	-0.5
4	1    2    3    4
4	5    6    2    1
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5"""
        fake_file_path = 'data/special_box.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr1 = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

        fake_file_content = """200.0	45.0	45.0	30.0
8	6	24
-0.5 -0.5 0.5
-0.5 0.5 0.5
0.5	0.5	0.5
0.5	-0.5 0.5
-0.5 -0.5 -0.5
-0.5 0.5 -0.5
0.5	0.5	-0.5
0.5	-0.5 -0.5
4	1    2    3    4
4	5    6    2    1
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5
4	8    7    6    5"""
        fake_file_path = 'data/special_cube.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr2 = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

        fake_file_content = """40.0	45.0	-30.0	-60.0
8	2	8
0.0 0.0 0.0
5.0 0.0 0.0
5.0 5.0 0.0
0.0 5.0 0.0
1.0 1.0 3.0
6.0 1.0 3.0
6.0 6.0 3.0
1.0 6.0 3.0
4	1    2    3    4
4	5    6    7    8"""
        fake_file_path = 'data/special_ccc.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr3 = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

        fake_file_content = """155.0	10.0 30.0 0.0
8	3	14
-0.5	-0.5	0.5
-0.5	0.5	0.5
0.5	0.5	0.5
0.5	-0.5	0.5
-0.5	-0.5	-0.5
-0.5	0.5	-0.5
0.5	0.5	-0.5
0.5	-0.5	-0.5
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5"""
        fake_file_path = 'data/special_something.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr4 = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

        fake_file_content = """120.0	45.0	-30.0	-60.0
8	2	8
0.0 0.0 0.0
1.0 0.0 0.0
1.0 1.0 0.0
0.0 1.0 0.0
0.2 0.2 0.6
1.2 0.2 0.6
1.2 0.6 0.6
0.2 0.6 0.6
4	1    2    3    4
4	5    6    7    8"""
        fake_file_path = 'data/special_ccc2.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr5 = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)

    def test_num_vertexes(self):
        self.assertEqual(len(self.polyedr.vertexes), 8)

    def test_num_facets(self):
        self.assertEqual(len(self.polyedr.facets), 4)

    def test_num_edges(self):
        self.assertEqual(len(self.polyedr.edges), 16)

    # У коробки два ребра едничной длины, удовлетворяющих условию
    def test_task69_1(self):
        self.polyedr1.task69()
        self.assertAlmostEqual(self.polyedr1.sigma, 2)

    # У кубика нет частично освещённых рёбер
    def test_task69_2(self):
        self.polyedr2.task69()
        self.assertAlmostEqual(self.polyedr2.sigma, 0)

    # Хоть у данных плоскостей и есть частично освещённые рёбра,
    # но их центр не проецируется в заданный круг
    def test_task69_3(self):
        self.polyedr3.task69()
        self.assertAlmostEqual(self.polyedr3.sigma, 0)

    def test_task69_4(self):
        self.polyedr4.task69()
        self.assertAlmostEqual(self.polyedr4.sigma, 1)

    def test_task69_5(self):
        self.polyedr5.task69()
        self.assertAlmostEqual(self.polyedr5.sigma, 1)
