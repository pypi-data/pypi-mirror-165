Welcome to the documentation for the Python SNMP library!

NOTE: This library is considered to be in the Beta development phase. For SNMPv1 support, use one of the 0.1.x versions. Version 0.2.x scrapped everything from the previous version, and currently supports only SNMPv3, and can only act as a manager. It will be advanced to v1.0.0 once SNMP versions 1 and 2c are fully supported, agent capabilities are enabled, and the code is adequately tested and documented.

If you are a new user, feel free to check out the Getting Started Guide (under development). A full class reference can be found here (add link).

The unit tests for this library are not intended to provide 100% line, branch, or path coverage, but rather to validate the guarantees made in the documentation. If there is a discrepancy between the unit tests and the class reference, the latter should be viewed as authoritative, and any non-compliant tests should be corrected. The class reference defines the public API. The code doesn't use leading underscores almost at all, so if something is not documented, there is no guarantee that its behavior will not change between "compatible" versions. Nevertheless, there is nothing to stop you from using these features, but you do so at your own risk.

The names of positional arguments are not required to match what is documented.

By convention, for any obj that defines __repr__, the expression "obj == eval(repr(obj))" will evaluate to True. This implies that the object must also define __eq__. This probably only applies to value types, not entities.

I'm starting to question the IncompleteChildClass as a child of SNMPLibraryBug; someone might subclass Asn1Encodable in their own code and get it wrong, but maybe that's a risk I shouldn't be worried about. That's really only a concern with a Constructed type, so I'll have to watch out for that.

Test Guidelines
===============
For all public attributes of each class, make the attribute
a) is defined (i.e. doesn't throw an AttributeError)
b) has the correct type
c) has the expected value
For each function and method, make sure it
a) exists
b) is callable
c) has the correct signature
   - verify select values for each argument
     - cover every case for which behavior is defined
   - verify the names and defaults of keyword arguments
d) returns the expected value and (duck) type
e) has the intended side effects
NOTE: testing cannot guarantee that a function does not have undocumented side-effects

snmp.utils
==========
# everything is noexcept unless noted otherwise, assuming you stick to defined behavior
DummyLock: Many higher-level classes use a lockType argument to allow users to select the type of concurrency protection they need. DummyLock presents a compatible interface, but empty implementations. It is suitable for cases where no concurrency protection is needed.
- supports use with context managers
- acquire(*args, **kwargs): returns True
- release()

NumberGenerator: An iterator object that yields integers spanning an n-bit range (signed or unsigned). It repeats itself every 2^n steps, and the last number in the sequence is always 0.
- __init__(nbits, signed=True)
- __iter__()
- __next__()

typename(obj, qualified=False)
- return the name of type(obj); if obj is an instance of type, it will just return its name
- if qualified is True, it will return a fully-qualified name

subbytes: A subbytes object is like an in-place slice, without the third "step" argument. It wraps a bytes-like object to present a sub-sequence of bytes. It is meant to closely mimic the behavior of a bytes-like object, but does not currently meet the criteria to be called bytes-like.
- __init__(self, data, start=0, stop=None)
  - data is either a bytes-like object or another instance of subbytes
  - start and stop mimic the behavior of the builtin slice() class
    - they must be integers or None
    - behavior for invalid types is not defined
- __bool__()
  - return True if the sequence is non-empty
- __eq__(other)
  - True if self and other represent identical sequences of bytes
- __iter__()
  - returns an iterator to the bytes in the sequence
- __len__()
  - return the length of the sequence
- __repr__()
  - an eval-able repr that will return a near-identical object
- __getitem__(key)
  - supports index or slice, return either a single byte or a slice of the underlying data
  - raises IndexError if the index is out of bounds
- consume()
  - return the first byte in the sequence and advance the head to the next byte
  - raise IndexError if the sequence is empty
- dereference()
  - return the first byte, but leave the sequence unchanged
  - raise IndexError if the sequence is empty
- prune(length)
  - truncate self to length bytes (maximum), and return a subbytes object referencing the excess bytes

snmp.ber
========
# everything is noexcept unless noted otherwise, assuming you stick to defined behavior
EncodeError: sub-type of snmp.exceptions.SNMPException
- indicates that an object cannot be encoded under BER
ParseError: sub-type of snmp.exceptions.IncomingMessageError
- indicates that a message (presumably from an external source) cannot be parsed

Identifier: represents a BER type identifier; documentation should link to a BER reference
- cls: class
- structure: primitive or constructed
- tag: tag
Note that there is nothing to prevent cls from being more than 2 bits, or structure from being more than 1 bit, but if passed to encode, extra bits will be ignored. A result from decode will be within the correct range for each of these fields.

Magic numbers for Identifier fields
- CLASS_UNIVERSAL
- CLASS_APPLICATION
- CLASS_CONTEXT_SPECIFIC
- CLASS_PRIVATE
- STRUCTURE_PRIMITIVE
- STRUCTURE_CONSTRUCTED

decode(data, expected=None, leftovers=False, copy=True): BER decode a sequence of bytes
- data: a bytes-like object or subbytes
- expected: Identifier or None
- leftovers: bool
- copy: bool
The output of this function varies depending on the arguments it receives.
- expected!=None, leftovers=False
  - return the object encoding
- in all other cases, it will return a tuple containing the following
  - an Identifier giving the object type
    - only present if expected is None
  - the object encoding
  - leftover data
    - only present if leftovers evaluates to True
- if copy is True, the object encoding will be a bytes-like object
- if copy is False, the object encoding will be a subbytes object
- the leftover data (if present) will always be a subbytes object referencing the data argument
- if the data is malformed in any way, including the case where the type does not match the expected argument, a ParseError will be raised

encode(identifier, data): BER encode a serialized ASN.1 object
- identifier: Identifier 
- data: a proper bytes-like object
This function contains logic to raise an EncodeError, but your computer doesn't have enough memory to trigger it.

snmp.types
==========
Identifier constants for fundamental types
- INTEGER
- OCTET_STRING
- NULL
- OBJECT_IDENTIFIER
- SEQUENCE

# Validate invariants in the constructor, make encode() noexcept
Asn1Encodable: abstract base class for all ASN.1 types
Inherited Interface:
- __eq__(other): True if (and only if)
  a) self and other are the the exact same type
  b) self.equals(other) returns True
- equals(other): compare the contents of two objects (see child class for more)
- classmethod decode(data, leftovers=False)
  - decode the given data to construct an instance of cls
  - data is a bytes-like object or an instance of subbytes
  - if leftovers is True, it will return a tuple
    - first element is the decoded object
    - second element is a subbytes object containing the leftover data
  - raises a ParseError if the data is malformed
- encode(): encode the object to bytes
  - raises a ValueError if the object is not valid

class Integer(Asn1Encodable): a signed 32-bit integer
- __init__(value: int)
- __repr__()
Inherited Methods:
- equals(other):
  - other must be Integer or a sub-type
  - True if the values of are the same
  - note that a negative value for a signed type is not equal to an unsigned type with the same binary representation
- decode(): raise a ParseError if the decoded value is not in the correct range
  - in some implementations, a 32-bit unsigned integer with the MSB set will be encoded as 5 bytes; to be forgiving to these implementations, this implementation of decode will accept an arbitrary number of leading zero bytes, as long as the value itself meets the constraints for the type
- encode(): raise a ValueError if the value is not in the correct range

class OctetString(Asn1Encodable): an array of bytes
- __init__(data=b"")
- __repr__()
Inherited Methods:
- equals(other):
  - other must be OctetString or a sub-type
  - True if all octets match
- decode(): raise a ParseError if the data is more than 65535 octets
- encode(): raise a ValueError if the data is more than 65535 octets

class Null(Asn1Encodable): an empty object
- __repr__()
- equals(other)
Inherited Methods:
- equals(other):
  - other must be Null or a sub-type
- decode(): if, for some reason, the encoding is non-empty, the contents will be ignored
- encode(): always succeeds

class OID(Asn1Encodable): an object identifier
Error types: I'm not 100% satisfied with these
- BadPrefix(IncomingMessageError)
- IndexDecodeError(IncomingMessageError)
Methods:
- equals(other)
- __repr__()
- __str__(): return the dot-separated version of the OID
- __getitem__()
- __len__()
- __init__(*nums): each number must be a valid sub-identifier
  - if you violate any of the following rules, behavior is undefined
      - the first one must be between 0 and 2 (semantic requirement)
      - the second one must be between 0 and 39 (encoding limitation)
      - the rest must be valid 32-bit unsigned integers
      - an OID may not contain more than 128 sub-identifiers
  - technically, an OID must contain at least 2 sub-identifiers, however, you may want to declare an OID for the root of a tree (such as OID(1) -- "iso"), and then use that to construct other OIDs. For this reason, it is valid to create an OID object with less than two identifiers.
- classmethod parse(oidstr): parse a string of the form "1.3.6.1..."  and return an OID object
  - Accepts a leading "." character
  - raise a ValueError if the string cannot be parsed, or if it would result in undefined behavior (see __init__)
  - side note: this function should accept OIDs with less than 2 sub-identifiers, for the same reasons explained above
  - this should be the preferred method for constructing OIDs
- extend(*nums): return a new OID instance, with the given numbers added to the end
  - the same undefined behavior as in __init__ applies to this function
- appendIndex(*index)
  - each item in index must be of a primitive Asn1Encodable type
  - used to take an OID defined by a MIB and apply the INDEX to point to a specific instance of that object
- extractIndex(prefix, *types)
  - the reverse of appendIndex; provide the expected base OID, and the types of the index, and it will extract the index field(s)
  - if len(types) is 1, the return value will be an instance of that object
  - if len(types) > 1, it returns a tuple of the objects that make up the index
  - if len(types) is 0, it will check that self matches prefix, and return None
  - raises BadPrefix if the OID does not begin with the given prefix
  - raises IndexDecodeError if an object in the index cannot be decoded, or if the entire OID is not consumed
    - this includes the case where len(types) is 0

class Constructed(Asn1Encodable): abstract base class for constructed objects
- __len__(): number of objects contained in this object
- equals(other): True if (and only if):
  a) len(self) == len(other)
  b) self[i] == other[i] for each i in range(len(self))

class Sequence(Asn1Encodable): ASN.1 SEQUENCE type
- currently an abstract class, though down the line it may need a concrete implementation

snmp.smi.v2
===========
class Integer32(Integer)
- behaves identically to Integer, but it's a distinct class

class IpAddress(OctetString)
- __init__(addr): addr must be a valid IPv4 address string "XXX.XXX.XXX.XXX"
- __repr__()
- equals(other): other must be an OctetString or a child type
  - true if the 4-byte encoding matches
- decode(): raise a ParseError if the data is not exactly 4 bytes long
- encode(): raise a ValueError if addr is not a valid IPv4 address

class Counter32(Integer)
- should behave the same as Unsigned

class Unsigned32(Integer)
- should behave the same as Unsigned

Gauge32: alias for Unsigned32

class TimeTicks(Integer)
- should behave the same as Unsigned

class Opaque(OctetString)
- should behave the same as OctetString

class Counter64(Unsigned)
- behaves like Unsigned, except for the valid range

zeroDotZero: a magic value representing the OID "0.0"
- encoded as a single 0 byte

snmp.pdu.v2
===========
NoSuchObject(Null): behaves just like Null, with a different Identifier
NoSuchInstance(Null): behaves just like Null, with a different Identifier
EndOfMibView(Null): behaves just like Null, with a different Identifier

VarBind(Sequence):
- __init__(name, value=None)
  - name: OID object or a string to pass to OID.parse
  - value: Asn1Encodable object; if None, it will use a Null() object
- __bool__(): True
- __iter__(): yields name and then value
- __len__(): 2
- __repr__()
- __str__()
- decode(): this will automatically detect the type of the value
  - the list of possible value types comes from RFC 3416 section 3
- encode()

VarBindList(Sequence):
- __init__(*args):
  - each arg may be either a VarBind object, or a value to pass to the first argument of the VarBind constructor
- __bool__(): indicates that the list is non-empty
- __getitem__(): return a VarBind or raise IndexError
- __iter__(): iterate over each VarBind
- __len__(): tells how many VarBinds are in the list
- __repr__()
- __str__()
- decode()
- encode()

PDU(Constructed):
- ErrorStatus: enum with each error status from RFC 3416 (names are spelled the same)
- __init__(*args, requestID=0, errorStatus=0, errorIndex=0, variableBindings=None):
  - *args will be passed to the VarBindList constructor
    - ignored if variableBindings is not None
  - requestID, errorStatus, errorIndex, all ints
  - variableBindings: VarBindList or None
- __len__(): 4
- __repr__()
- __str__()
Data Members:
- requestID: int
- errorStatus: PDU.ErrorStatus
- errorIndex: int
- variableBindings: VarBindList

BulkPDU(Constructed):
- __init__(*args, requestID=0, nonRepeaters=0, maxRepetitions=0, variableBindings=None)
  - same as PDU
- __len__(): 4
- __repr__()
- __str__()

PDU types:
- GetRequestPDU
- GetNextRequestPDU
- ResponsePDU
- SetRequestPDU
- InformRequestPDU
- TrapPDU
- ReportPDU

BulkPDU types:
- GetBulkRequestPDU

RFC3411 classes:
- Read
- Write
- Response
- Notification
- Internal
- Confirmed

snmp.security
=============
class SecurityLevel
- __init__(auth=False, priv=False):
  - raise ValueError if priv is True and auth is False
- __repr__()
- __str__(): returns one of "noAuthNoPriv", "authNoPriv", and "authPriv"
- __eq__()
- __lt__(): noAuthNoPriv < authNoPriv < authPriv
- auth: setting this property may raise a ValueError
- priv: setting this property may raise a ValueError

enum SecurityModel
- USM: 3 (from SNMP-FRAMEWORK-MIB::SnmpSecurityModel -- see RFC 3411)

snmp.security.levels
====================
# TODO: maybe SecurityLevels should be immutable, like OID
Magic SecurityLevel's: the names match the __str__() value
- noAuthNoPriv
- authNoPriv
- authPriv

snmp.security.usm
=================
class SecureData: basically just holds some data
- data: payload from a decoded message (should be an encoded PDU)
- engineParams: keyword arguments that can be passed to SecurityModule.addEngine()
- securityEngineID: from the message
- securityLevel: from the message; implies that the data passed the security checks
- securityName: from the message

interface AuthProtocol:
- classmethod localize(cls, secret, engineID): perform key localization
  - secret: the user's authentication secret
  - engineID: generate a key for the given engineID
  - returns a bytes object which should be used as the user's authKey for this engine
- __init__(key)
  - key: the localized authentication key
  - an instance of AuthProtocol is specific to a user and engine
- msgAuthenticationParameters: bytes object filled with zeros; used as a placeholder until the signature can be generated
- sign(data): generate a signature for the given data
  - data: the full message as a bytes-like object
  - returns a bytes-like object of the same length as msgAuthenticationParameters

interface PrivProtocol:
- __init__(key)
  - key: the localized privacy key (use AuthProtocol.localize())
  - an instance of PrivProtocol is specific to a user and engine
- encrypt(data, engineBoots, engineTime)
  - data: the plaintext data
  - engineBoots: msgAuthoritativeEngineBoots
  - engineTime: msgAuthoritativeEngineTime
  - returns (msgPrivParameters, encrypted data)
- decrypt(data, engineBoots, engineTime, msgPrivParameters)
  - returns plaintext data
  - note that the plaintext data may include padding at the end, so its contents should be BER decoded with leftovers=True
  - may raise an IncomingMessageError

class SecurityModule:
- __init__(lockType=snmp.utils.DummyLock)
- addEngine(engineID, engineBoots=0, bootTime=None)
  - provide the engineID of an engine, either local or remote
  - the latter parameters are a hint that may prevent a Time Window synchronization report
  - this needs to be done before it can send/receive secure messages to/from an engine
- addUser(engineID, userName, authProtocol=None, authKey=None, privProtocol=None, privKey=None)
  - if engineID has not been added with addEngine, you will get a ValueError
  - this needs to be done before you can send/receive secure messages with this userName
- prepareOutgoing(header, data, engineID, securityName, securityLevel):
  - header: message encoding up to msgSecurityParameters
  - data: encoding of the message payload (ScopedPDU)
  - engineID: securityEngineID
  - securityName: userName
  - securityLevel: instance of snmp.security.SecurityLevel
  - raise ValueError if
    - securityLevel is greater than noAuthNoPriv securityName has not been added with addUser()
    - the securityLevel requests features that are not enabled for the given user
  - returns a bytes object containing the encoded & secured message
- processIncoming(msg, securityLevel, timestamp=None):
  - msg: subbytes object, which must reference the complete encoded message in order for authentication to succeed, but which exposes only the portion beginning at msgSecurityParameters (i.e. the leftovers of decoding the beginning of a message)
  - securityLevel: the securityLevel advertised in the message header
  - timestamp: the UNIX epoch time at which the message was received (mostly just for unit testing)
  - raise IncomingMessageError if (may not be exhaustive)
    - fails to parse (ParseError)
    - it is addressed to an unknown userName
    - it claims a securityLevel that is unsupported for the user
    - the signature is invalid
    - the message is outside the time window
    - decryption fails
  - returns a SecureData instance

snmp.security.usm.auth
======================
AuthProtocol implementations:
- HmacMd5
- HmacSha
- HmacSha224
- HmacSha256
- HmacSha384
- HmacSha512

snmp.security.usm.priv
======================
PrivProtocol implementations:
- Aes128Cfb
- DesCbc

snmp.message.v3
===============
class MessageFlags(OctetString):
- AUTH_FLAG
- PRIV_FLAG
- REPORTABLE_FLAG
- __init__(byte=0):
  - byte is a combination of the *_FLAG variables above
- __repr__()
- __str__()
- authFlag: settable boolean property
- privFlag: settable boolean property
- reportableFlag: settable boolean property

class HeaderData(Sequence):
- __init__(msgID, msgMaxSize, msgFlags, msgSecurityModel)
  - msgID: int
  - msgMaxSize: int
  - msgFlags: MessageFlags
  - msgSecurityModel: snmp.security.SecurityModel
- __repr__()
- __str__()

class ScopedPDU(Sequence):
- __init__(pdu, contextEngineID, contextName=b"")
  - pdu: snmp.pdu.v2.PDU
  - contextEngineID: bytes
  - contextName: bytes
- __repr__()
- __str__()

SecurityModule interface:
- MODEL attribute: member of snmp.security.SecurityModel 
- prepareOutgoing(header, data, engineID, securityName, securityLevel)
  - return encoded message

class MessageProcessor:
- __init__(lockType=snmp.utils.DummyLock):
- secure(module, default=None): register a security module to use
  - module: SecurityModeule interface instance
  - default: True to use this security model by default
    - if None, the first provided security model will be used
    - each call overrides previous calls
      - if you call twice for the same model, the most recent will be used
      - if you call twice with default=True, the most recent will be used
- prepareOutgoingMessage(pdu, handle, engineID, securityName, securityLevel=noAuthNoPriv, securityModel=None, contextName=b"")
  - pdu: snmp.pdu.v2.PDU
  - handle: Handle interface
  - engineID: bytes
  - securityName: bytes
  - securityLevel: SecurityLevel
  - securityModel: SecurityModel or None
    - if None, use the default
      - ValueError if you have not provided a default using the secure() function
  - contextName: bytes
  - behavior:
    - generate a message ID
    - cache the message details using that ID
    - determine the security module to use
    - encode the message, applying the requested level of security
    - return the encoded message
- prepareDataElements(msg)
  - msg: subbytes wrapping the full message, but pointing to the start of the header data
  - raise IncomingMessageError if
    - unsupported security model
    - invalid security level
    - message contents do not match the request
    - something fails in the security module
  - return SecureData, Handle
    - SecureData.data points to scopedPDU
    - Handle will be the handle given to prepareOutgoingMessage
- TODO: add a way to mark a msgID as accepted and drop it from the cache
  - maybe they should also time out automatically

snmp.transport
==============
Listener interface:
- hear(transport, addr, data)
  - transport: The Transport object that received the data
  - addr: a normalized address
  - data: bytes
  - must handle all exceptions

enum TransportDomain
- UDP

TransportLocator:
- __init__(domain, address)
  - domain: TransportDomain
  - address: normalized address

Transport interface:
- classmethod Locator(address):
  - return a TransportLocator instance
  - address need not be normalized; this function will call normalizeAddress
- classmethod normalizeAddress(address)
  - validate and/or standardize address
  - return an address (whatever that means)
  - raise ValueError if address is not usable
- send(addr, packet)
  - addr: a normalized address
  - packet: bytes
- listen(listener)
  - some type of concurrency is assumed
  - listener: Listener interface
  - call listener.hear for each arriving packet
- stop()
  - stop listen()ing
- close()
  - release any resources held by the object

snmp.transport.udp
==================
UdpTransport: Transport interface
- __init__(self, host="", port=0)
  - host, port: local IP and port to bind to

snmp.dispatcher
===============
MessageProcessor interface
- VERSION: instance of snmp.message.MessageProcessingModel

Handle interface
- response: after a call to wait, response will refer to a SecureData object
  - data: ScopedPDU
- signal: called by the dispatcher when a response is available
- wait: call from the main thread to block until the response arrives
  - TODO: add a timeout
  - TODO: implement smart handlers to handle all possible Reports

class Dispatcher(Listener)
- __init__(lockType=snmp.utils.DummyLock)
- addMessageProcessor(mp):
  - mp: MessageProcessor
- connectTransport(transport)
  - transport: Transport
  - register transport for its domain
  - start the transport listening
    - ValueError if that domain already has a listening Transport
- hear(transport, address, data)
  - meant to be called by a transport
  - call prepareDataElements on the appropriate message processor, based on the message version
  - set handle.response of the returned handle to contain the SecureData
  - signal the handle
- sendPdu(domain, address, mpm, pdu, *args, **kwargs)
  - domain: TransportDomain
  - address: normalized address
  - mpm: MessageProcessingModel
  - pdu: PDU
  - args and kwargs depend on the message processing model
  - create a message to carry the pdu, and send it to the given address
- shutdown()
  - disconnect from all listening transports
  - after calling shutdown, it is legal to call connectTransport again and continue using the Dispatcher
  - if you have called connectTransport since the last call to shutdown, you must call shutdown when you are through with the Dispatcher

class Engine:
- __init__(lockType=snmp.utils.DummyLock, defaultDomain=UDP, defaultVersion=SNMPv3, defaultSecurityModel=USM)
  - defaultDomain: currently only supports UDP
  - defaultVersion: currently only supports SNMPv3
  - defaultSecurityModel: currently only supports USM
- shutdown(): you must call this if you have called connectTransport
  - after calling, you may call connectTransport again, but you'll have to shutdown again
- addUser(userName, authProtocol=None, authSecret=None, privProtocol=None, privSecret=None, secret=b"", default=None, defaultSecurityLevel=None, namespace="")
  - The Engine can use namespaces to partition remote engines with userName collisions (i.e. same userName, but different algorithms or secrets). By default, all engines and users are put into the "" namespace, but you have the option to make up your own namespaces to keep them separate. An engine can only belong to one namespace, but you can have users of the same name in multiple namespaces.
  - userName: str
  - authProtocol: AuthProtocol or None
  - authSecret: bytes or None
  - privProtocol: PrivProtocol or None
  - privSecret: bytes or None
  - secret: bytes
    - used if auth/priv Protocol is given without a secret
    - if your auth and priv use the same secret, this is a handy way to provide it only once
  - default: bool or None
    - set the given userName as the default for communicating with engines in this namespace
    - if default is None, but the namespace doesn't have a default, it will be treated as True
  - defaultSecurityLevel: SecurityLevel or None
    - default security level for this user
    - if None, then the default will be the most secure level supported for this user
  - namespace: str
- addRemoteEngine(engineID, namespace="", **kwargs)
  - engineID: bytes
  - namespace: str
  - kwargs: forwarded to the security module's addEngine function
NOTE: we should be able to call addUser and addRemoteEngine in any order
- in fact, a user shouldn't be added to the security module for an engine that it never talks to
- connectTransport(transport)
  - raise value error if the domain is already covered by another transport, or the domain is not supported
- manage(address, domain=None, version=None, securityModel=None, defaultUserName=None, namespace="", engineID=None)
  - Return a manager object that acts as a proxy for the remote engine
    - you don't have to worry about the domain, address, engineID, credentials, etc,
      - you just say "get(<pdu>)", and it can either return a handle or just block and return the response
  - address is the address of the remote engine
  - domain: TransportDomain or None
    - if None, use the engine's default domain
  - version: MessageProcessingModel or None
    - if None, use the engine's default message processing model
  - securityModel: SecurityModel or None
    - if None, use the engine's default security model
  - defaultUserName: str or None
    - if None, use the default user name for this namespace
      - ValueError if the namespace does not have a default user name
  - namespace: str
  - engineID: shortcut the discovery process and just use a hard-coded engineID

TODO: make sure that if engineBoots is provided as a hint, but the real engineBoots is less than the hint, it will still work
This version does not need to be robust against denial of service, so it's probably fine to trust ReportPDUs that provide
    the engineID and even the engineBoots, but eventually I'd like to make it properly secure
On discovery, trust the first response you get to be the correct engineID and
    engine parameters for that address

class Engine:
- __init__(lockType=snmp.utils.DummyLock, defaultDomain=UDP, defaultVersion=SNMPv3, defaultSecurityModel=USM, autowait=True)

- Manager(address, domain=None, autowait=None, version=None, ...
  - address will be normalized for the domain
  - if domain is None, use the default
  - if autowait is None, use the default
  - if version is None, use the default
  - raise ValueError if
    - address is not valid
    - domain is not valid
    - version is not valid
  - if version is SNMPv3:
    - ... engineID=None, securityModel=None, ...
    - if engineID is None, the Manager will have to discover it
    - if securityModel is None, use the default
    - raise ValueError if securityModel is not valid
    - if securityModel is USM:
      - ... defaultUserName=None, namespace=""):
      - if defaultUserName is None, use the defaut for the namespace
      - raise ValueError if
        - defaultUserName is None and the namespace doesn't have a default user
        - namespace is not valid
        - defaultUserName is not None and is not a valid userName

Manager data members:
- autowait: if False, getNext() and so on will return a Request object
            if True, the same functions will return the result of Request.wait()
- generator: iterator for generating requestIDs
- localEngine: reference to the Engine that the Manager is associated with
- locator: address and domain of the managed (remote) engine
- namespace: the namespace for USM credentials
- defaultUserName: default userName for outgoing requests
- defaultSecurityLevel: default security level for outgoing requests
- candidates: a set of engineIDs that may identify the managed engine
  - used for a Manager performing discovery
  - each ReportPDU indicating unknownEngineID will cause a candidate to be added
  - each time a candidate is added, outstanding requests are re-sent
  - each new request will be sent with all candidate engineIDs
  - once an authentic engineID is determined, all candidates will be discarded
- callback: callback to unregister discovery message
  - Manager is a private Dispatcher.Handle
  - once discovery is complete, it will call the callback to uncache the message
- needSync: if an engineID is provided to the Manager, then the first request
        with auth can expect a time window error; needSync is True before the
        first such request has been sent
- synchronized: related to needSync; if the Manager is performing discovery,
        then this will be set to True once the first candidate is added. If the
        engineID was provided by the constructor, then this will be set to True
        once the first authenticated response/report is received. Outgoing
        requests should be held up if the securityLevel indicates auth, needSync
        is not True, and synchronized is not True. On the rising edge of
        synchronized, all outstanding requests will be sent
- lock: mutex to protect all mutable data members that may be accessed in more
        than one thread; namely engineID, localEngine, candidates, requests,
        needSync, and synchronized
- requests: a min-heap of outstanding requests, sorted by when they next need
        to be updated (either re-sent or timed out)
  - this needs to use weak references
