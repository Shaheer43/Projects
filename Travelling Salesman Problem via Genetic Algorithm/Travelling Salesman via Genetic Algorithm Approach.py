import random
import matplotlib.pyplot as plt

# Define the points and their coordinates
points = {
    "Gulshan-e-Iqbal": (0, 0),
    "Gulistan-e-Johar": (5, 0),
    "Bahadurabad": (2.5, 5),
}

distances = {
    ("Gulshan-e-Iqbal", "Gulistan-e-Johar"): 8,
    ("Gulshan-e-Iqbal", "Uniroad", "Bahadurabad"): 10.7,
    ("Gulistan-e-Johar", "Bahadurabad"): 11,
    # Alternate Routes
    ("Gulshan-e-Iqbal", "Gulistan-e-Johar-Johar Mor - Rabia City Road"): 6,
    ("Gulshan-e-Iqbal", "Gulistan-e-Johar-Millennium Mall Road"): 6,
    ("Gulshan-e-Iqbal", "Bahadurabad-KDA Chowrangi - Tipu Sultan Road"): 2,
    ("Gulshan-e-Iqbal", "Bahadurabad-Askari Park Road"): 7,
    ("Gulistan-e-Johar", "Bahadurabad-Safoora Chowrangi - Abul Hasan Isphani Road"): 10,
    ("Gulistan-e-Johar", "Bahadurabad-Gulistan Chowrangi - Sharah-e-Faisal"): 13,
    ("Gulshan-e-Iqbal", "Shahrah-e-Faisal"): 9,
    ("Gulshan-e-Iqbal", "Rashid Minhas Road"): 7,
    ("Gulshan-e-Iqbal", "Shaheed-e-Millat Road"): 7,
    ("Gulistan-e-Johar", "University Road"): 9,
    ("Gulistan-e-Johar", "Shahrah-e-Faisal"): 11,
    ("Gulistan-e-Johar", "Rashid Minhas Road"): 10,
    # Add reverse directions
    ("Gulistan-e-Johar", "Gulshan-e-Iqbal"): 5,
    ("Bahadurabad", "Gulshan-e-Iqbal"): 7,
    ("Bahadurabad", "Gulistan-e-Johar"): 4,
    ("Gulistan-e-Johar-Johar Mor - Rabia City Road", "Gulshan-e-Iqbal"): 6,
    ("Gulistan-e-Johar-Millennium Mall Road", "Gulshan-e-Iqbal"): 6,
    ("Bahadurabad-KDA Chowrangi - Tipu Sultan Road", "Gulshan-e-Iqbal"): 9,
    ("Bahadurabad-Askari Park Road", "Gulshan-e-Iqbal"): 7,
    ("Bahadurabad-Safoora Chowrangi - Abul Hasan Isphani Road", "Gulistan-e-Johar"): 10,
    ("Bahadurabad-Gulistan Chowrangi - Sharah-e-Faisal", "Gulistan-e-Johar"): 13,
    ("Shahrah-e-Faisal", "Gulshan-e-Iqbal"): 9,
    ("Rashid Minhas Road", "Gulshan-e-Iqbal"): 7,
    ("Shaheed-e-Millat Road", "Gulshan-e-Iqbal"): 7,
    ("University Road", "Gulistan-e-Johar"): 9,
    ("Shahrah-e-Faisal", "Gulistan-e-Johar"): 11,
    ("Rashid Minhas Road", "Gulistan-e-Johar"): 10
}

# Function to calculate the distance of a given route
def calcDistance(route):
    distance = 0
    route_taken = []
    for i in range(len(route)):
        current_city = route[i]
        next_city = route[(i + 1) % len(route)]
        pair = (current_city, next_city)
        if pair not in distances:
            # If direct route is not found, check for alternate routes
            for alt_route, alt_distance in distances.items():
                if pair[0] in alt_route and pair[1] in alt_route:
                    distance += alt_distance
                    route_taken.append((alt_route, alt_distance))
                    break
        else:
            distance += distances[pair]
            route_taken.append((pair, distances[pair]))
    return distance, route_taken

# Generate the initial population
def generateInitialPopulation(pop_size):
    population = []
    for _ in range(pop_size):
        route = list(points.keys())
        random.shuffle(route)
        population.append(route)
    return population

# Perform crossover between two parents
def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    middle = parent1[start:end]
    remaining = [city for city in parent2 if city not in middle]
    child = remaining[:start] + middle + remaining[start:]
    return child

# Mutate a given route based on a mutation rate
def mutate(route, mutation_rate):
    route = route[:]
    for _ in range(len(route)):
        if random.random() < mutation_rate:
            idx1, idx2 = random.sample(range(len(route)), 2)
            route[idx1], route[idx2] = route[idx2], route[idx1]
    return route

# Perform tournament selection
def tournament_selection(population, tournament_size=3):
    selected = random.sample(population, tournament_size)
    return min(selected, key=lambda x: calcDistance(x)[0])

# Genetic Algorithm implementation
def geneticAlgorithm(population, pop_size, num_generations, base_mutation_rate):
    best_distance = float('inf')
    best_route = None
    best_route_taken = None
    routes_with_19_7_distance = []
    distance_records = []
    for generation in range(num_generations):
        population = sorted(population, key=lambda x: calcDistance(x)[0])
        current_best_distance, current_best_route_taken = calcDistance(population[0])
        distance_records.append((generation, current_best_distance, current_best_route_taken))
        if current_best_distance < best_distance:
            best_distance = current_best_distance
            best_route = population[0]
            best_route_taken = current_best_route_taken
            if round(best_distance, 1) == 19.7:
                routes_with_19_7_distance.append(best_route)
                print(f"New best found: {best_distance} at generation {generation}")
        new_population = [best_route]  # Elitism
        while len(new_population) < pop_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)
            child = mutate(child, base_mutation_rate)
            new_population.append(child)
        population = new_population
        if generation % 10 == 0:
            print(f"Generation: {generation}, Best distance: {best_distance}")
    return best_route, routes_with_19_7_distance, distance_records, best_route_taken

# Plotting function
def plotRoute(route):
    plt.figure(figsize=(8, 6))
    x, y = zip(*[points[city] for city in route + [route[0]]])  # Complete the cycle
    plt.plot(x, y, 'o-')
    for city, (city_x, city_y) in points.items():
        plt.text(city_x, city_y, city, fontsize=12)
    plt.title("Optimal Route")
    plt.xlabel("Distance (units)")
    plt.ylabel("Distance (units)")
    plt.grid(True)
    plt.show()

# Main function
def main():
    pop_size = 100
    num_generations = 1000
    mutation_rate = 0.01

    if any(isinstance(coord, complex) for point in points.values() for coord in point):
        raise ValueError("Complex coordinates found, which are invalid for TSP.")

    initial_population = generateInitialPopulation(pop_size)
    best_route, routes_with_19_7_distance, distance_records, best_route_taken = geneticAlgorithm(initial_population, pop_size, num_generations, mutation_rate)
    plotRoute(best_route)
    print("Best route:", best_route)
    print("Total distance:", calcDistance(best_route)[0])
    print("Route taken with distances:")
    for segment in best_route_taken:
        print(f"Route: {segment[0]}, Distance: {segment[1]}")
    print("Routes with distance 19.7:", routes_with_19_7_distance)
    print("Distance records:", distance_records)

main()