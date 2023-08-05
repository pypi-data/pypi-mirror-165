import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chaos_maps",
    version="0.1.2",
    author="Dr. Ioannis Kafetzis",
    author_email="ioanniskaf@gmail.com",
    description="A package for studying and visualizing the dynamical behavior of chaotic maps",
    long_description=long_description,
    keywords = "chaotic maps bifurcations Lyapunov exponents",
    licence = "MIT",
    long_description_content_type="text/markdown",
    url="https://github.com/iokaf/discrete_chaos",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['chaos_maps', 'chaos_maps.plotting'],
    install_requires = [
    "numpy",
    "matplotlib"
    ],
    python_requires=">=3.6",
)
