FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends git ca-certificates build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip setuptools wheel

WORKDIR /ws

RUN git clone https://github.com/sunpy/sunpy.git sunpy && \
    cd sunpy && \
    git fetch --all --tags --prune && \
    git checkout a1a081a && \
    rm pytest.ini

RUN python -m pip install --prefer-binary numpy astropy pandas matplotlib scipy pyerfa pytest

RUN python -m pip install -e /ws/sunpy

CMD ["bash"]

# docker build -t sunpy-test .

# docker run --rm sunpy-test pytest /ws/sunpy/sunpy/time/tests/test_time.py

# Este Dockerfile usa la imagen base python:3.12-slim para mantenerlo ligero. Configuro variables de entorno para que Python imprima directamente y pip no guarde caché.

#Instalo solo lo necesario del sistema: git para clonar el repo y ca-certificates para conexiones seguras.

#Actualizo pip, setuptools y wheel para evitar problemas al instalar dependencias. Luego clono el repositorio de SunPy en /opt/sunpy y hago checkout al commit exacto que pide la evaluación.

#Después instalo dependencias como numpy, astropy, scipy, pandas y matplotlib usando --prefer-binary para acelerar la instalación, y también instalo pytest para correr las pruebas.

#Finalmente, instalo SunPy desde la fuente en modo editable. El contenedor queda listo para ejecutar pruebas con pytest, aunque por defecto abre un bash.

#En pocas palabras: prepara un entorno limpio y ligero que instala SunPy desde el código fuente en un commit específico y lo deja listo para correr las pruebas requeridas."""

# english

#This Dockerfile starts from python:3.12-slim to keep it lightweight. I set environment variables so Python prints directly to the console and pip doesn’t use cache.

#I install only the essentials: git to clone the repository and ca-certificates for secure connections.

#Then I upgrade pip, setuptools, and wheel to avoid installation issues. After that, I clone the SunPy repo into /opt/sunpy and checkout the exact commit required for the assessment.

#Next, I install dependencies like numpy, astropy, scipy, pandas, and matplotlib with --prefer-binary to speed things up, and also add pytest so we can run tests.

#Finally, I install SunPy from source in editable mode. The container is ready to run the required tests with pytest, although by default it just opens a bash shell.

#In short: it sets up a clean and lightweight environment, installs SunPy from the source at the right commit, and makes sure everything is ready for testing.