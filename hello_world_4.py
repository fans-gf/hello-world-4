"""Minimal hello-world module for hello-world-4."""


def hello(name: str = "world") -> str:
    """Return a greeting for *name*."""
    name = name.strip()
    if not name:
        raise ValueError("name must not be empty")
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(hello())
