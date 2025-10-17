# GNG2101 Z13 Piano Assist Device

The following repository features the code for the 'Piano Assist Device' prosthetic. Designed for use on the Raspberry Pi Pico W (v1) and 433MHz transmitter and reciever. 
Primary Webpage on [[MakerRepo](https://makerepo.com/ctourangeau/2544.gng2101z13piano-assist-device)]

Team Members:
- M. Barette
- C. Tourangeau
- A. Gordon
- T. Guan

# For installation, use the latest version plugged into the OTG port. Refer to the user manual for detailed steps.

Bugs fixed in latest version (v4):
- Resolved an issue where it would hang on rising and falling edges. Issuing a machine.reset() in extreme cases also works.
- Every packet sent will open a new port number, which is incremented everytime. This will eventually cause an integer overflow when >65535. Adding an wrap around logic fixes this.
- Instead of sending every ~100ms, it has been reduced to ~20-50ms. Various minor additional changes were made to accomodate this higher frequency.


Index:
- v4 : Wi-Fi 2.4GHz band bugfix v3.X
- v3 : Wi-Fi 2.4GHz band bugfix v2.X
- v2 : Wi-Fi 2.4GHz band; brute force connection method (Improved connection rate)
- v1 : RF Transmitter and Receiver FS1000A and MX-FS-03V
