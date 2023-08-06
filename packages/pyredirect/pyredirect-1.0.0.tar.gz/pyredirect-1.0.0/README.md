# Install
* Linux
    > python3 -m pip install pyredirect
* Windows
    > python -m pip install pyredirect

# Author

**Discord** : *Lactua#1806*

**Github**: *[https://github.com/lactua](https://github.com/lactua)*

# Documentation

Before doing anything, import the class Redirection from the module.
```py
from pyredirect import Redirection
```

* ## Create a redirection

    To create a redirection, use the method **create** from the **Redirection** class.

    |Parameter|Type|Description|
    |:-|:-|:-|
    |name|string|The name of the redirection|
    |redirections|dictionnary|Redirections name and their url|

    Example :

    ```py
    from pyredirect import Redirection

    redirection = Redirection.create(
        name = 'name',
        redirections = {
            'default': 'https://google.com',
            'mozilla': 'https://youtube.com'
        }
    )
    ```

* ## Get a redirection

    To get a redirection init the **Redirection** class.

    |Parameter|Type|Description|
    |:-|:-|:-|
    |name|string|The name of the redirection|
    |secret_key|string|The secret key of the redirection that allows you to manage it|

    Example :

    ```py
    from pyredirect import Redirection

    redirection = Redirection(
        name = 'name',
        secret_key = 'wVXT8ZI81LzPPGp'
    )
    ```

* ## Delete a redirection

    To delete a redirection you must have a **Redirection object**.

    Example :

    ```py
    from pyredirect import Redirection

    redirection = Redirection(
        name = 'name',
        secret_key = 'wVXT8ZI81LzPPGp'
    )

    redirection.delete()
    ```
    or
    ```py
    from pyredirect import Redirection

    redirection = Redirection.create(
        name = 'name',
        redirections = {
            'default': 'https://google.com',
            'mozilla': 'https://youtube.com'
        }
    )

    redirection.delete()
    ```