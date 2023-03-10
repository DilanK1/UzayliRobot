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
         (os.path.join('share', package_name+'/my_robot'), glob('my_robot/*.py')), 
        (os.path.join('share', package_name+'/launch'), glob('launch/*.py')), 
        (os.path.join('share',package_name+'/urdf'),glob('urdf/*')),
        (os.path.join('share',package_name+'/rviz'),glob('rviz/*')),  
        (os.path.join('share',package_name+'/world'),glob('world/*')),    
        (os.path.join('share',package_name+'/config'),glob('config/*')),                    
        (os.path.join('share',package_name+'/maps'),glob('maps/*')),                 
        (os.path.join('share',package_name+'/models/amr_mini'),glob('models/amr_mini/*')),  
        (os.path.join('share',package_name+'/models/new_walls'),glob('models/new_walls/*')),  

        (os.path.join('share', package_name+'/urdf_amr'),
         glob('urdf_amr/*.xacro')),
        (os.path.join('share', package_name+'/urdf_amr'),
         glob('urdf_amr/*.urdf')),
        (os.path.join('share',package_name+'/urdf_amr/urdf_include'),glob('urdf_amr/urdf_include/*')),  
        (os.path.join('share', package_name+'/AmrMini_models/Amr_mini/meshes'),
         glob('AmrMini_models/Amr_mini/meshes/*')),   
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
                'initialpose_pub=my_robot.initialpose:main',
                'goalpose_pub=my_robot.goal_pose:main',
        ],
    },
)
