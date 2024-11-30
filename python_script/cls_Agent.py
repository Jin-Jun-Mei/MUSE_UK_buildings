# define the Agent class
class Agent:
    """
    Represents an agent with various attributes and methods.
    Attributes:
        Name (str): The name of the agent.
        AgentShare (float): The share of the agent.
        RegionName (str): The name of the region.
        Objective1 (str): The first objective of the agent.
        Objective2 (str): The second objective of the agent.
        Objective3 (str): The third objective of the agent.
        ObjData1 (float): A weight associated with the first objective
        ObjData2 (float): A weight associated with the second objective.
        ObjData3 (float): A weight associated with the third objective.
        Objsort1 (Boolean): Sets whether first objective is maximized or minimized. For both “adhoc” and “scipy” solvers this should be set to “True” for minimization and “False” for maximisation.
        Objsort2 (Boolean): The sorting criteria for the second objective.
        Objsort3 (Boolean): The sorting criteria for the third objective.
        SearchRule (str): The search rule for the agent.
        Quantity (float): Represents the fraction of new demand that is assigned to the agent 
        MaturityThreshold (float): The maturity threshold of the agent. Only applies when using the maturity search rule. 
        SpendLimit (int, optional): Only applies when using the spend_limit search rule.  
        AgentType (str): The type of the agent. Defaults to 'New'. (In MUSE this parameter is called "Type")
        (InitialShare (dict): The initial share of the agent. Defaults to None.)
    Methods:
        method1(): Placeholder method. Define the functionality of method1 here.
        method2(): Placeholder method. Define the functionality of method2 here.
    """
    instances = []  # Class variable to track instances of the class

    def __init__(self
                 , Name
                 , AgentShare
                 , RegionName = "UK"
                 , Objective1 = "LCOE"
                 , Objective2 = ""
                 , Objective3 = ""
                 , ObjData1 = 1
                 , ObjData2 = ""
                 , ObjData3 = ""
                 , Objsort1 = True
                 , Objsort2 = False
                 , Objsort3 = False
                 , SearchRule = "same_enduse" # Please see MUSE documentation for more details on search rules
                 , Quantity = 1
                 , MaturityThreshold = 0
                 , DecisionMethod = "singleObj"
                 , SpendLimit = 99999999999
                 , AgentType = 'New'
                 ):
        # Initialize any attributes or variables here
        self.Name = Name
        self.AgentShare = AgentShare
        self.RegionName = RegionName #if RegionName else "UK"
        self.Objective1 = Objective1 #if Objective1 else "TRUE"
        self.Objective2 = Objective2 #if Objective2 else "FALSE"
        self.Objective3 = Objective3 #if Objective3 else "FALSE"
        self.ObjData1 = ObjData1
        self.ObjData2 = ObjData2
        self.ObjData3 = ObjData3
        self.Objsort1 = Objsort1
        self.Objsort2 = Objsort2
        self.Objsort3 = Objsort3
        self.SearchRule = SearchRule
        self.Quantity = Quantity
        self.MaturityThreshold = MaturityThreshold
        self.DecisionMethod = DecisionMethod
        self.SpendLimit = SpendLimit
        self.AgentType = AgentType
        # InitialShare is expected to be a dictionary with keys as agent's number and values are shares(0 to 1) of the agent in each of the technology
        #self.InitialShare = InitialShare if InitialShare is not None else {}

        # Add each instance to the list
        Agent.instances.append(self)  

   

    def method1(self):
        # Define the functionality of method1 here
        pass

    def method2(self):
        # Define the functionality of method2 here
        pass

    # Add more methods as needed