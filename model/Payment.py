class Payment:
    def __init__(self, slots, discount, insurance):
        self.slots = slots
        self.discount = discount
        self.insurance = insurance
        self.sub_total = 0
        self.discount_total = 0
        self.insurance_total = 0
        self.total = 0

    def set_sub_total(self):
        sub_total = 0
        for slot in self.slots:
            print(slot.walk_in)
            if slot.walk_in == True:
                sub_total += 100
            else:
                sub_total += 150
        self.sub_total = sub_total

    def set_total_discount(self):
        total_discount = self.sub_total * self.discount
        self.discount_total = total_discount

    def set_total_insurance(self):
        total_insurance = self.sub_total * self.insurance
        self.insurance_total = total_insurance

    def set_total(self):
        total = self.sub_total - self.discount_total - self.insurance_total
        self.total = total

    def format_totals(self):
        self.total = "{:.2f}".format(self.total)
        self.sub_total = "{:.2f}".format(self.sub_total)
        self.discount_total = "{:.2f}".format(self.discount_total)
        self.insurance_total = "{:.2f}".format(self.insurance_total)

    def initialize(self):
        self.set_sub_total()
        self.set_total_discount()
        self.set_total_insurance()
        self.set_total()
        self.format_totals()
