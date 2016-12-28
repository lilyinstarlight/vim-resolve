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
            self.nvim.out_write('You must set a buffer name (e.g. save it to a file) to compile a resolve program.\n')
            return

        name, type, content = ResolvePlugin.get_args(self.nvim.current.buffer)

        try:
            jar = resolve.compile(name, type, content)
        except resolve.ResolveAPIError as e:
            self.nvim.out_write('Received error from resolve api: {}\n'.format(e))
            return
        except resolve.ResolveCompilerError as e:
            self.nvim.out_write('Received error from resolve compiler: {}\n'.format(e))
            return

        with tempfile.NamedTemporaryFile() as temp:
            temp.write(jar)
            temp.flush()

            subprocess.call(['java', '-jar', temp.name])

    @neovim.command('ResolveVerify')
    def verify(self):
        if self.nvim.current.buffer.name.startswith('/tmp/Verification Conditions - '):
            self.nvim.command('winc h')

        if not self.nvim.current.buffer.name:
            self.nvim.out_write('You must set a buffer name (e.g. save it to a file) to verify a resolve program.\n')
            return

        name, type, content = ResolvePlugin.get_args(self.nvim.current.buffer)

        try:
            vcs = resolve.genvcs(name, type, content)
        except resolve.ResolveAPIError as e:
            self.nvim.out_write('Received error from resolve api: {}\n'.format(e))
            return
        except resolve.ResolveCompilerError as e:
            self.nvim.out_write('Received error from resolve compiler: {}\n'.format(e))
            return

        codewin = self.nvim.current.window

        vcwin_name = '/tmp/Verification Conditions - {}'.format(name)
        for buffer in self.nvim.buffers:
            if buffer.valid and buffer.name == vcwin_name:
                self.nvim.command('{} bdelete'.format(buffer.number))
                break

        self.nvim.command('belowright vertical 50 new')
        vcwin = self.nvim.current.window

        vcwin.buffer.name = vcwin_name

        vcwin.buffer.options['swapfile'] = False
        vcwin.buffer.options['undofile'] = False
        vcwin.buffer.options['buftype'] = 'nofile'
        vcwin.buffer.options['bufhidden'] = 'delete'

        lines = {}
        line = 0
        last = 0

        double = 0
        double_start = 0

        for vc in vcs['vcs']:
            if vc['lineNum'] == last:
                double = True
            else:
                if double:
                    self.nvim.command('{},{} fold'.format(double_start, line))

                added = vc['lineNum'] - last - 1

                for _ in range(added):
                    if line == 0:
                        vcwin.buffer[0] = '~'
                    else:
                        vcwin.buffer.append('~')

                    line += 1

                double = False
                double_start = line + 1

            last = vc['lineNum']

            lines[vc['vc']] = line

            info = '* {}\nGoal: {}Given:\n\t{}'.format(vc['vcInfo'], vc['vcGoal'] if isinstance(vc['vcGoal'], str) and vc['vcGoal'].endswith('\n') else '{}\n'.format(vc['vcGoal']), '\n\t'.join(vc['vcGivens'].split('\n')[:-1]) if vc['vcGivens'] else 'None')

            start = line + 1

            for infoline in info.split('\n'):
                if line == 0:
                    vcwin.buffer[0] = infoline
                else:
                    vcwin.buffer.append(infoline)

                line += 1

            self.nvim.command('{},{} fold'.format(start, line))

        if double:
            self.nvim.command('{},{} fold'.format(double_start, line))

        vcwin.buffer.options['modifiable'] = False

        self.nvim.command('1')
        self.nvim.command('winc h')
        self.nvim.command('1')

        codewin.options['scrollbind'] = True
        vcwin.options['scrollbind'] = True


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

                line = lines[verification['id']]

                vcwin.buffer.options['modifiable'] = True

                vcwin.buffer[line] = result + vcwin.buffer[line][1:]

                vcwin.buffer.options['modifiable'] = False
        except resolve.ResolveAPIError as e:
            self.nvim.out_write('Received error from resolve api: {}'.format(e))
            return
        except resolve.ResolveCompilerError as e:
            self.nvim.out_write('Received error from resolve compiler: {}'.format(e))
            return
