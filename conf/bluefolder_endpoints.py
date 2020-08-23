import datetime

def getEndpoints(startDate, EndDate):

    endpoints = {"serviceRequests_created": {"url": "serviceRequests/list.aspx",
                                     "filters": "".join(["<request>",
                                                 "<listType>",
                                                 "basic",
                                                 "</listType>",
                                                 "<dateRange dateField='dateTimeCreated'>",
                                                "<startDate>",
                                                startDate.strftime("%m-%d-%Y") + " 00:00 AM",
                                                "</startDate>",
                                                "<endDate>",
                                                EndDate.strftime("%m-%d-%Y") + " 00:00 AM",
                                                "</endDate>",
                                                "</dateRange>",
                                                 "</request>"]),
                                     "id_column": "serviceRequestId",
                                     "id_column_is_string": False,
                                     "innerList": True,
                                     "saveTo": "serviceRequests_created",
                                     "table": "serviceRequests"
                                    },

                  "serviceRequests_created_prev": {"url": "serviceRequests/list.aspx",
                                     "filters": "".join(["<request>",
                                                 "<listType>",
                                                 "basic",
                                                 "</listType>",
                                                 "<dateRange dateField='dateTimeCreated'>",
                                                "<startDate>",
                                                (startDate - datetime.timedelta(days=30*6)).strftime("%m-%d-%Y") + " 00:00 AM",
                                                "</startDate>",
                                                "<endDate>",
                                                (EndDate - datetime.timedelta(days=30*6)).strftime("%m-%d-%Y") + " 00:00 AM",
                                                "</endDate>",
                                                "</dateRange>",
                                                 "</request>"]),
                                     "id_column": "serviceRequestId",
                                     "id_column_is_string": False,
                                     "innerList": True,
                                     "saveTo": "serviceRequests_created_prev",
                                     "table": "serviceRequests"
                                    },


                  "serviceRequests_closed": {"url": "serviceRequests/list.aspx",
                                     "filters": "".join(["<request>",
                                                 "<listType>",
                                                 "basic",
                                                 "</listType>",
                                                 "<dateRange dateField='dateTimeClosed'>",
                                                "<startDate>",
                                                startDate.strftime("%m-%d-%Y") + " 00:00 AM",
                                                "</startDate>",
                                                "<endDate>",
                                                EndDate.strftime("%m-%d-%Y") + " 00:00 AM",
                                                "</endDate>",
                                                "</dateRange>",
                                                 "</request>"]),
                                     "id_column": "serviceRequestId",
                                     "id_column_is_string": False,
                                     "innerList": True,
                                     "saveTo": "serviceRequests_closed",
                                     "table": "serviceRequests"
                                    },

                   "serviceRequests_closed_prev": {"url": "serviceRequests/list.aspx",
                                     "filters": "".join(["<request>",
                                                 "<listType>",
                                                 "basic",
                                                 "</listType>",
                                                 "<dateRange dateField='dateTimeClosed'>",
                                                "<startDate>",
                                                (startDate - datetime.timedelta(days=6*30)).strftime("%m-%d-%Y") + " 00:00 AM",
                                                "</startDate>",
                                                "<endDate>",
                                                (EndDate - datetime.timedelta(days=6*30)).strftime("%m-%d-%Y") + " 00:00 AM",
                                                "</endDate>",
                                                "</dateRange>",
                                                 "</request>"]),
                                     "id_column": "serviceRequestId",
                                     "id_column_is_string": False,
                                     "innerList": True,
                                     "saveTo": "serviceRequests_closed_prev",
                                     "table": "serviceRequests"
                                    },




                "contracts": {"url": "contracts/list.aspx",
                              "filters": "".join(["<request>",
                                                 "<listType>",
                                                 "basic",
                                                 "</listType>",
                                                 "</request>"]),
                              "id_column": "contractId",
                              "id_column_is_string": True,
                              "innerList": True,
                              "saveTo": "contracts",
                              "table": "contracts"
                            
                            
                            },
                "customers": {"url": "customers/list.aspx",
                              "filters": "".join(["<request>",
                                                 "<listType>",
                                                 "basic",
                                                 "</listType>",
                                                 "</request>"]),
                             "id_column": "customerId",
                             "id_column_is_string": False,
                             "innerList": False,
                             "saveTo": "customers",
                             "table": "customers"
                             
                            },
                "assignments": {"url": "serviceRequests/getAssignmentList.aspx",
                                "filters": "".join(["<request>",
                                                    "<serviceRequestAssignmentList>",
                                                    "<dateRangeStart>",
                                                    startDate.strftime("%m-%d-%Y") + " 00:00 AM",
                                                    "</dateRangeStart>",
                                                    "<dateRangeEnd>",
                                                    EndDate.strftime("%m-%d-%Y") + " 00:00 AM"
                                                    "</dateRangeEnd>",
                                                    "</serviceRequestAssignmentList>",
                                                 "</request>"]),
                               "id_column": "assignmentId",
                               "id_column_is_string": False,
                               "innerList": False,
                               "saveTo": "assignments",
                               "table": "assignments"
                               
                               
                                },
                "users": {"url": "users/list.aspx",
                          "filters": "".join(["<request>",
                                                 "<listType>",
                                                 "full",
                                                 "</listType>",
                                                 "</request>"]),

                          "id_column": "userId",
                          "innerList": False,
                          "id_column_is_string": False,
                          "saveTo": "users",
                          "table": "users"
                
                         }
                


                }


    return endpoints


 #"endpoints": {"serviceRequests/list.aspx": "serviceRequests",
 #              "contracts/list.aspx": "contracts",
 #              "customers/list.aspx": "customers",
 #              "attachments/list.aspx": "attachements",
 #              "appointments/list.aspx": "appointments",
 #              "serviceRequests/getAssignmentList.aspx": "assignments",
 #              "equipment/list.aspx": "equipment"},