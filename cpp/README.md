# C++ Extension

Build steps
1. Install pybind11 and a C++ compiler.
2. Configure and build:

```bash
mkdir -p build
cd build
cmake ..
cmake --build .
```

The built module should be importable as `bspricer_cpp`.
