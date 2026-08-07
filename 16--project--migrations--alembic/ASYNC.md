# Asynchronous Programming

## Why FastAPI is fast

One of the main reasons behind FastAPI's excellent performance 
is its built-in support for asynchronous programming.

When handling an HTTP request, an application often spends 
most of its time waiting for I/O operations to complete,
such as database queries, external API calls, or file access. 
During this waiting period, the CPU remains mostly idle.

In a synchronous application, the current thread is blocked until the operation finishes.

In an asynchronous application, however, control is returned to the event loop 
while the application waits for the I/O operation to complete.
The event loop can then process other incoming requests,
allowing a single thread to serve many clients concurrency.

The event loop does not distribute coroutines across multiple threads.
Instead, it manages many coroutines within a single thread,
switching between them whenever a coroutine reaches an `await` expression.

This is why FastAPI achieves very high throughput and, in *I/O-bound* applications,
deliver performance comparable to platforms built around asynchronous execution, such as Node.js.
In many real-world scenarios, it can also approach the performance of services written in Go,
although the actual results always depend on the workload.

It is important to understand that asynchronous programming does not make individual operation faster.
Instead, it makes much more efficient use of waiting time, 
allowing the application to handle significantly more concurrent requests.

## Asynchronous Programming vs. Multithreading

Although both asynchronous programming and multithreading allow an application to handle multiple tasks concurrently,
the use fundamentally different execution models.

- Asynchronous programming  uses a *single thread* to execute many coroutines.
  The event loop cooperatively switches between coroutines whenever they suspend execution with `await`,
  typically while waiting for I/O operations to complete.

- Multithreading uses *multiple threads*, each with its own call stack.
  Threads may run in parallel depending on the operating system and the Python implementation.

### When Asynchronous Programming Is More Effective

Asynchronous programming is particularly well suited for *I/O-bound* applications,
where tasks spend most of their time waiting for external resources:

- web applications that handle many simultaneous HTTP requests;
- database-intensive applications;
- services that communicate with external APIs
- applications performing network communication or file I/O;
- etc.

### When Multithreading Is More Effective

Multithreading is more appropriate when an application must execute *blocking synchronous code*
or perform multiple independent operations that cannot easily be expressed asynchronously:

- integrating with legacy synchronous libraries;
- running blocking operations without freezing the main thread;
- desktop applications that must keep the user interface responsive
  while background tasks are running;
- etc.


## Coroutines

In Python, asynchronous functions are declared with the `async` keyword:

```python
async def get_by_id(user_id: int) -> User:
    ...
```

An asynchronous function is called a *coroutine*.
Calling it does not execute the function immediately.
Instead, it returns a coroutine object that must be awaited.

The `await` keyword suspends the execution of the current coroutine 
until the awaited asynchronous operation completes:

```python
user: User = await get_by_id(1)
```

While the coroutine is waiting, the event loop is free to execute other coroutines.
This allows the application to continue serving other requests instead of blocking the current thread.

As a rule:

- Declare asynchronous functions `async def`.

- Call asynchronous functions with `await`.

- `await` can only be used inside another asynchronous function.
    
- The first coroutine is started by the application's runtime 
  (for example, `asyncio.run()`, Uvicorn, or `pytest-asyncio`).

Example:

```python
import asyncio

async def main():
    await do_work()

asyncio.run(main())
```

These components create the event loop and execute asynchronous code.
