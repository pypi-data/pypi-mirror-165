# TelamonApi

TelamonApi is a python package to scan ports with just 2 lines of code.

## Installation
pip install TelamonApi

## Usage
from TelamonApi import telamon

A)
port = 80
telamon.scan("example.com", port)

B)

minport = 79
maxport = 999
telamon.scanmulti("example.com", minport, maxport)

C)

telamon.scanall("example.com")

