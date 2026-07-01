FROM python:3.11-slim

# Set up a non-root user (Best practice for Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Switch back to root to install system dependencies
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Switch back to the non-root user
USER user

# Copy requirements file
COPY --chown=user requirements.txt .

# Install CPU-only PyTorch to save space and prevent timeouts
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install the python libraries from requirements
RUN pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt

# FIX: Force upgrade transformers and tokenizers to compatible versions
RUN pip install -U transformers tokenizers

# Copy all project files
COPY --chown=user . .

# Expose Hugging Face Spaces port
EXPOSE 7860

# FIX: Added --server.enableXsrfProtection=false to allow file uploads in Hugging Face iframes
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]