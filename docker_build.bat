@echo off
call docker volume create --name artifacts
call docker build --rm -t backend .