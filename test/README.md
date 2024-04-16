# Automated tests

The folders and files for this folder are as follows:


- TestCoilT.py: This test script is designed to test the functionalities of the CoilT module.

- TestMagneticCore.py: This test script is designed to test the functionalities of the the Magnetic Core module.

- TestInputFormat.py: This test script is designed to test the functionalities of the Input Format module.

- TestOutputVerification.py: This test script is designed to test the functionalities of the Output Verification module.


To run these tests, ensure you are in the directory containing the test files and use the following command:

python -m unittest discover -s . -p "Test*.py"
