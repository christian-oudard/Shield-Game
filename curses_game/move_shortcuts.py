northwest = (-1, -1)
west      = (-1,  0)
southwest = (-1,  1)
north     = ( 0, -1)
center    = ( 0,  0)
south     = ( 0,  1)
northeast = ( 1, -1)
east      = ( 1,  0)
southeast = ( 1,  1)

move_codes = {
    ('move', north): 'mn',
    ('move', south): 'ms',
    ('move', east): 'me',
    ('move', west): 'mw',
    ('move', northeast): 'mne',
    ('move', southeast): 'mse',
    ('move', southwest): 'msw',
    ('move', northwest): 'mnw',
    ('move', center): 'mc',
    ('shield', north): 'sn',
    ('shield', south): 'ss',
    ('shield', east): 'se',
    ('shield', west): 'sw',
    ('shield', northeast): 'sne',
    ('shield', southeast): 'sse',
    ('shield', southwest): 'ssw',
    ('shield', northwest): 'snw',
    ('shield', center): 'sc',
}
reverse_move_codes = dict((c, m) for m, c in move_codes.items())
