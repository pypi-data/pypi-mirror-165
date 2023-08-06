from setuptools import setup
import setuptools

required = ["cloudpickle==1.6.0",
"joblib==1.1.0",
"llvmlite==0.39.0",
"numba==0.56.0",
"numpy==1.21.6",
"packaging==21.3",
"pandas==1.3.5",
"pyparsing==3.0.9",
"python-dateutil==2.8.2",
"pytz==2022.1",
"scikit-learn==1.0.2",
"scipy==1.7.3",
"shap==0.41.0",
"six==1.16.0",
"slicer==0.0.7",
"threadpoolctl==3.1.0",
"tqdm==4.64.0",
"jedi==0.18.1"
]
setup(
  name='censius_explain',
  version='0.0.4',
  description='package for finding explainability_values from censius.ai',
  long_description='',
  package_data={'': ['.env']},
  long_description_content_type='text/markdown',
  install_requires=required,
  url="https://github.com/Censius/censius-explain.git",
  author="Censius",
  author_email="dev@censius.ai",
  packages=['censius_explain'],
  keywords=[],
  include_package_data=True,
  zip_safe=False
)