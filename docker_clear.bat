@echo off
call docker stop alvara
call docker rm alvara
call docker image rm backend
call docker volume rm artifacts