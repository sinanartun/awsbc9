# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.12

# Install necessary tools
RUN dnf install -y tar gzip xz git

# Download and install a static build of ffmpeg for the appropriate architecture
RUN curl -L https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz -o /tmp/ffmpeg.tar.xz \
    && mkdir -p /tmp/ffmpeg \
    && tar -xf /tmp/ffmpeg.tar.xz -C /tmp/ffmpeg --strip-components=1 \
    && mv /tmp/ffmpeg/ffmpeg /usr/local/bin/ \
    && mv /tmp/ffmpeg/ffprobe /usr/local/bin/ \
    && rm -rf /tmp/ffmpeg* \
    && chmod +x /usr/local/bin/ffmpeg \
    && chmod +x /usr/local/bin/ffprobe

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Install the necessary Python dependencies
RUN pip install boto3

# Set the CMD to your handler
CMD ["lambda_function.lambda_handler"]
