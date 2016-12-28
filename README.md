vim-resolve
===========

A complete syntax, compilation, and verification plugin for the RESOLVE language for Neovim. In addition to faculties for having Neovim/Vim parse and indent RESOLVE files, it includes a Neovim plugin that asynchronously contacts [https://resolve.cs.clemson.edu/](https://resolve.cs.clemson.edu/) and populates Neovim with related content via the commands below.


Commands
========


ResolveCompile
==============

The `ResolveCompile` command contacts RESOLVE servers and downloads a Java applet representing the compiled version of the application and runs it.


ResolveVerify
==============

The `ResolveVerify` command contacts RESOLVE servers to get verification conditions then asynchronously updates a buffer to indicate what the conditions are, where the conditions are, and whether they were met or not.
