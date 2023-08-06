from distutils.core import setup
import setuptools
# from setuptools import find_packages

setup(name='faCRSA',  # 包名
      version='1.0.4',  # 版本号
      description='faCRSA',
      long_description="An automated analysis pipeline for crop root phenotyping.",
      author='Ruinan Zhang',
      author_email='hellozrn9@gmail.com',
      url='https://zrn0.top/',
      install_requires=['Flask==1.1.4', 'huey==2.4.3', 'numpy==1.19.2', 'opencv_python==4.6.0.66',
                        'pandas==0.24.0', 'Pillow==8.4.0', 'scikit_image==0.17.2', 'tensorflow==2.4.0', 'yagmail==0.15.277', 'python-dotenv==0.20.0', 'pyparsing==2.4.7'],
      license='MIT License',
      packages=['faCRSA', 'faCRSA.facrsa_code', 'faCRSA.facrsa_code.library', 'faCRSA.facrsa_code.static', 'faCRSA.facrsa_code.templates', 'faCRSA.facrsa_code.library.analysis', 'faCRSA.facrsa_code.library.util',
                'faCRSA.facrsa_code.library.web', 'faCRSA.facrsa_code.library.analysis.database', 'faCRSA.facrsa_code.library.analysis.net', 'faCRSA.facrsa_code.library.analysis.net.rootseg.weight'],
      entry_points={
          'console_scripts': ['facrsa-web=faCRSA.start_web:start_web', 'facrsa-queue=faCRSA.start_queue:start_queue'],
      },
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      include_package_data=True
      )
