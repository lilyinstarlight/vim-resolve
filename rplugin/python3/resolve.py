import os.path
import subprocess
import sys
import tempfile

import neovim

sys.path.append(os.path.dirname(__file__))

import resolve

@neovim.plugin
class ResolvePlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim

    def get_args(buffer):
        return os.path.splitext(os.path.basename(buffer.name))[0], buffer[0][0].lower(), '\n'.join(buffer)

    @neovim.command('ResolveCompile')
    def compile(self):
        if not self.nvim.current.buffer.name:
            self.nvim.out_write('You must set a buffer name (e.g. save it to a file) to compile a resolve program.')
            return

        name, type, content = ResolvePlugin.get_args(self.nvim.current.buffer)

        try:
            jar = resolve.compile(name, type, content)
        except resolve.ResolveAPIError as e:
            self.nvim.out_write('Received error from resolve api: {}'.format(e))
            return
        except resolve.ResolveCompilerError as e:
            self.nvim.out_write('Received error from resolve compiler: {}'.format(e))
            return

        with tempfile.NamedTemporaryFile() as temp:
            temp.write(jar)
            temp.flush()

            subprocess.call(['java', '-jar', temp.name])

    @neovim.command('ResolveVerify')
    def verify(self):
        if not self.nvim.current.buffer.name:
            self.nvim.out_write('You must set a buffer name (e.g. save it to a file) to verify a resolve program.')
            return

        name, type, content = ResolvePlugin.get_args(self.nvim.current.buffer)

        try:
            vcs = resolve.genvcs(name, type, content)
        except resolve.ResolveAPIError as e:
            self.nvim.out_write('Received error from resolve api: {}'.format(e))
            return
        except resolve.ResolveCompilerError as e:
            self.nvim.out_write('Received error from resolve compiler: {}'.format(e))
            return

        codewin = a.current.window
        a.command('belowright vertical 50 sview "Verification Conditions"')
        vcwin = a.current.window

        codewin.options['scrollbind'] = True
        vcwin.options['scrollbind'] = True

        lines = {}
        line = 0
        last = 0

        for vc in vcs['vcs']:
            added = vc['lineNum'] - last

            last = vc['lineNum']

            vcwin.buffer.append(''.join('\n' for _ in range(added)))

            line += added

            lines[vc['vc']] = line

            info = '* {}\nGoal: {}\nGiven:\n\t{}'.format(vc['vcInfo'], vc['vcGoal'], '\n\t'.join(vc['Givens'].split('\n')))

            vcwin.buffer[line] = info

            start = line

            line += info.count('\n')

            a.command('{} {} fold'.format(start, line))

        a.command('winc h')

        try:
            for verification in resolve.verify(name, type, content):
                if verification['result'] == 0:
                    result = '✓'
                elif verification['result'] == 1:
                    result = '?'
                elif verification['result'] == 2:
                    result = '-'
                else:
                    result = '✗'

                vcwin.buffer[lines[verification['id']]][0] = result
        except resolve.ResolveAPIError as e:
            self.nvim.out_write('Received error from resolve api: {}'.format(e))
            return
        except resolve.ResolveCompilerError as e:
            self.nvim.out_write('Received error from resolve compiler: {}'.format(e))
            return
