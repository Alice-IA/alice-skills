import time

from behave import given, when

from alice.messagebus import Message

@given('a device is asleep')
def sleep_device(context):
    context.bus.emit(Message('recognizer_loop:sleep'))
    time.sleep(2)

@when('a wake up message is emitted')
def emit_wake_up(context):
    context.bus.emit(Message('alice.awoken'))
