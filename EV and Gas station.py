import random
import numpy as np
import matplotlib.pyplot as plt
import time

'''
def random_walk(dim, nsteps):
    city_grid = []
    for i in range(1, dim + 1):
        for j in range(1, dim + 1):
            element = (i, j)
            city_grid.append(element)
    city_matrix = np.zeros([dim, dim])
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    initial_position_x, initial_position_y = int(dim/2), int(dim/2)
    walk = [(initial_position_x, initial_position_y)]
    random_x = random.sample(range(1, dim + 1), dim)
    random_y = random.sample(range(1, dim + 1), dim)
    location_of_gas = []
    for i in range(len(random_x)):
        cord = (random_x[i], random_y[i])
        city_matrix[random_x[i]-1, random_y[i]-1] = city_matrix[random_x[i]-1, random_y[i]-1] + 1
        location_of_gas.append(cord)

    for _ in range(nsteps):  # not interested in values from a function but overall how many times the loop is running
        random.shuffle(moves)
        for dx, dy in moves:
            pos_x = initial_position_x + dx
            pos_y = initial_position_y + dy
            if (pos_x, pos_y) not in location_of_gas:
                walk.append((pos_x, pos_y))
                initial_position_x = pos_x
                initial_position_y = pos_y
                break
            else:
                print(f"reached gas station within in {len(walk) + 1} steps ")
            break

    return location_of_gas, walk, city_matrix

dim = 10
nsteps = 10
location_of_gas, walk, city_matrix = random_walk(dim, nsteps)

# Extract x and y coordinates for plotting
x_coords, y_coords = zip(*walk)
gas_x, gas_y = zip(*location_of_gas)

# Plot the walk
plt.figure(figsize=(8, 8))
plt.imshow(city_matrix, origin="lower", cmap="Greys")
plt.scatter(gas_x, gas_y, c='r', label='Gas Station', zorder=3)
plt.plot(x_coords, y_coords, marker='o', markersize=3, linestyle='-', linewidth=1)
plt.title(f"2D random walk ({len(walk)} steps)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()
'''

def random_walk(dim, nsteps):
    # Create an empty city matrix
    city_matrix = np.zeros((dim, dim))

    # Define possible moves
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Starting at almost the center of the grid
    initial_position = (dim // 2, dim // 2)
    walk = [initial_position]

    # Generate a list of random gas station positions.
    location_of_gas = []
    for _ in range(dim**2//10):
        g_x = random.randint(1, dim + 1)
        g_y = random.randint(1, dim + 1)
        location_of_gas.append((g_x, g_y))

    # Mark the gas station locations in the city_matrix.
    for x, y in location_of_gas:
        city_matrix[x - 2, y - 2] += 1

    current_position = initial_position

    # random walk code
    for _ in range(nsteps):
        random.shuffle(moves)  # Shuffle moves so the choice is random
        moved = False  # Flag to check if a valid move is made
        for dx, dy in moves:
            new_x = current_position[0] + dx
            new_y = current_position[1] + dy
            new_position = (new_x, new_y)

            # Check if new_position is within grid boundaries
            if new_x < 1 or new_x > dim or new_y < 1 or new_y > dim:
                continue  # Skip moves that take you out of the grid

            # If the new position is a gas station, stop the walk and report
            if new_position in location_of_gas:
                # print(f"Reached gas station at {new_position} after {len(walk)} steps.")
                return location_of_gas, walk, city_matrix

            # Otherwise, take the step
            else:
                walk.append(new_position)
                current_position = new_position
                moved = True
                break  # Accept the first valid move

        # If no valid move was found in any direction, break out of the loop
        if not moved:
            # print(f"No valid moves available after {len(walk)} steps.")
            break

    return (location_of_gas), walk, city_matrix


dim = 50
nsteps = 1250
location_of_gas, walk, city_matrix = random_walk(dim, nsteps)

print("Gas station locations:", location_of_gas)
print("Random walk path:", walk)
print("City matrix:\n", city_matrix)
print(len(location_of_gas), " no of gas stations in random")
# print("Probability of finding gas in 10 steps = ", times_found_gas/10, "%")

# Plotiing the path
walk_x, walk_y = zip(*walk)
gas_x, gas_y = zip(*location_of_gas)

plt.figure(figsize=(8, 8))
plt.scatter(gas_x, gas_y, color='red', label='Gas Station', zorder=3)
plt.plot(walk_x, walk_y, marker='o', color='blue', label='Walk Path', zorder=2)
plt.title(f"Random Walk in a {dim}x{dim} City Grid")
plt.grid()
plt.xlabel("Column")
plt.ylabel("Row")
plt.legend()
plt.show()



# Probability calculations
# Ofcourse the probability would be a better estimate for understanding if we take average over certain number of iterations for a certain 'nstep'

step_list = np.arange(int(dim/5), dim * 5, 2)
pro = []
for j in step_list:
    l_reached = 0
    l_notreached = 0
    for i in range(2500):
        length_of_walk = len(random_walk(dim, j)[1])
        if length_of_walk < j + 1 :
            l_reached = l_reached + 1
        else:
            l_notreached = l_notreached + 1
    pro.append(l_reached/25)

plt.plot(step_list, pro, label='probability at diffetent steps ')
plt.scatter(step_list, pro, c='r')
plt.grid()
plt.xlabel('steps')
plt.ylabel('probability')
plt.title("Probability at diffetent steps")
plt.legend()
plt.show()

# uniform case
def random_walk2(dim, nsteps):
    city_matrix = np.zeros((dim, dim))
    num_gas_station = int((dim * dim)/10)
    gas_station_location = [(random.randint(1, dim + 1), random.randint(1, dim + 1))]
    d_min = 1.7

    while len(gas_station_location) < num_gas_station:
        candidate = (random.randint(1, dim + 1), random.randint(1, dim + 1))
        for i in range(0, len(gas_station_location)):
            d = ((gas_station_location[i][0] - candidate[0])**2 + (gas_station_location[i][1] - candidate[1])**2)**0.5
            if d >= d_min:
                gas_station_location.append(candidate)
                break
            else:
                continue

    # Define possible moves
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Starting at almost the center of the grid
    initial_position = (dim // 2, dim // 2)
    walk = [initial_position]

    # Mark the gas station locations in the city_matrix.
    for x, y in gas_station_location:
        city_matrix[x - 2, y - 2] += 1

    current_position = initial_position

    # random walk code
    for _ in range(nsteps):
        random.shuffle(moves)  # Shuffle moves so the choice is random
        moved = False  # Flag to check if a valid move is made
        for dx, dy in moves:
            new_x = current_position[0] + dx
            new_y = current_position[1] + dy
            new_position = (new_x, new_y)

            # Check if new_position is within grid boundaries
            if new_x < 1 or new_x > dim or new_y < 1 or new_y > dim:
                continue  # Skip moves that take you out of the grid

            # If the new position is a gas station, stop the walk and report
            if new_position in gas_station_location:
                # print(f"Reached gas station at {new_position} after {len(walk)} steps.")
                return gas_station_location, walk, city_matrix

            # Otherwise, take the step
            else:
                walk.append(new_position)
                current_position = new_position
                moved = True
                break  # Accept the first valid move

        # If no valid move was found in any direction, break out of the loop
        if not moved:
            # print(f"No valid moves available after {len(walk)} steps.")
            break
    return gas_station_location, walk, city_matrix

dim = 50
nsteps = 1250
gas_station_location, walk2, city_matrix2 = random_walk(dim, nsteps)

print("Gas station locations:", gas_station_location)
print("Random walk path:", walk2)
print("City matrix:\n", city_matrix2)
print(len(gas_station_location), "no. of gas stations in uniform distribution")
# print("Probability of finding gas in 10 steps = ", times_found_gas/10, "%")

# Optional: Plotting the path
walk_x2, walk_y2 = zip(*walk2)
gas_x2, gas_y2 = zip(*gas_station_location)

plt.figure(figsize=(8, 8))
plt.scatter(gas_x2, gas_y2, color='red', label='Gas Station', zorder=3)
plt.plot(walk_x2, walk_y2, marker='o', color='blue', label='Walk Path', zorder=2)
plt.title(f"Random Walk in a {dim}x{dim} City Grid")
plt.grid()
plt.xlabel("Column")
plt.ylabel("Row")
plt.legend()
plt.show()

step_list = np.arange(int(dim/5), dim * 5, 2)
pro2 = []
for j in step_list:
    l_reached = 0
    l_notreached = 0
    for i in range(2500):
        length_of_walk = len(random_walk2(dim, j)[1])
        if length_of_walk < j + 1:
            l_reached = l_reached + 1
        else:
            l_notreached = l_notreached + 1
    pro2.append(l_reached/25)

plt.plot(step_list, pro2, label='probability at diffetent steps (uniform) ')
plt.scatter(step_list, pro2, c='b')
plt.plot(step_list, pro, label='probability at diffetent steps (random) ')
plt.scatter(step_list, pro, c='r')
plt.grid()
plt.xlabel('steps')
plt.ylabel('probability')
plt.title(f"Probability at diffetent steps for {dim}x{dim} sized city")
plt.legend()
plt.show()


