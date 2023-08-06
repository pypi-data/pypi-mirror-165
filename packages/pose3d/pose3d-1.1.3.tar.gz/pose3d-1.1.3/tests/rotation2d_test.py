from pose3d.rotation2d import Rotation2D

def euler2euler_test(angle: float, passing_criteria: float = 0.001):

    rotation = Rotation2D()
    rotation.from_euler(angle, degrees=True)

    assert (abs(angle - rotation.as_euler(degrees=True))/angle) < passing_criteria

    return True

def inv_test(angle: float, passing_criteria: float = 0.001):

    rotation = Rotation2D()
    rotation.from_euler(angle, degrees=True)
    rotation.inv()

    assert (abs(-angle - rotation.as_euler(degrees=True))/angle) < passing_criteria

    return True

def main():
    angle = 30

    test_passed = euler2euler_test(angle)
    if test_passed:
        print("euler2euler_test - Test Passed.")

    test_passed = inv_test(angle)
    if test_passed:
        print("inv_test - Test Passed.")

if __name__ == "__main__":
    main()
