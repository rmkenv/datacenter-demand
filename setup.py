from setuptools import setup

setup(
    name="datacenter-demand",
    version="1.0.0",
    author="Research Team",
    description="US Datacenter Power Demand Estimation Algorithm",
    install_requires=[l.strip() for l in open("requirements.txt") if l and not l.startswith("#")],
    packages=[],
    py_modules=['datacenter_power_predictor', 'data_utils', 'train_models', 'dcpower', 'visualization_utils'],
    entry_points={
        "console_scripts": ["dcpower=dcpower:cli"]
    }
)
