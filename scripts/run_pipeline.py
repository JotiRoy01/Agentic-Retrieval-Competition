from pathlib import Path

if __name__ == "__main__" :
    current = Path(__file__).resolve()
    resolve = current.parent
    print(f"currunt path: {current}")
    print(f"resolve path: {resolve}")