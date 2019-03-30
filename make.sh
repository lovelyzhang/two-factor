#!/usr/bin/env bash
set -e
rm -rf build && mkdir build && cd build && cmake .. && make && sudo cp lib2ndfactor* /lib/security
cd .. && cd auth_server/db && rm -rf auth.db && sqlite3 auth.db  < db.sql