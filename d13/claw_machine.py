import os


def parse_input(file_path, machine_number):
    """
    Parse the input file to extract coefficients for a specific machine.

    Args:
        file_path (str): Path to the input file.
        machine_number (int): Machine number to parse.

    Returns:
        tuple: Coefficients (a1, b1, c1, a2, b2, c2) for the equations.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError("Error: Unable to open file.")

    with open(file_path, "r") as file:
        lines = file.read().splitlines()

    current_machine = 0
    for i in range(0, len(lines), 4):  # Each machine has 4 lines (Button A, Button B, Prize, blank line)
        if current_machine == machine_number:
            # Parse Button A coefficients
            line = lines[i]
            a1, b1 = map(int, line.replace("Button A: X+", "").replace("Y+", "").split(", "))

            # Parse Button B coefficients
            line = lines[i + 1]
            a2, b2 = map(int, line.replace("Button B: X+", "").replace("Y+", "").split(", "))

            # Parse Prize coordinates
            line = lines[i + 2]
            c1, c2 = map(int, line.replace("Prize: X=", "").replace("Y=", "").split(", "))

            return a1, b1, c1, a2, b2, c2

        current_machine += 1

    raise ValueError(f"Machine number {machine_number} is out of range.")


def cramers_solution(a1, b1, c1, a2, b2, c2):
    """
    Solve the system of linear equations using Cramer's Rule.

    Args:
        a1, b1, c1, a2, b2, c2 (int): Coefficients of the equations.

    Returns:
        tuple: (x, y) if the solution exists, otherwise (None, None).
    """
    determinant = a1 * b2 - a2 * b1

    if determinant == 0:
        return None, None  # No solution or infinitely many solutions

    x = (c1 * b2 - c2 * b1) // determinant
    y = (a1 * c2 - a2 * c1) // determinant

    if x < 0 or y < 0 or x > 100 or y > 100:
        return None, None

    return x, y


def count_machine_tokens(x, y):
    """
    Calculate the number of tokens required.

    Args:
        x, y (int): Number of times Button A and Button B are pressed.

    Returns:
        int: Total tokens required, or 0 if no valid solution.
    """
    if x is None or y is None:
        return 0  # No valid solution
    return 3 * x + y


def solve_machine(file_path, machine_number):
    """
    Solve for the number of tokens required for a specific machine.

    Args:
        file_path (str): Path to the input file.
        machine_number (int): Machine number.

    Returns:
        int: Number of tokens required for the machine.
    """
    a1, b1, c1, a2, b2, c2 = parse_input(file_path, machine_number)
    x, y = cramers_solution(a1, b1, c1, a2, b2, c2)
    return count_machine_tokens(x, y)


def main():
    file_path = "input.txt"  # Path to the input file
    log_file = "output.log"  # Path to the output log file
    total_tokens = 0
    prizes = 0
    machines = []

    with open(log_file, "w") as log:
        log.write("Machine Results:\n")
        log.write("=================\n")
        
        # Assuming 320 machines in the input
        for machine_number in range(320):
            tokens = solve_machine(file_path, machine_number)
            if tokens > 0:  # Machine gives a prize
                total_tokens += tokens
                prizes += 1
                machines.append(machine_number)
                
                # Log to file
                log.write(f"Machine {machine_number}: Tokens required = {tokens}\n")
        
        # Write summary to log file
        log.write("\nSummary:\n")
        log.write("=================\n")
        log.write(f"Total tokens required: {total_tokens}\n")
        log.write(f"Total number of prizes: {prizes}\n")

    # Print summary to console
    print("Total tokens required:", total_tokens)
    print("Total number of prizes:", prizes)
    print(f"Detailed results saved to {log_file}")


if __name__ == "__main__":
    main()
