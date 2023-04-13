# -----------------------------------------------------------------------------
# Author               :   Coen Tempelaars
# -----------------------------------------------------------------------------

# Modified to work with ePaper 2.9 display

from writer import Writer

class CenterWriter():
    def __init__(self, device, font, verbose=True):
        self.device = device
        self.writer = Writer(device, font, verbose)
        self.writer.set_clip(row_clip=False, col_clip=False, wrap=False)
        self.spacing = 0
        self.shift = 0

    def set_vertical_spacing(self, spacing):
        self.spacing = spacing

    def set_vertical_shift(self, shift):
        self.shift = shift

    def write_lines(self, lines):
        total_height = (self.writer.height + self.spacing) * len(lines) - self.spacing
        row = (128 - total_height) // 2 + self.shift

        if row < 0 or (row + total_height) >= 128:
            raise ValueError('Text position exceeds display limit (vertical)')

        for line in lines:
            length = self.writer.stringlen(line)
            col = (296 - length) // 2 if length < 296 else 0

            self.writer.set_textpos(self.device, row, col)
            self.writer.printstring(line, invert=True)

            row += (self.writer.height + self.spacing)
            if row >= 128:
                break