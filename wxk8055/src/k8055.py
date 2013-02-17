import _k8055
from _k8055 import BoardError

kcmd=dict(
    INIT=0x00,
    SETDBT1=0x01,
    SETDBT2=0x02,
    RESETCNT1=0x03,
    RESETCNT2=0x04,
    SETOUTPUT=0x05
    )
    
def _msec_to_dbt_code(msec):
    """Function to convert msec to the DebounceTime encoding calculated by nicolas dot sutre at free dot fr"""
    if msec < 2:
        return 1
    elif msec < 10:
        return 3
    elif msec < 1000:
        return 8
    elif msec < 5000:
        return 88
    else:
        return 255

class Command(list):
    """Represent an empty command sent to board"""
    _len = 8
    def __init__(self, cmd=None):
        self[:] = [0 for i in range(self._len)]
        if cmd:
            self[0] = kcmd[cmd]
        
class OutputCommand(Command):
    def __init__(self):
        Command.__init__(self,'SETOUTPUT')

    def set_d(self, value): self[1] = value; return value
    def set_a1(self, value): self[2] = value; return value
    def set_a2(self, value): self[3] = value; return value

class Debounce1Command(Command):
    def __init__(self, value):
        Command.__init__(self,'SETDBT1')
        self[6] = _msec_to_dbt_code(value)

class Debounce2Command(Command):
    def __init__(self, value):
        Command.__init__(self,'SETDBT2')
        self[7] = _msec_to_dbt_code(value)

class Board:
    def __init__(self, address=0):
        self._output = OutputCommand()
        self.digital_outputs = [0,0,0,0,0,0,0,0]
        self.analog_output1 = 0
        self.analog_output2 = 0
        self.debounce1 = 0
        self.debounce2 = 0
        self.address = _k8055.open(address)
        self.reset()
        self.read()

    def reset(self):
        _k8055.write(self.address, Command('INIT'))
        self.set_analog1(0)
        self.set_analog2(0)
        self.reset_digital_outputs()

    def read(self):
        """Read all inputs channel and counter from board"""
        inputs = _k8055.read(self.address)
        
        self.counter1 = inputs['counter1']
        self.counter2 = inputs['counter2']

        self.analog1 = inputs['analog1']
        self.analog2 = inputs['analog2']

        d = inputs['digitals']
        self.digital_inputs = [d&(2**i)>0 for i in range(5)]

    def reset_counter1(self):
        _k8055.write(self.address, Command('RESETCNT1'))
    
    def reset_counter2(self):
        _k8055.write(self.address, Command('RESETCNT2'))

    def reset_digital_outputs(self):
        self.set_digital_outputs([0,0,0,0,0,0,0,0])

    def set_digital_outputs(self, outputs=None):
        """outputs is a list of 0,1 or None"""
        if outputs:
            self.digital_outputs = outputs
        self._output.set_d(sum([x*2**i for i,x in enumerate(self.digital_outputs)]))
        self._write()

    def _write(self):
        _k8055.write(self.address, self._output)
    
    def set_digital_output(self, channel, data=1):
        self.digital_outputs[channel%8] = data
        self.set_digital_outputs(self.digital_outputs)
    
    def set_analog1(self, value):
        """Set analog output"""
        self.analog_output1 = self._output.set_a1(value)
        self._write()
    
    def set_analog2(self, value):
        """Set analog output"""
        self.analog_output2 = self._output.set_a2(value)
        self._write()

    def set_debounce1(self, value):
        """Set debounce time for counter 1 (in msec)"""
        self.debounce1 = value
        _k8055.write(self.address, Debounce1Command(value))
        self._write()
    
    def set_debounce2(self, value):
        """Set debounce time for counter 2 (in msec)"""
        self.debounce2 = value
        _k8055.write(self.address, Debounce2Command(value))
        self._write()

    def close(self):
        _k8055.close(self.address)

    def __str__(self):
        self.read()
        ss = []
        ss.append("Board %s address -------" % self.address)
        ss.append(" digital inputs: %s" % self.digital_inputs)
        ss.append(" analog input 1: %d" % self.analog1)
        ss.append(" analog input 2: %d" % self.analog2)
        ss.append(" digital outputs: %s" % self.digital_outputs)
        ss.append(" analog output 1: %d" % self.analog_output1)
        ss.append(" analog output 2: %d" % self.analog_output2)
        ss.append(" counter 1: %d" % self.counter1)
        ss.append(" counter 2: %d" % self.counter2)
        ss.append(" debounce counter 1: %d" % self.debounce1)
        ss.append(" debounce counter 2: %d" % self.debounce2)
        return "\n".join(ss)

if __name__ == '__main__':
    print Board(address=0)

