class Payment:
    DISCOUNT_RATE = 0.8
    INSURANCE_RATE = 0.05
    WALK_IN_COST = 100
    ANNUAL_COST = 150

    def __init__(self, slots):
        self.slots = slots
        self.discount = self.DISCOUNT_RATE
        self.insurance = self.INSURANCE_RATE
        self.sub_total = 0
        self.discount_total = 0
        self.insurance_total = 0
        self.total = 0

    def set_sub_total(self):
        sub_total = 0
        for walk_in in self.slots:
            if walk_in:
                sub_total += self.WALK_IN_COST
            else:
                sub_total += self.ANNUAL_COST
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
