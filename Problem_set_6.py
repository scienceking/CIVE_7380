import random
import statistics
import matplotlib.pyplot as plt


def run_single_simulation(sim_hours=5, seed=None, no_passing=False):
    if seed is not None:
        random.seed(seed)

    T = sim_hours * 60.0  # Total simulation time in minutes
    departureA_list = []
    arrivalB_list = []
    departureB_list = []

    tDepartureA = 0.0  # Initial departure time from A

    while tDepartureA <= T:
        departureA_list.append(tDepartureA)

        # Generate travel time from A to B (Normal distribution)
        run_time = random.gauss(35, 7)
        if run_time < 0:
            run_time = 0.0  # Avoid negative travel time

        # Calculate arrival time at B
        tArrivalB = tDepartureA + run_time

        # If no passing is allowed, ensure the bus arrives no earlier than the previous bus leaves B
        if no_passing and len(departureB_list) > 0:
            if tArrivalB < departureB_list[-1]:
                tArrivalB = departureB_list[-1]

        arrivalB_list.append(tArrivalB)

        # Generate dwell time at B (Uniform distribution)
        dwell_time = random.uniform(2, 4)

        # Calculate departure time from B
        tDepartureB = tArrivalB + dwell_time
        departureB_list.append(tDepartureB)

        # Generate inter-arrival time (Exponential distribution, mean = 6 min)
        inter_arrival = random.expovariate(1 / 6.0)

        # Update next departure time from A
        tDepartureA += inter_arrival

    return departureA_list, departureB_list


def part_a(sim_hours=5):
    departureA, _ = run_single_simulation(sim_hours=sim_hours)

    hour_avg_hw = []
    for hour_idx in range(sim_hours):
        start_t = hour_idx * 60
        end_t = (hour_idx + 1) * 60
        times_in_hour = [t for t in departureA if (start_t <= t < end_t)]

        # Compute average headway in this hour
        if len(times_in_hour) > 1:
            hw_list = []
            for i in range(1, len(times_in_hour)):
                hw_list.append(times_in_hour[i] - times_in_hour[i - 1])
            hour_avg_hw.append(sum(hw_list) / len(hw_list))
        else:
            hour_avg_hw.append(0.0)

    # Plot hourly average headway
    plt.figure()
    plt.plot(range(sim_hours), hour_avg_hw, marker='o')
    plt.xlabel("Hour Index (0=7AM~8AM, 1=8AM~9AM, etc.)")
    plt.ylabel("Average Departure Headway at A (min)")
    plt.title("Part (a): Hourly Average Headway at A")
    plt.show()

    return hour_avg_hw


def part_b_and_c(sim_hours=5, total_runs=20):
    """
    (b) Run the simulation multiple times and compute:
        - The average and standard deviation of B-departure headway using the first 5, 10, 15, 20 runs
    (c) Plot how the mean and variance of B-departure headway evolve with replications.
    """
    avg_hw_B_each_run = []

    for r in range(total_runs):
        _, departureB = run_single_simulation(sim_hours=sim_hours)
        headways_B = []
        for i in range(1, len(departureB)):
            hw = departureB[i] - departureB[i - 1]
            headways_B.append(hw)
        if len(headways_B) > 0:
            avg_hw_B_each_run.append(sum(headways_B) / len(headways_B))
        else:
            avg_hw_B_each_run.append(0.0)

    # Print statistics for 5, 10, 15, 20 replications
    for n in [5, 10, 15, 20]:
        subset = avg_hw_B_each_run[:n]
        mean_n = statistics.mean(subset)
        stdev_n = statistics.pstdev(subset)
        print(f"First {n} simulations: Mean = {mean_n:.2f}, Std Dev = {stdev_n:.2f}")

    # (c) Convergence of mean and variance
    cum_means = []
    cum_vars = []
    for i in range(1, total_runs + 1):
        subset = avg_hw_B_each_run[:i]
        mu = statistics.mean(subset)
        if i > 1:
            var = statistics.pvariance(subset)
        else:
            var = 0.0
        cum_means.append(mu)
        cum_vars.append(var)

    # Mean convergence plot
    plt.figure()
    plt.plot(range(1, total_runs + 1), cum_means, marker='o')
    plt.xlabel("Number of replications")
    plt.ylabel("Mean of B-departure Headway (min)")
    plt.title("Part (c): Mean vs. # of replications (B-departure)")
    plt.grid(True)
    plt.show()

    # Variance convergence plot
    plt.figure()
    plt.plot(range(1, total_runs + 1), cum_vars, marker='o')
    plt.xlabel("Number of replications")
    plt.ylabel("Variance of B-departure Headway (min^2)")
    plt.title("Part (c): Variance vs. # of replications (B-departure)")
    plt.grid(True)
    plt.show()

    return avg_hw_B_each_run


def part_optional_no_passing(sim_hours=5, replications=20):
    """
    (Optional +20 pts)
    If overtaking is not allowed, run 20 replications and compute the
    mean and standard deviation of B-departure headways.
    """
    avg_hw_B_no_passing = []

    for r in range(replications):
        _, departureB = run_single_simulation(sim_hours=sim_hours, no_passing=True)
        headways_B = []
        for i in range(1, len(departureB)):
            headways_B.append(departureB[i] - departureB[i - 1])
        if len(headways_B) > 0:
            avg_hw_B_no_passing.append(sum(headways_B) / len(headways_B))
        else:
            avg_hw_B_no_passing.append(0.0)

    mean_val = statistics.mean(avg_hw_B_no_passing)
    stdev_val = statistics.pstdev(avg_hw_B_no_passing)
    return mean_val, stdev_val


if __name__ == "__main__":
    # (a)
    print("=== Part (a) ===")
    hour_avgA = part_a(sim_hours=5)
    print("Hourly average departure headway at A (minutes):", hour_avgA)

    # (b) & (c)
    print("\n=== Part (b) & (c) ===")
    part_b_and_c(sim_hours=5, total_runs=20)

    # (Optional +20 pts)
    print("\n=== Optional: No passing ===")
    mean_np, stdev_np = part_optional_no_passing(sim_hours=5, replications=20)
    print(f"No passing case (20 runs): Mean = {mean_np:.2f}, Std Dev = {stdev_np:.2f}")
