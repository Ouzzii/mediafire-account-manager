### Features

Can be used to upload/download to one or multiple mediafire accounts. you can manage your files and storage in the accounts without manual login to a browser

# Requirements for raspberry or non-display devices

```bash
#virtual screen
sudo apt-get -y install xvfb

#for headless mode
sudo apt-get install xorg xvfb gtk2-engines-pixbuf
sudo apt-get -y install dbus-x11 xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic xfonts-scalable

#optional
sudo apt-get -y install imagemagick x11-apps

#save changes permanently
Xvfb -ac :99 -screen 0 1280x1024x16 & export DISPLAY=:99
```

# Usage

```python
Python 3.9.2 (default, Mar 12 2021, 04:06:34)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from mediafire import Mediafire as m
>>> import os
>>> mediafire = m()
>>> mediafire.login(email="test@example.com", password="1234")
Login to test@example.com
>>> mediafire.get_account_storage()
{'total': 10737418240, 'used': 381311, 'empty': 10737036929}
>>> mediafire.get_file_info()
[
	{
		'url': 'https://www.mediafire.com/file/k3ejksiznbnj2p/MediaFire_-_Getting_Started.pdf/file', 
		'name': 'MediaFire - Getting Started.pdf', 
		'source': 'https://download2363.mediafire.com/9a4j3nxibtvgAuXTInGEWl-0Y-WUxHC39PHciCBAdzHirW_OiWrbDt1In_04f41Wt87Kl3tSUQAeXUI-p7GfnDB7d2RLlBG-crD7VLK0Q1TUWJQNi5qVPs6_mGJG7STaPXBkwQyhEobuIaz5DxoHpGjTBbAPEBQcd8qIe1ZbaBU0wQ/kejksiznbnj2pt/MediaFire+-+Getting+Started.pdf', 
		'filesize': '381311', 
		'email': 'test@example.com', 
		'password': '1234'
	}
]
>>> mediafire.upload(directory=os.getcwd(), file="screen.png")
/Your/path/screen.png Completed
>>> mediafire.get_file_info()
[
	{
		'url': 'https://www.mediafire.com/file/k3ejksiznbnj2p/MediaFire_-_Getting_Started.pdf/file', 
		'name': 'MediaFire - Getting Started.pdf', 
		'source': 'https://download2363.mediafire.com/635my5nzteegvJdy_Bv95TCYj-DU0z3vb_y8HVTFdIy8Ez1tdlfBPG7d-BBE_GcW3Wo87BtNZhQ6FFst0hvXNx_A4gZxam5qG2jTtH1pIshFh3-h7puy4kJTWj9gCwxNE8i9ifj1MFgWUa-23XsR8zLL26enNJ_71JLYS0g4w1CntQ/kejksiznbnj2pt/MediaFire+-+Getting+Started.pdf', 
		'filesize': '381311', 
		'email': 'test@example.com', 
		'password': '1234'
	}, 
	{
		'url': 'https://www.mediafire.com/file/kv5qfjsacywxkf/screen.png/file', 
		'name': 'screen.png', 
		'source': 'https://download1594.mediafire.com/1b9wye6gjtvgPqABqkYzAWJeZpC5CyTrNM1b4guM0BdVHjvRMmJ6bFumcYdT_oRSudbKA17T-mJlKYLZpLVORfbczf9VjquDw05ssp0SrpLqzR2l78tPKqnvSqUDPw-gWwyUXi836DuHV8sFbgymlDlCTyj3kjNQK_mR5GJiM5FaFQ/kv5qfjsacywxkfr/screen.png', 
		'filesize': '6148', 
		'email': 'test@example.com', 
		'password': '1234'
	}
]

```

# Deep notes

+ Mediafire by its very nature may terminate a session after using a function, once the session is terminated the next function you use will automatically detect the session termination and continue the process by logging in again. 

+ This application was created for personal needs and then decided to be opened to the public, function/variable names or functions in the source code that may be deemed unnecessary may be removed or updated over time
