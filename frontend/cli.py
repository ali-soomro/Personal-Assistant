"""CLI frontend for interacting with Personal Assistant backend."""

import requests


def main() -> None:
    """Start the CLI REPL loop."""
    print("Personal Assistant CLI (type 'quit' to exit)")
    while True:
        user_input = input("> ")
        if user_input.lower() in {"quit", "exit"}:
            break
        response = requests.post(
            "http://127.0.0.1:8000/query",
            json={"user_input": user_input},
            timeout=10
        )
        data = response.json()
        print(f"[{data['intent']}] {data['response']}")


if __name__ == "__main__":
    main()