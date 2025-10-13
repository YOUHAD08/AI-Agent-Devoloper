from setuptools import setup, find_packages

setup(
    name="agent-framework",
    version="0.1.0",
    description="A flexible AI agent framework with GAME architecture",
    author="Ayoub Youhad",
    author_email="yo_ayoub@etu.enset-media.ac.ma",
    packages=find_packages(),
    install_requires=[
        # Core LLM functionality
        'litellm>=1.77.0',
        'openai>=1.0.0',
        
        # Configuration
        'python-dotenv>=1.0.0',
        
        # Async support (if litellm needs it)
        'aiohttp>=3.12.0',
        
        # Data validation
        'pydantic>=2.0.0',
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
