FruityFuzz
========
---
## Introduction

This is a project for COMS E6998-9: Software Security and Exploitation.

I have created a simple mutation-based file fuzzer for Mac.  It is a work in progress and is not
fully functional.

## Usage
<pre><code class="python">
python fruityfuzzer.py -a <./path/to/executable> -f <./path/to/file> -t <./path/to/directory/for/test/files> [options]
    [required]
        -a: Path to Application Executable
        -f: File to seed the Fuzzness
    [options]
        -t: Directory to put the test cases (defaults to ./test/)
        -c: Number of test cases to run (defaults to 1000)
        -T: wait time between trials (default is 5 seconds)
        -v: Verbose
        -h: Help page

Ex: python FruityFuzz.py -a '/Applications/Preview.app/Contents/MacOS/Preview' 
        -f '/Users/username/Desktop/fuzzypsd.psd' -t '/Users/username/Desktop/fuzz2 -c 500 -T 3 -v

</code></pre>