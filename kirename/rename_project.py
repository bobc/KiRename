#
# rename a KiCad project
# 
# Usage: rename_project [-s <source>] [-d <dest>] [-t <tag>]
#
# Copyright Bob Cousins 2017
#
# Licensed under GPLv3
#
# version 1

version = "0.1 Beta"

import os, sys, re, shutil, errno, getopt
from datetime import datetime
from time import strftime

# handy methods from https://www.dotnetperls.com/between-before-after-python
def before(value, a):
    # Find first part and return slice before it.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    return value[0:pos_a]
    
def after(value, a):
    # Find and validate first part.
    pos_a = value.rfind(a)
    if pos_a == -1: return ""
    # Returns chars after the found string.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value): return ""
    return value[adjusted_pos_a:]

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def help(verbose):
    print 'rename_project.py [-s <source>] [-d <dest>] [-n <name> | -t <tag> ]'
    print
    print "Version %s - GPLv3 - Copyright Bob Cousins 2017" % version
    print '*** Beta test version: use with caution ***'
    print
    print 'rename a KiCad project'
    print
    print '-s               source directory (./)' 
    print '-d               destination directory (./)' 
    print '-n               new name' 
    print '-t               tag to add' 
    print '-x               dry run, do not change any files'
    print '-h | --help      show quick help | more help' 

    if verbose:
        print
        print 'Note: there must be only one project in source directory'
        print ''
        print 'Typical uses:'
        print ''
        print '1. Rename a project foo.pro to bar.pro' 
        print '$ rename_project -n new_name' 
        print ''
        print '2. Rename a project foo.pro to foo_v1.pro' 
        print '$ rename_project -t _v1' 
        print ''
        print '3. Rename a project foo.pro to /temp/bar.pro' 
        print '$ rename_project -d /temp -n bar' 
        print ''
        print '4. Rename a project foo.pro to /temp/foo_v1.pro' 
        print '$ rename_project -d /temp -t _v1' 
        print ''
        print '5. Rename a project foo.pro to ./YYYY-MM-DD_HH-MM-SS/foo.pro' 
        print '$ rename_project' 
        print ''
        print '6. Rename a project foo.pro to ./save1/foo.pro' 
        print '$ rename_project -d save1' 

#  destdir[_tag] / name[_tag]

#  destdir / name
#  destdir / name_tag

#  destdir_tag / name
#  destdir_tag / name_tag

# rename                    dest=src+date, name=project

# rename -t tag             dest=src,      name=project+tag
# rename -n name            dest=src,      name=name
# --
# rename -d dir             dest=src+dir,  name=project

# rename -d dir -t tag      dest=dir,      name=project+tag
# rename -d dir -n name     dest=dir,      name=name

## save [to date]
# rename -d 

## save [to tag]
# rename -d dir -t tag

def main(argv):

    mode = "none"
    new_name = ""
    sourcedir = ""
    suffix = ""
    destdir = ""
    recurse = False
    dry_run = False
    verbose = False
    overwrite = False

    try:
        opts, arg = getopt.getopt (argv,"s:d:n:t:hxv", ["help"])
    except getopt.GetoptError:
        help() 
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help(opt == "--help")
            sys.exit()
        elif opt in ("-s"):
            sourcedir = arg
        elif opt in ("-d"):
            destdir = arg
        elif opt in ("-t"):
            suffix = arg
        elif opt in ("-n"):
            new_name = arg
        elif opt in ("-x"):
            dry_run = True

    ## check args
    if sourcedir == "":
        sourcedir = os.getcwd()

    if not os.path.exists (sourcedir):
        print "error: %s is not a directory" % sourcedir
        quit()

    #
    top_level_files = [f for f in os.listdir(sourcedir) if os.path.isfile(os.path.join(sourcedir, f))]

    files = []
    if recurse:
        for root, dirnames, filenames in os.walk(sourcedir):
            for filename in filenames:
                # print os.path.join(after(root,sourcedir),filename)
                files.append ( os.path.join(after(root,sourcedir),filename) )
    else:
        files = [f for f in os.listdir(sourcedir) if os.path.isfile(os.path.join(sourcedir, f))]

    #
    # first find the project name

    project = ""
    for file in top_level_files:
        if file.endswith (".pro"):
        
            if project == "":
                project = before (file, ".pro")
            else:
                print "error: multiple projects found in %s" % sourcedir
                quit(1)

    if project == "":
        print "error: no project file found in %s" % sourcedir    
        quit(2)

    if destdir== "":
        if (suffix=="" and new_name==""):
            mode = "copy"
            destdir = os.path.join (sourcedir, strftime("%Y-%m-%d_%H-%M-%S"))
            new_name = project
        elif (suffix!="" and new_name!=""):
            print "error: must specify only one of name or tag"
            quit()
        elif suffix != "":
            mode = "rename"
            destdir = sourcedir
            new_name = project + suffix
        elif new_name != "":
            mode = "rename"
            destdir = sourcedir
            # new_name = new_name
    else:
        if (suffix=="" and new_name==""):
            mode = "copy"
            destdir = os.path.join(sourcedir, destdir)
            new_name = project
        elif (suffix!="" and new_name!=""):
            print "error: must specify only one of name or tag"
            quit()
        elif suffix != "":
            mode = "copy"
            # destdir = destdir
            new_name = project + suffix
        elif new_name != "":
            mode = "copy"
            # destdir = destdir
            # new_name = new_name
        


    ## 
    print "project name: %s" % project
    print "new project name: %s" % new_name
    print ""

    if dry_run:
        print "mode      : %s" % mode
        print "sourcedir : %s" % sourcedir
        print "destdir   : %s" % destdir
        print ""

    if dry_run:
        if not os.path.exists(destdir):
            print "create : %s" % destdir
    else:
        try:
            make_sure_path_exists (destdir)
        except:
            print "error creating dest folder %s" % destdir
            quit()

    try:
        # now copy files
        for file in files:
            if (file.endswith (".sch") or 
                file.endswith (".lib") or 
                file.endswith (".mod") or 
                file.endswith (".cmp") or 
                file.endswith (".brd") or 
                file.endswith (".kicad_pcb") or
                file.endswith (".pos") or 
                file.endswith (".net") or 
                file.endswith (".pro") or 
                file.endswith (".py") or 
                file.endswith (".pdf") or 
                file.endswith (".txt") or 
                file.endswith (".dcm") or 
                file.endswith (".kicad_wks") or 
                file == "fp-lib-table"):

                if file.startswith (project):
                    # copy with rename

                    source_file = os.path.join(sourcedir, file)
                    dest_file = os.path.join (destdir, new_name + after (file, project))
        
                    if dry_run:
                        print "rename : %s ==> %s" % (file, dest_file)
                    else:
                        if mode == "copy":
                            shutil.copy2 (source_file, dest_file)
                        else:
                            os.rename (source_file, dest_file)
                else:
                    if mode=="copy":
                        # straight copy
                        source_file = os.path.join(sourcedir, file)
                        dest_file = os.path.join (destdir, file)
                        if dry_run:
                            print "copy   : %s ==> %s" % (file, dest_file)
                        else:
                            shutil.copy2 (source_file, dest_file)

    except IOError as exception:
        print "error copying file %s : %s" % (exception.filename, exception.strerror)
        quit()


if __name__ == "__main__":
   main(sys.argv[1:])

