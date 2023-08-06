import numpy as np
from scipy.spatial.transform import Rotation

from pose3d.transform import Transform
from pose3d.pose import Pose
from pose3d.pose_comparison import PoseComparison


# Verify compatibility with poses
def pose_test(passing_criteria: float = 0.001):

    transf = Transform(name='demo')
    transf.random()

    inv_transf = transf.inv()

    pose = Pose(name='test')
    pose.random()

    result_1 = transf.apply(pose)
    result_2 = inv_transf.apply(result_1)

    position_difference, rotation_difference = PoseComparison.calc_difference(pose, result_2)
    assert np.linalg.norm(position_difference) < passing_criteria
    assert rotation_difference<passing_criteria

    return True


# Verify matrix generation
def transf_matrix_test(passing_criteria: float = 0.001):
    transf = Transform(name='demo')
    transf.random()

    inv_transf = transf.inv()

    mult = [np.matmul(transf.matrix(), inv_transf.matrix()),
            np.matmul(inv_transf.matrix(), transf.matrix())]

    for matrix in mult:
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                assert abs(matrix[i, j] - np.eye(4)[i, j]) < passing_criteria

    return True


# Verify inverse calculation
def inv_test(passing_criteria: float = 0.001):

    transf = Transform(name='demo')
    transf.translation = np.random.rand(3)
    transf.rotation = Rotation.random()

    inv_transf = transf.inv()

    input_vec = np.random.rand(3)
    result_1 = transf.apply(input_vec)
    result_2 = inv_transf.apply(result_1)

    assert np.linalg.norm(np.subtract(result_2, input_vec)) < passing_criteria

    return True


def main():

    pass_criteria = 1e-10

    test_passed = inv_test(passing_criteria=pass_criteria)
    if test_passed:
        print("Test Passed: inv_test")

    test_passed = transf_matrix_test(passing_criteria=pass_criteria)
    if test_passed:
        print("Test Passed: transf_matrix_test")

    test_passed = pose_test(passing_criteria=pass_criteria)
    if test_passed:
        print("Test Passed: pose_test")

if __name__ == "__main__":
    main()
