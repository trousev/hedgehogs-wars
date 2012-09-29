import sys
import socket
import struct
import pickle

__all__ = ('Connection', 'Server', 'Client', 'ProtoError', 'KilledError')

# BIG FAT TODO: Error handling is lacking. In particular, there's no mention
# of EOFError anywhere and a client can crash the server by simply
# disconnecting.

class ProtoError(IOError):
    """Malfunctioning server or client disregarded the protocol."""
    pass

# TODO This probably belongs in 'game' instead.
class KilledError(RuntimeError):
    pass

class Connection(object):
    def __init__(self):
        pass

    def _bind(self, socket):
        """Bind this connection object to the given socket."""
        self._socket = socket
        self._buffer = bytearray()

    def _recvall(self, length):
        """Receive a given number of bytes from the underlying socket."""

        # TODO Timeout handling here (accounting for *total* time consumed
        # during reception, not just one chunk)!

        while len(self._buffer) < length:
            self._buffer.extend(self._socket.recv(4096))
        result = self._buffer[:length]
        del self._buffer[:length]
        return result

    def send(self, *args):
        """Send the given Python object over the wire."""
        bytes = pickle.dumps(tuple(args))
        self._socket.sendall(struct.pack('!I', len(bytes)) + bytes)

    def receive(self):
        """Wait for the other party to send an object and return it."""
        try:
            size, = struct.unpack('!I', self._recvall(4))
            return pickle.loads(self._recvall(size))
        except struct.error:
            raise ProtoError('malformed packet header')
        except pickle.PickleError:
            raise ProtoError('failed to decode packet')

class Server(object):
    def __init__(self, width, height, players, address='127.0.0.1', port=8966): # TODO timeout?
        self.width, self.height = width, height
        print (port)
          # TODO Broadcast more game parameters (in a dict?)
        self.count = players
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((address, port))

    def greet(self):
        """Accept player connections and broadcast game parameters."""
        
        self._socket.listen(5)
        self.players = dict()
        for i in range(self.count):
            clisock, cliaddr = self._socket.accept()
            player = Player(clisock)

            try:
                name, = player.receive()
            except ValueError:
                raise ProtoError('invalid greeting packet')

            if not isinstance(name, str):
                raise ProtoError('invalid greeting packet')
            if name in self.players:
                raise RuntimeError('name conflict')

            player.name = name
            self.players[name] = player

        names = list(self.players.keys())
        
        for name, player in self.players.items():
            player.send(self.width, self.height, names)

        return names
        
    first_phase_pack = {
    
      'throw':          (0, 0),
      'go':             (2, 2),
      
    }
    
        
    def moves(self): #TODO now I made some shit here
        """Receive moves from players (phase 1) and return them in a generator."""
        """In fact, now there is not only moves"""
        for name, player in self.players.items():
            
            try:
                action, *params = player.receive()
                
                if action not in self.first_phase_pack or len(params) != len(self.first_phase_pack[action]):
                    raise ValueError
                """if (not isinstance(i, int) or abs(i) >= 2 or
                    not isinstance(j, int) or abs(j) >= 2):
                  raise ValueError"""
                for value, limit in zip(params, self.first_phase_pack[action]):
                    if not isinstance(value, int) or (limit != 0 and abs(value) >= limit):
                        raise ValueError
            except ValueError:
                player.status = 'proto-error'
            else:
                yield (name, action) + tuple(params)
                
                
             
    packets = {
      'relax':          (),
      #'throw':          (0, 0),
      'eat-from-cell':  (),
      'eat-from-bag':   (),
      'prick':          (2, 2, 0),
      'pick':           (),
    }

    def actions(self):
        """"Receive player actions (phase 2) and return them in a generator."""
        for name, player in self.players.items():
            try:
                action, *params = player.receive()
                if action not in self.packets or len(params) != len(self.packets[action]):
                    raise ValueError
                for value, limit in zip(params, self.packets[action]):
                    if not isinstance(value, int) or (limit != 0 and abs(value) >= limit):
                        raise ValueError
            except ValueError:
                player.status = 'proto-error'
            else:
                yield (name, action) + tuple(params)

    def kill(self, name):
        self.players[name].status = 'killed'

    def announce(self):
        for name, player in list(self.players.items()):
            player.send(player.status)
            if player.status != 'ok':
                player._socket.close()
                del self.players[name]

    def broadcast(self, data):
        for name, wdata in data:
           
            self.players[name].send(wdata)

    def shutdown(self):
        for player in self.players.values():
            player.send('done')
            player._socket.close()
        self._socket.close()

class Player(Connection):
    def __init__(self, sock):
        self._bind(sock)
        self.name = None
        self.status = 'ok'

class Client(Connection):
    def __init__(self, name, address='127.0.0.1', port = 8966):
        print (port)
        self.name = name
        self.server = (address, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._bind(sock)
        self._cab_flag = False

    def connect(self):
        self._socket.connect(self.server)
        self.send(self.name)
        self.fwidth, self.fheight, self.players = self.receive()

        self._phase = 3
        while True:
            wdata, = self.receive()
            self._phase = (self._phase + 1) % 4
            yield wdata
            assert self._phase % 2 == 1

            status, = self.receive()
            
            
            
            if status == 'ok':
                pass
            elif status == 'done':
                self._socket.close()
                raise StopIteration
            elif status == 'killed':
                self._socket.close()
                raise KilledError
            else:
                self._socket.close()
                raise ProtoError("unknown status code '{0}'".format(status))
                
            self._cab_flag = False
            #TODO check this flag!

    def go(self, i, j):
        assert (self._phase == 0 and isinstance(i, int) and abs(i) < 2 and
                                     isinstance(j, int) and abs(j) < 2)
        self.send('go', i, j)
        self._phase = 1

    def relax(self):
        assert self._phase == 2
        self.send('relax')
        self._phase = 3
        

    def throw_cabbage(self, i, j):
        assert self._phase == 0 and isinstance(i, int) and isinstance(j, int)
        self.send('throw', i, j)
        self._phase = 1
        self._cab_flag = True
        

    def eat_from_cell(self):
        assert (self._phase == 2 and self._cab_flag == False)
        self.send('eat-from-cell')
        self._phase = 3

    def eat_from_bag(self):
        assert (self._phase == 2 and self._cab_flag == False)
        self.send('eat-from-bag')
        self._phase = 3

    def prick(self, i, j, power):
        assert (self._phase == 2 and
                isinstance(i, int) and abs(i) < 2 and
                isinstance(j, int) and abs(j) < 2 and
                isinstance(power, int) and self._cab_flag == False)
        self.send('prick', i, j, power)
        self._phase = 3

    def pick(self):
        assert (self._phase == 2 and self._cab_flag == False)
        self.send('pick')
        self._phase = 3
