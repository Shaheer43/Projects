import random
import matplotlib.pyplot as plt

# Define fixed points (Gulshan-e-Iqbal, Gulistan-e-Johar, and Bahadurabad) with their coordinates and IDs
points = {
    "Gulshan-e-Iqbal": (0, 0),
    "Gulistan-e-Johar": (5, 0),
    "Bahadurabad": (2.5, 5)
}

# Pre-defined distances between points
distances = {
    ("Gulshan-e-Iqbal", "Gulistan-e-Johar"): 5,  # Update with your exact distances
    ("Gulshan-e-Iqbal", "Bahadurabad"): 8.7,       # Update with your exact distances
    ("Gulistan-e-Johar", "Bahadurabad"): 9,      # Update with your exact distances
    # Alternate Routes
    ("Gulshan-e-Iqbal", "Gulistan-e-Johar-Johar Mor - Rabia City Road"): 6,  # Update with your exact distances
    ("Gulshan-e-Iqbal", "Gulistan-e-Johar-Millennium Mall Road"): 8,         # Update with your exact distances
    ("Gulshan-e-Iqbal", "Bahadurabad-KDA Chowrangi - Tipu Sultan Road"): 9,   # Update with your exact distances
    ("Gulshan-e-Iqbal", "Bahadurabad-Askari Park Road"): 7,                   # Update with your exact distances
    ("Gulistan-e-Johar", "Bahadurabad-Safoora Chowrangi - Abul Hasan Isphani Road"): 10,  # Update with your exact distances
    ("Gulistan-e-Johar", "Bahadurabad-Gulistan Chowrangi - Sharah-e-Faisal"): 13,         # Update with your exact distances
    ("Gulshan-e-Iqbal", "Shahrah-e-Faisal"): 9,  # Update with your exact distances
    ("Gulshan-e-Iqbal", "Rashid Minhas Road"): 7,       # Update with your exact distances
    ("Gulshan-e-Iqbal", "Shaheed-e-Millat Road"): 7,      # Update with your exact distances
    ("Gulistan-e-Johar", "University Road"): 9,  # Update with your exact distances
    ("Gulistan-e-Johar", "Shahrah-e-Faisal"): 11,  # Update with your exact distances
    ("Gulistan-e-Johar", "Rashid Minhas Road"): 10,  # Update with your exact distances
    # Add reverse directions
    ("Gulistan-e-Johar", "Gulshan-e-Iqbal"): 5,  # Update with your exact distances
    ("Bahadurabad", "Gulshan-e-Iqbal"): 7,       # Update with your exact distances
    ("Bahadurabad", "Gulistan-e-Johar"): 4,      # Update with your exact distances
    ("Gulistan-e-Johar-Johar Mor - Rabia City Road", "Gulshan-e-Iqbal"): 6,  # Update with your exact distances
    ("Gulistan-e-Johar-Millennium Mall Road", "Gulshan-e-Iqbal"): 8,         # Update with your exact distances
    ("Bahadurabad-KDA Chowrangi - Tipu Sultan Road", "Gulshan-e-Iqbal"): 9,   # Update with your exact distances
    ("Bahadurabad-Askari Park Road", "Gulshan-e-Iqbal"): 7,                   # Update with your exact distances
    ("Bahadurabad-Safoora Chowrangi - Abul Hasan Isphani Road", "Gulistan-e-Johar"): 10,  # Update with your exact distances
    ("Bahadurabad-Gulistan Chowrangi - Sharah-e-Faisal", "Gulistan-e-Johar"): 13,         # Update with your exact distances
    ("Shahrah-e-Faisal", "Gulshan-e-Iqbal"): 9,  # Update with your exact distances
    ("Rashid Minhas Road", "Gulshan-e-Iqbal"): 7,       # Update with your exact distances
    ("Shaheed-e-Millat Road", "Gulshan-e-Iqbal"): 7,      # Update with your exact distances
    ("University Road", "Gulistan-e-Johar"): 9,  # Update with your exact distances
    ("Shahrah-e-Faisal", "Gulistan-e-Johar"): 11,  # Update with your exact distances
    ("Rashid Minhas Road", "Gulistan-e-Johar"): 10  # Update with your exact distances
}

# Calculate total distance of a route
def calcDistance(route):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distances[(route[i], route[i+1])]
    total_distance += distances[(route[-1], route[0])]  # Return to starting point
    return total_distance

# Generate initial population
def generateInitialPopulation(population_size):
    population = []
    for _ in range(population_size):
        route = list(points.keys())  # Start from Gulshan-e-Iqbal
        random.shuffle(route)
        population.append(route)
    return population

# Genetic algorithm
def geneticAlgorithm(population, population_size, num_generations,MUTATION_RATE):
    for gen_number in range(num_generations):
        new_population = []

        # Elitism: Select top 2 individuals from current population
        population.sort(key=lambda x: calcDistance(x))
        new_population.extend(population[:2])

        # Create offspring using crossover and mutation
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)

            # Perform crossover (ordered crossover)
            start, end = sorted(random.sample(range(len(parent1)), 2))
            child = parent1[start:end] + [city for city in parent2 if city not in parent1[start:end]]

            # Perform mutation (swap mutation)
            if random.random() < MUTATION_RATE:
                idx1, idx2 = random.sample(range(len(child)), 2)
                child[idx1], child[idx2] = child[idx2], child[idx1]

            new_population.append(child)

        population = new_population

        if gen_number % 10 == 0:
            print("Generation:", gen_number, "| Best Distance:", calcDistance(population[0]))

    return population[0]

# Plot the route with associated cost
def plotRoute(route):
    plt.figure(figsize=(8, 8))
    plt.scatter(*zip(*points.values()), color='red')
    for i, city in enumerate(route):
        x, y = points[city]
        plt.text(x, y, f'{city}\n{route[(i+1)%len(route)]}: {distances[(city, route[(i+1)%len(route)])]} km', fontsize=9)
    for i in range(len(route)):
        plt.plot(
            [points[route[i]][0], points[route[(i+1)%len(route)]][0]],
            [points[route[i]][1], points[route[(i+1)%len(route)]][1]],
            color='blue', linestyle='--')
    plt.title("Optimized Route")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.show()

# Main function
def main():
    # Parameters
    POPULATION_SIZE = 1000
    NUM_GENERATIONS = 200
    MUTATION_RATE = 0.1

    # Generate initial population
    population = generateInitialPopulation(POPULATION_SIZE)

    # Run genetic algorithm
    best_route = geneticAlgorithm(population, POPULATION_SIZE, NUM_GENERATIONS,MUTATION_RATE)

    # Plot the best route
    plotRoute(best_route)
    print("Best Route:", best_route)
    print("Total Distance:", calcDistance(best_route), "km")

if __name__ == "__main__":
    main()
