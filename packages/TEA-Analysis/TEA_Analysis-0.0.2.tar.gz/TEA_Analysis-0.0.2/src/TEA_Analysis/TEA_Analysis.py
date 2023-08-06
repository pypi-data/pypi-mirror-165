import numpy as np
import matplotlib.pyplot as plt

"""
TEA = Techno-Economic Analysis
TEA is the analysis of technologies, products, or research ideas considering both technical and economic factors.
There are multiple elements to consider for TEA:
1. Scoping:
(1.1) Purpose: road-mapping a technology, comparing products, alternate materials, alternate process ...
(1.2) Audience: researchers, manufacturers, policy makers,...
(1.3) Stage of the object being evaluated: research, development, demonstration, commercialization, mass production

2. Determine Baseline
(2.1) Determine baseline or reference case: survey product in the market, consulting experts in academia/market, literature review
(2.2) If publishing, benchmark the technology or costs without being specific to one company; making it broader.
(2.3) Selecting scenarios: product volumes; manufacturing locations; design parameters; process options;

3. Cost Models:
(3.1)Minimum Sustainable Prices = Overhead Cost + Manufacturing Cost
(3.2)Overhead Cost = research and development + sales_general_administrative 
(3.3)sales_general_administrative = marketing+ administrative labor + most taxes (corporate tax not included)
(3.4)Manufacturing Costs = materials + labor + electricity + maintenance + equipment costs + facilities
(3.5)Operating Margin = Interests Payments + Profit + Corporate Tax Rate
 
"""

def plot_TEA_by_scenarios(TEA_list, scenarios_list, my_xlabel, my_ylabel):
    n = len(TEA_list)

    RD=[]
    market=[]
    admin_labor=[]
    taxes=[]
    materials=[]
    labor=[]
    electricity=[]
    maintenance=[]
    equipment=[]
    facility=[]
    for i in range(n):
        RD.append ( TEA_list[i].research_and_development)
        market.append( TEA_list[i].marketing)
        admin_labor.append( TEA_list[i].administrative_labor)
        taxes.append( TEA_list[i].taxes)
        materials.append( TEA_list[i].materials)
        labor.append(  TEA_list[i].labor)
        electricity.append( TEA_list[i].electricity)
        maintenance.append( TEA_list[i].maintenance)
        equipment.append( TEA_list[i].equipment)
        facility.append( TEA_list[i].facility)

    TEA_arr = np.asarray([RD, market, admin_labor, taxes, materials, labor, electricity, maintenance,
                          equipment, facility])



    fig = plt.figure()
    ax= fig.add_subplot(111)
    for i in range(10):
        if i==0:
            ax.bar(scenarios_list, TEA_arr[0,:])
        else:
            ax.bar( scenarios_list, TEA_arr[i, :], bottom=TEA_arr[i-1,:])

    ax.set_xlabel(my_xlabel)
    ax.set_ylabel(my_ylabel)
    ax.legend(['RnD', 'marketing', 'admin_labor', 'taxes', 'materials' , 'labor' , 'electricity',
               'maintenance', 'equipment', 'facility'])
    plt.tight_layout()
    plt.savefig('TEA_001.png', dpi=600)
    plt.show()
    plt.close(fig)

def plot_TEA_by_items(TEA_list, scenarios_list, my_xlabel, my_ylabel):
    n = len(TEA_list)

    RD=[]
    market=[]
    admin_labor=[]
    taxes=[]
    materials=[]
    labor=[]
    electricity=[]
    maintenance=[]
    equipment=[]
    facility=[]
    for i in range(n):
        RD.append ( TEA_list[i].research_and_development)
        market.append( TEA_list[i].marketing)
        admin_labor.append( TEA_list[i].administrative_labor)
        taxes.append( TEA_list[i].taxes)
        materials.append( TEA_list[i].materials)
        labor.append(  TEA_list[i].labor)
        electricity.append( TEA_list[i].electricity)
        maintenance.append( TEA_list[i].maintenance)
        equipment.append( TEA_list[i].equipment)
        facility.append( TEA_list[i].facility)

    TEA_arr = np.asarray([RD, market, admin_labor, taxes, materials, labor, electricity, maintenance,
                          equipment, facility])
    TEA_arr = np.transpose(TEA_arr)
    print ('TEA shape: ', TEA_arr.shape)
    print (TEA_arr[0,:])


    fig = plt.figure()
    ax= fig.add_subplot(111)
    items = ['RnD', 'marketing', 'admin_labor', 'taxes', 'materials', 'labor', 'electricity',
     'maintenance', 'equipment', 'facility']
    for i in range(3):
        if i==0:
            ax.bar(items, TEA_arr[0,:])
        else:
            ax.bar( items, TEA_arr[i, :], bottom=TEA_arr[i-1,:])

    ax.set_xlabel(my_xlabel)
    ax.set_ylabel(my_ylabel)
    ax.legend( scenarios_list)
    plt.tight_layout()

    plt.savefig('TEA_002.png', dpi=600)
    plt.show()
    plt.close(fig)




class PYTEA:
    def __init__(self):
        self.note= "This is TEA analysis"
        self.show_operation_margin = False

    def get_RnD(self, research_and_development=0 ):
        self.research_and_development = research_and_development

    def get_SGA(self, marketing=0, administrative_labor=0, taxes=0):
        # taxes here don not include corporate tax
        self.marketing = marketing
        self.administrative_labor = administrative_labor
        self.taxes = taxes
        self.SGA = self.marketing + self.administrative_labor + self.taxes

    def get_overhead(self):
        self.overhead = self.research_and_development + self.SGA

    def get_manufacturing(self, materials=0, labor=0, electricity=0, maintenance=0, equipment=0, facility=0 ):
        self.materials = materials
        self.labor= labor
        self.electricity = electricity
        self.maintenance = maintenance
        self.equipment = equipment
        self.facility = facility

        self.manufacturing = self.materials + self.labor + self.electricity + \
                             self.maintenance+self.equipment + self.facility

    def get_MSP(self):
        # minimum sustainable price
        self.MSP = self.overhead + self.manufacturing

    def get_operation_margin(self, interest_payments=0, profit=0, corporate_tax=0):
        if not self.show_operation_margin:
            self.interest_payments = 0
            self.profit = 0
            self.corporate_tax = 0
        else:
            self.interest_payments = interest_payments
            self.profit = profit
            self.corporate_tax = corporate_tax

        self.operation_margin = self.interest_payments + self.profit + self.corporate_tax


"""
x = PYTEA()
x.get_RnD(100)
x.get_SGA(10, 20, 5)
x.get_overhead()
x.get_manufacturing( 12, 1, 2, 30, 14, 16)
x.get_MSP()
x.get_operation_margin(0,0,0)


y = PYTEA()
y.get_RnD(120)
y.get_SGA(13, 22, 15)
y.get_overhead()
y.get_manufacturing( 22, 11, 32, 50, 64, 6)
y.get_MSP()
y.get_operation_margin(0,0,0)

z = PYTEA()
z.get_RnD(200)
z.get_SGA(30, 22, 15)
z.get_overhead()
z.get_manufacturing( 32, 21, 42, 60, 44, 36)
z.get_MSP()
z.get_operation_margin(0,0,0)

plot_TEA_by_scenarios( [x,y,z], ['west','mid','east'], 'scenarios' ,'USDollar/Ton'  )
plot_TEA_by_items( [x,y,z], ['west','mid','east'], 'items' ,'USDollar/Ton'  )
"""