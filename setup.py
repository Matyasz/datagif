from pathlib import Path

from setuptools import setup, find_packages


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    src_dir = base_dir / 'src'

    about = {}
    with (src_dir / "datagif" / "__about__.py").open() as f:
        exec(f.read(), about)

    with (base_dir / "README.rst").open() as f:
        long_description = f.read()

    install_requirements = [
        'imageio',
        'pandas',
        'seaborn',
        'matplotlib'
    ]

    interactive_requirements = [
        'IPython',
        'jupyter'
    ]

    test_requirements = [

    ]

    doc_requirements = [

    ]

    setup(
        name=about['__title__'],
        version=about['__version__'],

        description=about['__summary__'],
        long_description=long_description,
        license=about['__license__'],
        url=about["__uri__"],

        author=about["__author__"],
        author_email=about["__email__"],

        package_dir={'': 'src'},
        packages=find_packages(where='src'),
        include_package_data=True,

        install_requires=install_requirements,
        tests_require=test_requirements,
        extras_require={
            'docs': doc_requirements,
            'test': test_requirements,
            'interactive': interactive_requirements,
            'dev': doc_requirements + test_requirements + interactive_requirements,
        },

        zip_safe=False,

        classifiers=[
            "Development Status :: 3 - Alpha",
            "Framework :: Flake8",
            "Framework :: Matplotlib",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Natural Language :: English",
            "Environment :: MacOS X",
            "Operating System :: POSIX",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Microsoft :: Windows",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Topic :: Artistic Software",
            "Topic :: Multimedia",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Visualization",
            "Topic :: Software Development :: Libraries"
        ],

        keywords=[
            'python', 'data', "science", 'data science', 'animated', 'gif',
            'matplotlib', 'seaborn', 'imageio'
        ]
    )
