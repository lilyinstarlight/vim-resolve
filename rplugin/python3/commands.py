import sys
import os.path

import neovim

sys.path.append(os.path.dirname(__file__))

import resolve

@neovim.plugin
class ResolvePlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command('ResolveCompile')
    def compile(self):
        self.nvim.command('echo "TODO"')

    @neovim.command('ResolveVerify')
    def verify(self):
        self.nvim.command('echo "TODO"')
