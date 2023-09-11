import sys
import requests

# if there are not args
if len(sys.argv) < 2:
    print("Usage: python pong-cli.py <command> <param>")
    sys.exit(1)

# command to cli
command = sys.argv[1]

if command == "start":
    # if time between ponging was not provided
    if len(sys.argv) < 3:
        print("Usage: python pong-cli.py start <pong_time_ms>")
        sys.exit(1)
    pong_time_ms = int(sys.argv[2])
    # start the servers
    response = requests.get(f"http://localhost:8000/start?pong_time_query={pong_time_ms}")
    print(response.json())
elif command == "pause":
    # pause the servers
    response1 = requests.get(f"http://localhost:8000/pause")
    response2 = requests.get(f"http://localhost:8001/pause")
    print(response1.json())
    print(response2.json())
elif command == "resume":
    # resume the servers
    response1 = requests.get(f"http://localhost:8000/resume")
    response2 = requests.get(f"http://localhost:8001/resume")
    print(response1.json())
    print(response2.json())
elif command == "stop":
    # stop the servers
    response1 = requests.get(f"http://localhost:8000/stop")
    response2 = requests.get(f"http://localhost:8001/stop")
    print(response1.json())
    print(response2.json())
else:
    print("Invalid command")
    sys.exit(1)
