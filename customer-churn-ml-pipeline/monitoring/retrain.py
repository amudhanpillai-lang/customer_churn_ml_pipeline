# Import subprocess
import subprocess
import sys


# Retrain model
def main():

    # Execute training module
    subprocess.run(
        [sys.executable, "-m", "src.train"],
        check=True
    )

    print("Model retraining completed.")


if __name__ == "__main__":
    main()