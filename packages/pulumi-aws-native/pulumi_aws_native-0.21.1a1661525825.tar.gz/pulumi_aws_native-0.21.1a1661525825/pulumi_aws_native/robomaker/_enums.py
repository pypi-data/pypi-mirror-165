# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'RobotApplicationRobotSoftwareSuiteName',
    'RobotApplicationRobotSoftwareSuiteVersion',
    'RobotApplicationSourceConfigArchitecture',
    'RobotArchitecture',
    'SimulationApplicationRenderingEngineName',
    'SimulationApplicationRobotSoftwareSuiteName',
    'SimulationApplicationRobotSoftwareSuiteVersion',
    'SimulationApplicationSimulationSoftwareSuiteName',
    'SimulationApplicationSimulationSoftwareSuiteVersion',
    'SimulationApplicationSourceConfigArchitecture',
]


class RobotApplicationRobotSoftwareSuiteName(str, Enum):
    """
    The name of robot software suite.
    """
    ROS = "ROS"
    ROS2 = "ROS2"
    GENERAL = "General"


class RobotApplicationRobotSoftwareSuiteVersion(str, Enum):
    """
    The version of robot software suite.
    """
    KINETIC = "Kinetic"
    MELODIC = "Melodic"
    DASHING = "Dashing"


class RobotApplicationSourceConfigArchitecture(str, Enum):
    """
    The architecture of robot application.
    """
    X8664 = "X86_64"
    ARM64 = "ARM64"
    ARMHF = "ARMHF"


class RobotArchitecture(str, Enum):
    """
    The target architecture of the robot.
    """
    X8664 = "X86_64"
    ARM64 = "ARM64"
    ARMHF = "ARMHF"


class SimulationApplicationRenderingEngineName(str, Enum):
    """
    The name of the rendering engine.
    """
    OGRE = "OGRE"


class SimulationApplicationRobotSoftwareSuiteName(str, Enum):
    """
    The name of the robot software suite.
    """
    ROS = "ROS"
    ROS2 = "ROS2"
    GENERAL = "General"


class SimulationApplicationRobotSoftwareSuiteVersion(str, Enum):
    """
    The version of the robot software suite.
    """
    KINETIC = "Kinetic"
    MELODIC = "Melodic"
    DASHING = "Dashing"
    FOXY = "Foxy"


class SimulationApplicationSimulationSoftwareSuiteName(str, Enum):
    """
    The name of the simulation software suite.
    """
    GAZEBO = "Gazebo"
    ROSBAG_PLAY = "RosbagPlay"
    SIMULATION_RUNTIME = "SimulationRuntime"


class SimulationApplicationSimulationSoftwareSuiteVersion(str, Enum):
    """
    The version of the simulation software suite.
    """
    SEVEN = "7"
    NINE = "9"
    SIMULATION_APPLICATION_SIMULATION_SOFTWARE_SUITE_VERSION_11 = "11"
    KINETIC = "Kinetic"
    MELODIC = "Melodic"
    DASHING = "Dashing"
    FOXY = "Foxy"


class SimulationApplicationSourceConfigArchitecture(str, Enum):
    """
    The target processor architecture for the application.
    """
    X8664 = "X86_64"
    ARM64 = "ARM64"
    ARMHF = "ARMHF"
