# Bologna
A tiny no-faff dependency injection module for python.

Bologna, formerly called tinyDI, is a tiny easy-to-use dependency injection library for python. 
This project has mainly evolved as a utility library for some
of my other projects, and is thus very utilitarian in its approach.
As the source code is only 100-ish lines, extending it is very easy.




## Usage

- Declare injectable dependencies with the `provide` function:

```python

from bologna import provide
from datetime import date

my_injectable_string = "Hello, DI. Today is"
my_injectable_object = date.today()

provide("greeting", my_injectable_string)
provide("thedate", my_injectable_object)
```
every injectable needs a unique name, which will be the function argument names.
 
- Mark functions that need to have arguments injected by the ´@inject´ annotation:

```python

from bologna import inject


@inject
def print_date(greeting=None, thedate=None):
    print(f"{greeting}; {thedate}")


print_date()
# prints 'Hello, DI. Today is; 2022-07-21'
```


## Features
What is included:

- Async function support


What is **not** included:

- Lazy evaluation
- Singletons
- ...And pretty much any other feature that is included in most full-fledged DI packages.


## Building and contributing
This project is built with `poetry` on 3.9.

To build, clone the repo and run `poetry install`. To run the tests, run `poetry run pytest`, to package, run `poetry build`.


## License
MIT license
```
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
```
