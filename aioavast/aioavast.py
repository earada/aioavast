#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio


class Avast():

    def __init__(self):
        self.connected = False

    @asyncio.coroutine
    def connect(self, sock="/var/run/avast/scan.sock"):
        self.r, self.w = yield from asyncio.open_unix_connection(sock)
        self.connected = True

        # Clean banner
        yield from self.r.readline()

    @asyncio.coroutine
    def scan(self, fname):
        message = "SCAN {}\n".format(fname)
        self.w.write(message.encode())
        yield from self.w.drain()

        analysis = {}
        while True:
            data = yield from self.r.readline()
            data = data.decode().strip()
            if data == "200 SCAN OK":
                return analysis
            elif data == "210 SCAN DATA":
                continue
            elif data.startswith("SCAN"):
                if data[len(fname) + 7] == "+":  # OK FILE
                    analysis[fname] = False
                elif data[len(fname) + 7] == "E":  # OK FILE
                    analysis[fname] = "EXCLUDED"
                elif data[len(fname) + 7] == "L":  # Detected
                    analysis[fname] = data[len(fname) + 15:]
            else:
                return None

    @asyncio.coroutine
    def checkurl(self, url):
        message = "CHECKURL {}\n".format(url)
        self.w.write(message.encode())
        yield from self.w.drain()

        analysis = {}
        data = yield from self.r.readline()
        data = data.decode().strip()
        if data == "200 CHECKURL OK":
            return True
        return False

    @asyncio.coroutine
    def exclude(self, fname=None):
        message = "EXCLUDE {}\n".format(fname) if fname else "EXCLUDE\n"
        self.w.write(message.encode())
        yield from self.w.drain()

        names = []
        while True:
            data = yield from self.r.readline()
            data = data.decode().strip()
            if data == "200 EXCLUDE OK":
                return names
            elif data == "210 EXCLUDE DATA":
                continue
            elif data.startswith("EXCLUDE"):
                names.append(data[8:])
            else:
                return None

    @asyncio.coroutine
    def flags(self, items=None):
        message = "FLAGS {}\n".format(items) if items else "FLAGS\n"
        self.w.write(message.encode())
        yield from self.w.drain()

        _ = yield from self.r.readline()
        data = yield from self.r.readline()
        data = data.decode().strip()[6:].split()
        _ = yield from self.r.readline()
        flags = {}
        for item in data:
            flags[item[1:]] = True if item[0] == "+" else False
        return flags

    @asyncio.coroutine
    def pack(self, items=None):
        message = "PACK {}\n".format(items) if items else "PACK\n"
        self.w.write(message.encode())
        yield from self.w.drain()

        _ = yield from self.r.readline()
        data = yield from self.r.readline()
        data = data.decode().strip()[5:].split()
        _ = yield from self.r.readline()
        pack = {}
        for item in data:
            pack[item[1:]] = True if item[0] == "+" else False
        return pack

    def disconnect(self):
        if self.w:
            self.w.close()
        self.connected = False

    def __del__(self):
        if self.connected:
            self.w.close()
