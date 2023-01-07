# Code for the Optical Bottle Beam

This repo includes the code to process and analyse the data for the Optical Bottle Beam experiment. Here we are going to present:


* Image processing methodologies to extract and track a Silica microparticle in a .mp4 video.
* Statistical tools to analyse gaussianity (Kolmogorov-Smirnov test) in the data.
* Functions to calculate Kullback-Leibler divergece between simulation and experiment, allowing to find which value of NA (Numerical Aberture) better fits the one in the experimental setup.
* Potential analysis. Here, from the probability distributions encountered of the microparticle center of mass coordinates, a `curve_fit` is executed considering a quartic potential. The fit results in the extraction of the following constants: $k_\rho$, $k_z$ and $k_{\rho,z}$. These parameters allow the reconstruction of the potential and provide useful insights regarding the optical trap.

## Installation

Well, now, how you can run this code? Follow the next steps.

1. First clone this repo in your computer. This can be done:
    * Via SSH:

    ```bash
    git clone https://github.com/QuantumAdventures/optical-bottle-beam.git
    ```

    * Via HTTPS:

    ```bash
    git clone git@github.com:QuantumAdventures/optical-bottle-beam.git
    ```

    * Or, by downloading the .zip of the repo.

2. Install the requirements, this is will set the libraries used in your computer. Inside the main folder of the project run the following command:

```bash
pip install -r requirements.txt
```

3. Download the data! A `data` folder is needed, to get all the data used and produced in the experiment you can

    * Follow the link of drive, and dowload it.

    ```bash
    git clone https://github.com/QuantumAdventures/optical-bottle-beam.git
    ```

    * Or, execute the following command inside the project folder (in the terminal like a boss :sunglasses:)

    ```bash
    ./download.sh
    ```

    For this you are going to need wget (can be install with `sudo apt get wget` or `brew install wget` depending on the OS you use).
    
In the end you should have the following directory structure:

.
├── data
│   ├── dataframes
│   │   ├── filtered
│   │   ├── outliers
│   │   └── raw
│   ├── images
│   │   ├── circle
│   │   ├── hour
│   │   ├── long
│   │   └── square
│   ├── plots
│   ├── quadrant
│   ├── results
│   ├── simulations
│   │   ├── error_analysis
│   │   ├── kl
│   │   └── obb_nas
│   └── videos
├── notebooks
│   ├── 1. Create frames from video.ipynb
│   ├── 2. Microparticle detection and tracking.ipynb
│   ├── 2.1. Execute detection for multiple images.ipynb
│   ├── 3. Potential Analysis with Multiple Parameters.ipynb
│   ├── 4. Kullback-Liebler Analysis.ipynb
│   ├── 5. Error Analysis for Intermediate Regime.ipynb
│   └── 6. Gaussianity tests for optical tweezers.ipynb
├── LICENSE
├── README.md
└── requirements.txt

## Usage

Easy explanation for the future

```python
aaaa
```

## License

This code is licensed by:

General Public License version 3.0 [GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)


Copyright (C) 2022  Quantum Adventures: Pontifical University of Rio de Janeiro
research group for optomechanics, quantum optics and quantum information of 

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Contact

#Name - [Linkedin](https://www.linkedin.com/in) [Email](email)

Project Link: [Repository](https://github.com)

## References

Author *Title* **2019 Latin American Robotics Symposium**. 2019.
[doi:10.1109/LARS-SBR-WRE48964.2019.00049](doi:10.1109/LARS-SBR-WRE48964.2019.00049)