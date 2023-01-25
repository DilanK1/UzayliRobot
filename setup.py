from setuptools import setup
import os
from glob import glob

package_name = 'my_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    package_data={'my_robot': ['launch/*.launch.py']},
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name+'/launch'), glob('launch/*.py')), 
        (os.path.join('share',package_name+'/urdf'),glob('urdf/*')),
        (os.path.join('share',package_name+'/rviz'),glob('rviz/*')),  
        (os.path.join('share',package_name+'/world'),glob('world/*')),                      
        (os.path.join('share',package_name+'config'),glob('config/*'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dilan',
    maintainer_email='74790204+DilanK1@users.noreply.github.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
