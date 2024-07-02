# Use an official Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.12

# Install required system packages
RUN dnf -y install wget git

# Install required Python packages
RUN pip install torch boto3

# Install Whisper from GitHub
RUN pip install git+https://github.com/openai/whisper.git

# Copy the function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD ["app.handler"]
