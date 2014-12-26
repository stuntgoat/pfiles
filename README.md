`pfiles`
========

### Write to many memoized files: NOT THREADSAFE!(yet)



(Example) Append event data in respective file names:

    from pfiles import File

    FILES = File('./data')

    for e in event_stream:
        # Create a file if none exists, otherwise use previously
        # opened file.
        f = FILES.add_or_open_file(e.name, 'a')
        f.write(e.data + '\n')
