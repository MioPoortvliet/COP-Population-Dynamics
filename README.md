# COP-Population-Dynamics
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
 
Contributors: Jonah Post, Mio Poortvliet, Iliya Bolotov

## How to run

Run main.py to run the animation.

If you don't want to execute from main.py, you need to specify your working directory to be the same as the root folder (```COP-Population-Dynamics```).

### Why is this project structured like this?

We intended to write a general evolution engine that will accept any static (food) and dynamic (animal) objects. This is why the project is structured like a library and is intended to be used by importing ```AnimalEvolution``` from ```population_dynamics.py```. Then you feed it your own food and animals, similar to how we feed it the classes from ```src/animals.py``` in the example ```examples/graphs.py```. 

## Features

- Population model simulation engine.
- Carrots, Rabbits and Foxes as an example.
- Supports evolution of a species.
- Create custom animals or food with custom behaviour and interactions.

## Dependencies

- Numpy
- Matplotlib
- Numba
- PyQt5

## Important files

- ```src/population_dynamics.py``` contains the structure of the playing field.
- ```src/animals``` contains class structure (```Entity```, ```Animal```) and specifically ```Carrot```, ```Rabbit``` and ```Fox```.
- Examples can be found in the examples folder. 
- You can process data using ```src/analysis.py```.
## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/MioPoortvliet"><img src="https://avatars.githubusercontent.com/u/6685801?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Mio Poortvliet</b></sub></a><br /><a href="https://github.com/I-Atlas/COP-Population-Dynamics/commits?author=MioPoortvliet" title="Code">💻</a> <a href="#data-MioPoortvliet" title="Data">🔣</a> <a href="https://github.com/I-Atlas/COP-Population-Dynamics/commits?author=MioPoortvliet" title="Documentation">📖</a> <a href="#example-MioPoortvliet" title="Examples">💡</a> <a href="#maintenance-MioPoortvliet" title="Maintenance">🚧</a> <a href="#tool-MioPoortvliet" title="Tools">🔧</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!