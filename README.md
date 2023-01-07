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

    * Or, execute the following command (in the terminal like a boss :like-a-boss)

    ```bash
    git clone git@github.com:QuantumAdventures/optical-bottle-beam.git
    ```

    * Or, by downloading the .zip of the repo.

## Usage

Easy explanation for the future

```python
import numpy as np
from pymentor import Mentor
# direct kinematics example
angles = [np.pi/6]*5
robot = Mentor()
pos, rot = robot.get_position(angles)
# pos is 4x1 vector 
# rot is 3x3 rotation matrix
       
pos = np.array([24.21323027, 13.97951501, -17.07885504, 1.0])
rot = np.array([[0.59049287, 0.23642905, -0.77163428],
    [-0.23642905, -0.86349762, -0.44550326],
    [-0.77163428, 0.44550326, -0.4539905 ]])
# pos is 4x1 vector 
# rot is 3x3 rotation matrix
angles = robot.get_angles(pos,rot)


# creating rotational matrix from alpha-beta-gamma angles
rot = robot.get_orientation(np.pi/6, np.pi/6, np.pi/6)
```

## License
General Public License version 3.0 [GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Contact

#Name - [Linkedin](https://www.linkedin.com/in) [Email](email)

Project Link: [Repository](https://github.com)

## References

Author *Title* **2019 Latin American Robotics Symposium**. 2019.
[doi:10.1109/LARS-SBR-WRE48964.2019.00049](doi:10.1109/LARS-SBR-WRE48964.2019.00049)