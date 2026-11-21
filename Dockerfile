# Entorno reproducible para ejecutar KineSIM y sus notebooks en JupyterLab.
FROM python:3.11-slim

ARG USER_ID=1000
ARG GROUP_ID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Usuario no privilegiado. Construye con UID/GID del usuario anfitrión para
# facilitar la escritura en carpetas montadas desde Linux.
RUN groupadd --gid "${GROUP_ID}" pmsuser \
    && useradd --uid "${USER_ID}" --gid "${GROUP_ID}" \
       --create-home --shell /bin/bash pmsuser

WORKDIR /workspace

COPY --chown=pmsuser:pmsuser pyproject.toml README.md LICENSE requirements.txt ./
COPY --chown=pmsuser:pmsuser src/ ./src/
COPY --chown=pmsuser:pmsuser notebooks/ ./notebooks/

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt \
    && chown -R "${USER_ID}:${GROUP_ID}" /workspace

USER pmsuser
ENV HOME=/home/pmsuser

EXPOSE 8888

# Jupyter conserva su autenticación por token y genera uno automáticamente.
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.root_dir=/workspace", "--ServerApp.allow_remote_access=True"]
