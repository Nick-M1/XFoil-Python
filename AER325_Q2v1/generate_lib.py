
def generateAirfoilNames() -> list[str]:
    max_chamber_pos = "4"          # Don't change

    airfoil_names = []
    for max_chamber in range(1, 9+1):           # 1 to 9
        for thickness in range(9, 40+1):        # 9 to 40
            airfoil_names.append(f"NACA{max_chamber}{max_chamber_pos}{thickness:02}")

    return airfoil_names


# tester = generateAirfoilNames()
# print(tester)




def generateAirfoil_maxchamber() -> list[str]:
    max_chamber_pos = "4"          # Dont' change
    thickness = "09"

    airfoil_names = []
    for max_chamber in range(1, 9+1):        # 9 to 40
        airfoil_names.append(f"NACA{max_chamber}{max_chamber_pos}{thickness}")

    return airfoil_names

tester = generateAirfoil_maxchamber()
print(tester)


def generateAirfoil_thickness() -> list[str]:
    max_chamber_pos = "4"          # Dont' change
    max_chamber = "1"

    airfoil_names = []
    for thickness in range(9, 23, 2):        # 9 to 40
        airfoil_names.append(f"NACA{max_chamber}{max_chamber_pos}{thickness:02}")

    return airfoil_names


tester = generateAirfoil_thickness()
print(tester)