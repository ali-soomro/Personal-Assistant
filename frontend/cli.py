"""CLI frontend for interacting with Personal Assistant backend."""

import requests

API = "http://127.0.0.1:8000/query"

def main() -> None:
    """Start the CLI REPL loop."""
    print("Personal Assistant CLI (type 'quit' to exit)")
    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting CLI.")
            break

        if user_input.lower() in {"quit", "exit"}:
            break

        try:
            response = requests.post(API, json={"user_input": user_input}, timeout=20)
            data = response.json()
        except Exception as exc:  # noqa: BLE001
            print(f"[error] {exc}")
            continue

        intent = data.get("intent", "?")

        if intent == "close_apps" and "classified" in data:
            print(f"[{intent}]")
            print("  Classified:")
            for app, cat in data["classified"].items():
                print(f"    {app}: {cat}")
            print(f"  Keeping: {', '.join(data['keeping'])}")
            print(f"  Closing: {', '.join(data['closing'])}")
            print(f"  Note: {data['note']}")
        else:
            # Fallback for stub intents and general responses
            print(f"[{intent}] {data.get('response', '')}")


if __name__ == "__main__":
    main()