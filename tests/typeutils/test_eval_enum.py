import unittest

from batutils.tpu import casting
import enum

from batutils.tpu.casting import enum_value_lookup_map
from batutils.tpu.structs.enumex import EnumEx


class TestEnumEval(unittest.TestCase):
    def test_enum_eval(self):
        class SomeEnum(enum.Enum):
            ALPHA = 0
            BETA = 1
            DELTA = 2

        class OtherEnum(enum.Enum):
            ONE = 1
            TWO = 2
            THREE = 3

        self.assertEqual(SomeEnum.ALPHA, casting.enum_eval('ALPHA', SomeEnum))
        self.assertEqual(SomeEnum.ALPHA, casting.enum_eval('Alpha', SomeEnum))
        self.assertEqual(SomeEnum.ALPHA, casting.enum_eval('alPHa ', SomeEnum))
        self.assertEqual(SomeEnum.ALPHA, casting.enum_eval('0 ', SomeEnum))
        self.assertEqual(SomeEnum.ALPHA, casting.enum_eval(0, SomeEnum))
        self.assertEqual(SomeEnum.ALPHA, casting.enum_eval('Yomama', SomeEnum, SomeEnum.ALPHA))
        self.assertIsNone(casting.enum_eval('Yomama', SomeEnum, None))

        self.assertEqual(SomeEnum.DELTA, casting.enum_eval('DELTA', SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval('Delta', SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval(' DeLtA  ', SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval('2 ', SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval('0b10', SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval(0b10, SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval(2, SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval(OtherEnum.TWO, SomeEnum))
        self.assertEqual(SomeEnum.DELTA, casting.enum_eval('Yomama', SomeEnum, SomeEnum.DELTA))
        self.assertIsNone(casting.enum_eval('Yomama', SomeEnum, None))

    def test_enum_value_lookup(self):
        class SomeEnum(enum.Enum):
            ALPHA = 0
            BETA = 1
            DELTA = 2

        class OtherEnum(enum.Enum):
            ONE = 1
            TWO = 2
            THREE = 3

        class MultiValEnum(enum.Enum):
            ALPHA = 0, 'alice'
            BETA = 1, 'bob'
            DELTA = 2, 'dave'

        class OtherMultiEnum(enum.Enum):
            ONE = 1, 'bob'  # Collides with THREE
            TWO = 2, 'dave'
            THREE = 3, 'bob'  # Collides with ONE

        self.assertEqual({0: SomeEnum.ALPHA, 1: SomeEnum.BETA, 2: SomeEnum.DELTA}, enum_value_lookup_map(SomeEnum))
        self.assertNotEqual({0: SomeEnum.ALPHA, 1: SomeEnum.BETA, 2: SomeEnum.DELTA}, enum_value_lookup_map(OtherEnum))
        self.assertEqual({1: OtherEnum.ONE, 2: OtherEnum.TWO, 3: OtherEnum.THREE}, enum_value_lookup_map(OtherEnum))
        self.assertEqual({
            (0, 'alice'): MultiValEnum.ALPHA,
            0: MultiValEnum.ALPHA,
            'alice': MultiValEnum.ALPHA,
            (1, 'bob'): MultiValEnum.BETA,
            1: MultiValEnum.BETA,
            'bob': MultiValEnum.BETA,
            (2, 'dave'): MultiValEnum.DELTA,
            2: MultiValEnum.DELTA,
            'dave': MultiValEnum.DELTA,
        }, enum_value_lookup_map(MultiValEnum))
        self.assertEqual({
            (1, 'bob'): OtherMultiEnum.ONE,
            1: OtherMultiEnum.ONE,
            'bob': OtherMultiEnum.THREE,  # Note the collision!!
            (2, 'dave'): OtherMultiEnum.TWO,
            2: OtherMultiEnum.TWO,
            'dave': OtherMultiEnum.TWO,
            (3, 'bob'): OtherMultiEnum.THREE,
            3: OtherMultiEnum.THREE,
        }, enum_value_lookup_map(OtherMultiEnum, allow_collision=True))

        with self.assertRaises(KeyError):
            enum_value_lookup_map(OtherMultiEnum, allow_collision=False)

    def test_enum_eval_multi_value(self):
        class MultiValEnum(enum.Enum):
            ALPHA = 0, 'alice'
            BETA = 1, 'bob'
            DELTA = 2, 'dave'

        class OtherEnum(enum.Enum):
            ONE = 1, 'bob'
            TWO = 2, 'dave'
            THREE = 3, 'ed'

        self.assertEqual(MultiValEnum.ALPHA, casting.enum_eval('ALPHA', MultiValEnum))
        self.assertEqual(MultiValEnum.ALPHA, casting.enum_eval('Alpha', MultiValEnum))
        self.assertEqual(MultiValEnum.ALPHA, casting.enum_eval('alPHa ', MultiValEnum))

        self.assertEqual(MultiValEnum.ALPHA, casting.enum_eval(0, MultiValEnum))
        self.assertEqual(MultiValEnum.ALPHA, casting.enum_eval('0 ', MultiValEnum))

        self.assertEqual(MultiValEnum.ALPHA, casting.enum_eval('Yomama', MultiValEnum, MultiValEnum.ALPHA))
        self.assertIsNone(casting.enum_eval('Yomama', MultiValEnum, None))

        self.assertEqual(MultiValEnum.DELTA, casting.enum_eval('DELTA', MultiValEnum))


        self.assertEqual(MultiValEnum.DELTA, casting.enum_eval('DELTA', MultiValEnum))
        self.assertEqual(MultiValEnum.BETA, casting.enum_eval((1, 'bob'), MultiValEnum))
        self.assertEqual(MultiValEnum.DELTA, casting.enum_eval(' DeLtA  ', MultiValEnum))

        self.assertEqual(MultiValEnum.DELTA, casting.enum_eval('2 ', MultiValEnum))
        self.assertEqual(MultiValEnum.DELTA, casting.enum_eval('0b10', MultiValEnum))
        self.assertEqual(MultiValEnum.DELTA, casting.enum_eval(0b10, MultiValEnum))
        self.assertEqual(MultiValEnum.DELTA, casting.enum_eval(2, MultiValEnum))

        self.assertEqual(MultiValEnum.DELTA, casting.enum_eval(OtherEnum.TWO, MultiValEnum))
        self.assertEqual(MultiValEnum.DELTA, casting.enum_eval('Yomama', MultiValEnum, MultiValEnum.DELTA))
        self.assertIsNone(casting.enum_eval('Yomama', MultiValEnum, None))

    def test_enum_ex(self):
        class SomeEnum(EnumEx):
            ALPHA = 0
            BETA = 1
            DELTA = 2

        class OtherEnum(EnumEx):
            ONE = 1
            TWO = 2
            THREE = 3

        self.assertEqual(SomeEnum.ALPHA, SomeEnum.from_any('ALPHA'))
        self.assertEqual(SomeEnum.ALPHA, SomeEnum.from_any('Alpha'))
        self.assertEqual(SomeEnum.ALPHA, SomeEnum.from_any('alPHa '))
        self.assertEqual(SomeEnum.ALPHA, SomeEnum.from_any('0 '))
        self.assertEqual(SomeEnum.ALPHA, SomeEnum.from_any(0))
        self.assertEqual(SomeEnum.ALPHA, SomeEnum.from_any('Yomama', SomeEnum.ALPHA))
        self.assertIsNone(SomeEnum.from_any('Yomama', None))

        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any('DELTA'))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any('Delta'))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any(' DeLtA  '))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any('2 '))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any('0b10'))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any(0b10))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any(2))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any(OtherEnum.TWO))
        self.assertEqual(SomeEnum.DELTA, SomeEnum.from_any('Yomama', SomeEnum.DELTA))
        self.assertIsNone(SomeEnum.from_any('Yomama', None))

    def test_enum_ex_eval_multi_value(self):
        class MultiValEnum(EnumEx):
            ALPHA = 0, 'alice'
            BETA = 1, 'bob'
            DELTA = 2, 'dave'

        class OtherEnum(EnumEx):
            ONE = 1, 'bob'
            TWO = 2, 'dave'
            THREE = 3, 'ed'

        self.assertEqual(MultiValEnum.ALPHA, MultiValEnum.from_any('ALPHA'))
        self.assertEqual(MultiValEnum.ALPHA, MultiValEnum.from_any('Alpha'))
        self.assertEqual(MultiValEnum.ALPHA, MultiValEnum.from_any('alPHa '))
        self.assertEqual(MultiValEnum.ALPHA, MultiValEnum.from_any(0))
        self.assertEqual(MultiValEnum.ALPHA, MultiValEnum.from_any('0 '))
        self.assertEqual(MultiValEnum.ALPHA, MultiValEnum.from_any('Yomama', MultiValEnum.ALPHA))
        self.assertIsNone(MultiValEnum.from_any('Yomama', None))
        self.assertEqual(MultiValEnum.DELTA, MultiValEnum.from_any('DELTA'))
        self.assertEqual(MultiValEnum.DELTA, MultiValEnum.from_any('Delta'))
        self.assertEqual(MultiValEnum.BETA, MultiValEnum.from_any((1, 'bob')))
        self.assertEqual(MultiValEnum.DELTA, MultiValEnum.from_any(' DeLtA  '))
        self.assertEqual(MultiValEnum.DELTA, MultiValEnum.from_any('2 '))
        self.assertEqual(MultiValEnum.DELTA, MultiValEnum.from_any('0b10'))
        self.assertEqual(MultiValEnum.DELTA, MultiValEnum.from_any(0b10))
        self.assertEqual(MultiValEnum.DELTA, MultiValEnum.from_any(2))
        self.assertEqual(MultiValEnum.DELTA, MultiValEnum.from_any(OtherEnum.TWO))
        self.assertEqual(MultiValEnum.DELTA, MultiValEnum.from_any('Yomama', MultiValEnum.DELTA))
        self.assertIsNone(MultiValEnum.from_any('Yomama', None))