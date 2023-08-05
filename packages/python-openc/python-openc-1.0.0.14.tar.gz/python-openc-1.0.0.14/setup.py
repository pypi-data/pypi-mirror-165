import io
import os
import os.path
import setuptools
# import skbuild
# from skbuild import cmaker


def main():
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))

    long_description = io.open("README.md", encoding="utf-8").read()
    version = "1.0.0.14"

    setuptools.setup(
        name="python-openc",
        version=version,
        url="https://github.com/opencv/opencv-python",
        license="MIT",
        description="Wrapper package for OpenCV python bindings.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        # packages=packages,
        # package_data=package_data,
        maintainer="OpenCV Team",
        # ext_modules=EmptyListWithLength(),
        install_requires="opencv-python",
        python_requires=">=3.6",
        classifiers=[
            # "Development Status :: 5 - Production/Stable",
            # "Environment :: Console",
            # "Intended Audience :: Developers",
            # "Intended Audience :: Education",
            # "Intended Audience :: Information Technology",
            # "Intended Audience :: Science/Research",
            # "License :: OSI Approved :: MIT License",
            # "Operating System :: MacOS",
            # "Operating System :: Microsoft :: Windows",
            # "Operating System :: POSIX",
            # "Operating System :: Unix",
            # "Programming Language :: Python",
            # "Programming Language :: Python :: 3",
            # "Programming Language :: Python :: 3 :: Only",
            # "Programming Language :: Python :: 3.6",
            # "Programming Language :: Python :: 3.7",
            # "Programming Language :: Python :: 3.8",
            # "Programming Language :: Python :: 3.9",
            # "Programming Language :: Python :: 3.10",
            # "Programming Language :: C++",
            # "Programming Language :: Python :: Implementation :: CPython",
            # "Topic :: Scientific/Engineering",
            # "Topic :: Scientific/Engineering :: Image Recognition",
            # "Topic :: Software Development",
        ],
    )


if __name__ == "__main__":
    main()
