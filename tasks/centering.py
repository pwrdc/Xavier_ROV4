import movements_itf as movement


class Centering:
    move = movement.IMovements()
    previousFlarePosX = 0
    previousFlarePosY = 0
    errorX = 0
    errorY = 0
    errorSumX = 0
    errorSumY = 0
    Ki = 2
    Kd = 3

    def center_rov(self, xPos, yPos):
        if self.previousFlarePosX != 0 & self.previousFlarePosY != 0:
            self.errorX = xPos - self.previousFlarePosX
            self.errorY = yPos - self.previousFlarePosY
            self.errorSumX += self.errorX
            self.errorSumY += self.errorY

        self.previousFlarePosX = xPos
        self.previousFlarePosY = yPos

        self.move.move_distance(0, (xPos * 10 + self.Ki * self.errorSumX + self.Kd * self.errorX),
                                (yPos * 10 + self.Ki * self.errorSumY + self.Kd * self.errorY))
