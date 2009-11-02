from Record import Record

# step 0. Make a record

class SalutationMessage(Record("salutation", "recipient")):
    pass

msg = SalutationMessage("Hello", "World")
print "%s, %s!" % (msg.salutation, msg.recipient)


# step 1. Override __str__

class EasySalutationMessage(SalutationMessage):
   def __str__(self):
      return "%s, %s!" % self

print EasySalutationMessage("Hello", "World")

# step 2. Override __new__ (not __init__!) to provide defaults
# step 3. Learn to use set_xyz() and alter()

class MessageToWorld(EasySalutationMessage):
    def __new__(cls, salutation = "Hello", recipient = "World"):
        return cls.new(salutation, recipient)

print MessageToWorld("Goodbye").set_recipient("Nation")
print MessageToWorld("Goodbye", "Nation").alter(salutation = "Hello", recipient = "World")


