import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    fh.close()

setuptools.setup(
    name="adamix_gpt2",
    version="0.0.1",
    author="Sahaj Agarwal",
    author_email="sahagar@microsoft.com",
    description="PyTorch implementation of low-rank adaptation (LoRA) and Adamix, a parameter-efficient approach to adapt a large pre-trained deep learning model which obtains performance better than full fine-tuning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/microsoft/AdaMix",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    dependency_links=[
        "https://download.pytorch.org/whl/torch_stable.html",
    ],
    install_requires=[
        "transformers==3.3.1",
        "spacy",
        "tqdm",
        "tensorboard",
        "progress",
        "loralib==0.1.1"
    ],
    keywords=['python', 'adamix' , 'peft']
)