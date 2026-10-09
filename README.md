# james_manipulation
MoveIt configuration and bottle picking for the James robot: a beer crate with an
OpenManipulator-X.

| Package | Contents |
|---|---|
| `james_moveit_config` | MoveIt configuration for the crate + arm model from `james_description` |

Planned: `james_manipulation` — node that picks a bottle from the crate and hands it over.

The overview of all James repositories is in the README of
[james_robot](https://github.com/timassman/james_robot); the container and the daily startup
of the Jetson in the README of [james_docker](https://github.com/timassman/james_docker).

---

## Simulated arm with MoveIt (laptop)

Needs a workspace with this repository, james_robot and the ROBOTIS humble packages, for
example `~/ros2_ws3`:

```bash
source ~/ros2_ws3/install/setup.bash
ros2 launch james_moveit_config demo.launch.py
```

The demo runs in its own ROS domain (77, localhost only), so the simulated arm cannot
interfere with the real arm on the network.

MotionPlanning panel → Planning tab → Planning Group `arm` → Goal State:

| Named state | Pose |
|---|---|
| `init` | All joints 0: arm pointing away from the crate |
| `home` | ROBOTIS rest pose |
| `grasp_r2c2` | Gripper around the cap of bottle r2c2, taught on the real arm |
| `handover` | Arm pointing away from the crate, forearm raised, bottle hanging upright |

MoveIt plans around the crate walls and the wooden planks. The bottles are not in the planning
scene yet.

---

## Credits and license

MIT, see [LICENSE](LICENSE). Exception: `james_moveit_config/config/james.srdf` is based on the
SRDF of ROBOTIS `open_manipulator_x_moveit_config` and is licensed under the Apache License 2.0
([james_moveit_config/LICENSE-APACHE-2.0](james_moveit_config/LICENSE-APACHE-2.0)).

The launch files load these ROBOTIS packages at runtime
([open_manipulator](https://github.com/ROBOTIS-GIT/open_manipulator), humble branch, Apache
License 2.0):

| Package | Used for |
|---|---|
| `open_manipulator_x_description` | Arm model and ros2_control hardware (via `james_description`) |
| `open_manipulator_x_moveit_config` | Kinematics solver and joint limits |
| `open_manipulator_x_bringup` | ros2_control controller configuration |
