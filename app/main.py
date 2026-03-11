import time
from app.cleanup import run_cleanup


RUNS_PER_CYCLE = 3
PAUSE_SECONDS = 300


def main():

    cycle = 1

    while True:

        print(f"\n=== CYCLE {cycle} START ===\n")

        work_done = False

        for run in range(1, RUNS_PER_CYCLE + 1):

            print(f"\n--- Batch Run {run} ---\n")

            result = run_cleanup()

            if result:
                work_done = True
            else:
                print("\nNo more emails to process.")
                print("Cleanup complete.")
                return

        if not work_done:
            print("No work detected. Stopping.")
            return

        print("\nCycle complete.")
        print(f"Pausing for {PAUSE_SECONDS} seconds...\n")

        time.sleep(PAUSE_SECONDS)

        cycle += 1


if __name__ == "__main__":
    main()