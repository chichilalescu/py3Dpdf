=======
py3Dpdf
=======

Translator of python (well, `numpy`) objects into things that can be
made into 3D Portable Document Format files.

At the moment I know of 2 ways of accomplishing this:
translate python objects into `asymptote` files (then call the `asy`
tool on these files), or use `MathGL` for printing directly.

There are a couple of other packages that attempt to interface python
with `asymptote`, but I don't think they do what I need.
They're at https://github.com/memmett/PyAsy, and
http://www.tex.ac.uk/tex-archive/graphics/asymptote/base/asymptote.py.

The `MathGL` sources (C++) compile their own python wrapper, which does
not seem to be that well documented, but the documentation seems to be
sufficient for my needs.

