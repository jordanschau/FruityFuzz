#!/usr/bin/env python

# FruityFuzz: The Mac Python Fuzzer!
# Created By Jordan Schau

import getopt, sys
import shutil
import os.path
import random
from os.path import join
import time
import pty
import signal

# Why use A's when you can use J's????? !!!!!!!!
overflowstrings = ["J" * 255, "J" * 256, "J" * 257, "J" * 420, "J" * 511, "J" * 512, "J" * 1023, "J" * 1024, "J" * 2047, "J" * 2048, "J" * 4096, "J" * 4097, "J" * 5000, "J" * 10000, "J" * 20000, "J" * 32762, "J" * 32763, "J" * 32764, "J" * 32765, "J" * 32766, "J" * 32767, "J" * 32768, "J" * 65534, "J" * 65535, "J" * 65536, "%x" * 1024, "%n" * 1025 , "%s" * 2048, "%s%n%x%d" * 5000, "%s" * 30000, "%s" * 40000, "%.1024d", "%.2048d", "%.4096d", "%.8200d", "%99999999999s", "%99999999999d", "%99999999999x", "%99999999999n", "%99999999999s" * 1000, "%99999999999d" * 1000, "%99999999999x" * 1000, "%99999999999n" * 1000, "%08x" * 100, "%%20s" * 1000,"%%20x" * 1000,"%%20n" * 1000,"%%20d" * 1000, "%#0123456x%08x%x%s%p%n%d%o%u%c%h%l%q%j%z%Z%t%i%e%g%f%a%C%S%08x%%#0123456x%%x%%s%%p%%n%%d%%o%%u%%c%%h%%l%%q%%j%%z%%Z%%t%%i%%e%%g%%f%%a%%C%%S%%08x", "%@" * 1000, "%@%%%d%D%i%u%U%hi%hu%qi%qu%x%X%qx%qX%o%O%f%e%E%g%G%c%C%s%S%p%L%a%A%F%z%t%j%ld%lx%lu%lx%f%g%lp%lx%p%lld%llx%llu%llx"]
LOG_DIR = os.path.expanduser("~/Library/Logs/DiagnosticReports/")
EXISTING_CRASHES = os.listdir(LOG_DIR)
sleep_time = 5

def run_tests(cases):
    """Runs the tests for X cases"""
    global test_dir
    
    if verbose:
        print "Running %d cases" % cases
        print "Application Path: %s" % app_path
        print "File Path: %s" % file_path
        
        
        
    if os.path.isdir(test_dir) == False:
        if verbose:
            print "Creating Test Directory %s" % os.path.abspath(test_dir)
        os.mkdir(test_dir)
        
    test_dir = os.path.abspath(test_dir)
    
    if os.path.isfile(file_path) == False:
        if verbose:
            print "%s is not a file!" % os.path.abspath(test_dir)
            sys.exit(2)
        
    basename, extension = os.path.splitext(file_path)
    
    executable_path, executable_name = os.path.split(app_path)
    
    shutil.copy(file_path, join(test_dir, "vanilla_file" + extension))
    
    original_file = "vanilla_file" + extension
    
    
    os.chdir(test_dir)
    
    i = 0
    while i < cases:
        test_file_name = "test_%d%s" % (i, extension)
        shutil.copy(original_file, test_file_name)
        add_fuzz(test_file_name)
        run_file2(test_file_name, executable_name)
        check_for_crash(test_file_name)
        i += 1

def add_fuzz(file):
    """Takes a file, jumps to a random offset and writes a string chosen at random
    from a dictionary"""
    if verbose:
        print "Fuzzing %s" % file       
    file_size = os.path.getsize(file)  
    offset = random.randint(1, file_size)
    fuzz = random.choice(overflowstrings)
    if verbose:
        print "Writing fuzz at offset %d" % offset
    try:         
        fd = os.open(file, os.O_RDWR)
        os.lseek(fd, offset, 0)
        os.write(fd, fuzz)
        os.close(fd)
    except:
        print "File write error!"
        

def run_file2(file, executable_name):
    try:
        print "Running %s" % file
        pid = os.fork()
        if pid==0:
            os.system("%s %s" % (app_path, file))
            os._exit(1)
            sys.exit()
        else:
            print "PID %s, os.getpid() %s" % (pid, os.getpid())
            time.sleep(4)
            os.kill(pid, signal.SIGKILL)
            os.system("killall %s" % executable_name)

                     
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)
    
    print "killing %s" % pid
    os.kill(pid, signal.SIGKILL)

    
def run_file(file):
    try:
        print "Running %s" % file
        pid, fd = pty.fork()
        if pid==0:
            if verbose:
                print "%s %s" % (app_path, file)
            os.system("%s %s" % (app_path, file))
            os._exit(1)
        else:
            time.sleep(1)
            if verbose:
                print "%s %s" % (app_path, file)
            time.sleep(sleep_time)
            print "pid: %d" % pid
            print "kill %s" % pid
            os.close(fd)
            #os.system("kill %s" % pid)
            os.kill(pid, signal.SIGTERM)
            #os.system("killall %s" % "VLC")
                     
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)
        

def check_for_crash(filename):
    crashes = os.listdir(LOG_DIR)
    if crashes == EXISTING_CRASHES:
        if verbose:
            print "removing %s" % join( test_dir, filename)
            
        remove_file(filename)
        #os.remove(os.path.join( test_dir, filename))
    else:
        existing = set(EXISTING_CRASHES)
        current_crashes = set(crashes)
        diff = current_crashes - existing
        new_log = diff.pop()
        new_log_path = os.path.join(LOG_DIR, new_log)  
             
        crash_file = filename + '.crash'
        
        if verbose:
            print "copying file %s as %s to %s" % (new_log, crash_file, test_dir) 
        
        shutil.move(new_log_path, os.path.join(test_dir, crash_file))
        

def remove_file(filename):
    try:
        os.remove(os.path.join( test_dir, filename))
    except OSError:
        print "file not found"
        pass
           
    
    

def usage():
    print
    print "FruityFuzzer 0.1, Simple fuzzing for Macs by Jordan Schau"
    print "http://www.jordanschau.com"
    print
    print "Usage:"
    print "python fruityfuzzer.py -a <./path/to/executable> -f <./path/to/file>"
    print "       -t <./path/to/directory/for/test/files> [options]"
    print
    print " [required]"
    print "        -a: Path to Application Executable"
    print "        -f: File to seed the Fuzzness"
    print " [options]"
    print "        -t: Directory to put the test cases (defaults to ./test/)"
    print "        -c: Number of test cases to run (defaults to 75)"
    print "        -T: wait time between trials (default is 5 seconds)"
    print "        -v: Verbose"
    print "        -h: Help page"
    print ""
    print "Ex: python FruityFuzz.py -a '/Applications/Preview.app/Contents/MacOS/Preview' "
    print "           -f '/Users/username/Desktop/fuzzypsd.psd' -t "
    print "             '/Users/username/Desktop/fuzz2 -c 500 -T 3 -v"

verbose = False
app_path = ""
file_path = ""
cases = 75 # Number of tests to run
sleep_time = 5
test_dir = ". /tests"


def main():
    global verbose
    global app_path
    global file_path
    global test_dir
    global cases
    global time
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha:f:t:c:T:v", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    try:
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                sys.exit()
            if o == "-a":
                app_path=a
            if o == "-f":
                file_path=a
            if o == "-t":
                test_dir=a
            if o == "-c":
                cases=int(a)
            if o == "-T":
                sleep_time=int(a)
            if o == "-v":
                verbose = True
                           
    except:
        usage()
        sys.exit(2)
        
    if app_path=="" or file_path=="":
        usage()
        sys.exit(2)
    else: #both paths have been specified
        run_tests(cases)
 

if __name__ == "__main__":
    main()
    