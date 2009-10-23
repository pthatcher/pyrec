from collections import namedtuple

def NamedTuple(name, *slots):
    class cls(namedtuple(name, slots)):
        @classmethod
        def new(cls, *values):
            return cls._make(values)

        @property
        def values(self):
            return tuple.__iter__(self)

        def alter(self, **kargs):
            return self._replace(**kargs)

        @property
        def namedValues(self):
            return ((self._fields[index], value) for (index, value) in enumerate(self.values))

        @classmethod
        def fromNamedValues(cls, named_values):
            return cls.fromDict(dict(named_values))

        @classmethod
        def fromDict(cls, dct, default = None):
            return cls.new(*(dct.get(slot, default) for slot in cls._fields))

        @classmethod
        def makeSetter(cls, index):
            return lambda self, value: self.setByIndex(index, value)

        def setByIndex(self, set_index, set_value):
            return self._make((set_value if set_index == index else value
                               for (index, value)
                               in enumerate(self.values)))


    for index, slot in enumerate(slots):
        setattr(cls, "set" + upper_first(slot), cls.makeSetter(index))
        
    cls.__name__ = name
    return cls

def upper_first(string):
    return string[0].upper() + string[1:]

class LinkedList(NamedTuple("LinkedList", "first", "rest")):
    def __new__(cls, first, rest = None):
        return cls.new(first, rest)

    # doesn't work with namedtuple :(
    #def __getitem__(self, index):
    #    return iget(self, index)

    def __iter__(rest):
        while True:
            first, rest = rest.values
            yield first
            if rest is None:
                raise StopIteration

    def cons(self, value):
        return self.new(value, self)

if __name__ == "__main__":
    # tests
    def err(code, err_type = Exception):
        try:
            code()
        except err_type, error:
            return error


    Person = NamedTuple("Person", "name", "age")

    name   = "peter"
    age    = 25

    peter  = Person(name, age)
    assert peter.name          == name 
    assert peter[0]            == name 
    assert peter.age           == age
    assert peter[1]            == age
    assert tuple(peter.values) == (name, age)
    assert tuple(peter)        == (name, age)
    assert list(peter.namedValues) == [("name", name), ("age", age)]
    assert peter               == Person("peter", 25)
    #assert repr(peter)         == "Person('peter', 25)"
    assert peter               == Person.fromNamedValues(peter.namedValues)
    assert peter               == Person.fromDict(dict(peter.namedValues))
    assert err(lambda : peter.height, AttributeError)
    assert err(lambda : peter[2],     IndexError)
    assert err(lambda : Person())
    assert err(lambda : Person("peter"))

    assert peter.alter(age = 29) == Person(name, 29)
    assert peter.setAge(29)      == Person(name, 29)
    assert peter.alter(name = "grandpa", age = 99) == Person("grandpa", 99)
    assert peter.setName("grandpa").setAge(99)     == Person("grandpa", 99)

    def iget(itr, index):
        try:
            itr = iter(itr)
            for _ in xrange(index):
                itr.next()
            return itr.next()
        except StopIteration:
            raise IndexError


    names1  = LinkedList("alice")
    names2  = names1.cons("bob")
    names2z = names1.cons("zed")
    names3  = names2.cons("charlie")

    assert list(names1)  == ["alice"]
    assert list(names2)  == ["bob", "alice"]
    assert list(names2z) == ["zed", "alice"]
    assert list(names3)  == ["charlie", "bob", "alice"]
    # doesn't work with namedtuple :(
    #assert names3[1]     == "bob"
    #assert names3[0]     == "charlie"
    assert err(lambda : names3[3], IndexError)

    assert names3.first == "charlie"
    assert (names3.first, list(names3.rest)) == ("charlie", ["bob", "alice"])
    print "passed"
