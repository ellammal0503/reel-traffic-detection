from setuptools import setup, find_packages

setup(
    name="reel-traffic-detection",
    version="0.1.0",
    description="Real-time Detection of Reel vs Non-Reel Traffic in Social Networking Applications",
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/yourusername/reel-traffic-detection",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "scikit-learn",
        "pandas",
        "numpy",
        "joblib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
