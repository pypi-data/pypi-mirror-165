import setuptools

import signup


def ensure_plain_text(file: str):
    with open(file, 'rt', encoding='utf-8') as fp:
        return fp.read()


setuptools.setup(
    name='anstu_sign_up',
    author='uncle_hoshino',
    author_email='hgenaaaa@gmail.com',
    version=signup.__version__,
    description='a simple script to deal with daily sign-up in AHSTU',
    long_description=ensure_plain_text("README.md"),
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/NoSimpleApple/ahstu_sign_up',
    python_requires='>=3.10',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
    packages=['signup'],
    data_files=[('', ["README.md", "help.txt", "conf/.template", "sign_up.cmd"])],
    include_package_data=True,
    package_dir={"signup": "signup"},
    zip_safe=False,
    entry_points={
        'signup': ['_ = signup.signup:main']
    }
)
