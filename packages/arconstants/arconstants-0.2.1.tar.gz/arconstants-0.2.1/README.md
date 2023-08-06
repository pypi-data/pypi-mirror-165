# ApolloRoboto.Constants

This is a utility library containing a collection of constant numbers making them easy to access and
explore. This repository aims at generating source codes to multiple languages and publish them.

It's a learning project, my main motivation was to explore the chalenges of code generation and
publishing them to multiple code repotitory.

## Currently Supported Language:
- C# - [Nuget](https://www.nuget.org/packages/ApolloRoboto.Constants)

## C# Example Usage: 
```c#
using System;
using static ApolloRoboto.Constants.Math;

public class Program
{
	public void Main(string[] args)
	{
		Console.WriteLine(PI * GOLDEN_RATIO)
	}
}
```

## Contributing

Workflows are configured to regenerate and publish code at each changes.

All constant numbers are declared in the `constants.yaml` file.

To generate the code locally, use the `generate.py` script
```bash
python ./generate.py
```

If you make a pull request, please increment the version number in `meta.yaml` by `0.0.1`