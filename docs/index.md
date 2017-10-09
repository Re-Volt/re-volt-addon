# Re-Volt Add-On Documentation

This is the documentation for Marv's Add-On for Re-Volt files.  
It is intended to be used with **Blender 2.79**.

[**Download** (rva_17.1009)](https://github.com/Yethiel/re-volt-addon/archive/master.zip)

[**Changelog**](changelog/index.html)

[**Tutorial**](http://learn.re-volt.io)

## Documentation

[**Features**](features/index.html)  
A list of currently supported features and what's to come.

[**Installation**](installation/index.html)  
A guide for the installation of the add-on.

[**Tools Panel**](tools-panel/index.html)  
Explanations to the tools panel located on the left hand side of the 3D view.

**Properties**:

‣ [**Object Properties**](object-properties/index.html)  
&nbsp;&nbsp;&nbsp;&nbsp;Re-Volt object properties found in the Properties editor.

‣ [**Scene Properties**](scene-properties/index.html)  
&nbsp;&nbsp;&nbsp;&nbsp;Re-Volt scene (.w) properties.

‣ [**Import and Export**](import-export/index.html)  
&nbsp;&nbsp;&nbsp;&nbsp;Read how the add-on handles import and export (advanced).

## Known Issues

**<u>UV Unwrap Reset broken</u>**  
Not an issue with this add-on directly, however, there is a bug in Blender that is caused by a feature used by the add-on. I reported this bug and it has recently been fixed. The fix sadly didn't make it into 2.79 yet. **To obtain a version with the fix included, download Blender from [builder.blender.org](http://builder.blender.org)**.

**<u>Only one BigCube</u>**  
Only one sphere (BigCube) is written around the entire level. This shouldn't impact performance too much, _other add-ons_ didn't do this any better but a fix should come eventually.