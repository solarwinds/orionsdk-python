# -*- coding: utf-8 -*-
"""SolarWinds Class Overview

The following class is used to create an object representing a SolarWinds Orion instance.  The object provides simple
getter and setter methods for common SolarWinds actions.  These methods abstract out the underlying details and SWQL
calls making SolarWinds automation more accessible to a broader audience.
Pass in port 17778 for pre-2023.1 Orion Platform.

"""

import logging
from .swisclient import SwisClient


class SolarWinds:

    def __init__(self, npm_server, username, password, logger=None, port=17774, verify=False):

        self.logger = logger or logging.getLogger('__name__')

        # Create the SWIS client for use throughout the instance.
        self.swis = SwisClient(npm_server, username, password, port, verify)

    def does_node_exist(self, node_name):
        """ Checks to see if a SolarWinds node exists with the given name.  Calls the get_node_id method of the class
            and uses the returned value to determine whether or not the node exists.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.

            Returns:
                True: The node exists.
                False: The node does not exist.

        """

        if self.get_node_id(node_name):
            return True
        else:
            return False

    def get_node_id(self, node_name):
        """ Returns the NodeID for the given NodeName.  Uses a SWIS query to the SolarWinds database to retrieve this
            information.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.

            Returns:
                node_id (string): The node ID that corresponds to the specified node name.

        """

        node_id = self.swis.query("SELECT NodeID, Caption FROM Orion.Nodes WHERE Caption = @caption",
                                  caption=node_name)

        self.logger.info("get_node_id - node_id query results: %s.", node_id)

        if node_id['results']:
            return node_id['results'][0]['NodeID']
        else:
            return ""

    def get_node_uri(self, node_name):
        """ Returns the NodeURI for the given NodeName.  Uses a SWIS query to the SolarWinds database to retrieve this
            information.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.

            Returns:
                node_id (string): The node URI that corresponds to the specified node name.

        """

        node_uri = self.swis.query("SELECT Caption, Uri FROM Orion.Nodes WHERE Caption = @caption",
                                   caption=node_name)

        self.logger.info("get_node_uri - node uri query results: %s.", node_uri)
        if node_uri['results']:
            return node_uri['results'][0]['Uri']
        else:
            return ""

    def get_node_caption_from_ip(self, ip_addr):
        """ Returns the NodeCaption for the given IP_Address.  Uses a SWIS query to the SolarWinds database to retrieve this
            information.

            Args:
                ip_addr(string): An IP which should equal the IP_Address used in SolarWinds for the node object.

            Returns:
                node_caption(string): A node name which should equal the caption used in SolarWinds for the node object.

        """

        node_caption = self.swis.query("SELECT Caption, IP_Address FROM Orion.Nodes WHERE IP_Address = @ip_addr",
                                   ip_addr=ip_addr)
        self.logger.info("get_node_caption_from_ip - node caption query results: %s.", node_caption)
        if node_caption['results']:
            return node_caption['results'][0]['Caption']
        else:
            return ""

    def get_ncmnode_id(self, node_caption):
        """ Returns the NCM NodeID for the given NodeName.  Uses a SWIS query to the SolarWinds database to retrieve this
            information.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.

            Returns:
                node_id (string): The ncm node id that corresponds to the specified node name.

        """

        node_id = self.swis.query("SELECT NodeID, NodeCaption FROM NCM.Nodes WHERE NodeCaption = @caption",
                                   caption=node_caption)

        self.logger.info("get_ncmnode_id - NCM node uri query results: %s.", node_id)
        if node_id['results']:
            return node_id['results'][0]['NodeID']
        else:
            return ""

    def add_node_using_snmp_v3(self, node_name, ip_address, snmpv3_username, snmpv3_priv_method, snmpv3_priv_pwd,
                               snmpv3_auth_method, snmpv3_auth_pwd):
        """ Creates a new node using the supplied name an IP address.  Configure with our standard SNMPv3 credentials.
            Once created, attached all of the standard Cisco pollers.

            Args:
                node_name(string): A node name to be used for the newly created node object.
                ip_address(string): The IP address that is associated with the supplied node name.
                snmpv3_username(string): The SNMPv3 username that will be associated with the node object.
                snmpv3_priv_method(string): The SNMPv3 privilege method that will be used.
                snmpv3_priv_pwd (string): The SNMPv3 privilege password that will be used.
                snmpv3_auth_method(string): The SNMPv3 authentication method that will be used.
                snmpv3_auth_pwd (string): The SNMPv3 authentication password that will be used.

            Returns:
                None.

        """

        if not self.does_node_exist(node_name):
            # set up property bag for the new node
            node_properties = {
                'IPAddress': ip_address,
                'EngineID': 1,
                'ObjectSubType': 'SNMP',
                'SNMPVersion': 3,
                'SNMPV3Username': snmpv3_username,
                'SNMPV3PrivMethod': snmpv3_priv_method,
                'SNMPV3PrivKeyIsPwd': True,
                'SNMPV3PrivKey': snmpv3_priv_pwd,
                'SNMPV3AuthMethod': snmpv3_auth_method,
                'SNMPV3AuthKeyIsPwd': True,
                'SNMPV3AuthKey': snmpv3_auth_pwd,
                'DNS': '',
                'SysName': '',
                'Caption': node_name
            }

            # Create base node object.
            results = self.swis.create('Orion.Nodes', **node_properties)
            self.logger.info("add_node - add node invoke results: %s", results)

            # Assign pollers to node.
            self.attach_poller_to_node(node_name, 'N.Status.ICMP.Native')
            self.attach_poller_to_node(node_name, 'N.Status.SNMP.Native', False)
            self.attach_poller_to_node(node_name, 'N.ResponseTime.ICMP.Native')
            self.attach_poller_to_node(node_name, 'N.ResponseTime.SNMP.Native', False)
            self.attach_poller_to_node(node_name, 'N.Details.SNMP.Generic')
            self.attach_poller_to_node(node_name, 'N.Uptime.SNMP.Generic')

    def is_poller_attached_to_node(self, node_name, poller_name):
        """ Checks to see if the specified poller is attached to the specified node.  Makes a SWIS query to see
            if there's a corresponding entry in the Orion.Pollers table.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
                poller_name(string): The name of the poller as represented in the SolarWinds database.

            Returns:
                True: The poller is currently attached to the node.
                False: The poller is not currently attached to the node.

        """

        net_object_id = str(self.get_node_id(node_name))
        net_object = 'N:' + net_object_id

        results = self.swis.query("SELECT PollerType FROM Orion.Pollers WHERE NetObject = @net_object AND PollerType "
                                  "= @poller_name", net_object=net_object, poller_name=poller_name)
        self.logger.info("is_poller_attached_to_node - check for poller query results: %s", results)

        if results['results']:
            return True
        else:
            return False

    def attach_poller_to_node(self, node_name, poller_name, enabled=True):
        """ Checks to see if the specified poller is attached to the specified node.  If it is not, a SWIS create is
            executed against Orion.Pollers to attach the poller to the node.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
                poller_name(string): The name of the poller as represented in the SolarWinds database.
                enabled(boolean): Whether or not to enable the attached poller.

            Returns:
                None.

        """

        if not self.is_poller_attached_to_node(node_name, poller_name):
            net_object_id = str(self.get_node_id(node_name))
            net_object = 'N:' + net_object_id

            poller_properties = {
                'PollerType': poller_name,
                'NetObject': net_object,
                'NetObjectType': 'N',
                'NetObjectID': net_object_id,
                'Enabled': enabled
            }

            results = self.swis.create('Orion.Pollers', **poller_properties)
            self.logger.info("attach_poller_to_node - poller create results: %s", results)

    def enable_hardware_health_on_node(self, node_name):
        """ Enables the hardware health monitoring on the specified node.  Executes a SWIS invoke of the
            'EnableHardwareHealth' verb, passing it the node's net object ID.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.

            Returns:
                None.

        """

        net_object_id = str(self.get_node_id(node_name))
        net_object = 'N:' + net_object_id

        results = self.swis.invoke('Orion.HardwareHealth.HardwareInfo', 'EnableHardwareHealth', net_object, 9)
        self.logger.info("enable_hardware_health - enable hardware health invoke results: %s", results)

    def add_node_to_ncm(self, node_caption):
        """ Adds the specified node to the SolarWinds NCM module.  Executes a SWIS invoke of the
            'AddNodetoNCM' verb, passing it the node's object ID.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.

            Returns:
                None.

        """

        results = self.swis.invoke('Cirrus.Nodes', 'AddNodeToNCM', self.get_node_id(node_caption))
        self.logger.info("add_node_to_ncm - add node to ncm invoke results: %s", results)
    
    def remove_node_from_ncm(self, node_caption):
        """ Removes the specified node from the SolarWinds NCM module. Executes a SWIS invoke of the
            'RemoveNode' verb, passing it the node's NCM node id.

            Args:
                node_caption(string): A node name which should equal the caption used in SolarWinds for the node object.

            Returns:
                None.

        """

        results = self.swis.invoke('Cirrus.Nodes', 'RemoveNode', self.get_ncmnode_id(node_caption))
        self.logger.info("remove_node_from_ncm - remove node from ncm invoke results: %s", results)

    def add_node_to_udt(self, node_name):
        udt_properties = {
            'NodeID': self.get_node_id(node_name),
            'Capability': '2',
            'Enabled': True
        }

        results = self.swis.create('Orion.UDT.NodeCapability', **udt_properties)
        self.logger.info("add_node_to_udt - add node at l2 to udt create results: %s", results)

        udt_properties = {
            'NodeID': self.get_node_id(node_name),
            'Capability': '3',
            'Enabled': True
        }

        results = self.swis.create('Orion.UDT.NodeCapability', **udt_properties)
        self.logger.info("add_node_to_udt - add node at l3 to udt create results: %s", results)

    def add_node_to_ip_vnqm(self, node_name):
        vnqm_node_properties = {
            'NodeID': self.get_node_id(node_name),
            'Name': node_name,
            'IsHub': False,
            'IsAutoConfigured': True
        }

        results = self.swis.create('Orion.IpSla.Sites', **vnqm_node_properties)
        self.logger.info("add_node_to_vnqm - add node to vnqm create results: %s", results)

    def add_icmp_echo_ip_sla_operation_to_node(self, node_name, ip_sla_operation_number, ip_sla_name):
        ip_sla_properties = {
            'NodeID': self.get_node_id(node_name),
            'OperationTypeID': 5,
            'OperationType': "ICMP Echo",
            'IsAutoConfigured': False,
            'Frequency': 10,
            'IpSlaOperationNumber': ip_sla_operation_number,
            'OperationName': ip_sla_name
        }

        results = self.swis.create('Orion.IpSla.Operations', **ip_sla_properties)
        self.logger.info("add_icmp_echo_ip_sla_operation_to_node - add IP SLA operation to node create results: %s", results)

    def add_group_custom_property(self, property_name, description, value_type, size):
        """ Add a new group custom property with the specified name and details.

            Args:
                property_name(string): Name of the new group property.
                description(string): Description for the new group property.
                value_type(string): Value type for the new group property (string, integer, datetime, single, double,
                    boolean)
                size(integer): The maximum length for string value types.  Ignored for other value types.

            Returns:
                None.

        """

        results = self.swis.invoke('Orion.GroupCustomProperties', 'CreateCustomProperty', property_name, description,
                                   value_type, size, "", "", "", "", "", "")
        self.logger.info("add_group_custom_property - add group custom property results: %s", results)

    def set_group_custom_property(self, group_name, custom_property_name, custom_property_value):
        """ For a given group, sets the specified custom property to the specified value.

            Args:
                group_name(string): A group name which should equal the caption used in Solarwinds for the group object.
                custom_property_name(string): The custom property who's value we want to change.  The custom property
                    needs to have been previously created or nothing will be changed.
                custom_property_value(string): The desired value that the custom property will be set to.

            Returns:
                None.

        """

        group_uri = self.get_group_uri(group_name)

        custom_property = {
            custom_property_name: custom_property_value
        }

        self.swis.update(group_uri + '/CustomProperties', **custom_property)
        
    def set_node_custom_property(self, node_name, custom_property_name, custom_property_value):
        """ For a given node, sets the specified custom property to the specified value.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
                custom_property_name(string): The custom property who's value we want to change.  The custom property
                    needs to have been previously created or nothing will be changed.
                custom_property_value(string): The desired value that the custom property will be set to.

            Returns:
                None.

        """

        node_uri = self.get_node_uri(node_name)

        custom_property = {
            custom_property_name: custom_property_value
        }

        self.swis.update(node_uri + '/CustomProperties', **custom_property)

    def get_node_custom_properties(self, node_name):
        """ For a given node, gets a list of the custom properties and values associated with it.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.

            Returns:
                custom_properties(list): A list of dictionaries.  Each dictionary is a single key/value pair that contains
                    the custom property name and value.

        """

        node_uri = self.get_node_uri(node_name)

        custom_properties = self.swis.read(node_uri + '/CustomProperties')
        self.logger.info("set_custom_properties - custom_properties read results: %s", custom_properties)

        return custom_properties

    def get_list_of_custom_pollers_for_node(self, node_name):
        """ For a given node, gets a list of the currently assigned custom pollers.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.

            Returns:
                custom_pollers(dictionary): Returns a dictionary that represents all of the custom pollers attached to
                    the node.  Each key is the custom property name and the value is the associated custom property
                    value.

        """

        node_id = self.get_node_id(node_name)

        custom_pollers = self.swis.query("SELECT CustomPollerName FROM Orion.NPM.CustomPollerAssignment WHERE NodeID "
                                         "= @node_id", node_id=node_id)
        self.logger.info("get_list_of_custom_pollers_by_name - custom_pollers query results: %s", custom_pollers)

        return custom_pollers['results']

    def remove_custom_poller_by_name(self, node_name, poller_name):
        """ For a given node, detaches the specified custom poller.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
                poller_name(string): The name of the custom poller that will be removed from the node.

            Returns:
                None.

        """

        node_id = self.get_node_id(node_name)

        custom_poller_id = self.swis.query("SELECT CustomPollerID FROM Orion.NPM.CustomPollers WHERE UniqueName = "
                                           "@poller_name", poller_name=poller_name)
        self.logger.info("remove_custom_poller_by_name - custom_poller_id query results: %s", custom_poller_id)

        custom_poller_uri = self.swis.query("SELECT Uri FROM Orion.NPM.CustomPollerAssignmentOnNode WHERE "
                                            "NodeID=@node_id AND CustomPollerID=@custom_poller_id", node_id=node_id,
                                            custom_poller_id=custom_poller_id['results'][0]['CustomPollerID'])
        self.logger.info("remove_custom_poller_by_name - custom_poller_uri query results: %s", custom_poller_uri)

        self.swis.delete(custom_poller_uri['results'][0]['Uri'])

    def add_custom_poller_by_name(self, node_name, poller_name):
        """ For a given node, attaches the specified custom poller.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
                poller_name(string): The name of the custom poller which is to be attached to the specified node.

            Returns:
                None.

        """

        node_id = self.get_node_id(node_name)

        custom_poller_id = self.swis.query(
            "SELECT CustomPollerID FROM Orion.NPM.CustomPollers WHERE UniqueName = @poller_name",
            poller_name=poller_name)
        self.logger.info("add_custom_poller_by_name - custom_poller_id query results: %s", custom_poller_id)

        poller_properties = {
            'NodeID': node_id,
            'customPollerID': custom_poller_id['results'][0]['CustomPollerID']
        }

        self.swis.create('Orion.NPM.CustomPollerAssignmentOnNode', **poller_properties)

    def does_group_exist(self, group_name):
        """ Checks to see if a SolarWinds group exists with the given name.  Calls the get_group_id method of the class
            and uses the returned value to determine whether or not the group exists.

            Args:
                group_name(string): A group name which should equal the name used in SolarWinds for the container
                    object.

            Returns:
                True: The group exists.
                False: The group does not exist.

        """

        if self.get_group_id(group_name):
            return True
        else:
            return False

    def get_group_id(self, group_name):
        """ Returns the ContainerID for the given Group Name.  Uses a SWIS query to the SolarWinds database to retrieve
            this information.

            Args:
                group_name(string): A group name which should equal the name used in SolarWinds for the container
                    object.

            Returns:
                group_id (string): The group ID that corresponds to the specified group name.

        """

        group_id = self.swis.query("SELECT ContainerID FROM Orion.Container WHERE Name = @group_name",
                                   group_name=group_name)
        self.logger.info("get_group_id - group_id query results: %s", group_id)

        if group_id['results']:
            return group_id['results'][0]['ContainerID']
        else:
            return ""

    def get_group_uri(self, group_name):
        """ Returns the ContainerUri for the given Group Name.  Uses a SWIS query to the SolarWinds database to retrieve this
            information.

            Args:
                group_name(string): A group name which should equal the name used in SolarWinds for the container object.

            Returns:
                group_uri (string): The group URI that corresponds to the specified group name.

        """

        group_uri = self.swis.query("SELECT Uri FROM Orion.Container WHERE Name = @group_name",
                                    group_name=group_name)
        self.logger.info("get_group_uri - group_uri query results: %s", group_uri)

        if group_uri['results']:
            return group_uri['results'][0]['Uri']
        else:
            return ""

    def add_group(self, group_name, owner='Core', refresh_frequency=60, status_rollup=0,
                  group_description='', polling_enabled=True, group_members=None):
        """ Creates a new empty group using the supplied name.  Sets all of the additional parameters to the default
            values.

            Args:
                group_name(string): A group name to be used for the newly created container.
                owner(string): Must be 'Core'.
                refresh_frequency(int): How often the group membership is updated.
                status_rollup(int): Status rollup mode.
                    # 0 = Mixed status shows warning
                    # 1 = Show worst status
                    # 2 = Show best status
                group_description(string):
                polling_enabled(boolean): Whether polling of the group is enabled or disabled.
                group_members(list): A list of group members and/or dynamic filters.

            Returns:
                None.

        """

        if group_members is None:
            group_members = []
        if not self.does_group_exist(group_name):
            results = self.swis.invoke('Orion.Container', 'CreateContainer', group_name, owner, refresh_frequency,
                                       status_rollup, group_description, polling_enabled, group_members)
            self.logger.info("add_group - add group invoke results: %s", results)

    def is_node_in_group(self, node_name, group_name):
        """ Checks to see if a node is a member of a particular group.  Runs a SWIS query against the ContainerMembers
            table to see if there's a corresponding table entry.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
                group_name(string): A group name which should equal the name used in SolarWinds for the container
                    object.

            Returns:
                True: The node is in the group.
                False: The node is not in the group.

        """

        results = self.swis.query("SELECT Name FROM Orion.ContainerMembers WHERE ContainerID = @group_id and FullName "
                                  "= @node_name", group_id=self.get_group_id(group_name), node_name=node_name)
        self.logger.info("is_node_in_group - is_node_in_group query results: %s", results)

        if results['results']:
            return True
        else:
            return False

    def add_node_to_group(self, node_name, group_name):
        """ If the specified node is not already in the specified group, a SWIS invoke of Orion.Container.AddDefinition
            is made to add the node to the group.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
                group_name(string): A group name which should equal the name used in SolarWinds for the container object.

            Returns:
                None.

        """

        if not self.is_node_in_group(node_name, group_name):
            member_definition = {"Name": node_name, "Definition": self.get_node_uri(node_name)}
            self.swis.invoke('Orion.Container', 'AddDefinition', int(self.get_group_id(group_name)), member_definition)

    def delete_group_by_id(self, group_id):
        """ Delete a group that has the specified group id.

            Args:
                group_id(string): A group id which should equal the ContainerID used in SolarWinds for the container
                    object.

            Returns:
                None.

        """

        self.swis.invoke('Orion.Container', 'DeleteContainer', int(group_id))

    def delete_group_by_name(self, group_name):
        """ Delete a group that has the specified group name.

            Args:
                group_name(string): A group name which should equal the Name used in SolarWinds for the container
                    object.

            Returns:
                None.

        """

        group_id = self.get_group_id(group_name)

        self.delete_group_by_id(group_id)

    def does_dependency_exist(self, dependency_name):
        """ Checks to see if a SolarWinds dependency exists with the given name.  Calls the get_dependency_id method of
            the class and uses the returned value to determine whether or not the dependency exists.

            Args:
                dependency_name(string): A dependency name which should equal the name used in SolarWinds for the
                    dependency object.

            Returns:
                True: The dependency exists.
                False: The dependency does not exist.

        """

        if self.get_dependency_id(dependency_name):
            return True
        else:
            return False

    def get_dependency_id(self, dependency_name):
        """ Returns the DependencyID for the given Dependency Name.  Uses a SWIS query to the SolarWinds database to
            retrieve this information.

            Args:
                dependency_name(string): A dependency name which should equal the name used in SolarWinds for the
                    dependency object.

            Returns:
                dependency_id (string): The dependency ID that corresponds to the specified dependency name.

        """

        dependency_id = self.swis.query("SELECT DependencyId FROM Orion.Dependencies WHERE Name = @dependency_name",
                                        dependency_name=dependency_name)
        self.logger.info("get_dependency_id - dependency_id query results: %s", dependency_id)

        if dependency_id['results']:
            return dependency_id['results'][0]['DependencyId']
        else:
            return ""

    def add_dependency(self, dependency_name, parent_name, child_name):
        """ Creates a new dependency using the specified parent and child.  Does a SWIS create to the Orion.Dependencies
            table to create the dependency.

            Args:
                dependency_name(string): A dependency name to be used for the newly created dependency.
                parent_name(string): Name of the parent to be used in the dependency definition.
                child_name(string): Name of the child to be used in the dependency definition.

            Returns:
                True: The dependency was successfully created.
                False: The dependency was not created.

        """

        if not self.does_dependency_exist(dependency_name):
            if self.does_node_exist(parent_name):
                self.logger.info("add-dependency - The parent is a node.")
                parent_id = self.get_node_id(parent_name)
                parent_uri = self.get_node_uri(parent_name)
                parent_entity_type = 'Orion.Nodes'
            elif self.does_group_exist(parent_name):
                self.logger.info("add-dependency - The parent is a group.")
                parent_id = self.get_group_id(parent_name)
                parent_uri = self.get_group_uri(parent_name)
                parent_entity_type = 'Orion.Groups'
            else:
                return False

            if self.does_node_exist(child_name):
                self.logger.info("add-dependency - The child is a node.")
                child_id = self.get_node_id(child_name)
                child_uri = self.get_node_uri(child_name)
                child_entity_type = 'Orion.Nodes'
            elif self.does_group_exist(child_name):
                self.logger.info("add-dependency - The child is a group.")
                child_id = self.get_group_id(child_name)
                child_uri = self.get_group_uri(child_name)
                child_entity_type = 'Orion.Groups'
            else:
                return False

            dependency_properties = {
                'Name': dependency_name,
                'ParentUri': parent_uri,
                'ParentEntityType': parent_entity_type,
                'ParentNetObjectId': parent_id,
                'ChildUri': child_uri,
                'ChildEntityType': child_entity_type,
                'ChildNetObjectId': child_id
            }

            self.swis.create('Orion.Dependencies', **dependency_properties)

    def get_list_of_interfaces(self, node_name):
        """ Returns a dictionary of existing Interfaces on a given Node Name. Uses a SWIS query to the SolarWinds
            database to retrieve this information.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
            Returns:
                list_interfaces_names(dictionary): Returns a dictionary that represents all of the interfaces, by name,
                attached to the node.
        """

        node_id = self.get_node_id(node_name)

        list_interfaces_names = self.swis.query("SELECT Name FROM Orion.NPM.Interfaces WHERE NodeID "
                                                "= @node_id", node_id=node_id)

        self.logger.info("get_list_of_interfaces_by_name - list_of_interface_names query results: %s",
                         list_interfaces_names)

        if list_interfaces_names['results']:
            return list_interfaces_names['results']
        else:
            return ""

    def remove_interface(self, node_name, interface_name):
        """ For a given node, remove the given interface from the node using the interface name.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
                interface_name(string): The name of the interface that will be removed from the node.
            Returns:
                True: Interface was successfully removed.
                False: Interface was not removed.

        """

        interface_uri = self.get_interface_uri(node_name, interface_name)

        if self.does_interface_exist(node_name, interface_name):
            self.logger.info("remove_interface_by_name - interface_uri query results: %s", interface_uri)
            self.swis.delete(interface_uri)
            return True
        else:
            return False

    def get_interface_uri(self, node_name, interface_name):
        """ Returns the URI for a given interface belonging to a given node. Uses a SWIS query to the SolarWinds
            database to retrieve this information

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
                interface_name(string): The name of the interface that you are getting the URI for

            Returns:
                interface_uri(string): The interface URI that corresponds to the specified interface name

        """

        node_id = self.get_node_id(node_name)

        interface_uri = self.swis.query(
            "SELECT Uri FROM Orion.NPM.Interfaces WHERE NodeID=@node_id AND "
            "InterfaceName=@interface_name", node_id=node_id, interface_name=interface_name)

        if interface_uri['results']:
            return interface_uri['results'][0]['Uri']
        else:
            return ""

    def get_interface_id(self, node_name, interface_name):
        """ Returns the InterfaceID for a given interface belonging to a given node. Uses a SWIS query to the SolarWinds
            database to retrieve this information

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
                interface_name(string): The name of the interface that you are getting the ID of.

            Returns:
                interface_id(string): The interface ID that corresponds to the specified interface name

        """

        node_id = self.get_node_id(node_name)

        interface_id = self.swis.query("SELECT InterfaceID FROM Orion.NPM.Interfaces WHERE NodeID=@node_id AND "
                                       "Name = @interface_name", node_id=node_id, interface_name=interface_name)

        if interface_id['results']:
            return interface_id['results'][0]['InterfaceID']
        else:
            return ""

    def does_interface_exist(self, node_name, interface_name):
        """ Checks to see if a SolarWinds interface, belonging to a given node, exists with the given name. Calls the
            get_interface_id method of the class and uses the returned value to determine whether or not the interface
            exists.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
                interface_name(string): The name of the interface that you are getting the URI for

            Returns:
                True: The interface exists.
                False: THe interface does not exist.

        """

        if self.get_interface_id(node_name, interface_name):
            return True
        else:
            return False

    def get_discovered_interfaces(self, node_name):
        """ Returns a dictionary of Discovered Interfaces on a node given that node's name. Uses a SWIS invoke for
            DiscoverInterfacesOnNode.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.

            Returns:
                discovered_interfaces(Dictionary): The set of discovered interfaces on the node.
        """

        node_id = self.get_node_id(node_name)

        discovered_interfaces = self.swis.invoke('Orion.NPM.Interfaces', 'DiscoverInterfacesOnNode', node_id)

        return discovered_interfaces['DiscoveredInterfaces']

    def add_interface(self, node_name, interface_name):
        """ For a given node, attach the given interface by that interface's name. The given interface must be a
            discovered interface to be attached to the node. Uses a SWIS invoke for AddInterfacesOnNode.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.
                interface_name(string): The name of the interface that will be added to the node.

            Returns:
                True: The interface was added to the node.
                False: The interface was not successfully added to the node.

        """

        node_id = self.get_node_id(node_name)

        discovered_interfaces = self.get_discovered_interfaces(node_name)
        discovered_interface = [

            x for x
            in discovered_interfaces
            if x['Caption'].startswith(interface_name)

        ]

        if discovered_interface:
            self.swis.invoke('Orion.NPM.Interfaces',
                             'AddInterfacesOnNode',
                             node_id,
                             discovered_interface,
                             'AddDefaultPollers')

        else:
            return False

    def ncm_download_nodes_running_config(self, node_name):
        """ For a given node, download the node's running configuration. Uses a SWIS query to find the Cirrus node I.
            Uses a Swis invoke of DownloadConfig.

            Args:
                node_name(string): A node name which should equal the caption used in SolarWinds for the node object.

            Returns:
                None.

        """

        results = self.swis.query('SELECT NodeID FROM Cirrus.Nodes WHERE NodeCaption = @node_name',
                                  node_name=node_name)['results']

        cirrus_node_id = results[0]['NodeID']

        self.swis.invoke('Cirrus.ConfigArchive', 'DownloadConfig', [cirrus_node_id], 'Running')

    def ncm_run_compliance_report(self, report_name):
        """ For a given report name, run the Policy Report. Uses a SWIS query to get the policy report ID. Uses a
            SWIS invoke of StartCaching to run the policy report.

            Args:
                report_name(string): A report name which should equal the Name used in SolarWinds for a Policy
                    Report object

            Returns:
                None.

        """

        results = self.swis.query('SELECT PolicyReportID FROM Cirrus.PolicyReports WHERE Name = @report_name',
                                  report_name=report_name)

        report_id = results['results'][0]['PolicyReportID']
        self.swis.invoke('Cirrus.PolicyReports', 'StartCaching', [report_id])

    def add_dns_a_record_with_ptr_to_ipam(self, name, ip_address, server, domain):
        """ Add a DNS A and PTR record to the specified domain with the supplied name and IP address.

            Args:
                ip_address(string):  The IP address to be used in the new DNS record.
                name(string): The name to be used in the new DNS record.
                server(string): The name or IP of the DNS server that hosts the domain.
                domain(string): The domain that the new DNS record will be added to.

            Returns:
                None.

        """

        self.swis.invoke('IPAM.IPAddressManagement', 'AddDnsARecordWithPtr', name, ip_address, server, domain)
  
