language: python

python:
    - 3.6
    - nightly

# install dependencies
install:
    - pip install -r requirements.txt

script:
    - pytest  # run tests
    - gunicorn manage:app
