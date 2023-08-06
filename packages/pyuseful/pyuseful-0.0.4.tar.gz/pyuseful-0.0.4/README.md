# pyuseful

The package contains a collection of tools I find useful. Check out [wiki](https://github.com/sikvelsigma/pytools-utils/wiki) page for more detail and examples.
# Install
Requires python 3.9

```
pip install pyuseful
```

# General info

Consists of several sub-packages:
- `classtools`

    ---

    - immutable
        - <kbd>class</kbd> `ImmutableProperties`

            Makes class propreties immutable
    ---
    - message
        - <kbd>class</kbd> `MessageThread`

            Creates a separate thread which prints messeges in queue
    ---
    - postint
        - <kbd>class</kbd> `PostInit`

            Adds a call to `__postinit__` method after init is complete
    ---
    - require
        - <kbd>class</kbd> `RequireAttrs`

            Adds attribute `require` which forces you to set listed attributes by the end of init

        - <kbd>class</kbd> `RequireDictParser`

            Parses `dict` or `json` file into a class and make attributes from keys. Adds attribute `require` and `require_any` which force you to set listed attributes by the end of init



- `decorators`

    ---

    - require

        - <kbd>decorator</kbd> `require_condition`

            Let's you specify a condition in which a method of a class can be called

        - <kbd>decorator</kbd> `once`

            Function can only be called once or it always returns the same result as the 1st call

        - <kbd>decorator</kbd> `limit`

            Limits a number of times a function can be called
    ---
    - thread
        - <kbd>decorator</kbd> `repeat_timer`

        Repeat a function every `timer` number of seconds. Returns a `Queue`-like object with results
    ---
    - timing
        - <kbd>decorator</kbd> `time_exec`

            Messure exec time of a function



- `filetools`

    ---

    - misc
        - <kbd>function</kbd> `mod_name_with_ext`

            Modify a path without modifying an extention
    ---
    - splicer
        - <kbd>class</kbd> `Splicer`

            Let's you specify blocks in files which can be pasted into other files
