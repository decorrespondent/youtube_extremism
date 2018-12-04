from setuptools import setup, find_packages

setup(name="youtubecollector",
      version=0.1,
      description="Module for getting data from youtube",
      url="https://github.com/CorrespondentData/YouTubeExtremism",
      author="The Correspondent",
      packages=find_packages('youtubecollector'),
      package_dir={"": "src"},
      install_requires=[
          "pandas",
          "numpy",
          "youtube_dl",
          "google-api-python-client",
          "webvtt-py",
          "jupyter",
          "requests"
      ])
