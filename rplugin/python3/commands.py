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
        return os.path.splitext(os.path.basename(buffer.name))[0], b'\n'.join(nvim.current.buffer)

    @neovim.command('ResolveCompile')
    def compile(self):
        if not self.nvim.current.buffer.name:
            self.nvim.out_write('You must set a buffer name (e.g. save it to a file) to compile a resolve program.')
            return

        name, content = ResolvePlugin.get_args(self.nvim.current.buffer)

        jar = resolve.compile(name, content)

        # run jar

    @neovim.command('ResolveVerify')
    def verify(self):
        if not self.nvim.current.buffer.name:
            self.nvim.out_write('You must set a buffer name (e.g. save it to a file) to verify a resolve program.')
            return

        name, content = ResolvePlugin.get_args(self.nvim.current.buffer)

        vcs = resolve.genvcs(name, content)

        # show vcs

        for verification in resolve.verify(name, content):
            # update vcs
            pass
