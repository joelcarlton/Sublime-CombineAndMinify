# Sublime-CombineAndMinify

Combine a list of JavaScript files Into a single master and minified version

## Created

8/2013

### Version

1.0

## Release Notes

- Initial build

# Setting Up CombineAndMinify

In order to use CombineAndMinify your project must be saved to a .sublime-project. 

1. Click Project from Menu Bar
2. Click Save Project As
3. Name and Save
4. Click Project > Edit Project
5. Add Settings for CombineAndMinify
6. Save project file
7. Make files.txt with a list of files that should be processed at the location specified with FileList
8. Run by using key command, tools menu, right click menu, or command palette


##### Minimum Settings
```json
"Combine: FileList": "/files.txt",
"Combine: InPath": "/public/js/"
```

##### Template
```json
{
	"folders":
	[
		{
			"path": "/path/to/working/files"
		}
	],
	"settings":
	{
		# Add Settings Here
		"Combine: FileList": "/files.txt",
		"Combine: InPath": "/public/js/",
		"Combine: OutPath": "/private/js/",
		"Combine: MasterName": "master.js",
		"Combine: MinifyName": "master.min.js"
	}
}
```

##### files.txt

```txt
################ Comments Are Ignored ################
externaljs.js
externaljs2.js
```

##### Defaults

- FileList and InPath are required. 
- OutPath is not required and will default to InPath unlesss specified otherwise. 
- MasterName and MinifyName are not required and will resolve to master.js and master.min.js unlesss specified otherwise

# License

GNU GENERAL PUBLIC LICENSE Version 2, June 1991