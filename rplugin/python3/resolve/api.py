import json

import urllib.parse
import urllib.request

import websocket

# api endpoint
endpoint = 'resolve.cs.clemson.edu/teaching'

# default information for resolve jobs
package = 'Default_Package'
project = 'Default_Project'
parent = 'undefined'

class ResolveAPIError(RuntimeError):
    # general resolve api error (e.g. api communication errors)
    pass

class ResolveCompilerError(RuntimeError):
    # general resolve error (e.g. syntax errors)
    pass

def decode_url(string):
    # url unquote but additionally decode '%20' and '%2B' again
    return urllib.parse.unquote(string).replace('%20', ' ').replace('%2B', '+')

def decode_xml(string):
    # remove xml tags from result
    return string.replace('<vcFile>', '').replace('</vcFile>', '')

def decode_json(payload):
    if isinstance(payload, dict):
        # store decoded json
        decoded = {}

        # iterate over dictionary
        for key in payload.keys():
            # recursively decode elements into more json
            decoded[key] = decode_json(payload[key])

        # return decoded dictionary
        return decoded
    elif isinstance(payload, list):
        # store decoded json
        decoded = []

        # iterate over dictionary
        for element in payload:
            # recursively decode elements into more json
            decoded.append(decode_json(element))

        # return decoded list
        return decoded
    elif isinstance(payload, str):
        # decode string
        element = decode_xml(decode_url(payload))

        try:
            # try to load is at json
            return decode_json(json.loads(element))
        except:
            # just return the plain string if that fails
            return element
    else:
        # return plain elements
        return payload

def decode(payload):
    # decode string as json
    return decode_json(json.loads(payload))

def encode_url(string):
    # url quote string
    return urllib.parse.quote(string)

def encode_json(payload):
    # store encoded json
    encoded = {}

    # iterate over dictionary
    for key in payload.keys():
        if isinstance(payload[key], str):
            # encode strings
            encoded[key] = encode_url(payload[key])
        else:
            # copy others
            encoded[key] = payload[key]

    # return encoded dictionary
    return encoded

def encode(payload):
    # encode as json
    return json.dumps(encode_json(payload))

def request(job, name, content, package=package, project=project, parent=parent, endpoint=endpoint):
    # create job data
    job_data = {
            'name': name,
            'pkg': package,
            'project': project,
            'content': content,
            'parent': parent,
            'type': 'f'
    }

    # open websocket
    sock = websocket.WebSocket()
    sock.connect('wss://{}/Compiler?job={}'.format(endpoint, job))

    # send job
    sock.send(encode(job_data))

    # get ack and results
    sock.recv()

    return sock

def compile(name, content, package=package, project=project, parent=parent, endpoint=endpoint):
    # send job buildJar to api
    sock = request('buildJar', name, content, package, project, parent, endpoint)

    # decode result into sane json
    resp = decode(sock.recv())

    # make sure job completed
    if resp['status'] != 'complete':
        try:
            raise ResolveCompilerError(resp['errors'][0]['errors'])
        except KeyError:
            raise ResolveAPIError(resp['bugs'][0]['bugs'])

    # download jar file
    with urllib.request.urlopen('https://{}/download?job=download&name={}&dir={}'.format(endpoint, resp['result']['jarName'], resp['result']['downloadDir'])) as response:
        jar = response.read()

    # return jar bytes
    return jar

def genvcs(name, content, package=package, project=project, parent=parent, endpoint=endpoint):
    # send job genVCs to api
    sock = request('genVCs', name, content, package, project, parent, endpoint)

    # decode result into sane json
    resp = decode(sock.recv())

    # make sure job completed
    if resp['status'] != 'complete':
        try:
            raise ResolveCompilerError(resp['errors'][0]['errors'])
        except KeyError:
            raise ResolveAPIError(resp['bugs'][0]['bugs'])

    # return vcs
    return resp['result']

def verify(name, content, package=package, project=project, parent=parent, endpoint=endpoint):
    # send job verify2 to api
    sock = request('verify2', name, content, package, project, parent, endpoint)

    # decode result into sane json
    resp = decode(sock.recv())

    while resp['status'] == 'processing':
        # parse results into a number indication prove result
        if 'Proved' in resp['result']['result']:
            result = 0
        elif 'Timeout' in resp['result']['result']:
            result = 1
        elif 'Skipped' in resp['result']['result']:
            result = 2
        else:
            result = 3

        # yield verification with id and result
        yield {'id': resp['result']['id'], 'result': result}

        # decode result into sane json
        resp = decode(sock.recv())

    # make sure job completed
    if resp['status'] != 'complete':
        try:
            raise ResolveCompilerError(resp['errors'][0]['errors'])
        except KeyError:
            raise ResolveAPIError(resp['bugs'][0]['bugs'])

if __name__ == '__main__':
    import os
    import os.path

    import sys

    from argparse import ArgumentParser, FileType

    parser = ArgumentParser(description='call resolve web api to compile, generate VCs, and verify resolve programs')
    parser.add_argument('-a', '--api', default=endpoint, dest='endpoint', help='endpoint for resolve web api')
    parser.add_argument('-k', '--package', default=package, dest='package', help='package the file is in')
    parser.add_argument('-p', '--project', default=project, dest='project', help='project the file is in')
    parser.add_argument('-r', '--parent', default=parent, dest='parent', help='parent to the file')
    parser.add_argument('-o', '--output', default=sys.stdout, type=FileType('w'), dest='output', help='output file (writes to stdout if omitted)')
    parser.add_argument('command', choices=['compile', 'genvcs', 'verify'], help='api command')
    parser.add_argument('file', type=FileType('r'), help='resolve file')

    args = parser.parse_args()

    def binary_write(data):
        # write binary data to output file
        os.fdopen(args.output.fileno(), 'wb').write(data)

    def json_write(obj):
        # write json to output file with trailing newline
        args.output.write(json.dumps(obj))
        args.output.write('\n')

    def iter_write(objs):
        for obj in objs:
            # write json to output file with trailing newline
            args.output.write(json.dumps(obj))
            args.output.write('\n')

            # flush data so caller can get it
            args.output.flush()

    # decode command into function and output
    if args.command == 'compile':
        command = compile
        output = binary_write
    elif args.command == 'genvcs':
        command = genvcs
        output = json_write
    elif args.command == 'verify':
        command = verify
        output = iter_write

    try:
        # run given command with given output
        output(command(os.path.splitext(os.path.basename(args.file.name))[0], args.file.read(), args.package, args.project, args.parent, args.endpoint))
    except ResolveAPIError as error:
        # output errors
        print(json.dumps(error.args))
        sys.exit(1)
