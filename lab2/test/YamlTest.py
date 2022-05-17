import unittest
import Serializer.serializers.yaml_serializer as lib

import data

ser = lib.YamlSerializer()


class TestYaml(unittest.TestCase):
    def test_func(self):
        self.assertEqual(
            data.test_func(),
            ser.loads(ser.dumps(data.test_func))()
        )

    def test_class(self):
        arg = 12
        obj1 = data.TestClass(arg, arg)
        obj2 = ser.loads(ser.dumps(data.TestClass))(arg, arg)
        self.assertEqual(obj1.count(), obj2.count())

    def test_obj(self):
        obj = data.test_obj
        obj.c = 22
        self.assertEqual(
            obj.count(),
            ser.loads(ser.dumps(obj)).count()
        )

    def test_module(self):
        func = data.func_with_external_logic
        self.assertEqual(
            func(),
            ser.loads(ser.dumps(func))()
        )

    def test_closure(self):
        (arg1, arg2) = (8, 5)
        self.assertEqual(
            data.test_closure()(arg1, arg2),
            ser.loads(ser.dumps(data.test_closure))()(arg1, arg2)
        )


if __name__ == '__main__':
    unittest.main()  # pragma: no cover