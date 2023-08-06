
class LCCA:
    def __init__(self):
        self.note = "This class is for life cycle cost analysis."

    def get_init_costs(self, init_costs):
        self.init_costs = init_costs

    def get_energy_costs(self, energy_costs):
        self.energy_costs = energy_costs

    def get_water_costs(self, water_costs):
        self.water_costs = water_costs

    def get_OMR_costs(self, OMR_costs):
        # operation/maintenance/repair costs
        self.OMR_costs = OMR_costs

    def get_replacement_costs(self, replacement_costs):
        self.replacement_costs = replacement_costs

    def get_residual_values(self, residual_values):
        self.residual_values = residual_values

    def get_other_costs(self, other_costs):
        # this includes financial charges, taxes
        self.other_costs = other_costs

    def calc_LCCA(self):
        self.LCCA = self.init_costs + self.replacement_costs - self.residual_values + \
                    self.energy_costs + self.water_costs + self.OMR_costs + self.other_costs

####################################################################################################################
x = LCCA()
x.get_init_costs(1000)
x.get_energy_costs(100)
x.get_water_costs(100)
x.get_OMR_costs(10000)
x.get_replacement_costs(10)
x.get_residual_values(2)
x.get_other_costs(300)
x.calc_LCCA()
print (x.LCCA)
