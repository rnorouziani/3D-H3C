from src.InputFormat import InputFormat
from src.MagneticCore import MagneticCore
from src.OutputVerification import OutputVerification
from src.OutputFormat import OutputFormat

inputFormat = InputFormat()
coils = inputFormat.load_coils("coils_config.json")
magneticCore = MagneticCore(coils)
while True:
    try:
        p = inputFormat.load_params()
        m = p["magnetic_moment_vector"]
        t = p["target_magnetic_torque"]
        f = p["target_magnetic_force"]
    except ValueError:
        print("Try again!")
        continue

    i_f = magneticCore.calculate_current_of_target_force(m, f)
    i_t = magneticCore.calculate_current_of_target_torque(m, t)

    outputVerification = OutputVerification(coils, m, f, t, i_f, i_t)
    if not outputVerification.is_currents_within_range():
        print("Warning: The calculated currents are outside of the range!")
    if not outputVerification.is_accurate_enough():
        print("Warning: The result is not accurate enough!")

    OutputFormat(i_f, i_t).display()

    response = input("Do you want to enter new force and torque? (yes/no): ").strip().lower()
    if response == "no":
        break
