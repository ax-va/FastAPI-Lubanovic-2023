# Testing

## Monkeypatch

- Monkeypatch replaces a real object with another real object.

- Use it when the code should continue working normally, but with a different implementation
  (e.g., an in-memory SQLite database).

## Mocker

- Mocker replaces an object with a `Mock`.

- Use it when you want to isolate the unit under test and verify interactions
  (`assert_called_once_with()`, `call_count`, `call_args`, etc.).