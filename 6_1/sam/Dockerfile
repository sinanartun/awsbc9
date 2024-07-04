# Stage 1: Build environment
FROM python:3.12-slim as builder

# Install required system packages
RUN apt-get update && apt-get install -y wget git ffmpeg libsndfile1 gcc

# Install Rust (needed for some Python packages)
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Set environment variables for Rust
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy requirements.txt first, to leverage Docker cache
COPY requirements.txt ./

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Manually install torch
RUN pip install torch -f https://download.pytorch.org/whl/torch_stable.html

# Download the Whisper model during the build process
RUN python -c "import whisper; whisper.load_model('small')"

# Stage 2: Deployment environment
FROM public.ecr.aws/lambda/python:3.12

# Copy the installed packages from the build environment
COPY --from=builder /usr/local/lib/python3.12/site-packages /opt/python/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Set environment variables to disable CUDA
ENV TORCH_CUDA_ARCH_LIST=""
ENV FORCE_CPU="1"
ENV USE_CUDA="0"

# Set the CMD to your handler
CMD ["app.handler"]
