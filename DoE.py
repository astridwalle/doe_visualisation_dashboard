

import openmdao.api as om

class Constant(om.ExplicitComponent):
    """
    returns 0
    """

    def setup(self):
        self.add_input('roof_length', val=0.0)
        self.add_input('front_length', val=0.0)
        self.add_input('back_length', val=0.0)        

        self.add_output('f_xyz', val=0.0)

#    def setup_partials(self):
#        self.declare_partials('*', '*')

    def compute(self, inputs, outputs):
        """
        returns 0
        """
        x = inputs['roof_length']
        y = inputs['front_length']
        z = inputs["back_length"]

        outputs['f_xyz'] = 0

 #   def compute_partials(self, inputs, partials):
 #       """
 #       Jacobian for our paraboloid.
 #       """
 #       x = inputs['x']
 #       y = inputs['y']

 #       partials['f_xy', 'x'] = 2.0*x - 6.0 + y
 #       partials['f_xy', 'y'] = 2.0*y + 8.0 + x

def definitions():
    doe_generators=["BoxBehnkenGenerator","FullFactorialGenerator","GeneralizedSubsetGenerator","LatinHypercubeGenerator","PlackettBurmanGenerator","UniformGenerator"]

    doe={}
    for i in doe_generators:
        doe[i]={}
    doe["BoxBehnkenGenerator"]["num_samples"]=False
    doe["FullFactorialGenerator"]["num_samples"]=False
    doe["GeneralizedSubsetGenerator"]["num_samples"]=False
    doe["LatinHypercubeGenerator"]["num_samples"]=False
    doe["PlackettBurmanGenerator"]["num_samples"]=False
    doe["UniformGenerator"]["num_samples"]=1

    doe["BoxBehnkenGenerator"]["samples"]=False
    doe["FullFactorialGenerator"]["samples"]=False
    doe["GeneralizedSubsetGenerator"]["samples"]=False
    doe["LatinHypercubeGenerator"]["samples"]=True
    doe["PlackettBurmanGenerator"]["samples"]=False
    doe["UniformGenerator"]["samples"]=False

    doe["BoxBehnkenGenerator"]["center"]=True
    doe["FullFactorialGenerator"]["center"]=False
    doe["GeneralizedSubsetGenerator"]["center"]=False
    doe["LatinHypercubeGenerator"]["center"]=False
    doe["PlackettBurmanGenerator"]["center"]=False
    doe["UniformGenerator"]["center"]=False

    doe["BoxBehnkenGenerator"]["levels"]=False
    doe["FullFactorialGenerator"]["levels"]=True
    doe["GeneralizedSubsetGenerator"]["levels"]=True
    doe["LatinHypercubeGenerator"]["levels"]=False
    doe["PlackettBurmanGenerator"]["levels"]=False
    doe["UniformGenerator"]["levels"]=False

    doe["BoxBehnkenGenerator"]["reduction"]=False
    doe["FullFactorialGenerator"]["reduction"]=False
    doe["GeneralizedSubsetGenerator"]["reduction"]=True
    doe["LatinHypercubeGenerator"]["reduction"]=False
    doe["PlackettBurmanGenerator"]["reduction"]=False
    doe["UniformGenerator"]["reduction"]=False

    return doe

def create_doe(method,levels,samples,num_samples,reduction,center):
    prob = om.Problem()
    model = prob.model

    model.add_subsystem('comp', Constant(), promotes=['*'])

    model.add_design_var('roof_length', lower=0.3, upper=0.76)
    model.add_design_var('front_length', lower=0.1, upper=0.25)
    model.add_design_var('back_length', lower=0.13, upper=0.29)

    model.add_objective('f_xyz')

    if method=="BoxBehnkenGenerator":
        prob.driver = om.DOEDriver(om.BoxBehnkenGenerator(center=center))
    elif method=="FullFactorialGenerator":
        prob.driver = om.DOEDriver(om.FullFactorialGenerator(levels=levels))
    elif method=="GeneralizedSubsetGenerator":
        prob.driver = om.DOEDriver(om.GeneralizedSubsetGenerator(levels=levels, reduction=reduction, n=1))
    elif method=="LatinHypercubeGenerator":
        prob.driver = om.DOEDriver(om.LatinHypercubeGenerator(samples=int(samples), criterion=None, iterations=5, seed=None))
    elif method=="PlackettBurmanGenerator":
        prob.driver = om.DOEDriver(om.PlackettBurmanGenerator())
    elif method=="UniformGenerator":
        prob.driver = om.DOEDriver(om.UniformGenerator(num_samples=int(num_samples), seed=None))
        
    #prob.driver = om.DOEDriver(om.UniformGenerator(num_samples=int(samples)))
    prob.driver.add_recorder(om.SqliteRecorder("cases.sql"))

    prob.setup()

    prob.set_val('roof_length', 0.3)
    prob.set_val('front_length', 0.1)
    prob.set_val('back_length', 0.13)

    prob.run_driver()
    prob.cleanup()

    cr = om.CaseReader("cases.sql")
    cases = cr.list_cases('driver')

    values = []
    for case in cases:
        outputs = cr.get_case(case).outputs
        values.append((outputs['roof_length'][0], outputs['front_length'][0], outputs['back_length'][0]))

    return values

#values=create_doe()
#print("\n".join(["x: %5.2f, y: %5.2f, f_xy: %6.2f" % xyf for xyf in values]))