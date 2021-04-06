from core import mwglobals
from core.mwrecord import MwRecord


class MwPGRD(MwRecord):
    def __init__(self):
        MwRecord.__init__(self)
        self.cell = None
        self.grid_x = 0
        self.grid_y = 0
        self.num_points = 0
        self.id_ = ''
        self.points = None
        self.edges = None

    def load(self):
        self.grid_x = self.parse_int('DATA')
        self.grid_y = self.parse_int('DATA', start=4)
        if self.id_ in mwglobals.interior_cells:
            cell = mwglobals.interior_cells[self.id_]
            cell.pgrd = self
            self.cell = cell
        else:
            cell = mwglobals.exterior_cells[(self.grid_x, self.grid_y)]
            cell.pgrd = self
            self.cell = cell
        self.num_points = self.parse_uint('DATA', start=10, length=2)

        self.id_ = self.parse_string('NAME')

        self.points = [MwPGRDPoint(self.parse_int('PGRP', start=i * 16),  # x
                                   self.parse_int('PGRP', start=4 + i * 16),  # y
                                   self.parse_int('PGRP', start=8 + i * 16),  # z
                                   (self.parse_uint('PGRP', start=12 + i * 16, length=1) & 0x1) == 0x1,  # autogenerated
                                   self.parse_uint('PGRP', start=13 + i * 16, length=1))  # num connections
                       for i in range(self.num_points)]

        self.edges = []
        if 'PGRC' in self.subrecords:
            pgrc_index = 0
            for index1 in range(len(self.points)):
                for _ in range(self.points[index1].num_connections):
                    index2 = self.parse_uint('PGRC', start=pgrc_index * 4)
                    self.edges.append((index1, index2))
                    pgrc_index += 1

    def record_details(self):
        return MwRecord.format_record_details(self, [
            ("|Name|", '__str__'),
            ("\n|Num Points|", 'num_points'),
            ("\n|Points|", 'points', []),
            ("\n|Edges|", 'edges', [])
        ])

    def __str__(self):
        if self.id_ in mwglobals.interior_cells:
            return self.id_
        return f"{self.id_} [{self.grid_x},{self.grid_y}]"

    def get_id(self):
        return str(self)

    def diff(self, other):
        return MwRecord.diff(self, other, ['num_points', 'points', 'edges'])


class MwPGRDPoint:
    def __init__(self, x, y, z, autogenerated, num_connections):
        self.x = x
        self.y = y
        self.z = z
        self.autogenerated = autogenerated
        self.num_connections = num_connections

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        return str(self)
