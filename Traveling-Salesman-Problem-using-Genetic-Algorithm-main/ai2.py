import random
import matplotlib.pyplot as plt

# Define fixed points (Gulshan-e-Iqbal, Gulistan-e-Johar, and Bahadurabad) with their coordinates and IDs
points = {
    "Gulshan-e-Iqbal": (0, 0),
    "Gulistan-e-Johar": (5, 0),
    "Bahadurabad": (2.5, 5),
    "Gulistan-e-Johar-Johar Mor - Rabia City Road": (5, 2),
    "Gulistan-e-Johar-Millennium Mall Road": (7, 1),
    "Bahadurabad-KDA Chowrangi - Tipu Sultan Road": (4, 4),
    "Bahadurabad-Askari Park Road": (3, 6),
    "Bahadurabad-Safoora Chowrangi - Abul Hasan Isphani Road": (2, 2),
    "Bahadurabad-Gulistan Chowrangi - Sharah-e-Faisal": (1, 3),
    "Shahrah-e-Faisal": (3, 0),
    "Rashid Minhas Road": (0, 2),
    "Shaheed-e-Millat Road": (1, 0),
    "University Road": (6, 1)
}

# Calculate Euclidean distance between two points
def calcEuclideanDistance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

# Pre-defined distances between points
distances = {}
for point1 in points:
    for point2 in points:
        if point1 != point2:
            distances[(point1, point2)] = calcEuclideanDistance(points[point1], points[point2])

# Generate initial population
def generateInitialPopulation(population_size):
    population = []
    for _ in range(population_size):
        route = list(points.keys())  # Start from Gulshan-e-Iqbal
        random.shuffle(route)
        population.append(route)
    return population

# Genetic algorithm
def geneticAlgorithm(population, population_size, num_generations, mutation_rate):
    for gen_number in range(num_generations):
        new_population = []

        # Elitism: Select top 2 individuals from current population
        population.sort(key=lambda x: calcEuclideanDistance(x))
        new_population.extend(population[:2])

        # Create offspring using crossover and mutation
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)

            # Perform crossover (ordered crossover)
            start, end = sorted(random.sample(range(len(parent1)), 2))
            child = parent1[start:end] + [city for city in parent2 if city not in parent1[start:end]]

            # Perform mutation (swap mutation)
            if random.random() < mutation_rate:
                idx1, idx2 = random.sample(range(len(child)), 2)
                child[idx1], child[idx2] = child[idx2], child[idx1]

            new_population.append(child)

        population = new_population

        if gen_number % 10 == 0:
            print("Generation:", gen_number, "| Best Distance:", calcEuclideanDistance(population[0]))

    return population[0]

# Plot the route with associated cost
def plotRoute(route):
    plt.figure(figsize=(8, 8))
    plt.scatter(*zip(*points.values()), color='red')
    for i, city in enumerate(route):
        x, y = points[city]
        plt.text(x, y, f'{city}\n{route[(i+1)%len(route)]}: {distances[(city, route[(i+1)%len(route)])]:.2f} km', fontsize=9)
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
    MUTATION_RATE = 0.2

    # Generate initial population
    population = generateInitialPopulation(POPULATION_SIZE)

    # Run genetic algorithm
    best_route = geneticAlgorithm(population, POPULATION_SIZE, NUM_GENERATIONS, MUTATION_RATE)

    # Plot the best route
    plotRoute(best_route)
    print("Best Route:", best_route)
    print("Total Distance:", calcEuclideanDistance(best_route), "km")

if __name__ == "__main__":
    main()
