from distutils.core import setup


setup(
  name = 'Multiple_Rotor_Enigma',         # How you named your package folder (MyLib)
  packages = ['Multiple_Rotor_Enigma'],   # Chose the same as "name"
  version = '0.2.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'An enhanced simulation of the enigma machine',
  
  author = 'Aradhya Goel',                   # Type in your name
  author_email = 'aradhyagnov@gmail.com',      # Type in your E-Mail   # I explain this later on
  keywords = ['Enigma'],   # Keywords that define your package best

  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
  ],
)