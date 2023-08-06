# discord.py Inter-process Communication (IPC)

<p style="text-align: center">
        <a href="https://github.com/Sn1F3rt/discord.py-ipc/actions?query=workflow%3AAnalyze+event%3Apush">
            <img alt="Analyze Status"
                 src="https://github.com/Sn1F3rt/discord.py-ipc/workflows/Analyze/badge.svg?event=push" />
        </a>
        <a href="https://github.com/Sn1F3rt/discord.py-ipc/actions?query=workflow%3ABuild+event%3Apush">
            <img alt="Build Status"
                 src="https://github.com/Sn1F3rt/discord.py-ipc/workflows/Build/badge.svg?event=push" />
        </a>
        <a href="https://discordpy-ipc.readthedocs.io/en/latest/?badge=latest">
            <img alt="Documentation Status"
                 src="https://readthedocs.org/projects/discordpy-ipc/badge/?version=latest" />
        </a>
</p>

## About

A discord.py extension for inter-process communication.

## Installation

Python **>=3.8.0** is required.

```py 
pip install --upgrade discord.py-ipc
```

## Links 

- [Documentation](https://discordpy-ipc.readthedocs.io)
- [Usage Examples](https://github.com/Sn1F3rt/discord.py-ipc/tree/main/examples)

## Support

![Discord Support](https://discord.com/api/guilds/957575152017764373/widget.png?style=banner2)

### Known Issues

- While simultaneously quering the IPC server, you may encounter a `Concurrent call to receive() is not allowed` error. I am aware of this and currently a fix is being implemented to address this issue. 

- If the IPC server is started as in the examples, the `ipc_ready` event wouldn't fire because the bot isn't ready (see [3745d65](https://github.com/Sn1F3rt/discord.py-ipc/commit/3745d65c8e2dbeeed5e8aa87a0d2f4e2ccc2df98)) which otherwise leads to a `RuntimeError`. Instead, you can start the server in the `on_ready` event of discord.py, however, in this case you need to install [nest-asyncio](https://pypi.org/project/nest-asyncio/) and add these two lines at the start of your main bot file (before `discord` imports).
    ```py
    import nest_asyncio
    nest_asyncio.apply()
    ```

## License

Copyright (c) 2022 Sn1F3rt  
Copyright (c) 2020-21 Ext-Creators
