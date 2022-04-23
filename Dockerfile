FROM python:3.10-alpine3.14
LABEL maintainer="arhimed@alvara.io"
RUN apk add gcc musl-dev
RUN pip install pillow aiohttp web3
WORKDIR /usr/alvara
COPY alvara_assets ./alvara_assets/
COPY AlvaraStorage.json artifacts_keeper.py async_server.py image_mixer.py meta_generator.py settings.json smart_client.py token_state.py utils.py ./
ENTRYPOINT ["python", "async_server.py"]
EXPOSE 8080