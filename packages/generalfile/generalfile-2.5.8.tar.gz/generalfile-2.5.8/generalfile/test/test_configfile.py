
from generalfile.test.test_path import PathTest
from generalfile.configfile import ConfigFile

from generallibrary import Ver
from generalfile import Path


class TestConfigFile(PathTest):
    def test_suffix(self):
        class A(ConfigFile):
            name = "foo"
        self.assertRaises(AssertionError, A, path="hi")
        self.assertRaises(AssertionError, A, path="json")
        self.assertRaises(AssertionError, A, path="foo.json.test")
        A(path="foo.json")
        A(path="foos.JSON")
        A(path="foo.cfg")
        A(path="foos.CFG")
        A(path="foo.test.cfg")

    def test_file(self):
        class A(ConfigFile):
            name = "foo"
        a = A(path="foo.json")

        self.assertEqual(False, a._path.exists())
        a.name = "bar"
        self.assertEqual(True, a._path.exists())

        b = A(path="foo.json")
        self.assertEqual("bar", b.name)

    def test_name(self):
        class A(ConfigFile):
            name = "foo"
        a = A(path="foo.json")
        self.assertEqual("foo", a.name)

        a.name = "bar"
        self.assertEqual("bar", a.name)

    def test_default_path(self):
        class A(ConfigFile):
            name = "foo"
            def __init__(self, path="foo.json"):
                pass
        a = A()

        self.assertEqual(False, a._path.exists())
        a.name = "bar"
        self.assertEqual(True, a._path.exists())

        b = A(path="foo.json")
        self.assertEqual("bar", b.name)

    def test_serializer_with_default(self):
        class A(ConfigFile):
            ver = Ver(0.2)
        a = A(path="foo.json")

        self.assertEqual(Ver(0.2), a.ver)
        a.write_config()
        a._read_config()
        self.assertEqual(Ver(0.2), a.ver)
        self.assertIsInstance(a.ver, Ver)

    def test_serializer_with_annotation(self):
        class A(ConfigFile):
            ver: Ver = Ver(0.2)
        a = A(path="foo.json")

        self.assertEqual(Ver(0.2), a.ver)
        a.write_config()
        a._read_config()
        self.assertEqual(Ver(0.2), a.ver)
        self.assertIsInstance(a.ver, Ver)

    def test_serializer_with_only_annotation(self):
        class A(ConfigFile):
            ver: Ver = None
        a = A(path="foo.json")

        self.assertIs(None, a.ver)
        a.write_config()
        a._read_config()
        self.assertIs(None, a.ver)

        a.ver = Ver("0.2.1")
        self.assertEqual(Ver("0.2.1"), a.ver)
        self.assertIsInstance(a.ver, Ver)

    def test_get_custom_serializers(self):
        class A(ConfigFile):
            ver: Ver = None
            ver2 = Ver(5)
            x = 2
            y = "foo"
            z = ["bar"]
            path = Path("foo")
            path2: Path = Path("bar")

            def __init__(self, path="foo.json"):
                pass

        self.assertEqual({
            "ver": Ver,
            "ver2": Ver,
            "path": Path,
            "path2": Path
        }, A(path="foo.json").get_custom_serializers())

        x = A().field_dict().copy()

        A().write_config()
        A()._read_config()

        self.assertEqual(x, A().field_dict())

    def test_recycle(self):
        class A(ConfigFile):
            pass

        self.assertIs(A("x.json"), A("x.json"))
        self.assertIsNot(A("x.json"), A("y.json"))

    def test_field_keys(self):
        class A(ConfigFile):
            ver: Ver = None
            ver2 = Ver(5)
            x = 2
            y = "foo"
            z = ["bar"]
            path = Path("foo")
            path2: Path = Path("bar")

        self.assertCountEqual([
            "ver",
            "ver2",
            "x",
            "y",
            "z",
            "path",
            "path2",
        ], A("foo.json").field_keys())

        a = A(path="foo.json")

        a.x = 3

        self.assertEqual({
            "ver": None,
            "ver2": Ver(5),
            "x": 2,
            "y": "foo",
            "z": ["bar"],
            "path": Path("foo"),
            "path2": Path("bar"),
        }, a.field_dict_defaults())

    def test_load_on_init(self):
        class A(ConfigFile):
            foo = "hi"

        Path("foo.json").write({"foo": "bar"})

        a = A("foo.json")
        self.assertEqual("bar", a.foo)

    def test_remove_unused(self):
        class A(ConfigFile):
            foo = "hi"

        Path("foo.json").write({
            "foo": "bar",
            "unused": True,
        })

        a = A("foo.json")
        self.assertEqual(a.foo, "bar")
        self.assertRaises(AttributeError, getattr, a, "unused")

        self.assertEqual({
            "foo": "bar",
            "unused": True,
        }, Path("foo.json").read())

        a.foo = "hi"

        # unused is removed at first write, dont force it
        self.assertEqual({
            "foo": "hi",
        }, Path("foo.json").read())

    def test_only_annotation(self):
        class A(ConfigFile):
            name: str
        a = A("foo.json")
        self.assertEqual([], a.field_keys())
        self.assertRaises(AttributeError, getattr, a, "name")

    def test_only_annotation_which_is_serializer(self):
        class A(ConfigFile):
            version: Ver
        a = A("foo.json")
        self.assertEqual([], a.field_keys())
        self.assertRaises(AttributeError, getattr, a, "ver")

    def test_dict(self):
        class A(ConfigFile):
            x = {"Foo": "bar", "5": 2}
        a = A(path="foo.json")

        self.assertEqual({"Foo": "bar", "5": 2}, a.x)
        a.write_config()
        a._read_config()
        self.assertEqual({"Foo": "bar", "5": 2}, a.x)





class TestConfigFileCFG(PathTest):
    def test_file(self):
        class A(ConfigFile):
            name = "foo"
        a = A(path="foo.cfg")

        self.assertEqual(False, a._path.exists())
        a.name = "bar"
        self.assertEqual(True, a._path.exists())

        b = A(path="foo.cfg")
        self.assertEqual("bar", b.name)

    def test_name(self):
        class A(ConfigFile):
            name = "foo"
        a = A(path="foo.cfg")
        self.assertEqual("foo", a.name)

        a.name = "bar"
        self.assertEqual("bar", a.name)

    def test_default_path(self):
        class A(ConfigFile):
            name = "foo"
            def __init__(self, path="foo.cfg"):
                pass
        a = A()

        self.assertEqual(False, a._path.exists())
        a.name = "bar"
        self.assertEqual(True, a._path.exists())

        b = A(path="foo.cfg")
        self.assertEqual("bar", b.name)

    def test_serializer_with_default(self):
        class A(ConfigFile):
            ver = Ver(0.2)
        a = A(path="foo.cfg")

        self.assertEqual(Ver(0.2), a.ver)
        a.write_config()
        a._read_config()
        self.assertEqual(Ver(0.2), a.ver)
        self.assertIsInstance(a.ver, Ver)

    def test_serializer_with_annotation(self):
        class A(ConfigFile):
            ver: Ver = Ver(0.2)
        a = A(path="foo.cfg")

        self.assertEqual(Ver(0.2), a.ver)
        a.write_config()
        a._read_config()
        self.assertEqual(Ver(0.2), a.ver)
        self.assertIsInstance(a.ver, Ver)

    def test_serializer_with_only_annotation(self):
        class A(ConfigFile):
            ver: Ver = None
        a = A(path="foo.cfg")

        self.assertIs(None, a.ver)
        a.write_config()
        a._read_config()
        self.assertIs(None, a.ver)

        a.ver = Ver("0.2.1")
        self.assertEqual(Ver("0.2.1"), a.ver)
        self.assertIsInstance(a.ver, Ver)

    def test_get_custom_serializers(self):
        class A(ConfigFile):
            ver: Ver = None
            ver2 = Ver(5)
            x = 2
            y = "foo"
            z = ["bar"]
            path = Path("foo")
            path2: Path = Path("bar")

            def __init__(self, path="foo.cfg"):
                pass

        self.assertEqual({
            "ver": Ver,
            "ver2": Ver,
            "path": Path,
            "path2": Path
        }, A(path="foo.cfg").get_custom_serializers())

        x = A().field_dict().copy()

        A().write_config()
        A()._read_config()

        self.assertEqual(x, A().field_dict())

    def test_recycle(self):
        class A(ConfigFile):
            pass

        self.assertIs(A("x.cfg"), A("x.cfg"))
        self.assertIsNot(A("x.cfg"), A("y.cfg"))

    def test_field_keys(self):
        class A(ConfigFile):
            ver: Ver = None
            ver2 = Ver(5)
            x = 2
            y = "foo"
            z = ["bar"]
            a = {"foo": "bar"}
            path = Path("foo")
            path2: Path = Path("bar")

        self.assertCountEqual([
            "ver",
            "ver2",
            "x",
            "y",
            "z",
            "a",
            "path",
            "path2",
        ], A("foo.cfg").field_keys())

        a = A(path="foo.cfg")

        a.x = 3

        self.assertEqual({
            "ver": None,
            "ver2": Ver(5),
            "x": 2,
            "y": "foo",
            "z": ["bar"],
            "a": {"foo": "bar"},
            "path": Path("foo"),
            "path2": Path("bar"),
        }, a.field_dict_defaults())

    def test_load_on_init(self):
        class A(ConfigFile):
            foo = "hi"

        Path("foo.cfg").cfg.write({A._CFG_HEADER_NAME: {"foo": "bar"}})

        a = A("foo.cfg")
        self.assertEqual(a.foo, "bar")

    def test_remove_unused(self):
        class A(ConfigFile):
            foo = "hi"

        Path("foo.cfg").cfg.write({A._CFG_HEADER_NAME: {
            "foo": "bar",
            "unused": True,
        }})

        a = A("foo.cfg")
        self.assertEqual(a.foo, "bar")
        self.assertRaises(AttributeError, getattr, a, "unused")

        self.assertEqual({A._CFG_HEADER_NAME: {
            "foo": "bar",
            "unused": True,
        }}, Path("foo.cfg").cfg.read())

        a.foo = "hi"

        # unused is removed at first write, dont force it
        self.assertEqual({A._CFG_HEADER_NAME: {
            "foo": "hi",
        }}, Path("foo.cfg").cfg.read())

    def test_only_annotation(self):
        class A(ConfigFile):
            name: str
        a = A("foo.cfg")
        self.assertEqual([], a.field_keys())
        self.assertRaises(AttributeError, getattr, a, "name")

    def test_only_annotation_which_is_serializer(self):
        class A(ConfigFile):
            version: Ver
        a = A("foo.cfg")
        self.assertEqual([], a.field_keys())
        self.assertRaises(AttributeError, getattr, a, "ver")

    def test_dict(self):
        class A(ConfigFile):
            x = {"Foo": "bar", "5": 2}
        a = A(path="foo.cfg")

        self.assertEqual({"Foo": "bar", "5": 2}, a.x)
        a.write_config()
        a._read_config()
        self.assertEqual({"Foo": "bar", "5": 2}, a.x)

    def test_list(self):
        class A(ConfigFile):
            x = ["foo", "bar"]
        a = A(path="foo.cfg")

        self.assertEqual(["foo", "bar"], a.x)
        a.write_config()
        a._read_config()
        self.assertEqual(["foo", "bar"], a.x)
















