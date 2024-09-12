<p align="center">
    <a>
        <img src="https://raw.githubusercontent.com/gri-gus/proxymanager-streamdeck-plugin/main/assets/git_cover.png" 
        alt="proxymanager-streamdeck-plugin">
    </a>
</p>

# proxymanager-streamdeck-plugin

Stream Deck plugin for enabling and disabling proxies on MacOS.

## Requirements

**Operating systems:**

* MacOS: 10.14 or later

**Stream Deck application:** 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7

**Python:** 3.8 or later

## Features

* Supports `http`, `https` and `socks` proxies.
* The color of the button changes depending on its state.

## Installation

### Python

> If you have difficulty, then look at articles or videos on the Internet about it.

1. Download Python from the official website and install it: https://www.python.org/downloads/

   > ⚠️ Python version must be 3.8.0 or later.


2. Check that Python is available from the command line:

   <details><summary>MacOS</summary>

   Open the `Terminal` application, enter the command below and press Return(Enter):

   ```shell
   python3 -V
   ```

   If you get a response that looks like `Python 3.10.4`, then you have done everything right.

   If there is no response, then you have installed Python incorrectly.

   </details>

   <details><summary>Windows</summary>

   Open the `Command Prompt` application, enter the command below and press Return(Enter):

   ```shell
   python -V
   ```

   If you get a response that looks like `Python 3.10.4`, then you have done everything right.

   If there is no response, then you have installed Python incorrectly.

   </details>

3. Restart your computer.

### Stream Deck

Download the Stream Deck app from the official website and install it: https://www.elgato.com/en/downloads

### Proxy Manager Stream Deck Plugin

> ⚠️ During the installation of the plugin, you must have internet access.

> Errors may occur during installation. If they are, then a message about it will appear on the screen.

Latest release: https://github.com/gri-gus/proxymanager-streamdeck-plugin/releases

You need to download a file called `com.ggusev.proxymanager.streamDeckPlugin`. Once downloaded, double-click on it. The
Stream Deck application prompts you to install the plugin.

After installation, you will have a `Network` category and actions.

> ⚠️ The button may not start working immediately after installing the plugin, but after about 40 seconds. At this time,
> dependencies are installed. If you do not receive an error message on the screen, but an exclamation mark is displayed
> when you click on the button, then the plugin is not fully installed yet, and you need to wait. This only happens
> after installing the plugin. There is no need to wait for the next use.

## Dependencies

[streamdeck-python-sdk](https://github.com/gri-gus/streamdeck-python-sdk)

[streamdeck-javascript-sdk](https://github.com/elgatosf/streamdeck-javascript-sdk)
