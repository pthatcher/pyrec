# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import operator
from itertools import islice

def Record(*slots):
    class cls(RecordBase):
        pass

    cls.setSlots(slots)

    return cls

class RecordBase(tuple):
    SLOTS = ()

    ## overide this one instead of __init__
    def __new__(cls, *values):
        assert len(values) == len(cls.SLOTS)
        return tuple.__new__(cls, values)

    ## use this when overriding __new__
    @classmethod
    def new(cls, *values):
        assert len(values) == len(cls.SLOTS)
        return tuple.__new__(cls, values)

    def __iter__(self):
        return islice(tuple.__iter__(self), len(self.SLOTS))

    ## use this when overriding __iter__
    @property
    def values(self):
        return islice(tuple.__iter__(self), len(self.SLOTS))


    def __repr__(self):
        return self.__class__.__name__ + repr(tuple(self.values))

    def alter(self, **value_by_slot):
        return self.new(*(value_by_slot.get(self.SLOTS[index], value)
                          for index, value
                          in enumerate(self.values)))

    def getByIndex(self, index):
        return tuple.__getitem__(self, index)

    def setByIndex(self, set_index, set_value):
        return self.new(*(set_value if set_index == index else value
                          for (index, value)
                          in enumerate(self.values)))


    ## setting up getters and setters
    @classmethod
    def setSlots(cls, slots):
        cls.SLOTS = slots
        for index, slot in enumerate(slots):
            setattr(cls, slot,                      property(cls.makeGetter(index)))
            setattr(cls, "set" + upper_first(slot), cls.makeSetter(index))

    @classmethod
    def makeGetter(cls, index):
        return lambda self : self.getByIndex(index)

    @classmethod
    def makeSetter(cls, index):
        return lambda self, value: self.setByIndex(index, value)

    ## for Pickling

    def __getnewargs__(self):
        return self

def upper_first(string):
    return string[0].upper() + string[1:]
    

class LinkedList(Record("first", "rest")):
    def __new__(cls, first, rest = None):
        return cls.new(first, rest)

    def __getitem__(self, index):
        return iget(self, index)

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
        
    class Person(Record("name", "age")):
        pass

    name   = "peter"
    age    = 25

    peter  = Person(name, age)
    assert peter.name          == name 
    assert peter[0]            == name 
    assert peter.age           == age
    assert peter[1]            == age
    assert tuple(peter.values) == (name, age)
    assert tuple(peter)        == (name, age)
    assert peter               == Person("peter", 25)
    assert repr(peter)         == "Person('peter', 25)"
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
    assert names3[1]     == "bob"
    assert names3[0]     == "charlie"
    assert err(lambda : names3[3], IndexError)

    assert (names3.first, list(names3.rest)) == ("charlie", ["bob", "alice"])
