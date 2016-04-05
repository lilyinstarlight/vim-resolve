import sys
import os.path

import neovim

sys.path.append(os.path.dirname(__file__))

import resolve

@neovim.plugin
class ResolvePlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim

    def get_args(buffer):
        return os.path.splitext(os.path.basename(buffer.name))[0], '\n'.join(buffer)

    @neovim.command('ResolveCompile')
    def compile(self):
        if not self.nvim.current.buffer.name:
            self.nvim.out_write('You must set a buffer name (e.g. save it to a file) to compile a resolve program.')
            return

        name, content = ResolvePlugin.get_args(self.nvim.current.buffer)

        try:
            jar = resolve.compile(name, content)
        except resolve.ResolveAPIError as e:
            self.nvim.out_write('Received error from resolve api: {}'.format(e))
            return
        except resolve.ResolveCompilerError as e:
            self.nvim.out_write('Received error from resolve compiler: {}'.format(e))
            return

        # run jar

    @neovim.command('ResolveVerify')
    def verify(self):
        if not self.nvim.current.buffer.name:
            self.nvim.out_write('You must set a buffer name (e.g. save it to a file) to verify a resolve program.')
            return

        name, content = ResolvePlugin.get_args(self.nvim.current.buffer)

        try:
            vcs = resolve.genvcs(name, content)
        except resolve.ResolveAPIError as e:
            self.nvim.out_write('Received error from resolve api: {}'.format(e))
            return
        except resolve.ResolveCompilerError as e:
            self.nvim.out_write('Received error from resolve compiler: {}'.format(e))
            return

        # show vcs

        try:
            for verification in resolve.verify(name, content):
                # update vcs
                pass
        except resolve.ResolveAPIError as e:
            self.nvim.out_write('Received error from resolve api: {}'.format(e))
            return
        except resolve.ResolveCompilerError as e:
            self.nvim.out_write('Received error from resolve compiler: {}'.format(e))
            return
