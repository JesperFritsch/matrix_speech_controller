# matrix_speech_controller
This is a project for controlling an application of home_led_matrix

https://github.com/alphacep/vosk is used for speech recognition

the idea is to use open AIs function calling API, although it is not bound to use open AI, im sure one can get this to work
with another AI provider. the backend works with an interface ILLMAgent, and the class for handling communication with open ai implements this interface.

to run it just clone the repo and run pip install in some venv.