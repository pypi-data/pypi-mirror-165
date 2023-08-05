
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import pytz
import traceback
import platform
import configparser
import atexit
import re
import ast


from .DS_Requests import TokenRequest, Instrument, Properties, DataRequest, DataType, Date, DSUserObjectFault

#--------------------------------------------------------------------------------------
class Datastream:
    """Datastream helps to retrieve data from DSWS web rest service"""
    url = "https://product.datastream.com"
    username = ""
    password = ""
    _timeout = 300
    _proxy = None
    _sslCert = None
    reqSession = requests.Session()
    appID = "DatastreamUCSPy-1.0.6"
    reqSession.headers['User-Agent'] = reqSession.headers['User-Agent'] + ' DatastreamUCSPy/1.0.6'
    certfile = None
    token = None
    tokenExpiry = None
   
    
#--------Constructor ---------------------------  
    def __init__(self, config = None, username = None, password = None, proxies = None, sslCer = None):
        """
        Constructor: user details can be supplied from a config file or passed directly as parameters in the constructor of the derived user object type class.

        1) Using ini file (e.g. config.ini) with format

        [credentials]
        username=YourID
        password=YourPwd

        [proxies]
        # of the form: { 'http' : proxyHttpAddress,  'https' : proxyHttpsAddress } See https://docs.python-requests.org/en/latest/user/advanced/
        proxies=ProxyDetails   

        [cert]
        sslCertFile=YourCertFile
        # only read if no sslCertFile entry
        sslCertPath=YourCertPath  

        # first logon with your credentials. Creating a DatastreamUserCreated_TimeSeries instance (derived from DSConnect) with your credentials automatically logs on for you 
        timeseriesClient = DatastreamUserCreated_TimeSeries('config.ini')

        2) Bypassing a config file and using your credentials directly:

        timeseriesClient = DatastreamUserCreated_TimeSeries(None, 'YourId', 'YourPwd')
        """

        if (config):
            parser = configparser.ConfigParser()
            parser.read(config)

            # Warning: Only override the url for the API service if directed to by Refinitiv.
            if parser.has_section('url'):
                self.url = self.url if parser.get('url', 'path').strip() == '' else parser.get('url', 'path').strip()
                self.url = self.url.lower()
                if self.url:  # we only support https on the API
                    if re.match("^http:", self.url):
                        self.url = self.url.replace('http:', 'https:', 1)
            
            # you can override the web query timeout value
            if parser.has_section('app'):
                self._timeout = 300 if parser.get('app', 'timeout').strip() == '' else int(parser.get('app', 'timeout').strip())

            # You can optionally provide the Datastream credentials from your config file, or optionally override from the constructor
            if parser.has_section('credentials'):
                self.username = None if parser.get('credentials', 'username').strip() == '' else parser.get('credentials', 'username').strip()
                self.password = None if parser.get('credentials', 'password').strip() == '' else parser.get('credentials', 'password').strip()

            # Optionally provide the proxies details and certfile from the config file also
            if parser.has_section('proxies'):
                configProxies = None if parser.get('proxies','proxies').strip() == '' else parser.get('proxies', 'proxies').strip()
                if configProxies:
                    self._proxy = ast.literal_eval(configProxies)

            # Optionally specify a specific cert file from the config, or alternatively an override for the cert path
            if parser.has_section('cert'):
                configCert = None if parser.get('cert','sslCertFile').strip() == '' else parser.get('cert', 'sslCertFile').strip()
                if configCert:
                    self._sslCert = configCert
                else:
                    configPath = None if parser.get('cert','sslCertPath').strip() == '' else parser.get('cert', 'sslCertPath').strip()
                    if configPath: #override system root certificates path
                        self.certfile = configPath

        # set the full reference to the API service from the supplied url
        self.url = self.url +'/DSWSClient/V1/DSService.svc/rest/'
        # You can also override any config by specifying your user credentials, proxy or ssl certificate as parameters in the constructor
        # proxy input must be of the form:
        # proxies = { 'http' : proxyHttpAddress,  'https' : proxyHttpsAddress } # see https://docs.python-requests.org/en/latest/user/advanced/
        if proxies:
            self._proxy = proxies
        if sslCer: # option to specify specific ssl certificate file in constructor
            self._sslCert = sslCer

        # any user credentials loaded from the config file can be over-ridden from credentials supplied as constructor parameters
        if username:
            self.username = username
        if password:
            self.password = password

        # with the given user credentials, we try and logon to the API service to retrieve a token for use with all subsequent queries
        # Must be some credentials supplied and not the stub credentials
        if isinstance(self.username, str) and len(self.username) > 0 and self.username != 'YourID' and isinstance(self.password, str) and len(self.password) > 0:
            self._get_token()
        else:
            raise Exception("You must supply some user credentials.")

#-------------------------------------------------------  
#------------------------------------------------------- 
    def post_user_request(self, tickers, fields=None, start='', end='', freq='', kind=1, retName=False):
        """ This function helps to form requests for get_bundle_data. 
            Each request is converted to JSON format.
            
            Args:
               tickers: string, Dataypes 
               fields: List, default None
               start: string, default ''
               end : string, default ''
               freq : string, default '', By deafult DSWS treats as Daily freq
               kind: int, default 1, indicates Timeseries as output

          Returns:
                  Dictionary"""

            
        if fields == None:
            fields=[]
        
        index = tickers.rfind('|')
        propList = []
        try:
            if index == -1:
                instrument = Instrument(tickers, None)
            else:
                #Get all the properties of the instrument
                instprops = []
                if tickers[index+1:].rfind(',') != -1:
                    propList = tickers[index+1:].split(',')
                    for eachProp in propList:
                        instprops.append(Properties(eachProp, True))
                else:
                    propList.append(tickers[index+1:])
                    instprops.append(Properties(tickers[index+1:], True))

                instrument = Instrument(tickers[0:index], instprops)
                        
            datypes=[]
            if 'N' in propList:
                prop = [{'Key':'ReturnName', 'Value':True}] 
                retName = True
            else:
                prop = None

            
            if len(fields) > 0:
                for eachDtype in fields:
                    datypes.append(DataType(eachDtype, prop))
            else:
                datypes.append(DataType(fields, prop))
                        
            date = Date(start, freq, end, kind)
            request = {"Instrument":instrument,"DataTypes":datypes,"Date":date}
            return request, retName
        except Exception:
            print("post_user_request : Exception Occured")
            print(traceback.sys.exc_info())
            print(traceback.print_exc(limit=5))
            return None
            
    def get_data(self, tickers, fields=None, start='', end='', freq='', kind=1):
        """This Function processes a single JSON format request to provide
           data response from DSWS web in the form of python Dataframe
           
           Args:
               tickers: string, Dataypes 
               fields: List, default None
               start: string, default ''
               end : string, default ''
               freq : string, default '', By deafult DSWS treats as Daily freq
               kind: int, default 1, indicates Timeseries as output
               retName: bool, default False, to be set to True if the Instrument
                           names and Datatype names are to be returned

          Returns:
                  DataFrame."""
                 

        getData_url = self.url + "GetData"
        raw_dataRequest = ""
        json_dataRequest = ""
        json_Response = ""
        
        if fields == None:
            fields = []
        
        try:
            retName = False
            req, retName = self.post_user_request(tickers, fields, start, end, freq, kind, retName)
            datarequest = DataRequest()
            self.Check_Token() # check and renew token if within 15 minutes of expiry
            raw_dataRequest = datarequest.get_Request(req, self.token)
               
            if (raw_dataRequest != ""):
                json_Response = self._get_json_Response(getData_url, raw_dataRequest)
                
                #format the JSON response into readable table
                if 'DataResponse' in json_Response:
                    if retName:
                        self._get_metadata(json_Response['DataResponse'])
                    response_dataframe = self._format_Response(json_Response['DataResponse'])
                    return response_dataframe
                else:
                    if 'Message' in json_Response:
                        raise Exception(json_Response['Message'])
                    return None
            else:
                return None
        except Exception:
            print("get_data : Exception Occured")
            print(traceback.sys.exc_info())
            print(traceback.print_exc(limit=5))
            return None
    
    def get_bundle_data(self, bundleRequest=None, retName=False):
        """This Function processes a multiple JSON format data requests to provide
           data response from DSWS web in the form of python Dataframe.
           Use post_user_request to form each JSON data request and append to a List
           to pass the bundleRequset.
           
            Args:
               bundleRequest: List, expects list of Datarequests 
               retName: bool, default False, to be set to True if the Instrument
                           names and Datatype names are to be returned

            Returns:
                  DataFrame."""

        getDataBundle_url = self.url + "GetDataBundle"
        raw_dataRequest = ""
        json_dataRequest = ""
        json_Response = ""
       
        if bundleRequest == None:
            bundleRequest = []
        
        try:
            datarequest = DataRequest()
            self.Check_Token() # check and renew token if within 15 minutes of expiry
            raw_dataRequest = datarequest.get_bundle_Request(bundleRequest, self.token)

            #print(raw_dataRequest)
            if (raw_dataRequest != ""):
                 json_Response = self._get_json_Response(getDataBundle_url, raw_dataRequest)
                     #print(json_Response)
                 if 'DataResponses' in json_Response:
                     if retName:
                         self._get_metadata_bundle(json_Response['DataResponses'])
                     response_dataframe = self._format_bundle_response(json_Response)
                     return response_dataframe
                 else:
                    if 'Message' in json_Response:
                        raise Exception(json_Response['Message'])
                    return None
            else:
                return None
        except Exception:
            print("get_bundle_data : Exception Occured")
            print(traceback.sys.exc_info())
            print(traceback.print_exc(limit=5))
            return None
    
#------------------------------------------------------- 
#-------------------------------------------------------             
#-------Helper Functions---------------------------------------------------
    def _get_Response(self, reqUrl, raw_request):
        try:
            #convert raw request to json format before post
            jsonRequest = self._json_Request(raw_request)
            
            if self._sslCert:
                http_Response = self.reqSession.post(reqUrl, json=jsonRequest,  proxies=self._proxy, verify = self._sslCert, timeout= self._timeout)
            else:
                http_Response = self.reqSession.post(reqUrl, json=jsonRequest,  proxies=self._proxy, verify = self.certfile, timeout= self._timeout)
            return http_Response

        except requests.exceptions.ConnectionError as conerr:
            print(conerr)
            raise
        except requests.exceptions.ConnectTimeout as conto:
            print(conto)
            raise
        except requests.exceptions.ContentDecodingError as decerr:
            print(decerr)
            raise
        except requests.exceptions.HTTPError as httperr:
            print(httperr)
            raise
        except requests.exceptions.ProxyError as prxyerr:
            print(prxyerr)
            raise
        except requests.exceptions.RequestException as reqexp:
            print(reqexp)
            raise
        except requests.exceptions.SSLError as sslerr:
            print(sslerr)
            raise
        except requests.exceptions.URLRequired as urlerr:
            print(urlerr)
            raise
        except requests.exceptions.RequestsDependencyWarning as reqwarn:
            print(reqwarn)
            raise
        except requests.exceptions.ReadTimeout as readtout:
            print(readtout)
            raise
        except requests.exceptions.InvalidHeader as inverr:
            print(inverr)
            raise
        except requests.exceptions.InvalidProxyURL as invPrxy:
            print(invPrxy)
            raise
        except requests.exceptions.InvalidURL as invurl:
            print(invurl)
            raise
        except requests.exceptions.InvalidHeader as invhdr:
            print(invhdr)
            raise
        except requests.exceptions.InvalidSchema as invschma:
            print(inschma)
            raise
        except Exception as otherexp:
            print(otherexp)
            raise

        
    def _get_json_Response(self, reqUrl, raw_request):
        try:
          httpResponse = self._get_Response(reqUrl, raw_request)
          # check the response
          if httpResponse.ok:
              json_Response = dict(httpResponse.json())
              return json_Response
          elif httpResponse.status_code == 400 or httpResponse.status_code == 403:
                # possible DSFault exception returned due to permissions, etc
                try:
                    tryJson = json.loads(httpResponse.text)
                    if 'Message' in tryJson.keys() and 'Code' in tryJson.keys():
                        faultDict = dict(tryJson)
                        raise DSUserObjectFault(faultDict)
                except json.JSONDecodeError as jdecodeerr:
                    pass
          # unexpected response so raise as an error
          httpResponse.raise_for_status()
        except json.JSONDecodeError as jdecodeerr:
            print("_get_json_Response : JSON decoder Exception Occured: " + jdecodeerr)
            raise
        except Exception as exp:
            print("_get_json_Response : Exception Occured: ")
            print(exp)
            raise
    
    def _get_token(self, isProxy=False):
        token_url = self.url + "GetToken"
        try:
            propties = []
            propties.append(Properties("__AppId", self.appID))
           
            tokenReq = TokenRequest(self.username, self.password, propties)
            raw_tokenReq = tokenReq.get_TokenRequest()
            
            #Load windows certificates to a local file
            pf = platform.platform()
            if pf.upper().startswith('WINDOWS'):
                self._loadWinCerts()
            else:
                self.certfile = requests.certs.where()

            #Post the token request to get response in json format
            json_Response = self._get_json_Response(token_url, raw_tokenReq)
            self.tokenExpiry = self.jsonDateTime_to_datetime(json_Response['TokenExpiry'])
            self.token = json_Response['TokenValue']
            
        except Exception:
            print("_get_token : Exception Occured")
            print(traceback.sys.exc_info())
            print(traceback.print_exc(limit=2))
            return None

    def IsValid(self):
        return isinstance(self.token, str) and len(self.token) > 0 and isinstance(self.tokenExpiry, datetime)

    def Check_Token(self):
        if not self.IsValid():
            raise Exception("You are not logged on. Please recreate the DatastreamEconomicFilters client supplying valid user credentials.")
        # A function called before every query to check and renew the token if within 15 minutes of expiry time or later
        timeRenew = datetime.utcnow() + timedelta(minutes = 15) # curiously utcnow() method doesn't set the time zone to utc. We need to do so to compare with token.
        timeRenew = datetime(timeRenew.year, timeRenew.month, timeRenew.day, timeRenew.hour, timeRenew.minute, timeRenew.second, 0, tzinfo=pytz.utc)
        if self.tokenExpiry <= timeRenew :
            self._get_token()

    
    def _json_Request(self, raw_text):
        #convert the dictionary (raw text) to json text first
        jsonText = json.dumps(raw_text)
        byteTemp = bytes(jsonText,'utf-8')
        byteTemp = jsonText.encode('utf-8')
        #convert the json Text to json formatted Request
        jsonRequest = json.loads(byteTemp)
        return jsonRequest

    def jsonDateTime_to_datetime(self, jsonDate):
        # Convert a JSON /Date() string to a datetime object
        if jsonDate is None:
            return None
        try:
            match = re.match(r"^(/Date\()(-?\d*)(\)/)", jsonDate)
            if match == None:
                match = re.match(r"^(/Date\()(-?\d*)([+-])(..)(..)(\)/)", jsonDate)
            if match:
                return datetime(1970, 1, 1, tzinfo=pytz.utc) + timedelta(seconds=float(match.group(2))/1000)
            else:
                raise Exception("Invalid JSON Date: " + jsonDate)
        except Exception as exp:
            print("_get_Date : Exception Occured")
            print(traceback.sys.exc_info())
            print(traceback.print_exc(limit=2))
            return None
            
    def _get_Date(self, jsonDate):
        try:
            #match = re.match("^/Date[(][0-9]{13}[+][0-9]{4}[)]/", jsonDate)
            match = re.match(r"^(/Date\()(-?\d*)([+-])(..)(..)(\)/)", jsonDate)
            if match:
                #d = re.search('[0-9]{13}', jsonDate)
                d = float(match.group(2))
                ndate = datetime(1970,1,1) + timedelta(seconds=float(d)/1000)
                utcdate = pytz.UTC.fromutc(ndate).strftime('%Y-%m-%d')
                return utcdate
            else:
                raise Exception("Invalid JSON Date")
        except Exception:
            print("_get_Date : Exception Occured")
            print(traceback.sys.exc_info())
            print(traceback.print_exc(limit=2))
            return None
            
            
    
    def _get_DatatypeValues(self, jsonResp):
        df = pd.DataFrame()
        multiIndex = False
        valDict = {"Instrument":[],"Datatype":[],"Value":[],"Currency":[]}
        #print (jsonResp)
        for item in jsonResp['DataTypeValues']: 
            datatype = item['DataType']
            
            for i in item['SymbolValues']:
               instrument = i['Symbol']
               currency = None
               if 'Currency' in i:
                   currency = i['Currency'] if i['Currency'] else 'NA'

               valDict["Datatype"].append(datatype)
               valDict["Instrument"].append(instrument)
               if currency:
                   valDict['Currency'].append(currency)
                   colNames = (instrument, datatype, currency)
               else:
                   colNames = (instrument, datatype)
               values = i['Value']
               valType = i['Type']
               df[colNames] = None
               
               #Handling all possible types of data as per DSSymbolResponseValueType
               if valType in [7, 8, 10, 11, 12, 13, 14, 15, 16]:
                   #These value types return an array
                   #The array can be of double, int, string or Object
                   rowCount = df.shape[0]
                   valLen = len(values)
                   #If no of Values is < rowcount, append None to values
                   if rowCount > valLen:
                       for i in range(rowCount - valLen):
                            values.append(None)
                  #Check if the array of Object is JSON dates and convert
                   for x in range(0, valLen):
                       values[x] = self._get_Date(values[x]) if str(values[x]).find('/Date(') != -1 else values[x] 
                   #Check for number of values in the array. If only one value, put in valDict
                   if len(values) > 1:
                       multiIndex = True
                       df[colNames] = values
                   else:
                       multiIndex = False
                       valDict["Value"].append(values[0])   
               elif valType in [1, 2, 3, 5, 6]:
                   #These value types return single value
                   valDict["Value"].append(values)
                   multiIndex = False
               else:
                   if valType == 4:
                       #value type 4 return single JSON date value, which needs conversion
                       values = self._get_Date(values) if str(values).find('/Date(') != -1 else values
                       valDict["Value"].append(values)
                       multiIndex = False
                   elif valType == 9:
                       #value type 9 return array of JSON date values, needs conversion
                       date_array = []
                       if len(values) > 1:
                          multiIndex = True
                          for eachVal in values:
                              date_array.append(self._get_Date(eachVal)) if str(eachVal).find('/Date(') != -1 else eachVal 
                          df[colNames] = date_array
                       else:
                          multiIndex = False
                          date_array.append(self._get_Date(values[0])) if str(values[0]).find('/Date(') != -1 else values[0]
                          valDict["Value"].append(date_array[0])
                   else:
                       if valType == 0:
                           #Error Returned
                           #12/12/2019 - Error returned can be array or a single 
                           #multiIndex = False
                           valDict["Value"].append(values)
                           df[colNames] = values
               if multiIndex:
                   if currency:
                        df.columns = pd.MultiIndex.from_tuples(df.columns, names=['Instrument','Field','Currency'])
                   else:
                        df.columns = pd.MultiIndex.from_tuples(df.columns, names=['Instrument','Field'])
                   
        if not multiIndex:
            indexLen = range(len(valDict['Instrument']))
            if valDict['Currency']:
                newdf = pd.DataFrame(data=valDict,columns=["Instrument", "Datatype", "Value", "Currency"],
                                 index=indexLen)
            else:
                newdf = pd.DataFrame(data=valDict,columns=["Instrument", "Datatype", "Value"],
                                 index=indexLen)
            return newdf
        return df 
            
    def _format_Response(self, response_json):
        # If dates is not available, the request is not constructed correctly
        response_json = dict(response_json)
        if 'Dates' in response_json:
            dates_converted = []
            if response_json['Dates'] != None:
                dates = response_json['Dates']
                for d in dates:
                    dates_converted.append(self._get_Date(d))
        else:
            return 'Error - please check instruments and parameters (time series or static)'
        
        # Loop through the values in the response
        dataframe = self._get_DatatypeValues(response_json)
        if (len(dates_converted) == len(dataframe.index)):
            if (len(dates_converted) > 1):
                #dataframe.insert(loc = 0, column = 'Dates', value = dates_converted)
                dataframe.index = dates_converted
                dataframe.index.name = 'Dates'
        elif (len(dates_converted) == 1):
            dataframe['Dates'] = dates_converted[0]
        
        return dataframe

    def _format_bundle_response(self,response_json):
       formattedResp = []
       for eachDataResponse in response_json['DataResponses']:
           df = self._format_Response(eachDataResponse)
           formattedResp.append(df)      
           
       return formattedResp
   
    def _loadWinCerts(self):
        import wincertstore
        cfile = wincertstore.CertFile()
        cfile.addstore('CA')
        cfile.addstore('ROOT')
        cfile.addstore('MY')
        self.certfile = cfile.name
        atexit.register(cfile.close)
        #print(self.certfile.name)
        
    def _get_metadata(self, jsonResp):
        names = {}
        if jsonResp['SymbolNames']:
            for i in jsonResp['SymbolNames']:
                names.update({i['Key']: i['Value']})
                
        if jsonResp['DataTypeNames']:
            for i in jsonResp['DataTypeNames']:
                names.update({i['Key']: i['Value']})
        
        print(names)
        
    def _get_metadata_bundle(self, jsonResp):
        for eachDataResponse in jsonResp:
            self._get_metadata(eachDataResponse)
#-------------------------------------------------------------------------------------

