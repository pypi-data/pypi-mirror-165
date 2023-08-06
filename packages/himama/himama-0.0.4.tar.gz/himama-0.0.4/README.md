# himama: HiMama Downloader

Python/Selenium based utility in Python, to download 
pictures and videos offline.

# Installation

Install *Python 3.9* or Higher.

Run this in your Command Prompt or Terminal:

```shell
python -m pip install himama
```

Depending on which Operating System you use, the command could either be
`python3` or even `python3.9`.

Now download and install a supported WebDriver. Currently it
tries to use:

- [Mac - Safari Driver](https://technical-qa.com/how-do-i-enable-safaridriver/)
- [Windows - Edge Driver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
- [All - Firefox Gecko Driver](https://github.com/mozilla/geckodriver/releases)
- [All - Chrome Driver](https://chromedriver.chromium.org/downloads)
- [All - Opera Driver](https://github.com/operasoftware/operachromiumdriver/releases)

If you are running Linux, there may already be a package for your system
and you may want to install it through your package manager.

and level of support may vary from time to time.

# Usage

To Download, run:

```shell
himama
```

To run non-interactively such as a Cron Script, set these variables
in your environment.

```shell
set HIMAMA_USER=daddy@daddy.com
set HIMAMA_PASSWORD=changeMe
```

It needs a non-headless mode, or a virtual display to run.

# Questions and Feedback

I wrote this in my spare time. All feedback and patches welcome.
