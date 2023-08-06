import numpy as np
from scipy.spatial.transform import Rotation


class PoseComparison:
    @staticmethod
    def different_pose(pose_1, pose_2, passing_criteria: float = 1e-5) -> bool:

        position_difference, rotation_difference = PoseComparison.calc_difference(pose_1, pose_2)

        if np.linalg.norm(position_difference) < passing_criteria and rotation_difference < passing_criteria:
            return True

        return False


    @staticmethod
    def calc_difference(pose_1, pose_2, degrees: bool = False):
        position_difference = np.subtract(pose_1.position, pose_2.position)

        if position_difference.shape == (2,):
            rotation_difference = abs(pose_1.orientation.as_euler(degrees) - pose_2.orientation.as_euler(degrees))

        elif position_difference.shape == (3,):
            mat = np.matmul(pose_1.orientation.inv().as_matrix(), pose_2.orientation.as_matrix())
            compound_rot = Rotation.from_matrix(mat)
            rotation_difference = np.linalg.norm(compound_rot.as_rotvec(degrees=degrees))

        return position_difference, rotation_difference