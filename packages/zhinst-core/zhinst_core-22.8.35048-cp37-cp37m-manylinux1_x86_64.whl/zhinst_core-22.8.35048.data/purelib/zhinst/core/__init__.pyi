from typing import (
    List,
    Union,
    overload,
    Any,
    Dict,
    Tuple,
)

# typing.Literal requires Python 3.8+
from typing_extensions import Literal
from enum import Enum
import numpy as np

__version__: str

_VectorTypes = Union[int, float, complex]
_Vector = Union[np.ndarray, List[_VectorTypes], Tuple[_VectorTypes, ...], str]
_PollReturnFlatTrue = Dict[str, Dict[str, Any]]
_PollReturnFlatFalse = Dict[str, Dict[str, _PollReturnFlatTrue]]
_DeviceInterface = Literal[
    "USB",
    "PCIe",
    "1GbE",
]
_LogStyle = Literal[0, 1, 2]
_DebugLevel = Literal[0, 1, 2, 3, 4, 5, 6]
_APILevel = Literal[0, 1, 4, 5, 6]  # enum ZIAPIVersion_enum
_ListNodesFlags = Union[ziListEnum, int]
_MultipleNodeItems = Union[List[Tuple[str, Any]], Tuple[Tuple[str, Any]]]
_NodePath = str
_MultipleNodePaths = List[_NodePath]
_SingleOrMultipleNodePaths = Union[_NodePath, _MultipleNodePaths]

class ziListEnum(Enum):
    absolute: int
    all: int
    basechannel: int
    denominator: int
    excludestreaming: int
    excludevectors: int
    getonly: int
    imag: int
    leafsonly: int
    leavesonly: int
    names: int
    numerator: int
    real: int
    recursive: int
    settingsonly: int
    streamingonly: int
    subscribedonly: int

class ModuleBase:
    def clear(self) -> None:
        """clear(self: zhinst.core.ModuleBase) -> None

        End the module thread."""
    def execute(self) -> None:
        """execute(self: zhinst.core.ModuleBase) -> None

        Start the module execution. Subscription or unsubscription is not
        possible until the execution is finished."""
    def finish(self) -> None:
        """finish(self: zhinst.core.ModuleBase) -> None

        Stop the execution. The execution may be restarted by calling
        'execute' again."""
    def finished(self) -> bool:
        """finished(self: zhinst.core.ModuleBase) -> bool

        Check if the execution has finished. Returns True if finished."""
    @overload
    def get(self, path: str, flat: Literal[True]) -> Dict[str, Any]:
        """get(self: zhinst.core.ModuleBase, path: str, flat: bool = False) -> object

        Return a dict with all nodes from the specified sub-tree.
            path: Path string of the node. Use wild card to
                  select all.
            flat: Specify which type of data structure to return.
                  Return data either as a flat dict (True) or as a nested
                  dict tree (False). Default = False."""
    @overload
    def get(self, path: str, flat: Literal[False]) -> Dict[str, Dict[str, Any]]: ...
    @overload
    def get(
        self, path: str, flat: bool = False
    ) -> Union[Dict[str, Any], Dict[str, Dict[str, Any]]]: ...
    def getDouble(self, path: str) -> float:
        """getDouble(self: zhinst.core.ModuleBase, path: str) -> float

        Return the floating point double value for the specified path.
            path: Path string of the node."""
    def getInt(self, path: str) -> int:
        """getInt(self: zhinst.core.ModuleBase, path: str) -> int

        Return the integer value for the specified path.
            path: Path string of the node."""
    def getString(self, path: str) -> str:  # Wrong return type in docs (object)
        """getString(self: zhinst.core.ModuleBase, path: str) -> object

        Return the string value for the specified path.
            path: Path string of the node."""
    def getStringUnicode(self, path: str) -> str:  # Wrong return type in docs (object)
        """getStringUnicode(self: zhinst.core.ModuleBase, path: str) -> object

        Return the unicode encoded string value for the specified path.
        Only relevant for Python versions older than V3.0.
        For Python versions 3.0 and later, getString can be used instead.
            path: Path string of the node."""
    def help(self, path: str = "*") -> None:
        """help(self: zhinst.core.ModuleBase, path: str = '*') -> None

        Prints a well-formatted description of a module parameter.
            path: Path for which the nodes should be listed. The path may
                  contain wildcards so that the returned nodes do not
                  necessarily have to have the same parents."""
    def listNodes(
        self,
        path: str,
        *args: _ListNodesFlags,
        recursive=False,
        absolute=True,
        leavesonly=False,
        settingsonly=False,
        streamingonly=False,
        subscribedonly=False,
        basechannelonly=False,
        excludestreaming=False,
        excludevectors=False
    ) -> List[str]:
        """listNodes(self: zhinst.core.ModuleBase, path: str, *args, **kwargs) -> list

        This function returns a list of node names found at the specified path.

        Positional arguments:
            path:  Path for which the nodes should be listed. The path may
                   contain wildcards so that the returned nodes do not
                   necessarily have to have the same parents.
        Optional positional arguments:
            flags: Flags specifying how the selected nodes are listed
                   (see zhinst.core.ziListEnum). Flags can also specified by
                   the keyword arguments below.

        Keyword arguments:
            recursive: Returns the nodes recursively (default: False)
            absolute: Returns absolute paths (default: True)
            leavesonly: Returns only nodes that are leaves, which means they
                   are at the outermost level of the tree (default: False).
            settingsonly: Returns only nodes which are marked as setting
                   (default: False).
            streamingonly: Returns only streaming nodes (default: False).
            subscribedonly: Returns only subscribed nodes (default: False).
            basechannelonly: Return only one instance of a node in case of
                   multiple channels (default: False).
            excludestreaming: Exclude streaming nodes (default: False).
            excludevectors: Exclude vector nodes (default: False)."""
    def listNodesJSON(
        self,
        path: str,
        *args: _ListNodesFlags,
        settingsonly=False,
        streamingonly=False,
        subscribedonly=False,
        basechannelonly=False,
        excludestreaming=False,
        excludevectors=False
    ) -> str:  # `object` in documentation
        """listNodesJSON(self: zhinst.core.ModuleBase, path: str, *args, **kwargs) -> str

        Returns a list of nodes with description found at the specified path.

        Positional arguments:
            path:  Path for which the nodes should be listed. The path may
                   contain wildcards so that the returned nodes do not
                   necessarily have to have the same parents.
        Optional positional arguments:
            flags: Flags specifying how the selected nodes are listed
                   (see zhinst.core.ziListEnum). Flags can also specified by
                   the keyword arguments below. They are the same as for
                   listNodes(), except that recursive, absolute, and leavesonly
                   are enforced.

        Keyword arguments:
            settingsonly: Returns only nodes which are marked as setting
                   (default: False).
            streamingonly: Returns only streaming nodes (default: False).
            subscribedonly: Returns only subscribed nodes (default: False).
            basechannelonly: Return only one instance of a node in case of
                   multiple channels (default: False).
            excludestreaming: Exclude streaming nodes (default: False).
            excludevectors: Exclude vector nodes (default: False)."""
    def progress(self) -> np.ndarray:
        """progress(self: zhinst.core.ModuleBase) -> object

        Reports the progress of the execution with a number between
        0 and 1."""
    @overload
    def read(
        self, flat: bool = False
    ) -> Union[Dict[str, Any], Dict[str, Dict[str, Any]]]:
        """read(self: zhinst.core.ModuleBase, flat: bool = False) -> object

        Read the module output data. If the module execution is still ongoing
        only a subset of data is returned. If huge data sets are produced call
        this method to keep memory usage reasonable.
            flat: Specify which type of data structure to return.
                  Return data either as a flat dict (True) or as a nested
                  dict tree (False). Default = False."""
    @overload
    def read(self, flat: Literal[True]) -> Dict[str, Any]: ...
    @overload
    def read(self, flat: Literal[False]) -> Dict[str, Dict[str, Any]]: ...
    def save(self, filename: str) -> None:
        """save(self: zhinst.core.ModuleBase, filename: str) -> None

        Save measured data to file.
            filename: File name string (without extension)."""
    @overload
    def set(self, path: str, value: Any) -> None:
        """set(*args, **kwargs)
        Overloaded function.

        1. set(self: zhinst.core.ModuleBase, path: str, value: object) -> None

        Set the specified module parameter value. Use 'help' to learn more
        about available parameters.
            path:  Path string of the node.
            value: Value of the node.

        2. set(self: zhinst.core.ModuleBase, items: object) -> None

            items: A list of path/value pairs."""
    @overload
    def set(self, items: _MultipleNodeItems) -> None: ...
    def subscribe(self, path: _SingleOrMultipleNodePaths) -> None:
        """subscribe(self: zhinst.core.ModuleBase, path: str) -> None

        Subscribe to one or several nodes. After subscription the module
        execution can be started with the 'execute' command. During the
        module execution paths can not be subscribed or unsubscribed.
            path: Path string of the node. Use wild card to
                  select all. Alternatively also a list of path
                  strings can be specified."""
    def trigger(self) -> None:
        """trigger(self: zhinst.core.ModuleBase) -> None

        Execute a manual trigger, if applicable."""
    def unsubscribe(self, path: _SingleOrMultipleNodePaths) -> None:
        """unsubscribe(self: zhinst.core.ModuleBase, path: str) -> None

        Unsubscribe from one or several nodes. During the
        module execution paths can not be subscribed or unsubscribed.
            path: Path string of the node. Use wild card to
                  select all. Alternatively also a list of path
                  strings can be specified."""

class AwgModule(ModuleBase): ...
class DataAcquisitionModule(ModuleBase): ...
class DeviceSettingsModule(ModuleBase): ...
class ImpedanceModule(ModuleBase): ...
class MultiDeviceSyncModule(ModuleBase): ...
class PidAdvisorModule(ModuleBase): ...
class PrecompensationAdvisorModule(ModuleBase): ...
class QuantumAnalyzerModule(ModuleBase): ...
class RecorderModule(ModuleBase): ...
class ScopeModule(ModuleBase): ...
class SweeperModule(ModuleBase): ...
class ZoomFFTModule(ModuleBase): ...

class ziDAQServer:
    @overload
    def __init__(self, host: str, port: int) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
    @overload
    def __init__(
        self, host: str, port: int, api_level: _APILevel, **kwargs: Any
    ) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: zhinst.core.ziDAQServer, host: str, port: int) -> None

        Connect to the server by using host address and port number.
            host: Host string e.g. '127.0.0.1' for localhost.
            port: Port number e.g. 8004 for the ziDataServer.

        2. __init__(self: zhinst.core.ziDAQServer, host: str, port: int, api_level: int, **kwargs) -> None

        Connect to the server by using host address and port number.
            host: Host string e.g. '127.0.0.1' for localhost.
            port: Port number e.g. 8004 for the ziDataServer.
            api_level: API level number."""
    def asyncSetDouble(self, path: str, value: float) -> None:
        """asyncSetDouble(self: zhinst.core.ziDAQServer, path: str, value: float) -> None

        Use with care: returns immediately, any errors silently ignored.
            path:  Path string of the node.
            value: Value of the node."""
    def asyncSetInt(self, path: str, value: int) -> None:
        """asyncSetInt(self: zhinst.core.ziDAQServer, path: str, value: int) -> None

        Use with care: returns immediately, any errors silently ignored.
            path:  Path string of the node.
            value: Value of the node."""
    def asyncSetString(self, path: str, value: str) -> None:
        """asyncSetString(self: zhinst.core.ziDAQServer, path: str, value: object) -> None

        Use with care: returns immediately, any errors silently ignored.
            path:  Path string of the node.
            value: Value of the node."""
    def awgModule(self) -> AwgModule:
        """awgModule(self: zhinst.core.ziDAQServer) -> zhinst.core.AwgModule

        Create a AwgModule object. This will start a thread for
        running an asynchronous module."""
    def connect(self) -> None:
        """connect(self: zhinst.core.ziDAQServer) -> None"""
    def connectDevice(
        self, dev: str, interface: _DeviceInterface, params: str = ""
    ) -> None:
        """connectDevice(self: zhinst.core.ziDAQServer, dev: str, interface: str, params: str = '') -> None

        Connect with the data server to a specified device over the specified
        interface. The device must be visible to the server. If the device is
        already connected the call will be ignored. The function will block
        until the device is connected and the device is ready to use. This
        method is useful for UHF devices offering several communication
        interfaces.
            dev: Device serial.
            interface: Device interface.
            params: Optional interface parameters string."""
    def dataAcquisitionModule(self) -> DataAcquisitionModule:
        """dataAcquisitionModule(self: zhinst.core.ziDAQServer) -> zhinst.core.DataAcquisitionModule

        Create a DataAcquisitionModule object. This will start a thread for
        running an asynchronous module."""
    def deviceSettings(self) -> DeviceSettingsModule:
        """deviceSettings(*args, **kwargs)
        Overloaded function.

        1. deviceSettings(self: zhinst.core.ziDAQServer) -> zhinst.core.DeviceSettingsModule

        Create a DeviceSettingsModule object. This will start a thread for
        running an asynchronous module.

        2. deviceSettings(self: zhinst.core.ziDAQServer, timeout_ms: int) -> zhinst.core.DeviceSettingsModule

        DEPRECATED, use deviceSettings() without arguments.
        Create a DeviceSettingsModule class. This will start a thread for running
        an asynchronous DeviceSettingsModule.
            timeout_ms: Timeout in [ms]. Recommended value is 500ms.
                  DEPRECATED, ignored"""
    def disconnect(self) -> None:
        """disconnect(self: zhinst.core.ziDAQServer) -> None"""
    def disconnectDevice(self, dev: str) -> None:
        """disconnectDevice(self: zhinst.core.ziDAQServer, dev: str) -> None

        Disconnect a device on the data server. This function will return
        immediately. The disconnection of the device may not yet finished.
            dev: Device serial string of device to disconnect."""
    def echoDevice(self, dev: str) -> None:  # Deprecated
        """echoDevice(self: zhinst.core.ziDAQServer, dev: str) -> None

        Deprecated, see the 'sync' command.
        Sends an echo command to a device and blocks until
        answer is received. This is useful to flush all
        buffers between API and device to enforce that
        further code is only executed after the device executed
        a previous command.
            dev: Device string e.g. 'dev100'."""
    def flush(self) -> None:  # Deprecated
        """flush(self: zhinst.core.ziDAQServer) -> None

        Deprecated, see the 'sync' command.
        The flush command is identical to the sync command."""
    @overload
    def get(
        self, paths: str, flat=Literal[True], all=False, settingsonly=True
    ) -> Dict[str, Any]:
        """get(self: zhinst.core.ziDAQServer, paths: str, *args, **kwargs) -> object

        Return a dict with all nodes from the specified sub-tree.
        Note: Flags are ignored for a path that specifies one or more leaf nodes.
              Specifying flags, either as positional or keyword argument is
              mandatory if an empty set would be returned given the
              default flags (settingsonly).
              High-speed streaming nodes (e.g. /devN/demods/0/sample) are
              are never returned.

        Positional arguments:
            paths: Path string of the node. Multiple paths can be specified
                   as a comma-separated list. Wild cards are supported to
                   select multiple matching nodes.
        Optional positional arguments:
            flat_: Superseded by keyword argument `flat` which takes
                   precedence (see below).
            flags: Flags to specify which type of nodes to include in the
                   result (see zhinst.ziListEnum). Flags specified as
                   keyword arguments take precedence (see below).

        Keyword arguments:
            flat:  Specify which type of data structure to return.
                   Return data either as a flat dict (True) or as a nested
                   dict tree (False, default).
            all:   Return all nodes. Is evaluated first and resets the flags if
                   set to True (default: False).
            settingsonly: Return only nodes which are marked as setting
                   (default: True).
        Moreover, all flags supported by listNodes() can be used."""
    @overload
    def get(
        self, paths: str, flat=Literal[False], all=False, settingsonly=True
    ) -> Dict[str, Dict[str, Any]]: ...
    @overload
    def get(
        self, path: str, flat=False, all=False, settingsonly=True
    ) -> Union[Dict[str, Any], Dict[str, Dict[str, Any]]]: ...
    def getAsEvent(self, path: str) -> None:
        """getAsEvent(self: zhinst.core.ziDAQServer, path: str) -> None

        Trigger an event on the specified node. The node data is returned by a
        subsequent poll command.
            path:  Path string of the node. Note: Wildcards and paths
                   referring to streaming nodes are not permitted."""
    def getAuxInSample(self, path: str) -> Dict[str, np.ndarray]:
        """getAuxInSample(self: zhinst.core.ziDAQServer, path: str) -> object

        Returns a single auxin sample. The auxin data is averaged in contrast to
        the auxin data embedded in the demodulator sample.
            path: Path string"""
    def getByte(self, path: str) -> str:
        """getByte(self: zhinst.core.ziDAQServer, path: str) -> object

        Get a byte array (string) value from the specified node.
            path: Path string of the node."""
    def getComplex(self, path: str) -> complex:
        """getComplex(self: zhinst.core.ziDAQServer, path: str) -> complex

        Get a complex double value from the specified node.
            path: Path string of the node."""
    def getConnectionAPILevel(self) -> _APILevel:  # Deprecated
        """getConnectionAPILevel(self: zhinst.core.ziDAQServer) -> int

        DEPRECATED, use api_levelReturns ziAPI level used for the active connection."""
    def getDIO(self, path: str) -> Dict[str, np.ndarray]:
        """getDIO(self: zhinst.core.ziDAQServer, path: str) -> object

        Returns a single DIO sample.
            path: Path string"""
    def getDebugLogpath(self) -> str:
        """getDebugLogpath(self: zhinst.core.ziDAQServer) -> str

        Returns the path where logfiles are stored. Note, it will return
        an empty string if the path has not been set or logging has not been
        enabled via setDebugLevel()."""
    def getDouble(self, path: str) -> float:
        """getDouble(self: zhinst.core.ziDAQServer, path: str) -> float

        Get a double value from the specified node.
            path: Path string of the node."""
    def getInt(self, path: str) -> int:
        """getInt(self: zhinst.core.ziDAQServer, path: str) -> int

        Get a integer value from the specified node.
            path: Path string of the node."""
    def getList(self, path: str, flags: int = 8) -> List[str]:  # Deprecated
        """getList(self: zhinst.core.ziDAQServer, path: str, flags: int = 8) -> object

        DEPRECATED: superseded by get(...).
        Return a list with all nodes from the specified sub-tree.
            path:  Path string of the node. Use wild card to
                   select all.
            flags: Specify which type of nodes to include in the
                   result. Allowed:
                   ZI_LIST_NODES_SETTINGSONLY = 0x08 (default)
                   ZI_LIST_NODES_ALL = 0x00 (all nodes)"""
    def getSample(self, path: str) -> Dict[str, np.ndarray]:
        """getSample(self: zhinst.core.ziDAQServer, path: str) -> object

        Returns a single demodulator sample (including DIO and AuxIn). For more
        efficient data recording use subscribe and poll methods.
            path: Path string"""
    def getString(self, path: str) -> str:  # `object` in documentation
        """getString(self: zhinst.core.ziDAQServer, path: str) -> object

        Get a string value from the specified node.
            path: Path string of the node."""
    def getStringUnicode(self, path: str) -> str:  # `object` in documentation
        """getStringUnicode(self: zhinst.core.ziDAQServer, path: str) -> object

        Get a unicode string value from the specified node.
        The returned string is unicode encoded.
        Only relevant for Python versions older than V3.0.
        For Python versions 3.0 and later, getString can be used instead.
            path: Path string of the node."""
    def help(self, path: str) -> None:
        """help(self: zhinst.core.ziDAQServer, path: str) -> None

        Prints a well-formatted description of a node. Only UHF and MF devices
        support this functionality.
            path: Path for which the nodes should be listed. The path may
                  contain wildcards so that the returned nodes do not
                  necessarily have to have the same parents."""
    def impedanceModule(self) -> ImpedanceModule:
        """impedanceModule(self: zhinst.core.ziDAQServer) -> zhinst.core.ImpedanceModule

        Create a ImpedanceModule object. This will start a thread for
        running an asynchronous module."""
    def listNodes(
        self,
        path: str,
        *args: _ListNodesFlags,
        all=False,
        recursive=False,
        absolute=True,
        leavesonly=False,
        settingsonly=False,
        streamingonly=False,
        subscribedonly=False,
        basechannelonly=False,
        excludestreaming=False,
        excludevectors=False
    ) -> List[str]:
        """listNodes(self: zhinst.core.ziDAQServer, path: str, *args, **kwargs) -> list

        This function returns a list of node names found at the specified path.

        Positional arguments:
            path:  Path for which the nodes should be listed. The path may
                   contain wildcards so that the returned nodes do not
                   necessarily have to have the same parents.
        Optional positional arguments:
            flags: Flags specifying how the selected nodes are listed
                   (see zhinst.core.ziListEnum). Flags can also specified by
                   the keyword arguments below.

        Keyword arguments:
            all: Return all nodes (resets flags if set to True).
            recursive: Returns the nodes recursively (default: False)
            absolute: Returns absolute paths (default: True)
            leavesonly: Returns only nodes that are leaves, which means they
                   are at the outermost level of the tree (default: False).
            settingsonly: Returns only nodes which are marked as setting
                   (default: False).
            streamingonly: Returns only streaming nodes (default: False).
            subscribedonly: Returns only subscribed nodes (default: False).
            basechannelonly: Return only one instance of a node in case of
                   multiple channels (default: False).
            excludestreaming: Exclude streaming nodes (default: False).
            excludevectors: Exclude vector nodes (default: False)."""
    def listNodesJSON(
        self,
        path: str,
        *args: _ListNodesFlags,
        all=False,
        settingsonly=False,
        streamingonly=False,
        subscribedonly=False,
        basechannelonly=False,
        excludestreaming=False,
        excludevectors=False
    ) -> List[str]:  # `object` in documentation
        """listNodesJSON(self: zhinst.core.ziDAQServer, path: str, *args, **kwargs) -> str

        Returns a list of nodes with description found at the specified path.
        HF2 devices do not support this functionality.

        Positional arguments:
            path:  Path for which the nodes should be listed. The path may
                   contain wildcards so that the returned nodes do not
                   necessarily have to have the same parents.
        Optional positional arguments:
            flags: Flags specifying how the selected nodes are listed
                   (see zhinst.core.ziListEnum). Flags can also specified by
                   the keyword arguments below. They are the same as for
                   listNodes(), except that recursive, absolute, and leavesonly
                   are enforced.

        Keyword arguments:
            all: Return all nodes (resets flags if set to True).
            settingsonly: Returns only nodes which are marked as setting
                   (default: False).
            streamingonly: Returns only streaming nodes (default: False).
            subscribedonly: Returns only subscribed nodes (default: False).
            basechannelonly: Return only one instance of a node in case of
                   multiple channels (default: False).
            excludestreaming: Exclude streaming nodes (default: False).
            excludevectors: Exclude vector nodes (default: False)."""
    def logOff(self) -> None:
        """logOff(self: zhinst.core.ziDAQServer) -> None

        Disables logging of commands sent to a server."""
    def logOn(self, flags: int, filename: str, style: _LogStyle = 2) -> None:
        """logOn(self: zhinst.core.ziDAQServer, flags: int, filename: str, style: int = 2) -> None

        Enables logging of commands sent to a server.
            flags: Flags (LOG_NONE:             0x00000000
                          LOG_SET_DOUBLE:       0x00000001
                          LOG_SET_INT:          0x00000002
                          LOG_SET_BYTE:         0x00000004
                          LOG_SET_STRING:       0x00000008
                          LOG_SYNC_SET_DOUBLE:  0x00000010
                          LOG_SYNC_SET_INT:     0x00000020
                          LOG_SYNC_SET_BYTE:    0x00000040
                          LOG_SYNC_SET_STRING:  0x00000080
                          LOG_GET_DOUBLE:       0x00000100
                          LOG_GET_INT:          0x00000200
                          LOG_GET_BYTE:         0x00000400
                          LOG_GET_STRING:       0x00000800
                          LOG_GET_DEMOD:        0x00001000
                          LOG_GET_DIO:          0x00002000
                          LOG_GET_AUXIN:        0x00004000
                          LOG_GET_COMPLEX:      0x00008000
                          LOG_LISTNODES:        0x00010000
                          LOG_SUBSCRIBE:        0x00020000
                          LOG_UNSUBSCRIBE:      0x00040000
                          LOG_GET_AS_EVENT:     0x00080000
                          LOG_UPDATE:           0x00100000
                          LOG_POLL_EVENT:       0x00200000
                          LOG_POLL:             0x00400000
                          LOG_ALL :             0xffffffff)
            filename: Log file name.
            style: Log style (LOG_STYLE_TELNET: 0, LOG_STYLE_MATLAB: 1,
                   LOG_STYLE_PYTHON: 2 (default))."""
    def multiDeviceSyncModule(self) -> MultiDeviceSyncModule:
        """multiDeviceSyncModule(self: zhinst.core.ziDAQServer) -> zhinst.core.MultiDeviceSyncModule

        Create a MultiDeviceSyncModule object. This will start a thread for
        running an asynchronous module."""
    def pidAdvisor(self) -> PidAdvisorModule:
        """pidAdvisor(*args, **kwargs)
        Overloaded function.

        1. pidAdvisor(self: zhinst.core.ziDAQServer) -> zhinst.core.PidAdvisorModule

        Create a PidAdvisorModule object. This will start a thread for
        running an asynchronous module.

        2. pidAdvisor(self: zhinst.core.ziDAQServer, timeout_ms: int) -> zhinst.core.PidAdvisorModule

        DEPRECATED, use pidAdvisor() without arguments.
        Create a PidAdvisorModule class. This will start a thread for running an
        asynchronous PidAdvisorModule.
            timeout_ms: Timeout in [ms]. Recommended value is 500ms.
                  DEPRECATED, ignored"""
    @overload
    def poll(
        self,
        recording_time_s: float,
        timeout_ms: int,
        flags: int = 0,
        flat: Literal[True] = ...,
    ) -> _PollReturnFlatTrue:
        """poll(self: zhinst.core.ziDAQServer, recording_time_s: float, timeout_ms: int, flags: int = 0, flat: bool = False) -> object

        Continuously check for value changes (by calling pollEvent) in all
        subscribed nodes for the specified duration and return the data. If
        no value change occurs in subscribed nodes before duration + timeout,
        poll returns no data. This function call is blocking (it is
        synchronous). However, since all value changes are returned since
        either subscribing to the node or the last poll (assuming no buffer
        overflow has occurred on the Data Server), this function may be used
        in a quasi-asynchronous manner to return data spanning a much longer
        time than the specified duration. The timeout parameter is only
        relevant when communicating in a slow network. In this case it may be
        set to a value larger than the expected round-trip time in the
        network.
        Poll returns a dict tree containing the recorded data (see `flat`).
            recording_time_s: Recording time in [s]. The function will block
                  during that time.
            timeout_ms: Poll timeout in [ms]. Recommended value is 500ms.
            flags: Poll flags.
                  DEFAULT = 0x0000: Default.
                  FILL    = 0x0001: Fill holes.
                  THROW   = 0x0004: Throw EOFError exception if sample
                                    loss is detected (only possible in
                                    combination with DETECT).
                  DETECT  = 0x0008: Detect data loss holes.
            flat: Specify which type of data structure to return.
                  Return data either as a flat dict (True) or as a nested
                  dict tree (False). Default = False."""
    @overload
    def poll(
        self,
        recording_time_s: float,
        timeout_ms: int,
        flags: int = 0,
        flat: Literal[True] = ...,
    ) -> _PollReturnFlatFalse: ...
    @overload
    def poll(
        self,
        recording_time_s: float,
        timeout_ms: int,
        flags: int = 0,
        flat: bool = False,
    ) -> Union[_PollReturnFlatTrue, _PollReturnFlatFalse]: ...
    def pollEvent(self, timeout_ms: int) -> Dict[str, Any]:
        """pollEvent(self: zhinst.core.ziDAQServer, timeout_ms: int) -> dict

        Return a dict, `{path: data}`, of changes that occurred in one single
        subscribed node. This is a low-level function to obtain a single event
        from the data server connection. To get all data waiting in the buffers,
        this command should be executed continuously until an empty dict is
        returned. The `poll()` function is better suited in many cases, as it
        returns the data accumulated over some time period.
            timeout_ms: Poll timeout in [ms]. Recommended value is 500ms."""
    def precompensationAdvisor(self) -> PrecompensationAdvisorModule:
        """precompensationAdvisor(self: zhinst.core.ziDAQServer) -> zhinst.core.PrecompensationAdvisorModule

        Create a PrecompensationAdvisorModule object. This will start a thread for
        running an asynchronous module."""
    def programRT(self, dev: str, filename: str) -> None:
        """programRT(self: zhinst.core.ziDAQServer, dev: str, filename: str) -> None

        Program RT.
            dev: Device identifier e.g. 'dev99'.
            filename: File name of the RT program."""
    def quantumAnalyzerModule(self) -> QuantumAnalyzerModule:
        """quantumAnalyzerModule(self: zhinst.core.ziDAQServer) -> zhinst.core.QuantumAnalyzerModule

        Create a QuantumAnalyzerModule object. This will start a thread for
        running an asynchronous module."""
    def record(self) -> RecorderModule:  # Deprecated arguments not included
        """record(*args, **kwargs)
        Overloaded function.

        1. record(self: zhinst.core.ziDAQServer) -> zhinst.core.RecorderModule

        Create a RecorderModule object. This will start a thread for
        running an asynchronous module.

        2. record(self: zhinst.core.ziDAQServer, duration_s: float, timeout_ms: int, flags: int = 1) -> zhinst.core.RecorderModule

        DEPRECATED, use record() without arguments.
            duration_s: Maximum recording time for single triggers in [s].
                   DEPRECATED, set 'buffersize' param instead.
            timeout_ms: Timeout in [ms]. Recommended value is 500ms.
                   DEPRECATED, ignored.
            flags: Record flags.
                   DEPRECATED, set 'flags' param instead.
                   FILL  = 0x0001 : Fill holes.
                   ALIGN = 0x0002 : Align data that contains a
                                    timestamp.
                   THROW = 0x0004 : Throw EOFError exception if
                                    sample loss is detected.
                   DETECT = 0x0008: Detect data loss holes."""
    def revision(self) -> int:
        """revision(self: zhinst.core.ziDAQServer) -> int

        Get the revision number of the Python interface of Zurich Instruments."""
    def scopeModule(self) -> ScopeModule:
        """scopeModule(self: zhinst.core.ziDAQServer) -> zhinst.core.ScopeModule

        Create a ScopeModule object. This will start a thread for
        running an asynchronous module."""
    @overload
    def set(self, items: _MultipleNodeItems) -> None:
        """set(*args, **kwargs)
        Overloaded function.

        1. set(self: zhinst.core.ziDAQServer, items: object) -> None

        Set multiple nodes. A transaction is used if more than a single
        path/value pair is specified.
            items: A list of path/value pairs.

        2. set(self: zhinst.core.ziDAQServer, path: str, value: object) -> None

            path: Path string of the node.
            value: (u)int8, (u)int16, (u)int32, (u)int64, float, double
                   or string to write."""
    @overload
    def set(self, path: str, value: Union[int, float, str]) -> None: ...
    def setByte(self, path: str, value: Any) -> None:
        """setByte(self: zhinst.core.ziDAQServer, path: str, value: object) -> None

        path:  Path string of the node.
        value: Value of the node."""
    def setComplex(self, path: str, value: complex) -> None:
        """setComplex(self: zhinst.core.ziDAQServer, path: str, value: complex) -> None

        path:  Path string of the node.
        value: Value of the node."""
    def setDebugLevel(self, severity: _DebugLevel) -> None:
        """setDebugLevel(self: zhinst.core.ziDAQServer, severity: int) -> None

        Enables debug log and sets the debug level (resets the debug levels for
        individual sinks).
            severity: Debug level (trace:0, debug:1, info:2, status:3, warning:4,
                      error:5, fatal:6)."""
    def setDebugLevelConsole(self, severity: _DebugLevel) -> None:
        """setDebugLevelConsole(self: zhinst.core.ziDAQServer, severity: int) -> None

        Enables debug log and sets the debug level for the console output.
            severity: Debug level (trace:0, debug:1, info:2, status:3, warning:4,
                      error:5, fatal:6)."""
    def setDebugLevelFile(self, severity: _DebugLevel) -> None:
        """setDebugLevelFile(self: zhinst.core.ziDAQServer, severity: int) -> None

        Enables debug log and sets the debug level for the file output.
            severity: Debug level (trace:0, debug:1, info:2, status:3, warning:4,
                      error:5, fatal:6)."""
    def setDebugLogpath(self, path: str) -> None:
        """setDebugLogpath(self: zhinst.core.ziDAQServer, path: str) -> None

        Sets the path where logfiles are stored. Note, it will restart logging
        if it was already enabled via setDebugLevel().
            path: Path to directory where logfiles are stored."""
    def setDeprecated(self, items: _MultipleNodeItems) -> None:
        """setDeprecated(self: zhinst.core.ziDAQServer, items: object) -> None

        Set multiple nodes.
            items: A list of path/value pairs."""
    def setDouble(self, path: str, value: float) -> None:
        """setDouble(self: zhinst.core.ziDAQServer, path: str, value: float) -> None

        path:  Path string of the node.
        value: Value of the node."""
    def setInt(self, path: str, value: int) -> None:
        """setInt(self: zhinst.core.ziDAQServer, path: str, value: int) -> None

        path:  Path string of the node.
        value: Value of the node."""
    def setString(self, path: str, value: str) -> None:
        """setString(self: zhinst.core.ziDAQServer, path: str, value: object) -> None

        path:  Path string of the node.
        value: Value of the node."""
    def setVector(self, path: str, value: _Vector) -> None:
        """setVector(self: zhinst.core.ziDAQServer, path: str, value: object) -> None

        path:  Path string of the node.
        value: Vector ((u)int8, (u)int16, (u)int32, (u)int64, float, double)
               or string to write."""
    def subscribe(self, path: _SingleOrMultipleNodePaths) -> None:
        """subscribe(self: zhinst.core.ziDAQServer, path: object) -> None

        Subscribe to one or several nodes. Fetch data with the poll
        command. In order to avoid fetching old data that is still in the
        buffer, execute a sync command before subscribing to data streams.
            path: Path string of the node. Use wild card to
                  select all. Alternatively also a list of path
                  strings can be specified."""
    def sweep(self) -> SweeperModule:  # Deprecated arguments not included
        """sweep(*args, **kwargs)
        Overloaded function.

        1. sweep(self: zhinst.core.ziDAQServer) -> zhinst.core.SweeperModule

        Create a SweeperModule object. This will start a thread for
        running an asynchronous module.

        2. sweep(self: zhinst.core.ziDAQServer, timeout_ms: int) -> zhinst.core.SweeperModule

        DEPRECATED, use sweep() without arguments.
        Create a sweeper class. This will start a thread for asynchronous
        sweeping.
            timeout_ms: Timeout in [ms]. Recommended value is 500ms.
                  DEPRECATED, ignored"""
    def sync(self) -> None:
        """sync(self: zhinst.core.ziDAQServer) -> None

        Synchronize all data paths. Ensures that get and poll
        commands return data which was recorded after the
        setting changes in front of the sync command. This
        sync command replaces the functionality of all syncSet,
        flush, and echoDevice commands."""
    def syncSetDouble(self, path: str, value: float) -> float:
        """syncSetDouble(self: zhinst.core.ziDAQServer, path: str, value: float) -> float

        path:  Path string of the node.
        value: Value of the node."""
    def syncSetInt(self, path: str, value: int) -> int:
        """syncSetInt(self: zhinst.core.ziDAQServer, path: str, value: int) -> int

        path:  Path string of the node.
        value: Value of the node."""
    def syncSetString(self, path: str, value: str) -> str:
        """syncSetString(self: zhinst.core.ziDAQServer, path: str, value: object) -> None

        path:  Path string of the node.
        value: Value of the node."""
    def unsubscribe(self, path: _SingleOrMultipleNodePaths) -> None:
        """unsubscribe(self: zhinst.core.ziDAQServer, path: object) -> None

        Unsubscribe data streams. Use this command after recording to avoid
        buffer overflows that may increase the latency of other command.
            path: Path string of the node. Use wild card to
                  select all. Alternatively also a list of path
                  strings can be specified."""
    def update(self) -> None:
        """update(self: zhinst.core.ziDAQServer) -> None

        Check if additional devices are attached. This function is not needed
        for servers running under windows as devices will be detected
        automatically."""
    def version(self) -> str:
        """version(self: zhinst.core.ziDAQServer) -> str

        Get version string of the Python interface of Zurich Instruments."""
    def writeDebugLog(self, severity: _DebugLevel, message: str) -> None:
        """writeDebugLog(self: zhinst.core.ziDAQServer, severity: int, message: str) -> None

        Outputs message to the debug log (if enabled).
            severity: Debug level (trace:0, debug:1, info:2, status:3, warning:4,
                      error:5, fatal:6).    message:  Message to output to the log."""
    def zoomFFT(self) -> ZoomFFTModule:  # Arguments deprecated
        """zoomFFT(*args, **kwargs)
        Overloaded function.

        1. zoomFFT(self: zhinst.core.ziDAQServer) -> zhinst.core.ZoomFFTModule

        Create a ZoomFFTModule object. This will start a thread for
        running an asynchronous module.

        2. zoomFFT(self: zhinst.core.ziDAQServer, timeout_ms: int) -> zhinst.core.ZoomFFTModule

        DEPRECATED, use zoomFFT() without arguments.
        Create a ZoomFFTModule class. This will start a thread for running an
        asynchronous ZoomFFTModule.
            timeout_ms: Timeout in [ms]. Recommended value is 500ms.
                  DEPRECATED, ignored"""
    @property
    def host(self) -> str:
        """The host used for the active connection.

        .. versionadded:: 22.08"""
    @property
    def port(self) -> int:
        """The port used for the active connection.

        .. versionadded:: 22.08"""
    @property
    def api_level(self) -> _APILevel:
        """The ziAPI level used for the active connection.

        .. versionadded:: 22.08"""

class ziDiscovery:
    def __init__(self) -> None:
        """__init__(self: zhinst.core.ziDiscovery) -> None"""
    def find(self, dev: str) -> str:
        """find(self: zhinst.core.ziDiscovery, dev: str) -> str

        Return the device id for a given device address.
            dev: Device address string e.g. UHF-DEV2000."""
    def findAll(self) -> List[str]:
        """findAll(self: zhinst.core.ziDiscovery) -> list

        Return a list of all discoverable devices."""
    def get(self, dev: str) -> Dict[str, Any]:
        """get(self: zhinst.core.ziDiscovery, dev: str) -> object

        Return the device properties for a given device id.
            dev: Device id string e.g. DEV2000."""
    def setDebugLevel(self, severity: _DebugLevel) -> None:
        """setDebugLevel(self: zhinst.core.ziDiscovery, severity: int) -> None

        Set debug level.
            severity: debug level."""

def compile_seqc(
    code: str, devtype: str, options: Union[str, List[str]], samplerate: float, **kwargs
) -> Tuple[bytes, Dict[str, Any]]:
    """compile_seqc(code: str, devtype: str, options: object = '', index: int = 0, **kwargs) -> tuple

    Compile the sequencer code.

    .. versionadded:: 22.08

    Args:
        code (str): SeqC input
        devtype (str): target device type, e.g., HDAWG8, SHFQC
        options (str or list): list of device options, or string of
            options separated by newlines as returned by node
            /dev.../features/options.
        index (int): index of the AWG core

    Keyword Args:
        samplerate (float): target sample rate of the sequencer
            Mandatory and only respected for HDAWG. Should match the
            value set on the device:
            `/dev.../system/clocks/sampleclock/freq`.
        sequencer (str): one of 'qa', 'sg', or 'auto'.
            Mandatory for SHFQC.
        wavepath (str): path to directory with waveforms. Defaults to
            path used by LabOne UI or AWG Module.
        waveforms (str): list of CSV waveform files separated by ';'.
            Defaults to all CSV files in `wavepath`.
        output (str): name of embedded ELF filename.

    Returns:
        Tuple (elf, extra) of binary ELF data for sequencer and extra
        dictionary with compiler output."""
