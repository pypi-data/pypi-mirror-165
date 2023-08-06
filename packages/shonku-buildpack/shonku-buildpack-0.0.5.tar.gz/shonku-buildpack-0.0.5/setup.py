from setuptools import setup

setup(
    name='shonku-buildpack',
    version='0.0.5',    
    description='Buildpack for shonku',
    # url='https://github.com/shuds13/pyexample',
    author='Shafin Hasnat',
    author_email='shafinhasnat97@gmail.com',
    license='BSD 2-clause',
    packages=['.'],
    # install_requires=['mpi4py>=2.0',
    #                   'numpy',                     
    #                   ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)