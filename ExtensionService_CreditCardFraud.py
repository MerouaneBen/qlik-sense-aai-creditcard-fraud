#! /usr/bin/env python3
import argparse
import json
import logging
import logging.config
import os
import sys
import time
from concurrent import futures
from datetime import datetime

# Added for linear regression modeling
import numpy
import pylab
from sklearn import linear_model

# Add Generated folder to module path.
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(PARENT_DIR, 'Generated'))

import ServerSideExtension_pb2 as SSE
import grpc
from SSEData_CreditCardFraud import FunctionType
from ScriptEval_CreditCardFraud import ScriptEval

# Tensorflow, Keras
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import keras
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

# Read data from a file used for training/test
df_for_modelling = pd.read_csv('./data/creditcard.csv')
df_for_modelling['Class'].unique() # 0 = no fraud, 1 = fraudulent
X = df_for_modelling.iloc[:, :-1].values
X_train, X_test= train_test_split(X,test_size=0.1, random_state=1)

# Define StandardScaler and calculate fit
sc = StandardScaler()
sc.fit(X_train)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ExtensionService(SSE.ConnectorServicer):
    """
    A simple SSE-plugin created for the HelloWorld example.
    """

    def __init__(self, funcdef_file):
        """
        Class initializer.
        :param funcdef_file: a function definition JSON file
        """
        self._function_definitions = funcdef_file
        self.ScriptEval = ScriptEval()
        if not os.path.exists('logs'):
            os.mkdir('logs')
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logger.config')
        logging.config.fileConfig(log_file)
        logging.info('Logging enabled')

    @property
    def function_definitions(self):
        """
        :return: json file with function definitions
        """
        return self._function_definitions

    @property
    def functions(self):
        """
        :return: Mapping of function id and implementation
        """
        return {
            0: '_predict_fraud',
            1: '_my_func_aggr',
            2: '_cache',
            3: '_no_cache'
        }

    @staticmethod
    def _get_function_id(context):
        """
        Retrieve function id from header.
        :param context: context
        :return: function id
        """
        metadata = dict(context.invocation_metadata())
        header = SSE.FunctionRequestHeader()
        header.ParseFromString(metadata['qlik-functionrequestheader-bin'])

        return header.functionId

    """
    Implementation of added functions.
    """

    @staticmethod
    def _predict_fraud(request, context):
        """
        Mirrors the input and sends back the same data.
        :param request: iterable sequence of bundled rows
        :return: the same iterable sequence as received
        """

        # Disable caching.
        md = (('qlik-cache', 'no-store'),)
        context.send_initial_metadata(md)

        Time = [];
        V01 = [];
        V02 = [];
        V03 = [];
        V04 = [];
        V05 = [];
        V06 = [];
        V07 = [];
        V08 = [];
        V09 = [];
        V10 = [];
        V11 = [];
        V12 = [];
        V13 = [];
        V14 = [];
        V15 = [];
        V16 = [];
        V17 = [];
        V18 = [];
        V19 = [];
        V20 = [];
        V21 = [];
        V22 = [];
        V23 = [];
        V24 = [];
        V25 = [];
        V26 = [];
        V27 = [];
        V28 = [];
        Amount = [];

        for request_rows in request:
            response_rows = []
            for row in request_rows.rows:
                Time.append(row.duals[0].numData)
                V01.append(row.duals[1].numData)
                V02.append(row.duals[2].numData)
                V03.append(row.duals[3].numData)
                V04.append(row.duals[4].numData)
                V05.append(row.duals[5].numData)
                V06.append(row.duals[6].numData)
                V07.append(row.duals[7].numData)
                V08.append(row.duals[8].numData)
                V09.append(row.duals[9].numData)
                V10.append(row.duals[10].numData)
                V11.append(row.duals[11].numData)
                V12.append(row.duals[12].numData)
                V13.append(row.duals[13].numData)
                V14.append(row.duals[14].numData)
                V15.append(row.duals[15].numData)
                V16.append(row.duals[16].numData)
                V17.append(row.duals[17].numData)
                V18.append(row.duals[18].numData)
                V19.append(row.duals[19].numData)
                V20.append(row.duals[20].numData)
                V21.append(row.duals[21].numData)
                V22.append(row.duals[22].numData)
                V23.append(row.duals[23].numData)
                V24.append(row.duals[24].numData)
                V25.append(row.duals[25].numData)
                V26.append(row.duals[26].numData)
                V27.append(row.duals[27].numData)
                V28.append(row.duals[28].numData)
                Amount.append(row.duals[29].numData)

        data = {
            'V00': Time,
            'V01': V01,
            'V02': V02,
            'V03': V03,
            'V04': V04,
            'V05': V05,
            'V06': V06,
            'V07': V07,
            'V08': V08,
            'V09': V09,
            'V10': V10,
            'V11': V11,
            'V12': V12,
            'V13': V13,
            'V14': V14,
            'V15': V15,
            'V16': V16,
            'V17': V17,
            'V18': V18,
            'V19': V19,
            'V20': V20,
            'V21': V21,
            'V22': V22,
            'V23': V23,
            'V24': V24,
            'V25': V25,
            'V26': V26,
            'V27': V27,
            'V28': V28,
            'V29': Amount
        }

        df = pd.DataFrame(data)

        # Standardize input data
        X_input = sc.transform(df)

        with tf.Session() as sess:
            # Load predictive model
            model = load_model('model.hdf5')
            classes = model.predict_classes(X_input, batch_size=128)

        sess.close()
        # logging.info(classes)

        response_rows = []
        for row in classes.tolist():
            duals = iter([SSE.Dual(numData=row[0])])
            response_rows.append(SSE.Row(duals=duals))
        yield SSE.BundledRows(rows=response_rows)

    @staticmethod
    def _my_func_aggr(request, context):
        """
        Aggregates the parameters to a single comma separated string.
        :param request: iterable sequence of bundled rows
        :return: string
        """
        params = []

        # Iterate over bundled rows
        for request_rows in request:
            # Iterate over rows
            for row in request_rows.rows:
                # Retrieve string value of parameter and append to the params variable
                # Length of param is 1 since one column is received, the [0] collects the first value in the list
                param = [d.strData for d in row.duals][0]
                params.append(param)

        # Aggregate parameters to a single string
        result = ', '.join(params)

        # Create an iterable of dual with the result
        duals = iter([SSE.Dual(strData=result)])

        # Yield the row data as bundled rows
        yield SSE.BundledRows(rows=[SSE.Row(duals=duals)])

    @staticmethod
    def _cache(request, context):
        """
        Cache enabled. Add the datetime stamp to the end of each string value.
        :param request: iterable sequence of bundled rows
        :param context: not used.
        :return: string
        """
        # Iterate over bundled rows
        for request_rows in request:
            # Iterate over rows
            for row in request_rows.rows:
                # Retrieve string value of parameter and append to the params variable
                # Length of param is 1 since one column is received, the [0] collects the first value in the list
                param = [d.strData for d in row.duals][0]

                # Join with current timedate stamp
                result = param + ' ' + datetime.now().isoformat()
                # Create an iterable of dual with the result
                duals = iter([SSE.Dual(strData=result)])

                # Yield the row data as bundled rows
                yield SSE.BundledRows(rows=[SSE.Row(duals=duals)])

    @staticmethod
    def _no_cache(request, context):
        """
        Cache disabled. Add the datetime stamp to the end of each string value.
        :param request:
        :param context: used for disabling the cache in the header.
        :return: string
        """
        # Disable caching.
        md = (('qlik-cache', 'no-store'),)
        context.send_initial_metadata(md)

        # Iterate over bundled rows
        for request_rows in request:
            # Iterate over rows
            for row in request_rows.rows:
                # Retrieve string value of parameter and append to the params variable
                # Length of param is 1 since one column is received, the [0] collects the first value in the list
                param = [d.strData for d in row.duals][0]

                # Join with current timedate stamp
                result = param + ' ' + datetime.now().isoformat()
                # Create an iterable of dual with the result
                duals = iter([SSE.Dual(strData=result)])

                # Yield the row data as bundled rows
                yield SSE.BundledRows(rows=[SSE.Row(duals=duals)])

    """
    Implementation of rpc functions.
    """

    def GetCapabilities(self, request, context):
        """
        Get capabilities.
        Note that either request or context is used in the implementation of this method, but still added as
        parameters. The reason is that gRPC always sends both when making a function call and therefore we must include
        them to avoid error messages regarding too many parameters provided from the client.
        :param request: the request, not used in this method.
        :param context: the context, not used in this method.
        :return: the capabilities.
        """
        logging.info('GetCapabilities')
        # Create an instance of the Capabilities grpc message
        # Enable(or disable) script evaluation
        # Set values for pluginIdentifier and pluginVersion
        capabilities = SSE.Capabilities(allowScript=True,
                                        pluginIdentifier='Hello World - Qlik',
                                        pluginVersion='v1.0.0-beta1')

        # If user defined functions supported, add the definitions to the message
        with open(self.function_definitions) as json_file:
            # Iterate over each function definition and add data to the capabilities grpc message
            for definition in json.load(json_file)['Functions']:
                function = capabilities.functions.add()
                function.name = definition['Name']
                function.functionId = definition['Id']
                function.functionType = definition['Type']
                function.returnType = definition['ReturnType']

                # Retrieve name and type of each parameter
                for param_name, param_type in sorted(definition['Params'].items()):
                    function.params.add(name=param_name, dataType=param_type)

                logging.info('Adding to capabilities: {}({})'.format(function.name,
                                                                     [p.name for p in function.params]))

        return capabilities

    def ExecuteFunction(self, request_iterator, context):
        """
        Execute function call.
        :param request_iterator: an iterable sequence of Row.
        :param context: the context.
        :return: an iterable sequence of Row.
        """
        # Retrieve function id
        func_id = self._get_function_id(context)

        # Call corresponding function
        logging.info('ExecuteFunction (functionId: {})'.format(func_id))

        return getattr(self, self.functions[func_id])(request_iterator, context)

    def EvaluateScript(self, request, context):
        """
        This plugin provides functionality only for script calls with no parameters and tensor script calls.
        :param request:
        :param context:
        :return:
        """
        # Parse header for script request
        metadata = dict(context.invocation_metadata())
        header = SSE.ScriptRequestHeader()
        header.ParseFromString(metadata['qlik-scriptrequestheader-bin'])

        logging.info("ScriptEval")

        # Retrieve function type
        func_type = self.ScriptEval.get_func_type(header)

        # Verify function type
        if (func_type == FunctionType.Aggregation) or (func_type == FunctionType.Tensor):
            return self.ScriptEval.EvaluateScript(header, request, context, func_type)
        else:
            # This plugin does not support other function types than aggregation  and tensor.
            # Make sure the error handling, including logging, works as intended in the client
            msg = 'Function type {} is not supported in this plugin.'.format(func_type.name)
            context.set_code(grpc.StatusCode.UNIMPLEMENTED)
            context.set_details(msg)
            # Raise error on the plugin-side
            raise grpc.RpcError(grpc.StatusCode.UNIMPLEMENTED, msg)

    """
    Implementation of the Server connecting to gRPC.
    """

    def Serve(self, port, pem_dir):
        """
        Sets up the gRPC Server with insecure connection on port
        :param port: port to listen on.
        :param pem_dir: Directory including certificates
        :return: None
        """
        # Create gRPC server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        SSE.add_ConnectorServicer_to_server(self, server)

        if pem_dir:
            # Secure connection
            with open(os.path.join(pem_dir, 'sse_server_key.pem'), 'rb') as f:
                private_key = f.read()
            with open(os.path.join(pem_dir, 'sse_server_cert.pem'), 'rb') as f:
                cert_chain = f.read()
            with open(os.path.join(pem_dir, 'root_cert.pem'), 'rb') as f:
                root_cert = f.read()
            credentials = grpc.ssl_server_credentials([(private_key, cert_chain)], root_cert, True)
            server.add_secure_port('[::]:{}'.format(port), credentials)
            logging.info('*** Running server in secure mode on port: {} ***'.format(port))
        else:
            # Insecure connection
            server.add_insecure_port('[::]:{}'.format(port))
            logging.info('*** Running server in insecure mode on port: {} ***'.format(port))

        # Start gRPC server
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', nargs='?', default='50055')
    parser.add_argument('--pem_dir', nargs='?')
    parser.add_argument('--definition-file', nargs='?', default='FuncDefs_CreditCardFraud.json')
    args = parser.parse_args()

    # need to locate the file when script is called from outside it's location dir.
    def_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), args.definition_file)

    calc = ExtensionService(def_file)
    calc.Serve(args.port, args.pem_dir)
