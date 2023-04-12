# AI-Theremin

AI Theremin is a funny application which uses hand tracking to simulate a musical instrument called the theremin.

![](https://cdn.discordapp.com/attachments/941779514860666951/1095748665601163294/ezgif.com-optimize.gif)

## Features
Left hand detection for volume control
Right hand detection for frequency control
Real-time display of hand coordinates, frequency, and volume
Real-time sound generation based on hand position

## Installation

1. Clone this repository:

```bash
https://github.com/AnodeGrindYo/DiffusionModels
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## usage

Run the `main.py` file to start the application:

```bash
python main.py
```

Place your hands in front of the webcam to interact with the virtual theremin. Move your left hand vertically to control the volume and your right hand vertically to control the frequency.

## Contributing
I'd be excited to receive contributions from the community! 

## License
This project is licensed under the MIT License. For more information, please see the LICENSE file.

Feel free to provide suggestions and contribute to this project. Together, we can create an even better virtual theremin experience!

## Todo 
- Improve sound quality
- Improve user interface
  - add a tuner to know which note is played
  - add a scale choser which adds lines on the video were are the notes of the scale
  - add other oscillator shapes with a selector

And maybe later :
- recode it in C++ with JUCE to make a VST