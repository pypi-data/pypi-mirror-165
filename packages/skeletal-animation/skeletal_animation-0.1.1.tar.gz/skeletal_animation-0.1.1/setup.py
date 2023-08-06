from setuptools import setup, find_packages

setup(name='skeletal_animation',
      version='0.1.1',
      description='Standalone package for skeletal animation',
      long_description="# This is a work in progrees",
      long_description_content_type='text/markdown',
      url='https://gitlab-etu.ing.he-arc.ch/isc/2021-22/niveau-3/tb-iscdlm/226/tb-animation-squelettale',
      author='Dimitri "Kerzoum" Kohler',
      author_email='dimitri.kohler@he-arc.ch',      
      license='MIT',
      classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Multimedia :: Graphics',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 3.7'
            ],
      packages=find_packages(),
      package_data={
            'skeletal_animation': ['animated_models/*.pkl', 'examples/*', 'gui/*', 'gui/assets/shaders/*.glsl'],
      },
      include_package_data=True,
)