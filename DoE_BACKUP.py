# This code is built based on the examples provided here:
# https://openmdao.org/newdocs/versions/latest/features/building_blocks/drivers/doe_driver.html?highlight=design%20experiments#running-a-doe-in-parallel-with-a-parallel-model


# Estimate the number of design points from number of parameters!
# Can be overridden by manual input!

########################################################################
# Imports
########################################################################


import openmdao.api as om
#from openmdao.test_suite.components.paraboloid import Paraboloid

prob = om.Problem()
model = prob.model

class Constant(om.ExplicitComponent):
    """
    Always returns 0
    """

    def setup(self):
        self.add_input('x', val=0.0)
        self.add_input('y', val=0.0)

        self.add_output('f_xy', val=0.0)

    def setup_partials(self):
        self.declare_partials('*', '*')

    def compute(self, inputs, outputs):
        """
        0
        """
        x = inputs['x']
        y = inputs['y']

        outputs['f_xy'] = 0*x + 0*y

model.add_subsystem('comp', Constant())

model.add_design_var('x', lower=-10, upper=10)
model.add_design_var('y', lower=-10, upper=10)
model.add_objective('f_xy')

prob.driver = om.DOEDriver(om.UniformGenerator(num_samples=5))
prob.driver.add_recorder(om.SqliteRecorder("cases.sql"))

prob.setup()

prob.set_val('x', 0.0)
prob.set_val('y', 0.0)

prob.run_driver()
prob.cleanup()

cr = om.CaseReader("cases.sql")
cases = cr.list_cases('driver')

values = []
for case in cases:
    outputs = cr.get_case(case).outputs
    values.append((outputs['x'], outputs['y'], outputs['f_xy']))

print("\n".join(["x: %5.2f, y: %5.2f, f_xy: %6.2f" % xyf for xyf in values]))

# Parameters and results are taken from the simulation class
# There the respective files are read

""" model.add_subsystem('sim',simulation(),promotes_inputs=simulation.params["name"].to_list(),promotes_outputs=simulation.results["name"].to_list())
for idx,row in simulation.params.iterrows():
    model.add_design_var(row[0],lower=row[2],upper=row[3])
for idx,row in simulation.results.iterrows():
    model.add_objective(row[0])

# TODO Implement the different DoE Driver calls!

doe_generators=["BoxBehnkenGenerator","FullFactorialGenerator","GeneralizedSubsetGenerator","LatinHypercubeGenerator","PlackettBurmanGenerator","UniformGenerator"]

# Different calls depending on the selected DoE Driver:
# openmdao.drivers.doe_generators.BoxBehnkenGenerator(center=None) 
# openmdao.drivers.doe_generators.CSVGenerator(filename)
# openmdao.drivers.doe_generators.FullFactorialGenerator(levels=2) --> a dict can be given with specific levels for each parameter
# openmdao.drivers.doe_generators.GeneralizedSubsetGenerator(levels, reduction, n=1)
# openmdao.drivers.doe_generators.LatinHypercubeGenerator(samples=None, criterion=None, iterations=5, seed=None)
# openmdao.drivers.doe_generators.PlackettBurmanGenerator --> extension of Box-Behnken
# openmdao.drivers.doe_generators.UniformGenerator(num_samples=1, seed=None)

# Estimation of sample number based on the number & spacing of parameters:
no_factors=len(simulation.params)

# Initialize the DoE Driver
prob.driver = om.DOEDriver(om.UniformGenerator(num_samples=5))
prob.driver.add_recorder(om.SqliteRecorder("cases.sql"))

prob.setup()

for idx,row in simulation.params.iterrows():
    prob.set_val(row[0],row[1])

prob.run_driver()

# TODO Make cleanup a part of commandline options
# Cleanup calls a function to remove all created simulation directories
#prob.cleanup()

cr = om.CaseReader("cases.sql")
cases = cr.list_cases('driver')

values = []
for case in cases:
    outputs = cr.get_case(case).outputs
    print(outputs) """