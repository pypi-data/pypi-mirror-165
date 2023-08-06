import anytree
import pandas as pd
from anytree import RenderTree, findall
from .functions_aux import chunks
from .v3wrapper import retrieve_multiple_telemetries_flex_schedule,parameter_to_return_value

pd.set_option('display.max_columns', None)

class Node(anytree.Node):
    '''
    THIS EXPANDS THE NODE CLASS IN THE ANYTREE LUBRARY WITH THE FOLLOWING FUNCTIONALITY:
    adding: node1 + node2 will calculate the union sets and return a tuple with the resulting (sensor_ids,sensor_names)
    subtracting: node1 - node2 will return a tuple of the (sensor_ids, sensor_names) in node1 so long as they dont appear in node2
    render: node.render() will perform a basic rendering of such node, all the way downwards
    '''
    def __add__(self,other):
        sensor_ids=self.sensor_ids.copy()
        sensor_names=self.sensor_names.copy()
        for sensor_id, sensor_name in zip(other.sensor_ids,other.sensor_names):
            if not(sensor_id in sensor_ids):
                sensor_ids+=[sensor_id]
                sensor_names+=[sensor_name]
        # print(sensor_ids,sensor_names)
        temp_node = Node(name="temp",parent=None)
        temp_node.sensor_ids = sensor_ids
        temp_node.sensor_names = sensor_names
        return temp_node

    def __sub__(self, other):
        sensor_ids=[]
        sensor_names=[]
        for sensor_id,sensor_name in zip(self.sensor_ids,self.sensor_names):
            if not(sensor_id in other.sensor_ids):
                sensor_ids+=[sensor_id]
                sensor_names+=[sensor_name]

        # print(sensor_ids,sensor_names)
        temp_node = Node(name="temp",parent=None)
        temp_node.sensor_ids = sensor_ids
        temp_node.sensor_names = sensor_names
        return temp_node

    def render(self):
        for pre, _, node in RenderTree(self):
            print("%s%s" % (pre, node.name))

    def zip(self):
        return zip(self.sensor_ids,self.sensor_names)

    def search(self,space_name,partial_match=False,first_result=True,verbose=False):
        '''
        :param space_name: string to search for
        :param partial_match: if True, will return nodes that contain the space_name. If false, it will only bring exact matches
        :param first_result: if True, only returns one result
        :param verbose: if True, will print number of search results alongside sensor count
        :return: single Node or tuple of Nodes depending on the options. If no results found, then None.
        '''
        if partial_match:
            found = findall(self,filter_=lambda node: space_name in node.name)
        else:
            found = findall(self,filter_=lambda node: node.name in [space_name])
        if verbose:
            print(f"{len(found)} results found")
            for node in found:
                print(node.name + f"---- {len(node.sensor_ids)} sensors")
            if len(found)>1 and first_result:
                print("returning first match only")
        if len(found)>0:
            if first_result or len(found)==1:
                return found[0]
            else:
                return found
        else:
            return None

    def filter(self,configuration_df,attribute_names,attribute_values):
        '''
        :param configuration_df: dataframe with at the very least sensor ids ("asset_id") plus columns for any attributes sought
        :param attribute_names: list of columns in the df reflecting attributes to filter by
        :param attribute_values:list of values corresponding to each attribute for which we want to select sensors
        :return: new Node with only the selected ids (ALL attributes need to match concurrently), parent=None
        '''
        df = configuration_df.copy()
        df = df[(df["asset_id"].isin(self.sensor_ids))]
        for attribute_name,attribute_value in zip(attribute_names,attribute_values):
            df = df[df[attribute_name]==attribute_value]
        temp = Node(name="filtered",parent=None)
        sensor_ids = list(df["asset_id"])
        sensor_names = list(df["sensor_name"])
        temp.sensor_ids = sensor_ids
        temp.sensor_names = sensor_names
        return temp

class Params:
    def __init__(self,params_dict):
        for parameter in params_dict:
            exec("self."+parameter+"=params_dict[parameter]")


class SensorData:
    def __init__(self,root_node):
        self.name = root_node.name
        self.sensor_names = root_node.sensor_names
        self.sensor_ids = root_node.sensor_ids

    def load_params(self,params_dict):
        '''
        :param params_dict: format as per the below
        params_dict={"max_num_sensors_per_call":10,"user":user,"pwd":pwd,
             "id_list":[str(x) for x in s.sensor_ids],
             "id_to_name_dictionary":None,
             "telemetry_list":telemetries,"interval_minutes":frequency_minutes,"from_local_time":from_local_time,"to_local_time":to_local_time,
             "max_days_per_call":31,"tz_code":tz_code,"schedule":schedule,"exclude_holidays_country_region":exclude_holidays_country_region,
             "operation":operation,
             "group_by":"asset","na_fill":"ffill"}
        :return: it creates a self.params attribute that can be accessed further, for instance self.params.telemetry_list.
        It also creates for each telemetry a self.TEMPERATURE (for instance) where the list of downloaded dfs per sensor will be stored
        '''
        self.params = Params(params_dict)
        for parameter in self.params.telemetry_list:
            exec("self."+parameter+"=[None]*"+str(len(self.sensor_ids)))

    def load_data(self):
        '''
        needs to have loaded params first!
        :return: each telemetry will have a list of dfs corresponding to the data downloaded for each sensor in self.sensor_ids
        '''

        batches = chunks(lst=self.sensor_ids,n=self.params.max_num_sensors_per_call)

        for batch in batches:
            #set id_to_name_dictionary = None so that we get sensor id, not name, back in the columns
            temp_df = retrieve_multiple_telemetries_flex_schedule(self.params.user,self.params.pwd,batch,None,self.params.telemetry_list,
                                                                  self.params.interval_minutes,self.params.from_local_time,self.params.to_local_time,
                                                                  self.params.max_days_per_call,self.params.tz_code,self.params.schedule,
                                                                  self.params.exclude_holidays_country_region,self.params.operation,
                                                                  self.params.group_by,self.params.na_fill)
            for telemetry in self.params.telemetry_list:
                metric = parameter_to_return_value[telemetry]
                relevant_cols = [col for col in temp_df.columns if ("_"+metric) in col]
                temp_df_metric = temp_df.copy()[relevant_cols]
                temp_df_metric.columns = ["_".join(x.split("_")[:-1]) for x in temp_df_metric.columns]

                for i,sensor_id in zip(range(0,len(self.sensor_ids)),self.sensor_ids):
                    if sensor_id in batch:
                        try:
                            sensor_metric = temp_df_metric[[str(sensor_id)]]
                            if len(sensor_metric)>0:
                                exec("self."+telemetry+"["+str(i)+"]=sensor_metric")
                        except:
                            print(f"Data not found for sensor {sensor_id} ({telemetry}")

    def merge_data(self,telemetry,transform_function="plain",use_sensor_names=False,configuration_df=None,attribute_names=[],attribute_values=[]):
        '''
        :param telemetry: single telemetry (eg "AREA_COUNT")
        :param transform_function: "plain" if we want sensor by sensor results, any of the pandas functions ("sum", "min", "max", "median" etc) if not. Applied horizontally to all sensors.
        :param use_sensor_names: if True, it will return sensor names instead of sensor ids as columns
        :param configuration_df: optional - if we want to filter by attribute name and value, this df will contain asset_id plus the attribute names
        :param attribute_names: list of attribute names (columns of configuration_df) we want to filter by
        :param attribute_values: list of attribute values we want to filter by. All need to match concurrently.
        :return: df with the resulting data, and where the columns are either sensor names ("plain") or telemetry_operation (eg "AREA_COUNT_sum")
        '''
        global _combined_df
        df_list=[]
        for sensor_id, sensor_df in zip(self.sensor_ids,self.__text_to_property(telemetry)):
            if sensor_df is None:
                pass
            else:
                df_list+=[sensor_df]

        #*****30-08-22 add filtering*****
        if configuration_df is None:
            pass
        else:
            for attribute_name, attribute_value in zip(attribute_names,attribute_values):
                configuration_df = configuration_df[configuration_df[attribute_name]==attribute_value]
            eligible_sensors = [str(sensor) for sensor in list(configuration_df["asset_id"])]
            df_list = [df for df in df_list if str(df.columns[0]) in eligible_sensors]
        # *****30-08-22 add filtering*****

        if len(df_list)>0:
            _combined_df = pd.concat(df_list,axis=1)
            _combined_df.index.name=telemetry
            if transform_function!="plain":
                exec("global _combined_df;_combined_df = _combined_df."+transform_function+"(axis=1).to_frame()")
                _combined_df.columns=[telemetry+"_"+transform_function]
            if use_sensor_names and transform_function=="plain":
                cols = list(_combined_df.columns)
                new_cols = []
                id_to_name_dictionary = res = {str(self.sensor_ids[i]): self.sensor_names[i] for i in range(len(self.sensor_ids))}
                for i in range(0,len(cols)):
                    new_cols+=[id_to_name_dictionary[str(cols[i])]]
                _combined_df.columns=new_cols
            return _combined_df
        else:
            return None

    def __text_to_property(self,property_name):
        print(self.name)
        exec("global temp;temp=self."+property_name)
        return temp



def create_tree(configuration_df,levels,initial_depth,add_sensor_names=False):
    '''
    :param configuration_df: a df containing sensor names and ids plus whatever fields we deem appropriate for accordion classification. Must have the columns sensor_name and asset_id
    :param levels: a list with the names of the grouping columns we want to generate the tree from, eg levels=["building","group","level_01","level_02","level_03"]
    :param initial_depth: the level we want to start the tree at (e.g. in the example above depth=0 starts with "building"
    :param add_sensor_names: if True, it will add sensor name and ID at the end of each node
    :return: a list of the root Nodes of the tree
    '''
    global id
    id = 0
    global return_nodes
    return_nodes=[]
    def __recursive_tree(df,levels,initial_depth,parent=None,add_sensor_names=False):
        global id
        depth=initial_depth
        level=levels[0:depth+1]
        idx = df.groupby(level,dropna=True).indices
        if (len(idx)==0) and (add_sensor_names==True):
            for sensor_name, sensor_id in zip(parent.sensor_names,parent.sensor_ids):
                id=id+1
                sensor_node = Node(name=sensor_name+" - "+str(sensor_id),parent=parent)
                exec("global ID"+str(id)+";ID"+str(id)+"=sensor_node")
            # print(parent.sensor_names)
            # print(id)

        for item in idx:
            if type(item)==str:
                new_node=item
            else:
                new_node=item[-1]
            new_df=df[df[levels[depth]]==new_node]
            node = Node(new_node,
                        parent=parent,
                        sensor_names=list(new_df["sensor_name"]),
                        sensor_ids=list(new_df["asset_id"]))
            exec("global ID"+str(id)+";ID"+str(id)+"=node")
            if parent==None:
                exec("global ID"+str(id)+";return_nodes+=[ID"+str(id)+"]")

            id=id+1
            if (depth+1)<len(levels):
                __recursive_tree(df=new_df,levels=levels,initial_depth=depth+1,parent=node,add_sensor_names=add_sensor_names)

    __recursive_tree(df=configuration_df,levels=levels,initial_depth=initial_depth,parent=None,add_sensor_names=add_sensor_names)
    return return_nodes

