# **PingPongServers**
Ping Pong Servers using FastApi for Dataloop AI Technical Assignment


## Usage:
### python pong-cli.py start <pong_time_ms>
*  Starting the ping-pong game between the servers, with pong_time_ms delay between the pings

### python pong-cli.py pause
*  Pausing the servers and saving their current time between the pings

### python pong-cli.py resume
*  Resuming the servers from the time when they have been paused

### python pong-cli.py stop
*  Stopping the servers and reset their pong_time_ms

## Files:
### instance1.py
*  First server, responsible for starting and sending the first ping

### instance2.py
*  Second server

### pong-cly.py
*  Responsible for game behaviour between the servers: Starting, Pausing, Resuming, Stopping


