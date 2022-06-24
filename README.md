<p align=center>
    <img src="misc/Soft Serve.png" alt="Soft Serve Logo" width=60%>
</p>

<img src="https://img.shields.io/github/license/pebaz/soft-serve" alt="zlib licensed" align="right">
<img src="https://img.shields.io/github/sponsors/pebaz" alt="GitHub Sponsor Count" align="right">

# Soft Serve

> IEEE 754 Soft Floating Point Library

## Building

Ensure that [Berkeley-SoftFloat-3](https://github.com/ucb-bar/berkeley-softfloat-3)
is cloned next to Soft-Serve's root directory.

To build Berkeley-SoftFloat-3, run `make` in whatever platform directory you
need (`build/Linux-x86_64-GCC/` or `build/Win32-MinGW`, etc.).

*One important thing is to rename the resulting `softfloat.a` to
`libsoftfloat.a` so that GCC can find it.*

```bash
$ gcc src/main.c \
    -I ../berkeley-softfloat-3/source/include \
    -L ../berkeley-softfloat-3/build/Linux-x86_64-GCC \
    -l softfloat
    -o soft-serve.exo  # "Executable Object"
```
