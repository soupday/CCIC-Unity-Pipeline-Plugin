# CC/iClone Unity Pipeline Plugin
**(Installed in CC5 / CC4 and iClone 8)**

**This plugin is for Character Creator 5, Character 4 and iClone 8**

This is a python plugin for Character Creator and iClone to facilitate the export of characters, props, lights, cameras and their animations to Unity.

Installation
============

### Upgrading
- **Important**: Remove **all** previous versions of this plug-in from the OpenPlugin folder.
    - Existing previous versions will cause conflicts with the current version and it _will not_ work correctly.
- Follow the Manual Installation procedure below.

### Automatic Installation
- Run the Install.bat to install the plugin automatically into CC5, CC4 and iClone8.

### Manual Installation
- Download the Zip file (__CCiC-Unity-Pipeline-Plugin-main.zip__) from the [**Code** button](https://github.com/soupday/CCiC-Unity-Pipeline-Plugin/archive/refs/heads/main.zip).
- Unzip the zip file. There should be a folder: **CCiC-Unity-Pipeline-Plugin-main**
- Create the folder **OpenPlugin** in the <Character Creator 4 install directory>**\Bin64\OpenPlugin**
    - e.g: **C:\Program Files\Reallusion\Character Creator 4\Bin64\OpenPlugin**
- Copy or move the folder CC4-Unity-Tools-Plugin-main into the **OpenPlugin** folder.
    - e.g: **C:\Program Files\Reallusion\Character Creator 4\Bin64\OpenPlugin\CC4-Unity-Tools-Plugin-main**
- The plugin functionality can be found from the menu: **Plugins > Unity Pipeline**

### Run Without Installing
- Alternatively the main.py script can run as a standalone script from the **Script > Load Python** menu.

Troubleshooting
===============

If after installing this plugin the plugin menu does not appear in Character Creator:

- Make sure your version of Character Creator / iClone is up to date.
- If the plugin still does not appear it may be that the Python API did not installed correctly and you may need to re-install Character Creator from the Reallusion Hub.

Links
=====

[CC/iC Unity Tools Discussion Thread](https://discussions.reallusion.com/t/unity-auto-setup/12570/1)

Changelog
=========

### 2.2.2
- Send buttons disabled when waiting for remote response.
- Relink will sync selected characters Link ID back to CC/iC.

### 2.2.1
- Spotlight error fix.

### 2.2.0
- Shader name fix.

### 2.1.1
- Re-link function added.
- Send motions allowed when character not present in Unity.
- Camera switch data fix to camera exports.
- Frame Rate export options added.

### 2.1.0
- First release
