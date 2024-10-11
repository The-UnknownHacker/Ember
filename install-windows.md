# Ember Language Installation Guide for Windows

This guide will help you install and set up the Ember language on a Windows system.


# Important Notice

## Ember for windows is not official yet so it may break or not even work at all
## We are not responsible for any changes done to your system

## Prerequisites

Ensure that you have the following:

- **Python**: Since the Ember language relies on Python, you need Python installed.
  - You can download Python from the official site: [Python Downloads](https://www.python.org/downloads/)
  - During the installation, make sure to check the box that says "Add Python to PATH".

## Step 1: Download Ember Language Files

1. Go to the [Ember GitHub Releases](https://github.com/The-UnknownHacker/Ember/releases) page.
2. Download the latest release of the Ember language for Windows, which should include a `.zip` or `.exe` file.

## Step 2: Install Ember

If you downloaded a `.zip` file:

1. Extract the contents of the `.zip` file to a folder.
2. Inside the folder, you should find the necessary Ember files.

If you downloaded a `.exe` file:

1. Run the `.exe` file to install Ember.

## Step 3: Add Ember to Your PATH

1. Move the extracted Ember folder (or the location where the `.exe` installed it) to a directory on your system, such as:

    """
    C:\Program Files\ember\
    """

2. Add this directory to your system’s `PATH`:

   - Right-click **This PC** or **My Computer**, select **Properties**.
   - Click **Advanced system settings**.
   - Select **Environment Variables**.
   - In the **System variables** section, find **Path**, and click **Edit**.
   - Click **New** and enter the path to the folder where Ember is located (e.g., `C:\Program Files\ember\`).

   - Click **OK** to save your changes.

## Step 4: Verify Installation

To verify the installation, open **Command Prompt** and type:

```
ember --version
```

This should display the version of Ember you installed.

## Step 5: Running Ember Scripts

You can now run `.em` scripts using:

```
ember script.em
```

Replace `script.em` with the name of your Ember language script.

## Uninstallation

To uninstall, simply delete the Ember folder from your system and remove the entry from your system's `PATH`:

- Go to **Advanced system settings** > **Environment Variables**.
- Edit the **Path** variable and remove the Ember path entry.
- Click **OK** to save the changes.

## Additional Resources

- [Ember GitHub Repository](https://github.com/The-UnknownHacker/Ember)
- [Python Downloads](https://www.python.org/downloads/)
