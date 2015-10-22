class Player:
    name = 'max'
    hand_total = 0
    hand_count = 0
    count = 0
    chips = 1000
    soft = False

    def get_wager(self):
        # if self.count > 5:
        #     return min(50, self.chips)
        # else:
        #     return 10
        #return min(max(10 * self.count / 2, 10), self.chips)
        if self.count > 10:
            return int(self.chips / 4)
        elif self.count > 6:
            return int(self.chips / 8)
        else:
            return min(10, self.chips)

    def hit(self, dealerUpCard):
        if not self.soft:
            if self.hand_total < 12:
                return True
            elif self.hand_total == 12:
                return dealerUpCard < 4 or dealerUpCard > 6
            elif 12 < self.hand_total < 17:
                return dealerUpCard > 6
            else:
                return False
        else:
            return self.hand_total < 8

    def double_down(self, dealerUpCard):
        if self.hand_count > 2:
            return False
        if not self.soft:
            return self.hand_total == 11 or \
                   (self.hand_total == 10 and 10 > dealerUpCard > 1) or \
                   (self.hand_total == 9 and 7 > dealerUpCard > 1) or \
                   (self.hand_total == 9 and 4 < dealerUpCard < 7)
        else:
            if self.hand_total > 2 and self.hand_total < 7:
                return 3 < dealerUpCard < 7
            elif self.hand_total == 7:
                return 1 < dealerUpCard < 7
            elif self.hand_total == 8:
                return 2 < dealerUpCard < 7
            elif self.hand_total == 9:
                return dealerUpCard == 6
            else:
                return False


    def add_card(self, card):
        self.hand_count += 1
        self.hand_total += card['value']
        if card['value'] == 1 and self.hand_total < 12:
            self.soft = True
        elif self.soft and self.hand_total >= 12:
            self.soft = False

    def view_card(self, card):
        if card['value'] < 7:
            self.count += 1
        elif card['value'] == 10:
            self.count -= 1
