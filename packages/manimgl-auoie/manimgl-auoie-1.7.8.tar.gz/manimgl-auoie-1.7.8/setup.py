# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manimlib',
 'manimlib.animation',
 'manimlib.camera',
 'manimlib.event_handler',
 'manimlib.mobject',
 'manimlib.mobject.svg',
 'manimlib.mobject.types',
 'manimlib.once_useful_constructs',
 'manimlib.scene',
 'manimlib.utils']

package_data = \
{'': ['*'],
 'manimlib': ['shaders/*',
              'shaders/image/*',
              'shaders/inserts/*',
              'shaders/mandelbrot_fractal/*',
              'shaders/newton_fractal/*',
              'shaders/quadratic_bezier_fill/*',
              'shaders/quadratic_bezier_stroke/*',
              'shaders/surface/*',
              'shaders/textured_surface/*',
              'shaders/true_dot/*',
              'tex_templates/*']}

install_requires = \
['ManimPango>=0.4.1,<0.5.0',
 'Pillow>=9.2.0,<10.0.0',
 'PyOpenGL>=3.1.6,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'Pygments>=2.13.0,<3.0.0',
 'colour>=0.1.5,<0.2.0',
 'ipython>=8.4.0,<9.0.0',
 'isosurfaces>=0.1.0,<0.2.0',
 'mapbox-earcut>=1.0.0,<2.0.0',
 'matplotlib>=3.5.3,<4.0.0',
 'moderngl-window>=2.4.1,<3.0.0',
 'moderngl>=5.6.4,<6.0.0',
 'numpy>=1.23.2,<2.0.0',
 'pydub>=0.25.1,<0.26.0',
 'pyperclip>=1.8.2,<2.0.0',
 'rich>=12.5.1,<13.0.0',
 'scipy>=1.9.0,<2.0.0',
 'screeninfo>=0.8,<0.9',
 'skia-pathops>=0.7.2,<0.8.0',
 'svgelements>=1.7.2,<2.0.0',
 'sympy>=1.11,<2.0',
 'tqdm>=4.64.0,<5.0.0',
 'validators>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['manim-render = manimlib.__main__:main',
                     'manimgl = manimlib.__main__:main']}

setup_kwargs = {
    'name': 'manimgl-auoie',
    'version': '1.7.8',
    'description': 'Animation engine for explanatory math videos',
    'long_description': None,
    'author': '3b1b',
    'author_email': 'grant@3blue1brown.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/auoie/manim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
