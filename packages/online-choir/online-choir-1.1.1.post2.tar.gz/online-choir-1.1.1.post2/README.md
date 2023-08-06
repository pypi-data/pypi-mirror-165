Online Choir is online rehearsal tool. 
Unlike most software of this kind, it does not require a low-latency or broad internet connection.
It works with pretty much any connection, including mobile.

Of course, it does not either offer a full two-way audio link between musicians. 
Instead, it allows a single user (usually the director) to hear all musicians singing (or playing) together 
in a nice live _synchronized_ mix.

The package offers three executables:
 * The master client (aka director app) to be used by the choir director.
 * The slave client (aka singer app) to be used by the singers (or any musician)
 * The server, which handles the communication between the clients.

# Installation

_online-choir_ is a Python package on Pypi and hence can be installed on any platform equipped with Python 
(greater than 3.7) and `pip`:
````shell
pip3 install online-choir
````
However, some of its dependencies require (on some platforms) that some libraries are present.
Therefore, we make the following recommendations for specific operating systems:

## Stand-alone apps

On MacOS and Windows, we recommend the stand-alone apps, which do not require Python or any other library to be 
installed on the host computer. 
They can be downloaded under the following likns:
 * [Director App Mac](https://gitlab.com/odousse/online-choir/-/jobs/artifacts/master/download?job=mac-director-app)
 * [Director App Windows (installer)](https://gitlab.com/odousse/online-choir/-/jobs/artifacts/master/raw/src/Output/online-choir-director-setup.exe?job=win-app)
 * [Director App Windows (stand-alone app)](https://gitlab.com/odousse/online-choir/-/jobs/artifacts/master/raw/src/dist/Online\%20Choir\%20Director.exe?job=win-app)
 * [Singer App Mac](https://gitlab.com/odousse/online-choir/-/jobs/artifacts/master/download?job=mac-singer-app)
 * [Singer App Windows (installer)](https://gitlab.com/odousse/online-choir/-/jobs/artifacts/master/raw/src/Output/online-choir-singer-setup.exe?job=win-app)
 * [Singer App Windows (stand-alone app)](https://gitlab.com/odousse/online-choir/-/jobs/artifacts/master/raw/src/dist/Online\%20Choir\%20Singer.exe?job=win-app)

Please refer to the user manual for instructions on how to use the apps:
 * [Master client user manual](https://gitlab.com/odousse/online-choir/-/jobs/artifacts/master/raw/docs/user_manual_director.pdf?job=documentation)
 * [Slave client user manual](https://gitlab.com/odousse/online-choir/-/jobs/artifacts/master/raw/docs/user_manual_singer.pdf?job=documentation)

Note that that is no stand-alone app for the server part.

## MacOS

If you don't want to use the stand-alone apps or want to run the server on MacOS, you can of cource install the Python 
package instead.
We do recommend to use [Homebrew](https://brew.sh) for installing Python and the required libraries on MacOS; 
Please follow the installation instructions from Homebrew first.
Then, issue the following command to install Python and the required libraries:
```shell
brew install python-tk portaudio libsndfile faad2
```
Then proceed with the usual installation of the package using `pip3` (see above).

## Debian/Ubuntu

In order to use the package, you need to install the following first:
```shell
apt install python3-tk python3-pip python3-numpy python3-soundfile libportaudio2 libsndfile1
```
Then proceed with the usual installation of the package using `pip` (see above).

# Usage

## Rehearsing with online-choir

In order to use _online-choir_, you need a server instance to run on a machine that is reachable from all clients.
Then, each singer needs to run the slave client on their computer, and have headphones and a microphone attached to it.
Finally, the director uses the master client to play some audio track that all singers hear. 
Singers sing along the audio track, and in return the director hears all singers (optionally together with the audio 
track). 

The main limitation of the software is that the singers do not hear each other.
As a counterpart for this limitation, the software works with nearly any internet connection, even if some have high
latencies. Latency and jitter *do not* disturb the synchronicity of the mix. 
This means that the voice of signers with high-latency connections come exactly at the same time to the director as 
those of singers with low-latency connections.

### Live session

The audio track played to the singers is typically read from a pre-recorded audio file provided by the director (e.g.
a karaoke-style instrumental track).
Alternatively, the input audio file can be replaced by a direct streaming from the director's local computer.
In this mode, the choir is not played back immediately to the director (mute mode).
The director should listen to the recoreded mix after the session instead.

## Running the software

Once installed, the package provides three commands:
 * `online-choir-director`
 * `online-choir-singer`
 * `online-choir-server`
each corresponding to one piece of the software.
   
If you did not install the package via pip and only downloaded the source code, you can invoke the same three scripts
using the following commands from the root directory of the project:
 * `python3 bin/run_master_client.py`
 * `python3 bin/run_slave_client.py`
 * `python3 bin/run_server.py`

### Common options

All three commands accept the following options:
 * `--log-level [LEVEL]` sets the logging level in the terminal (logs at all levels are anyways recorded into the log 
   file, see below)
 * `--log-file [LOG_FILE]` determines where to record the logs as well as the content of `stderr`.
   By default, the log file is:
    * MacOS: `~/Library/Logs/Online Choir/<script name>.log`
    * Windows: `%APPDATA%\Online Choir\<script name>.log`
    * Linux: `~/.online-choir/<script name>.log`
 * `--console` prevents the content of `stderr` from being re-routed into the log file.

### Master client options

`--no-gui` runs the master client in CLI mode. Otherwise, it runs in GUI mode. For more detail on how to use the GUI, 
please refer to the [user manual](https://gitlab.com/odousse/online-choir/-/jobs/artifacts/master/raw/documentation/user_manual_director.pdf?job=documentation).

In CLI mode, each invocation of the client starts a singing session. The client exists after each session. 
The following options are available:
 * `--input [INPUT_FILE]` specifies the audio file that is played to the singers. The file needs to be in WAV format, 
   stereo, with 44.1kHz sampling rate and 16 bits per sample.
 * `--live` alternatively to playing from a file, this option allows to send the computer's default audio input to the
   singers (see section on live sessions below)
 * `--mute` do not play the mix aloud (implied by `--live`)
 * `--output [OUTPUT_FILE]` records the mix into the given file (either in WAV or FLAC format, depending on the 
   extension)
 * `--server [SERVER_ADDRESS]` the hostname of the server
 * `--port [PORT_NUMBER]` the port number on the server (default is 8878)
 * `--skip-seconds [NUMBER_OF_SECONDS]` if playing from a file, skip this amount of seconds at the beginning of the file
 * `--monitor-level [LEVEL]` the level of the input file in the mix

### Slave client options

`--no-gui` runs the master client in CLI mode. Otherwise, it runs in GUI mode. For more detail on how to use the GUI, 
please refer to the [user manual](https://gitlab.com/odousse/online-choir/-/jobs/artifacts/master/raw/documentation/user_manual_singer.pdf?job=documentation).

In CLI mode, each invocation of the client starts a singing session. The client exists after each session. 
The following options are available:
 * `--server [SERVER_ADDRESS]` the hostname of the server
 * `--port [PORT_NUMBER]` the port number on the server (default is 8868)
 * `--latency [LATENCY]` specifies the latency of the audio devices on the host computer. This should be an integer.
   Each unit corresponds to 11.6ms (e.g. a value of 5 means 58ms). The GUI mode provides a tool to measure this latency.

### Server options

 * `--master-port` [PORT_NUMBER] the port to which master clients should connect
 * `--slave-port` [PORT_NUMBER] the port to which slave clients should connect
 * `--control-port`[PORT_NUMBER] the port to which master clients should connect for controlling the mix. The master 
   client always uses <mater port> + 20. Therefore, if you configure this option to anything else than <master-port> 
    + 20, the mixing desk feature of the master client will not work.
 * `--ices` see section below.

### Web Radio

Optionally the server script can start an instance of `ices2` (needs to be installed separately) in order to stream the 
input file to an IceCast server. 
This is useful when some singers are unable to use the slave client; as a replacement, they can get the same audio cue 
from the web radio and participate in the rehearsal.
This option is activated by the `--ices <ices_config>` option of the server script. It requires a valid config file for
`ices2`.

# Annex

## Description of the network protocol

### General rules

The following rules apply to all communication among programs:
 * Raw TCP channels with fixed sized transmission chunks: the programs communicate directly through TCP, and use the 
   `readexactly()` method to await data chunks, as their size is predefined.
 * Immediately after establishing the TCP connection to the server, clients (both master and slave) send a predefined 
   authentication frame (see `common/auth.py`) to the server. If anything else is sent first, the server drops the 
   connection.
 * After authentication, client and server communicate by sending fixed-sized chunks to each-other. The chunk sizes are
   the following:
   * master to server: 514 bytes
   * server to master 1028 bytes
   * slave to server: 260 bytes
   * server to slave: 514 bytes
 * The first 4 bytes of the chunks are always carrying a "chunk index" (a 32-bit signed integer), and the rest is 
   payload.
 * The chunk index must be a multiple of 199 (prime number). In the sequel we omit this multiplier for clarity, i.e. 
   chunk no. 3 would actually be sent as number 3 * 199 = 597.
 * The payload is either empty or contains audio signal. If there is any audio content, it is invariably 512 audio 
   frames.
   The type of encoding determines the actual payload size (4 bytes less than the packet size):
   * master to server and server to slave: stereo ADPCM, 512 bytes
   * slave to server: mono ADPCM, 256 bytes
   * server to master: raw mono PCM, 1024 bytes
 * Chunks containing actual audio have positive chunk indices (including 0), while negative indices are for signalling.

### Master-server protocol

The master client only establishes a connection to the server when the session starts. 
After the authentication packet has been sent, the master client proceeds and sends the audio content directly.
When it wants to end the session (either because there is no audio left to send, or because the user presses the Stop 
button), it terminates the session with a chunk with index -1 (remember that all indices are actually multiplied by 199
in the chunk's data, hence the chunk begins with -199 encoded in its 4 first bytes; the rest of the chunk's payload does
not matter).

On the downlink, the server sends the mix back to the client. 
It uses no signalling chunk at all and just proceeds with audio chunks as soon as they are available. 
The master client waits until it receives exactly as many audio chunks as it sent to the server.
After receiving all the chunks, the client closes the connection with the server.

### Slave-server protocol

The slave client connects to the server as soon as it is opened, sends its authentication paket and then waits for audio
content to come from the server.

If the connection is idle for more than 10 seconds, it sends a keep-alive chunk to the server. 
Keep-alive chunks are chunks with index -3.
Likewise, the server will send keep-alive chunks on a regular basis to the client. 
The client shall drop the connection if no chunk at all has arrived in the last 30 seconds.

The client knows that a session starts when it receives a chunk with index 0. 
Immediately after receiving that chunk, the client acknowledges that it will participate in the session by sending back
a chunk with index -1 (aka check-in chunk).
Then it proceeds and start sending its audio stream (the participant's voice) as soon as available.
THE SLAVE CLIENT IS RESPONSIBLE FOR SYNCHRONIZING ITS AUDIO STREAM WITH THAT IT RECEIVED. 
That means that the audio content it sends with index i shall contain the audio recorded exactly when chunk number i was
played to the ears of the participant. 

The server send a chunk with index -1 to signal the end of the session.
The salve client does not need to signal the end of its audio stream, as the server expects to receive exactly as many 
chunks from the slave as it sent to it.

If for technical reasons the slave needs to drop from the session (for example, it experienced a playback buffer 
under-run, causing the singing to be interrupted and no longer smooth), it sends a chunk with index -2 to signal the
error. 
The server then knows that is shall not expect further audio from that client and will ignore it in the mix. 

## Credits

Icon by [Muhammad Haq](https://freeicons.io/profile/823) on [freeicons.io](https://freeicons.io)
