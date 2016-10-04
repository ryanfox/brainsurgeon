#!/usr/bin/python3

import os
import sys

import curses
from curses import wrapper

def move_down(state, cursor):
    return state, (cursor[0] + 1, cursor[1])

def move_up(state, cursor):
    if cursor[0] == 0:
        return cursor
    
    return (cursor[0] - 1, cursor[1])

def move_left(cursor):
    if cursor[1] == 0:
        return cursor

    return (cursor[0], cursor[1] - 1)

def move_right(state, cursor):
    return state, (cursor[0], cursor[1] + 1) 

def increment(state, cursor):
    try:
        return put(state, cursor, (state[cursor[0]][cursor[1]] + 1) % 128)
    except IndexError:
        return put(state, cursor, 1)

def decrement(state, cursor):
    try:
        return put(state, cursor, (state[cursor[0]][cursor[1]] - 1) % 128)
    except IndexError:
        return put(state, cursor, 127)


def put(state, cursor, c):
    new_state = state[:]
    row, col = cursor
    
    if len(new_state) <= row:
        for _ in range(row - len(new_state) + 1):
            new_state.append([])
    
    if len(new_state[row]) <= col:
        for _ in range(col - len(new_state[row]) + 1):
            new_state[row].append(0)
    
    new_state[row][col] = c
    
    return new_state


def save(state, filename):
    with open(filename, 'wb') as f:
        for line in state:
            f.write(bytes(line + [ord('\n')]))

def render(chars):
    return ''.join(chr(character or 32) for character in chars)


def main(stdscr):
    stdscr.clear()
 
    cursor = (0, 0)
    
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
            with open(sys.argv[1], 'rb') as f:
                lines = [line.strip() for line in f.readlines()]
                state = [[char % 128 for char in line] for line in lines]
        else:
            state = []
    else:
        state = []

    while True:
        for i in range(len(state)):
            stdscr.addstr(i, 0, render(state[i]))
        
        stdscr.move(*cursor)
        stdscr.refresh()

        try:
            c = stdscr.getkey()
        except KeyboardInterrupt:
            break
        
        if c == 'v':
            state, cursor = move_down(state, cursor)
        elif c == '^':
            cursor = move_up(state, cursor)
        elif c == '<':
            cursor = move_left(cursor)
        elif c == '>':
            state, cursor = move_right(state, cursor)
        elif c == '+':
            state = increment(state, cursor)
        elif c == '-':
            state = decrement(state, cursor)
        elif c == ',':
            new_c = stdscr.getch()
            state = put(state, cursor, new_c)
        
        if c == '.':
            prompt = 'save as (enter to save as \'{}\'): '.format(sys.argv[1])
            stdscr.addstr(curses.LINES - 1, 0, prompt)
            stdscr.refresh()
            
            curses.echo()
            filename = stdscr.getstr(curses.LINES - 1, len(prompt)).decode('ascii')
            curses.noecho()
            
            if len(filename) == 0:
                filename = sys.argv[1]
            sys.argv[1] = filename
            
            save(state, filename)
            stdscr.move(curses.LINES - 1, 0)
            stdscr.clrtoeol()
            stdscr.addstr(curses.LINES - 1, 0, '{} saved'.format(filename))
        else:
            stdscr.clear()
        

wrapper(main)

