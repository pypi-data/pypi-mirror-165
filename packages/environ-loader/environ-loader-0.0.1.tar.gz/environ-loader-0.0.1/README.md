# Environ Loader

A module for loading environment variables from various sources, like Windows .bat files and Bash .sh files.

Sometimes when writing a Python script, you want to load environment variables are defined in a text file. For example, when running Conan with the virtualenv generator,
Conan will generate shell files for Windows and Linux that contain variables like PATH that are configured to use the library/tool. So, if you are installing
a tool that the script uses with Conan, then you will have to load the environment variables before calling the tool. This is actually the original motivation
for the module.

It is not very sophisticated yet, only simple variable declarations are supported right now (for examples, Bash's $VAR style variable expansion is not supported, only ${VAR}).

## Features

- TODO

## Requirements

- TODO

## Installation

You can install _Environ Loader_ via [pip] from [PyPI]:

```console
$ pip install environ-loader
```

## License

Distributed under the terms of the [MIT license][license],
_Environ Loader_ is free and open source software.

