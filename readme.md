### Features

Can be used to upload/download to one or multiple mediafire accounts. you can manage your files and storage in the accounts without manual login to a browser

The library uses selenium and mediafire api simultaneously for content. Due to Mediafire's current bot protection system, selenium is used in headless mode in the workaround login section, and the upload process is done through selenium running in the background while uploading, except for these functions, the mediafire api is used.

# Requirements for raspberry or non-display devices

```bash
#virtual screen
sudo apt-get -y install xvfb

#for headless mode
sudo apt-get install xorg xvfb gtk2-engines-pixbuf
sudo apt-get -y install dbus-x11 xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic xfonts-scalable

#optional
sudo apt-get -y install imagemagick x11-apps

#Apply
Xvfb -ac :99 -screen 0 1280x1024x16 & export DISPLAY=:99
```

## Available functions
+ mediafire.login(email, password), privileges to connect to a specific mediafire account
+ mediafire.upload(directory, file), is used to upload a file
+ mediafire.get_account_storage(), storage information of the logged in mediafire account is shown
+ mediafire.get_content(), all file and folder information of the logged in mediafire account is given as output
+ mediafire.download(file, target_directory, save_as, silent), used to download all mediafire files in public status, Values other than file are optional


# Usage

## First start

The functioning of the library depends on the mediafire.login() function, the functions associated with an account will not be available unless the login() function is used, so it is important to use mediafire.login() at the beginning

```python
Python 3.9.2 (default, Mar 12 2021, 04:06:34)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from mediafire import Mediafire as m
>>> mediafire = m()
>>> mediafire.login(email="test@example.com", password="1234")
Login to test@example.com
```

## Get account contents

The get_content function provides a detailed view of all files in the account, including which mediafire folder they are in, file sizes and download links.

```python
Python 3.9.2 (default, Mar 12 2021, 04:06:34)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from mediafire import Mediafire as m
>>> mediafire = m()
>>> mediafire.login(email="test@example.com", password="1234")
>>> mediafire.get_content()
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
```


## Get account storage

The get_account_storage function shows the storage data for the currently entered mediafire account

```python
Python 3.9.2 (default, Mar 12 2021, 04:06:34)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from mediafire import Mediafire as m
>>> mediafire = m()
>>> mediafire.get_account_storage()
{'total': 10737418240, 'used': 381311, 'empty': 10737036929}
```

## Upload a file

The upload function uploads the file depending on the parameters entered in the currently entered mediafire account. It is important to have a full file path, so you should be careful to use os.getcwd() if necessary

```python
Python 3.9.2 (default, Mar 12 2021, 04:06:34)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from mediafire import Mediafire as m
>>> import os
>>> mediafire = m()
>>> mediafire.upload(directory=os.getcwd(), file="screen.png")
/Your/path/screen.png Completed
>>> mediafire.get_content()
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

## Download a file

### A file can be downloaded in 3 different ways
#### filename
+ If the get_content() function was previously executed with the account containing this file, the function automatically writes all file data, including this file, into accounts.json. This way, even if you are working on multiple accounts, or even if no account is entered, all files in the account.json file can be downloaded just by filename
#### file download link
+ The file can be downloaded using the mediafire link to the file
#### file quick key
+ The file can be downloaded using the key called quick key of the file, you can learn the quick key data from the accounts.json file

### There are 4 parameters of the download function
### file
+ The parameter where you specify which file to download, file name, file link, quick key of the file can be entered
### target_directory
+ Parameter where you specify the directory to save the downloaded file, optional, by default it targets your current location
### save_as
+ If you want to decide the name of the file to be downloaded, you can use it, it is the person, if left blank the file will be saved with its own name.
### silent
+ It takes a boolean type value, the default value is False, if you want the file to download silently you can give the value True, by default the download status will be shown as a bar.

```python
Python 3.9.2 (default, Mar 12 2021, 04:06:34)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from mediafire import Mediafire as m
>>> mediafire = m()
>>> mediafire.download("bobtherobber2.swf")
bobtherobber2.swf 10% ███████████████▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞
```

## Accounts.json file

This file is automatically generated by the mediafire library. When a function of the library is executed, the response of the function is automatically saved in this file so that some functions can run faster without the need to run the function again, and can also be used externally by users
+ When the ```mediafire.get_account_storage()``` function is executed, the storage data for the account is saved 
+ when the ````mediafire.get_content()``` function is executed, all folders and files belonging to the account are stored in a detailed format

!! email address and password are saved in the accounts.json file, pay attention when storing or sharing files

### accounts.json file example

```json
{
  "email@example.com": {
    "password": "password",
    "storage": {
      "total": 53664022528,
      "used": 47879737127,
      "space": 5784285401
    },
    "files": [
      {
        "filename": "bobtherobber2.swf",
        "filekey": "qr8cj6eff0mlkcz",
        "filehash": "7350b3ef64918b22496ca0eb0ee1d6da683fac8134ec8763a4e3dccf71352166",
        "path": "/myfiles/Flash Oyunlar/",
        "path_as_key": "/myfiles/smvbefe19ba0k/",
        "filetype": "video",
        "mimetype": "application/x-shockwave-flash",
        "size_as_byte": 8796739,
        "size_as_mb": 8.3892240524292,
        "link": "https://www.mediafire.com/file/qr8cj6eff0mlkcz/bobtherobber2.swf/file",
        "downloads": "0",
        "views": "0",
        "privacy": "public",
        "created_at": "2020-12-31 00:10:09"
      }
    ],
    "folders": [
      "/myfiles/Flash Oyunlar/"
    ]
  }
}
```


# Deep notes

+ Mediafire by its very nature may terminate a session after using a function, once the session is terminated the next function you use will automatically detect the session termination and continue the process by logging in again. 

+ This application was created for personal needs and then decided to be opened to the public, function/variable names or functions in the source code that may be deemed unnecessary may be removed or updated over time
