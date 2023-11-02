"""CSC148 Assignment 1 - Simulation

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This contains the main Simulation class that is actually responsible for
creating and running the simulation. You'll also find the
 function run_example_simulation
here at the bottom of the file, which you can use as a starting point to run
your simulation on a small configuration.

Note that we have provided a fairly comprehensive list of attributes for
Simulation already. You may add your own *private* attributes, but should not
modify/remove any of the existing attributes.
"""
# You MAY import more things from these modules (e.g., additional types from
# typing), but you may not import from any other modules.
from typing import Any
from python_ta.contracts import check_contracts

import a1_algorithms
from a1_entities import Person, Elevator
from a1_visualizer import Direction, Visualizer


@check_contracts
class Simulation:
    """The main simulation class.

    Instance Attributes:
    - arrival_generator: the algorithm used to generate new arrivals.
    - elevators: a list of the elevators in the simulation
    - moving_algorithm: the algorithm used to decide how to move elevators
    - num_floors: the number of floors
    - visualizer: the Pygame visualizer used to visualize this simulation
    - waiting: a dictionary of people waiting for an elevator, where:
        - The keys are floor numbers from 1 to num_floors, inclusive
        - Each corresponding value is the list of people waiting at that floor
          (could be an empty list)

    Representation Invariants:
    - len(self.elevators) >= 1
    - self.num_floors >= 2
    - list(self.waiting.keys()) == list(range(1, self.num_floors + 1))
    """
    arrival_generator: a1_algorithms.ArrivalGenerator  # done
    elevators: list[Elevator]  # done
    moving_algorithm: a1_algorithms.MovingAlgorithm  # done
    num_floors: int  # done
    visualizer: Visualizer  # done
    waiting: dict[int, list[Person]]  # done

    def __init__(self,
                 config: dict[str, Any]) -> None:
        """Initialize a new simulation using the given configuration.

        Preconditions:
        - config is a dictionary in the format found on the assignment handout
        - config['num_floors'] >= 2
        - config['elevator_capacity'] >= 1
        - config['num_elevators'] >= 1

        A partial implementation has been provided to you; you'll
         need to finish it!
        """

        # Initialize the algorithm attributes (this is done for you)
        self.arrival_generator = config['arrival_generator']
        self.moving_algorithm = config['moving_algorithm']

        # Initialize elevators by creating each elevator instance (James)
        self.elevators = []
        for new_elevator in range(config['num_elevators']):
            capacity = config['elevator_capacity']
            new_elevator = Elevator(capacity)
            self.elevators.append(new_elevator)

        self.num_floors = config['num_floors']

        # Initialize self.waiting with empty list
        # of people for each floor (James)
        self.waiting = {}
        for floor in range(1, self.num_floors + 1):
            self.waiting[floor] = []

        # Initialize the visualizer (this is done for you).
        # Note that this should be executed *after* the other attributes
        # have been initialized, particularly
        # self.elevators and self.num_floors.
        self.visualizer = Visualizer(self.elevators, self.num_floors,
                                     config['visualize'])

    ############################################################################
    # Handle rounds of simulation.
    ############################################################################
    def run(self, num_rounds: int) -> dict[str, int]:
        """Run the simulation for the given number of rounds.

        Return a set of statistics for this simulation run, as specified in the
        assignment handout.

        Preconditions:
        - num_rounds >= 1
        - This method is only called once for each Simulation instance
            (since we have not asked you to "reset" back to the initial simulation state
            for this assignment)
        """
        for i in range(num_rounds):
            self.visualizer.render_header(i)

            # Stage 1: elevator disembarking
            self.handle_disembarking()

            # Stage 2: new arrivals
            self.generate_arrivals(i)

            # Stage 3: elevator boarding
            self.handle_boarding()

            # Stage 4: move the elevators
            self.move_elevators()

            # Stage 5: update wait times
            self.update_wait_times()

            # Pause for 1 second
            self.visualizer.wait(1)

        # The following line waits until the user closes the Pygame window
        self.visualizer.wait_for_exit()

        return self._calculate_stats()

    def handle_disembarking(self) -> None:
        """Handle people leaving elevators.

        Hints:
        - You shouldn't loop over a list (e.g. elevator.passengers) and mutate
        it within the
          loop body. This will cause unexpected behaviour due to how Python
          implements looping!
        - It's fine to reassign elevator.passengers to a new list. If you do so,
          make sure to call elevator.update() so that the new "fullness"
           of the elevator
          gets visualized properly.
        """

    def generate_arrivals(self, round_num: int) -> None:
        """Generate and visualize new arrivals."""
        new_arrival = self.arrival_generator.generate(round_num)
        self.visualizer.show_arrivals(new_arrival)
        for floor in new_arrival:
            for person in new_arrival[floor]:
                if person not in self.waiting[floor]:
                    self.waiting[floor].append(person)

    def handle_boarding(self) -> None:
        """Handle boarding of people and visualize."""
        for floor in range(1, self.num_floors + 1):
            waiting_person = self.waiting[floor]
            for elevator in self.elevators:
                for person in waiting_person:
                    if elevator.current_floor == person.start and elevator.fullness() < 1.0 \
                            and elevator.target_floor <= person.target:
                        elevator.add_passenger(person)
                        waiting_person.remove(person)
                        self.visualizer.show_boarding(person, elevator)

    def move_elevators(self) -> None:
        """Update elevator target floors and then move them."""

    def update_wait_times(self) -> None:
        """Update the waiting time for every person waiting in this simulation.

        Note that this includes both people waiting for an elevator AND people
        who are passengers on an elevator. It does not include people who have
        reached their target floor.
        """
        for floor in self.waiting:
            for person in self.waiting[floor]:
                person.wait_time += 1
        for elevator in self.elevators:
            for person in elevator.passengers:
                person.wait_time += 1

    ############################################################################
    # Statistics calculations
    ############################################################################
    def _calculate_stats(self) -> dict[str, int]:
        """Report the statistics for the current run of this simulation.

        Preconditions:
        - This method is only called after the simulation rounds have finished

        You MAY change the interface for this method (e.g., by adding new
         parameters).
        We won't call it directly in our testing.
        """
        return {
            'num_rounds': 0,
            'total_people': 0,
            'people_completed': 0,
            'max_time': 0,
            'avg_time': 0
        }


###############################################################################
# Simulation runner
###############################################################################
def run_example_simulation() -> dict[str, int]:
    """Run a sample simulation, and return the simulation statistics.

    This function is provided to help you test your work. You MAY change it
    (e.g., by changing the configuration values) for further testing.
    """
    num_floors = 6
    num_elevators = 2
    elevator_capacity = 2

    config = {
        'num_floors': num_floors,
        'num_elevators': num_elevators,
        'elevator_capacity': elevator_capacity,
        'arrival_generator': a1_algorithms.SingleArrivals(num_floors),
        'moving_algorithm': a1_algorithms.EndToEndLoop(),
        'visualize': True
    }

    sim = Simulation(config)
    stats = sim.run(15)
    return stats


if __name__ == '__main__':
    # We haven't provided any doctests for you
    # , but if you add your own the following
    # code will run them!
    import doctest
    doctest.testmod()

    # Uncomment this line to run our sample simulation (and print the
    # statistics generated by the simulation).
    sample_run_stats = run_example_simulation()
    print(sample_run_stats)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['a1_entities', 'a1_visualizer', 'a1_algorithms'],
        'max-nested-blocks': 4,
        'max-attributes': 10,
        'max-line-length': 100
    })
