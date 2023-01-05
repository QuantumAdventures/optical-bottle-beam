# Code for the Optical Bottle Beam

Add explanation lalallalalala

Awesome bullet points

* One.
* Two.
* Ragatanga

## Installation

How to install this code

```bash
pip install ------
```
Download data

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