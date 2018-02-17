class Star:

    commonId = 1

    def __init__(self, x, y, z):
        self.id = self.commonId
        self.commonId += 1
        self.x = x
        self.y = y
        self.z = z
