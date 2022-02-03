"""
Unit tests for flobject module
"""
import weakref
from ansys.fluent.solver import flobject
from collections.abc import MutableMapping

class Setting:
    """Base class for setting objects"""
    def __init__(self, parent):
        self.parent = None if parent is None else weakref.proxy(parent)

class PrimitiveSetting(Setting):
    """Primitive setting objects"""
    value = None

    def get_state(self):
        return self.value

    def set_state(self, value):
        self.value = value

    @classmethod
    def get_static_info(cls):
        ret = { 'type' : cls.objtype }
        if cls.__doc__:
            ret['help'] = cls.__doc__
        return ret

class Bool(PrimitiveSetting):
    objtype = 'boolean'

class Int(PrimitiveSetting):
    objtype = 'integer'

class Real(PrimitiveSetting):
    objtype = 'real'

class String(PrimitiveSetting):
    objtype = 'string/symbol'

class BoolList(PrimitiveSetting):
    objtype = 'boolean-list'

class IntList(PrimitiveSetting):
    objtype = 'integer-list'

class RealList(PrimitiveSetting):
    objtype = 'real-list'

class StringList(PrimitiveSetting):
    objtype = 'string-list'

class Group(Setting):
    """Group objects"""

    objtype = 'group'
    members = {}
    commands = {}

    def __init__(self, parent):
        super().__init__(parent)
        self.objs = { c : v(self) for c, v in self.members.items() }

    def get_state(self):
        ret = {}
        for c in self.members:
            ret[c] = self.objs[c].get_state()
        return ret

    def set_state(self, value):
        for c in self.members:
            v = value.get(c)
            if v is not None:
                self.objs[c].set_state(v)

    def get_child(self, c):
        return self.objs[c]

    def get_command(self, c):
        return self.commands[c](self)

    @classmethod
    def get_static_info(cls):
        ret = { 'type' : cls.objtype }
        if cls.__doc__:
            ret['help'] = cls.__doc__
        if cls.members:
            ret['children'] = {
                    c: v.get_static_info()
                    for c, v in cls.members.items()
                    }
        if cls.commands:
            ret['commands'] = {
                    c: v.get_static_info()
                    for c, v in cls.commands.items()
                    }
        return ret

class NamedObject(Setting, MutableMapping):
    """NamedObject class"""

    objtype = 'named-object'
    commands = {}
    # To be overridden by child classes
    # child_object_type = None

    def __init__(self, parent):
        super().__init__(parent)
        self._objs = {}

    def __getitem__(self, name):
        return self._objs[name].get_state()

    def __setitem__(self, name, value):
        if name not in self._objs:
            self._objs[name] = self.child_object_type(self)
        return self._objs[name].set_state(value)

    def __delitem__(self, name):
        del self._objs[name]

    def __iter__(self):
        return iter(self._objs)

    def __len__(self):
        return len(self._objs)

    def get_child(self, c):
        return self._objs[c]

    def rename(self, new, old):
        self._objs = {
                (new if k == old else k) : v
                for k, v in self._objs.items()
                }

    def get_object_names(self):
        return list(self._objs.keys())

    def get_command(self, c):
        return self.commands[c](self)

    def get_state(self):
        return { c : v.get_state() for c, v in self._objs.items() }

    def set_state(self, state):
        for k, v in state.items():
            self[k] = v

    @classmethod
    def get_static_info(cls):
        ret = { 'type' : cls.objtype }
        if cls.__doc__:
            ret['help'] = cls.__doc__
        ret['object-type'] = cls.child_object_type.get_static_info()
        if cls.commands:
            ret['commands'] = {
                    c: v.get_static_info()
                    for c, v in cls.commands.items()
                    }
        return ret


class ListObject(Setting):
    """ListObject class"""

    objtype = 'list-object'
    commands = {}
    # To be overridden by child classes
    # child_object_type = None

    def __init__(self, parent):
        super().__init__(parent)
        self._objs = []

    def __getitem__(self, index):
        return self._objs[index].get_state()

    def __setitem__(self, index, value):
        return self._objs[index].set_state(value)

    def __iter__(self):
        return iter(self._objs)

    def __len__(self):
        return len(self._objs)

    def size(self):
        return len(self._objs)

    def resize(self, l):
        if l > len(self._objs):
            # pylint: disable=unused-variable
            for i in range(len(self._objs), l):
                self._objs.append(self.child_object_type(self))
        elif l < len(self._objs):
            self._objs = self._objs[:l]

    def get_child(self, c):
        return self._objs[int(c)]

    def get_command(self, c):
        return self.commands[c](self)

    def get_state(self):
        return [ x.get_state() for x in self._objs ]

    def set_state(self, value):
        self.resize(len(value))
        for i, v in enumerate(value):
            self[i] = v

    @classmethod
    def get_static_info(cls):
        ret = { 'type' : cls.objtype }
        if cls.__doc__:
            ret['help'] = cls.__doc__
        ret['object-type'] = cls.child_object_type.get_static_info()
        if cls.commands:
            ret['commands'] = {
                    c: v.get_static_info()
                    for c, v in cls.commands.items()
                    }
        return ret

class Command(Group):
    """Command class"""

    objtype = 'command'
    # To be overridden by child classes
    # arguments = None
    # cb = None

    def __call__(self, **kwds):
        args = []
        for k, v in self.arguments.items():
            a = kwds.get(k, v(self).get_state())
            args.append(a)
        return self.cb(*args)

    @classmethod
    def get_static_info(cls):
        ret = { 'type' : cls.objtype }
        if cls.__doc__:
            ret['help'] = cls.__doc__
        if cls.arguments:
            ret['arguments'] = {
                    c: v.get_static_info()
                    for c, v in cls.commands.items()
                    }
        return ret

class Root(Group):
    """Root class"""
    class G1(Group):
        members = {
                'r-1' : Real,
                'i-2' : Int,
                'b-3' : Bool,
                's-4' : String,
                }

    class N1(NamedObject):
        class NC(Group):
            members = {
                    'rl-1' : RealList,
                    'sl-1' : StringList,
                    }

        child_object_type = NC

    class L1(ListObject):
        class LC(Group):
            members = {
                    'il-1' : IntList,
                    'bl-1' : BoolList,
                    }
        child_object_type = LC

    class Command1(Command):
        """Command1 class"""
        class A1(Real):
            value = 2.3

        class A2(Bool):
            value = True

        arguments = {
                'a1' : A1,
                'a2' : A2,
                }

        def cb(self, a1, a2):
            if a2 is True:
                self.parent.objs['g-1'].objs['r-1'].value += a1
            else:
                self.parent.objs['g-1'].objs['r-1'].value -= a1

    members = {
            'g-1' : G1,
            'n-1' : N1,
            'l-1' : L1,
            }

    commands = {
            'c-1' : Command1,
            }

class Proxy:
    """Proxy class"""

    root = Root

    def __init__(self):
        self.r = self.root(None)

    def get_obj(self, path):
        if not path:
            return self.r
        obj = self.r
        for c in path.split('/'):
            obj = obj.get_child(c)
        return obj

    def get_var(self, path):
        return self.get_obj(path).get_state()

    def set_var(self, path, value):
        return self.get_obj(path).set_state(value)

    def rename(self, path, new, old):
        return self.get_obj(path).rename(new, old)

    def create(self, path, name):
        self.get_obj(path)[name] = {}

    def delete(self, path, name):
        del self.get_obj(path)[name]

    def resize_list_object(self, path, size):
        return self.get_obj(path).resize(size)

    def get_list_size(self, path):
        return self.get_obj(path).size()

    def get_object_names(self, path):
        return self.get_obj(path).get_object_names()

    def execute_cmd(self, path, command, **kwds):
        return self.get_obj(path).get_command(command)(**kwds)

    @classmethod
    def get_obj_static_info(cls):
        return cls.root.get_static_info()

def test_primitives():
    r = flobject.get_root(Proxy())
    r.g_1.r_1 = 3.2
    assert r.g_1.r_1() == 3.2
    r.g_1.i_2 = -3
    assert r.g_1.i_2() == -3
    r.g_1.b_3 = True
    assert r.g_1.b_3() is True
    r.g_1.b_3 = False
    assert r.g_1.b_3() is False
    r.g_1.s_4 = 'foo'
    assert r.g_1.s_4() == 'foo'
    return True

def test_group():
    r = flobject.get_root(Proxy())
    r.g_1 = {'r_1' : 3.2, 'i_2' : -3, 'b_3' : False, 's_4' : 'foo' }
    assert r.g_1() == { 'r_1': 3.2, 'i_2' : -3, 'b_3' : False, 's_4' : 'foo' }
    r.g_1 = {'s_4' : 'bar'}
    assert r.g_1() == { 'r_1': 3.2, 'i_2' : -3, 'b_3' : False, 's_4' : 'bar' }
    r.g_1.i_2 = 4
    assert r.g_1() == { 'r_1': 3.2, 'i_2' : 4, 'b_3' : False, 's_4' : 'bar' }
    return True

def test_named_object():
    r = flobject.get_root(Proxy())
    assert r.n_1.object_names == []
    r.n_1['n1'] = {}
    r.n_1['n2'] = {}
    assert r.n_1.object_names == ['n1', 'n2']
    r.n_1.rename('n3', 'n1')
    assert r.n_1.object_names == ['n3', 'n2']
    r.n_1.create('n4')
    assert r.n_1.object_names == ['n3', 'n2', 'n4']
    del r.n_1['n3']
    assert r.n_1.object_names == ['n2', 'n4']
    r.n_1['n1'] = { 'rl_1' : [1.2, 3.4], 'sl_1' : ['foo', 'bar']}
    assert r.n_1['n1']() == { 'rl_1' : [1.2, 3.4], 'sl_1' : ['foo', 'bar']}
    r.n_1 = {'n5' : { 'rl_1' : [4.3, 2.1], 'sl_1' : ['oof', 'rab']} }
    assert r.n_1.object_names == ['n2', 'n4', 'n1', 'n5']
    assert r.n_1['n5']() == { 'rl_1' : [4.3, 2.1], 'sl_1' : ['oof', 'rab']}

    return True

def test_list_object():
    r = flobject.get_root(Proxy())
    assert r.l_1.size == 0
    r.l_1.resize(3)
    assert r.l_1.size == 3
    r.l_1.resize(2)
    assert r.l_1.size == 2
    assert r.l_1() == [{'il_1' : None, 'bl_1' : None},
                       {'il_1' : None, 'bl_1' : None}]
    r.l_1[1].il_1 = [1, 2]
    assert r.l_1() == [{'il_1' : None, 'bl_1' : None},
                       {'il_1' : [1, 2], 'bl_1' : None}]
    r.l_1 = [{'il_1' : [3], 'bl_1' : [True, False]}]
    assert r.l_1() == [{'il_1' : [3], 'bl_1' : [True, False]}]

    return True

def test_command():
    r = flobject.get_root(Proxy())
    r.g_1.r_1 = 2.4
    r.c_1()
    assert r.g_1.r_1() == 2.4 + 2.3
    r.c_1(a2 = False)
    assert r.g_1.r_1() == 2.4 + 2.3 - 2.3
    r.c_1(a1 = 3.2, a2 = True)
    assert r.g_1.r_1() == 2.4 + 2.3 - 2.3 + 3.2
    r.c_1(a1 = 4.5, a2 = False)
    assert r.g_1.r_1() == 2.4 + 2.3 - 2.3 + 3.2 - 4.5