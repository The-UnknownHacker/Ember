# Ember Language Install Guide

Welcome to Ember! Follow the steps below to install and set up the Ember command-line tool on your system.

## Prerequisites

Make sure you have the following installed on your system:

- **Homebrew**: If you don't have Homebrew installed, you can install it by running:

    ```
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

## Installation Steps

### Step 1: Tap the Ember Repository

Run the following command to tap the Ember repository:

```
brew tap The-UnknownHacker/Ember
```

### Step 2: Install the Ember Interpreter

After successfully tapping the repository, you can install the Ember interpreter using the following command:

```
brew install ember
```

### Step 3: Verify Installation

To confirm that the installation was successful, you can check the version of the Ember interpreter:

```
ember --version
```

### Step 4: Running an Ember Script

You can now run an Ember script with the following command:

```
ember script.em
```

Replace `script.em` with the name of your Ember script.

## Uninstallation

If you want to uninstall the Ember interpreter, you can do so with the following command:

```
brew uninstall ember
```

To remove the tap, use:

```
brew untap The-UnknownHacker/Ember
```

## Additional Resources

- [GitHub Repository](https://github.com/The-UnknownHacker/Ember)
- [Homebrew Documentation](https://docs.brew.sh)

## Support

If you encounter any issues or have questions, feel free to open an issue in the GitHub repository or contact the project maintainer.

Happy coding with Ember!
