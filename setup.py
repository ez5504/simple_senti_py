# Copyright 2016 Jacob Taylor - Idkoru Technologies

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#from distutils.core import setup
from setuptools import setup
setup(
  name = 'simple_senti_py',
  packages = ['simple_senti_py'], # this must be the same as the name above
  version = '0.1',
  description = 'A simple Sentiment Analysis library',
  author = 'Jacob Taylor',
  author_email = 'ez5504@gmail.com',
  url = 'https://github.com/ez5504/simple_senti_py', # use the URL to the github repo
  download_url = 'https://github.com/ez5504/simple_senti_py/tarball/0.1', # I'll explain this in a second
  keywords = ['sentiment', 'analysis', 'nlp'], # arbitrary keywords
  classifiers = [],
)