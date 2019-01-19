import os
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

    def popout(self, name):
        for buffer in self.nvim.buffers:
            if buffer.name == name:
                self.nvim.command('{} bdelete'.format(buffer.number))

        self.nvim.command('belowright vertical 50 new')
        win = self.nvim.current.window

        win.buffer.name = name

        win.buffer.options['swapfile'] = False
        win.buffer.options['undofile'] = False
        win.buffer.options['buftype'] = 'nofile'
        win.buffer.options['bufhidden'] = 'delete'

        return win

    def display_lines(self, win, objs, ln, key, gen):
        lines = {}
        line = 0
        last = 0

        double = False
        double_start = 0

        for obj in objs:
            if ln(obj) == last:
                double = True
            else:
                if double:
                    self.nvim.command('{},{} fold'.format(double_start, line))

                added = ln(obj) - last - 1

                for _ in range(added):
                    if line == 0:
                        win.buffer[0] = '~'
                    else:
                        win.buffer.append('~')

                    line += 1

                double = False
                double_start = line + 1

            last = ln(obj)

            if key:
                lines[key(obj)] = line

            info = gen(obj)

            start = line + 1

            for infoline in info.split('\n'):
                if line == 0:
                    win.buffer[0] = infoline
                else:
                    win.buffer.append(infoline)

                line += 1

            self.nvim.command('{},{} fold'.format(start, line))

        if double:
            self.nvim.command('{},{} fold'.format(double_start, line))

        win.buffer.options['modifiable'] = False

        self.nvim.command('1')
        self.nvim.command('winc h')
        self.nvim.command('1')

        return lines

    @neovim.command('ResolveCompile')
    def compile(self):
        popout_prefix = '{}/Compilation Output - '.format(os.readlink('/tmp'))

        if self.nvim.current.buffer.name.startswith(popout_prefix):
            self.nvim.command('winc h')

        if not self.nvim.current.buffer.name:
            self.nvim.out_write('You must set a buffer name (e.g. save it to a file) to compile a resolve program.\n')
            return

        name, type, content = ResolvePlugin.get_args(self.nvim.current.buffer)
        codewin = self.nvim.current.window

        try:
            jar = resolve.compile(name, type, content)
        except resolve.ResolveAPIError as e:
            ewin = self.popout(popout_prefix + name)

            lines = self.display_lines(ewin, e.args[0], lambda err: err['error']['ln'], None, lambda err: 'Error: {}'.format(err['error']['msg'][:-1]))

            codewin.options['scrollbind'] = True
            ewin.options['scrollbind'] = True
            return
        except resolve.ResolveCompilerError as e:
            ewin = self.popout(popout_prefix + name)

            lines = self.display_lines(ewin, e.args[0], lambda err: err['error']['ln'], None, lambda err: 'Error: {}'.format(err['error']['msg'][:-1]))

            codewin.options['scrollbind'] = True
            ewin.options['scrollbind'] = True
            return

        with tempfile.NamedTemporaryFile() as temp:
            temp.write(jar)
            temp.flush()

            subprocess.call(['java', '-jar', temp.name])

    @neovim.command('ResolveVerify')
    def verify(self):
        popout_prefix = '{}/Verification Conditions - '.format(os.readlink('/tmp'))

        if self.nvim.current.buffer.name.startswith(popout_prefix):
            self.nvim.command('winc h')

        if not self.nvim.current.buffer.name:
            self.nvim.out_write('You must set a buffer name (e.g. save it to a file) to verify a resolve program.\n')
            return

        name, type, content = ResolvePlugin.get_args(self.nvim.current.buffer)
        codewin = self.nvim.current.window

        try:
            vcs = resolve.genvcs(name, type, content)
        except resolve.ResolveAPIError as e:
            ewin = self.popout(popout_prefix + name)

            lines = self.display_lines(ewin, e.args[0], lambda err: err['error']['ln'], None, lambda err: 'Error: {}'.format(err['error']['msg'][:-1]))

            codewin.options['scrollbind'] = True
            ewin.options['scrollbind'] = True
            return
        except resolve.ResolveCompilerError as e:
            ewin = self.popout(popout_prefix + name)

            lines = self.display_lines(ewin, e.args[0], lambda err: err['error']['ln'], None, lambda err: 'Error: {}'.format(err['error']['msg'][:-1]))

            codewin.options['scrollbind'] = True
            ewin.options['scrollbind'] = True
            return

        vcwin = self.popout(popout_prefix + name)
        lines = self.display_lines(vcwin, vcs['vcs'], lambda vc: vc['lineNum'], lambda vc: vc['vc'], lambda vc: '* {}\nGoal: {}Given:\n\t{}'.format(vc['vcInfo'], vc['vcGoal'] if isinstance(vc['vcGoal'], str) and vc['vcGoal'].endswith('\n') else '{}\n'.format(vc['vcGoal']), '\n\t'.join(vc['vcGivens'].split('\n')[:-1]) if vc['vcGivens'] else 'None'))

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
