# Remote Texture
automatic downloading of textures from the internet, for autodesk maya

###Installation

* Download, unzip and move the file "remote-texture" into your maya scripts directory.
* Create a shelf icon and add the following PYTHON code:

``` python
import remote_texture
```

You're done!

Click your shelf icon when you start up Maya, and the tool will run in the background untill you next close Maya.

###To use the tool, it is very simple.

* Go onto your favourite search engine and find a picture you want. 
* Grab copy the web address of the image. Be sure it ends in .jpg .png .gif etc.
* Create or modify an existing texture. In the "file" node where you would normally place a local image as the texture, paste the web address. OPTIONAL: If you open the script editor you can see the download happening. Once downloaded your texture will show up.

If the image does not show up. Check your script editor for information. It may be that your web address does not work.

Enjoy! :)
