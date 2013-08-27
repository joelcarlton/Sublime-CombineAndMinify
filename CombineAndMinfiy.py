# Plugin

import sublime as s
import sublime_plugin as sp


class BuildCommand(sp.TextCommand):
    def run(self, edit):
        def process(fileList, inPath, outPath, jsMaster, jsMinify):
            # FILE MANAGEMENT
            import os.path
            # SHELL
            #import subprocess
            # POST
            import urllib
            import urllib2
            # TIME
            import time

            jsMaster = outPath + jsMaster
            jsMinify = outPath + jsMinify

            # Clear screen for new run
            #subprocess.Popen('cmd')

            # Start script
            print '\nInitiating Minification'
            start = time.time()

            # Read in order file
            if os.path.isfile(fileList):
                order = open(fileList, 'r')

                # Create Array
                orderArray = []
                # Get List of files
                for line in order:
                    if not '#' in line:
                        # Remove newlines
                        if '\r' in line:
                            line = line.replace('\r', '')
                        if '\n' in line:
                            line = line.replace('\n', '')
                        # Add to array
                        orderArray.append(line)

                # Create Array
                masterArray = []
                # Get contents of files
                for entry in orderArray:
                    file = open(inPath + entry, 'r')
                    masterArray.append(file.read())

                # Check for old master then remove
                if os.path.isfile(jsMaster):
                    print 'Trashing Old Master File'
                    os.remove(jsMaster)

                # Create new master file
                master = open(jsMaster, 'a')
                # Add contents of files to master
                for i in masterArray:
                    master.write(i)

                # Close master and reopen for reading
                master.close()
                master = open(jsMaster, 'r')

                # Set up POST
                print 'Sending JavaScript for Minification'
                url = 'http://marijnhaverbeke.nl/uglifyjs'
                user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
                values = {'js_code': master.read()}
                headers = {'User-Agent': user_agent}
                data = urllib.urlencode(values)
                req = urllib2.Request(url, data, headers)
                response = urllib2.urlopen(req)

                # Add minified output to minify file
                print 'Saving Minified Version'
                minify = open(jsMinify, 'w')
                minify.write(response.read())

                # Clean up
                order.close()
                master.close()
                minify.close()

                # Calculate and display run time
                end = time.time()
                time = round(end - start, 2)
                print '\nOperation Compleated in ' + str(time) + ' seconds.\n'
                s.status_message('CombineAndMinify: Operation Compleated in ' + str(time) + ' seconds. Check ' + outPath + ' for new files.')
            else:
                print 'CombineAndMinify Build Failed: FileList Does Not Exist'
                s.status_message('CombineAndMinify Build Failed: FileList Does Not Exist')

        ########################## Begin ##########################
        print ''
        settings = s.load_settings('CombineAndMinfiy.sublime-settings')
        print 'CombineAndMinfiy Version: ' + settings.get('Version')
        print 'Build Initiated'
        s.status_message('CombineAndMinify Build Initiated')
        print ''

        # Load settings from project
        fileList = s.active_window().active_view().settings().get('Combine: FileList')
        inPath = s.active_window().active_view().settings().get('Combine: InPath')
        outPath = s.active_window().active_view().settings().get('Combine: OutPath')
        jsMaster = s.active_window().active_view().settings().get('Combine: MasterName')
        jsMinify = s.active_window().active_view().settings().get('Combine: MinifyName')

        # Check to see that user set up required project settings
        if fileList is None:
            print 'CombineAndMinify: "Combine: FileList" Project Path Setting not Set'
            s.status_message('CombineAndMinify: "Combine: FileList" Project Path Setting not Set')
        elif inPath is None:
            print 'CombineAndMinify: "Combine: InPath" Project Path Setting not Set'
            s.status_message('CombineAndMinify: "Combine: InPath" Project Path Setting not Set')
        else:
            # Check to see that user set up optional project settings
            if outPath is None:
                outPath = inPath
                # Notify User
                print 'CombineAndMinify: "Combine: OutPath" Project Path Setting not Set, using same as InPath'
                s.status_message('CombineAndMinify: "Combine: OutPath" Project Path Setting not Set, using same as InPath')
            if jsMaster is None:
                jsMaster = 'master.js'
                # Notify User
                print 'CombineAndMinify: "Combine: MasterName" Project Path Setting not Set, using "master.js"'
                s.status_message('CombineAndMinify: "Combine: MasterName" Project Path Setting not Set, using "master.js"')
            if jsMinify is None:
                jsMinify = 'master.min.js'
                # Notify User
                print 'CombineAndMinify: "Combine: MinifyName" Project Path Setting not Set, using "master.min.js"'
                s.status_message('CombineAndMinify: "Combine: MinifyName" Project Path Setting not Set, using "master.min.js"')
            process(fileList, inPath, outPath, jsMaster, jsMinify)
