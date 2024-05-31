# Testing

Saint Michel Annecy, IT Campus, testing for L3 CSI and Master MS2D.
It covers many aspects of modern software testing, from unit tests to, integration test, embedded development testing,
etc

## Official skills to acquire

* Savoir développer et mettre en place des tests unitaires sur une application
* Savoir développer et mettre en place des tests d’intégration sur une application
* Savoir configurer un pipeline d’intégration continue sur une application

## The official program

1. Les tests unitaires
    * Qu’est-ce qu’un test ?
    * Les tests unitaires
    * Les bonnes pratiques
    * Le Test Driven Development
    * Le code coverage
    * Tests avec langage naturel

2. Les tests d’intégrations
    * Les tests d’intégration
    * Le fonctionnement
    * Les bonnes pratiques

3. L’intégration continue
    * Mise en place d’une plateforme d’intégration continue (GitLab CI)
    * Conteneurisation d’une application (API)
    * Configuration d’un pipeline de tests

## Testing using Pytest

Pytest means Python, it's a framework to test Python using Python.
First create a virtual environment.

```bash
python3 -m venv venv
```

Then activate it.

```bash
source venv/bin/activate
```

Then install pytest and other dependencies of that project.

```bash
pip install -r requirements.txt
```

Running the tests.

```bash
pytest
```

## Embedded development testing

A piece of code can test another piece of code from the same project.
But testing can be performed through a more abstract protocol, radio, serial, etc.
The goal of those tests is to discover a very cheap microcontroller, the ATMega328P,
and its development environment, the Arduino one.
It highlights the differences between the Arduino framework and its simple MCU
and our modern desktop environment looking at various aspects such as arithmetic precision
and memory management.

### Arduino

Development will be made under VSCode using Arduino plugin to access copilot
and easily develop the embedded software and Arduino IDE to have the full set of
options of the Arduino environment. See
the [IDE installation procedure on the Arduino website](https://support.arduino.cc/hc/en-us/articles/360019833020-Download-and-install-Arduino-IDE).

Open the `arduino/arduino.ino` file with Arduino IDE and upload it to the board.
At the point the test `test_arduino.py` should pass.

## Installation

Pytest means Python, it's a framework to test Python using Python.
First create a virtual environment.

```bash
python3 -m venv venv
```

Then activate it.

```bash
source venv/bin/activate
```

Then install pytest and other dependencies of that project.

```bash
pip install -r requirements.txt
```

## Build the documentation

This README is just a help, the complete documentation is available in the `doc` folder as a LaTex source.
To build it to a PDF it required `LuaLaTex`.
Dependencies can be installed on Ubuntu with the following command :

```bash
sudo apt install sudo apt install texlive-luatex texlive-latex-base texlive-latex-recommended texlive-pictures texlive-latex-extra fonts-ebgaramond
```

Then build the PDF documentation :

```bash
/usr/bin/bash compile-latex.sh
```

To compress the PDF, install `ghostscript` :

 ```bash
 sudo apt install ghostscript
 ```

And run the following command :

```bash
/usr/bin/bash compress-pdf.sh
```

To compress images, install `pngcrush` and `jpegoptim` using the following command :

```bash
sudo apt install pngcrush jpegoptim
```

Then run the following command :

```bash
/usr/bin/bash compress-image.sh
```

Check the LaTex syntax in an active virtual environment :

```bash
/usr/bin/bash checkmytex.sh
```