import sys

colors = ['\033[95m',
          '\033[94m',
          '\033[92m',
          '\033[93m',
          '\033[91m']
last_color = -1
processes = {}

def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()

def main():
    while 1:
        write_stdout('READY\n') # transition from ACKNOWLEDGED to READY
        line = sys.stdin.readline()  # read header line from stdin
        headers = dict([ x.split(':') for x in line.split() ])
        data = sys.stdin.read(int(headers['len'])) # read the event payload
        write_stdout('RESULT %s\n%s'%(len(data), data)) # transition from READY to ACKNOWLEDGED

def event_handler(event, response):
    global last_color
    line, data = response.split('\n', 1)
    headers = dict([ x.split(':') for x in line.split() ])
    if headers['processname'] not in processes:
        last_color += 1
        last_color %= len(colors)
        processes[headers['processname']] = colors[last_color]
    preamble = '{} {} {} \033[0m| '.format(processes[headers['processname']],
                                           headers['processname'],
                                           headers['channel'])
    for line in data.splitlines():
        print preamble + line

if __name__ == '__main__':
    main()
