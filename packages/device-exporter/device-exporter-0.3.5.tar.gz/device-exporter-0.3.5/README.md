# device-exporter
Tool device-exporter gathers local system data, logs it to file and presents via API (/proc for processor data, /net for network data). API endpoints contains JSON outputs and allows for in-depth browsing (f.e. /proc/data/model_name).

## Command

Syntax:

device-exporter **[options]**

optional:
 - --log-path Path to directory for storing log files
 - --log-file Name of log file
 - --api-address Address exposing API
 - --api-port Port exposing API

- --no-api Do not expose API
- --no-log Do not log to a file
- --daemon Run as daemon - no stdout printouts
- --verbose Increase verbosity

### Data types

Network: bus, interface_name, vendor_id, vendor_name, device_id, device_name, driver_name, driver_version, firmware_version, branded_firmware_psid, numa_node, vf, 'dpdk, transceiver_vendor_name, transceiver_vendor_pn, port_connection_type, port_speed
