# Blazer

A gui to track progress on anything - such as revision, in a way to provide maximum customisation options to make it your own
Designed to guilt trip you and keep you addicted to keeping up your productivity steak, with full customisibility
File selection is kinda ugly, sorry about that had to use tkinter cos pygame dosent work as well for it 
Currently only linux compatible, if theres demmand for whatever reason and someone actually good at coding cant be bothered to make a better 
version there will be compatibility updates for mac and windows
## Install
```bash
# Recommended
pipx install git+https://github.com/demtellme/Blazer.git

# Or with pip
pip install --user git+https://github.com/demtellme/Blazer.git
```

## Uninstall
```bash
pipx uninstall Blazer
```

## Usage
```bash
blzr # runs the program
```

# Customisation
Go into `config.json`, under the `USER` section, select the options you want to use for your Blazer app

*For example*: 

```json
//one of my prefered setups
  "USER": {
    "colourscheme": "forest",   // Changing forest -> ocean to change the base pallet to be more blue
    "background": "dark23",     // Changing dark23 -> solarized to change the background
    "font": "notoserif",        // you probably get it by now
    "fontsize": 40              // There arent presets for font size so you can change it yourself
  },
```



# Boring documentatation for nerds
###### Dont get offended, you gotta be a certain level of nerd to wanna know how a specific program works
## Getting the configuration for user's customisations

The config is stored as a `.json` file,
This is so there can be set presets without them needing to be hardcoded into the python, 
personally id much rather edit a json than a python file for customisation

so in python we need to
```python
import os
import json

CONF = os.path.join(os.path.dirname(__file__), 'config.json')
# bunch of code
 
with open(CONF, "r") as f:
    config = json.load(f)

userconfig = config['USER']

COLOURS = tuple(config['colourschemes'][userconfig['colourscheme']]) # example of data gotten from USER
# bunch of code 
```
The `CONF = [...]` line is to make sure were using the right config file, in the same folder as the program
The data from that file is then saved as `config` using the json library
Then the part we actually care about, `USER` is set as `userconfig` which is a list of the user choices.

```python
tuple() 
```
is used for making the list into an array () that is needed for certain pygame features () 

The code then finds the user `colourscheme` in the `colourschemes` part of the json file and reads the list of colours as arrays
A similar process is used for all the other parts of the user's config

## The user interface

Blazer uses `pygame` as a gui, there are much better ways im sure but oh well
To display the main user iterface the program uses 
```python
#functions already defined earlier in the code
 if state == 'home':
            dipslayhomescreen()
elif state == 'commitscreen':
    displaycommitscreen()
```
this checks what state the gui should be in and renders it appropriatley
to display actual ui elements the functions use rectangles and text with functions:
```python
def square(x, y, width, height, colour, border_radius):
    pygame.draw.rect(screen, colour, (x, y, width, height), border_radius=border_radius)

def text(font, text, colour):
    return font.render(text, True, colour)
```
These functions make creating ui elements easier, for example:
```python
def displaycommitscreen():
    square(40, 30, 200, 40, BGSECONDARY, 5)
    square(40, 90, 560, 120, BGSECONDARY, 5)
    screen.blit(text(FONT, "Message:", MID), (50, 27))

    square(40, 230, 175, 40, BGSECONDARY, 5)
    square(40, 290, 560, 120, BGSECONDARY, 5)
    screen.blit(text(FONT, "Files:", MID), (50, 228))

    square(232, 500, 175, 45, DARK, 5)
    screen.blit(text(FONT, "COMMIT", MID), (240, 500))
    ...
```
