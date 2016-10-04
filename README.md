# brainsurgeon

`brainsurgeon` is a text editor inspired by the [brainfuck](https://en.wikipedia.org/wiki/Brainfuck)
programming language.  It is not user-friendly.

## HOW TO USE

Make the file executable:

    $ chmod u+x brainsurgeon.py

Open `foo.txt` in the editor (will be created if does not exist)

    $ ./brainsurgeon.py foo.txt

### MOVING THE CURSOR

The cursor starts at the first row and column. The cursor can be moved via

    `^` moves the cursor up one line
    `v` moves the cursor down one line
    `<` moves the cursor left one character
    `>` moves the cursor right one character.

### EDITING

The character at the cursor's current location can be edited several ways.

    `, <character>` replaces the current character with <character>
    (same as reading a character in BF).

For example, `, a` replaces the current character with a.
    
    `+` increments the character at the cursor's current location by 1,
    modulo 128.
    
    `-` decrements the character at the cursor's current location by 1,
    modulo 128.

If you decrement 0 or increment 127, it wraps around.

### SAVING

Hit `.` to save.  You will be prompted to provide a filename.  Leave it
blank to use the current filename (will be overwritten).  Hit enter to
save.

### QUITTING

Hit `Ctrl-C` to quit.  If you have unsaved changes, you will not be
prompted to save them.  If you wanted a nice editor, you're in the wrong
part of town.

### Caveats

The editor is currently limited to the size of your terminal window.
It only handles handles basic ascii (or binary values up to 128).

Also, it's based on brainfuck.