import csv

class GameRecord:
    def __init__(self, file):
        self.moves = []
        self.file = file
        self.settings = None
        self.result = None
        
    def record_settings(self, size, mode, blue_type, red_type):
        self.settings = (size, mode, blue_type, red_type)
        
    def record_move(self, row, col, letter, player):
        self.moves.append((row, col, letter, player))
    
    def record_result(self, winner):
        self.result = winner if winner is not None else "draw"
        
    def save(self):
        with open(self.file, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(["size", "mode", "blue_type", "red_type"])
            w.writerow(self.settings)
            w.writerow([])
            w.writerow(["row", "col", "letter", "player"])
            w.writerows(self.moves)
            w.writerow([])
            w.writerow(["result", self.result])
            
    @classmethod
    def load(cls, file):
        record = cls(file)
        with open(file) as f:
            read = csv.reader(f)
            next(read)
            record.settings = tuple(next(read))
            next(read); next(read)
            for row in read:
                if not row: continue
                if row[0] == "result":
                    record.result = row[1]
                    break
                rr, cc, letter, player = row
                record.moves.append((player, int(rr), int(cc), letter))
        return record