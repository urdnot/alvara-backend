@echo off
call docker run -d^
                --name alvara^
                --mount type=volume,source=artifacts,destination=/usr/alvara^
                -p 8080:8080^
                backend