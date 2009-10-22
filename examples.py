from Record import Record

# Hello, World!
# step 1. Make a record
# step 2. Override __str__

class FancyMessage(Record("salutation", "recipient")):
   def __str__(self):
      return "%s, %s!" % self

print FancyMessage("Hello", "World")

# step 3. Override __new__ (not __init__!) to provide defaults
# step 4. Learn to use setXYZ() and alter()

class MessageToWorld(FancyMessage):
    def __new__(cls, salutation = "Hello", recipient = "World"):
        return cls.new(salutation, recipient)

print MessageToWorld()
print MessageToWorld("Goodbye").setRecipient("Nation")
print MessageToWorld("Goodbye", "Nation").alter(salutation = "Hello", recipient = "World")


