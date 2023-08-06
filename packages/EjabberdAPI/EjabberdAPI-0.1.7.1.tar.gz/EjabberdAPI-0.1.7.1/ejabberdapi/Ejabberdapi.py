import os
import os.path
import requests
import getpass
from collections import OrderedDict

###
# Dict helper class.
# Defined at top level so it can be pickled.
###
class AttribAccessDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError("Attribute not found: " + str(attr))

    def __setattr__(self, attr, val):
        if attr in self:
            raise AttributeError("Attribute-style access is read only")
        super(AttribAccessDict, self).__setattr__(attr, val)

class Ejabberd:

    name = 'Ejabberd API wrapper'

    def __init__(self, api_base_url=None, local_vhost=None, admin_account=None, admin_pass=None):

        self.__ejabberd_config_path = "secrets/ejabberd_secrets.txt"

        is_setup = self.__check_setup(self)

        if is_setup:

            self.__api_base_url = self.__get_parameter("api_base_url", self.__ejabberd_config_path)
            self.__local_vhost = self.__get_parameter("local_vhost", self.__ejabberd_config_path)
            self.__admin_account = self.__get_parameter("admin_account", self.__ejabberd_config_path)
            self.__admin_pass = self.__get_parameter("admin_pass", self.__ejabberd_config_path)

        else:

            self.__api_base_url, self.__local_vhost, self.__admin_account, self.__admin_pass = self.setup(self)

    def check_account(self, username, host):

        data = {'user':username,
                'host':self.__local_vhost,
            }

        endpoint = self.__api_base_url + '/api/check_account?'
        
        response = self.__api_request(endpoint, data)

        account_exists = True if response.json() == 0 else False

        return account_exists

    def register(self, username, host, user_password):

        account_exists = self.check_account(username, host)

        if not account_exists:

            data = {'user':username,
                    'host':self.__local_vhost,
                    'password':user_password,
                }

            endpoint = self.__api_base_url + '/api/register?'

            response = self.__api_request(endpoint, data)

            is_registered = response.ok

            if is_registered:

                response_text = response.json()

            else:

                response_text = f"{response.json()['status']}: {response.json()['message']}"

        else:

            is_registered = False

            response_text = f"el compte {username}@{host} ja existeix!"

        return (is_registered, response_text)

    def unregister(self, username, host):

        is_unregistered = False

        is_admin = False

        if username+'@'+host == self.__admin_account:

            is_admin = True

            return (is_unregistered, is_admin)

        data = {'user':username,
                'host':self.__local_vhost,
            }

        endpoint = self.__api_base_url + '/api/unregister?'
        
        response = self.__api_request(endpoint, data)

        is_unregistered = response.ok

        return (is_unregistered, is_admin)

    def stats(self):

        names_temp = ["registeredusers","onlineusers","onlineusersnode","uptimeseconds","processes"]

        names = OrderedDict.fromkeys(names_temp).keys()

        stats_dict = {}

        for name in names:

            data = {
                "name": name
                }

            endpoint = self.__api_base_url + '/api/stats?'
            
            response = self.__api_request(endpoint, data)
            
            result = response.json()['stat']

            stats_dict[name] = result

        stats = self.__json_allow_dict_attrs(stats_dict)

        return stats

    def status(self):

        data = {
            }

        endpoint = self.__api_base_url + '/api/status?'

        response = self.__api_request(endpoint, data)

        result = response.json()

        return result

    def user_sessions_info(self, username, host):

        temp_dict = {}

        sessions_dict = {}

        data = {'user':username,
                'host':self.__local_vhost,
            }

        endpoint = self.__api_base_url + '/api/user_sessions_info?'

        response = self.__api_request(endpoint, data)

        i = 0
        while i < len(response.json()):

            temp_dict['connection'] = response.json()[i]['connection']
            temp_dict['ip'] = response.json()[i]['ip']
            temp_dict['port'] = response.json()[i]['port'] 
            temp_dict['priority'] = response.json()[i]['priority']
            temp_dict['node'] = response.json()[i]['node']
            temp_dict['uptime'] = response.json()[i]['uptime']
            temp_dict['status'] = response.json()[i]['status']
            temp_dict['resource'] = response.json()[i]['resource']
            temp_dict['statustext'] = response.json()[i]['statustext']

            if len(sessions_dict) > 0:

                ds = [temp_dict, sessions_dict]
                sessions_temp = {}
                for k in temp_dict.keys():
                    sessions_temp[k] = tuple(sessions_temp[k] for sessions_temp in ds)

            else:

                sessions_dict = temp_dict.copy()

                sessions_temp = sessions_dict.copy()

            i += 1

        sessions = self.__json_allow_dict_attrs(sessions_temp)

        return sessions

    def __api_request(self, endpoint, data):

        try:

            response = requests.post(url = endpoint, json = data, auth=(self._Ejabberd__admin_account, self._Ejabberd__admin_pass))

        except Exception as e:

            raise EjabberdNetworkError(f"Could not complete request: {e}")

        if response is None:

            raise EjabberdIllegalArgumentError("Illegal request.")             

        if not response.ok:

                try:
                    if isinstance(response, dict) and 'error' in response:
                        error_msg = response['error']
                    elif isinstance(response, str):
                        error_msg = response
                    else:
                        error_msg = None
                except ValueError:
                    error_msg = None

                if response.status_code == 404:
                    ex_type = EjabberdNotFoundError
                    if not error_msg:
                        error_msg = 'Endpoint not found.'
                        # this is for compatibility with older versions
                        # which raised EjabberdAPIError('Endpoint not found.')
                        # on any 404
                elif response.status_code == 401:
                    ex_type = EjabberdUnauthorizedError
                elif response.status_code == 500:
                    ex_type = EjabberdInternalServerError
                elif response.status_code == 502:
                    ex_type = EjabberdBadGatewayError
                elif response.status_code == 503:
                    ex_type = EjabberdServiceUnavailableError
                elif response.status_code == 504:
                    ex_type = EjabberdGatewayTimeoutError
                elif response.status_code >= 500 and \
                    response.status_code <= 511:
                    ex_type = EjabberdServerError
                else:
                    ex_type = EjabberdAPIError

                raise ex_type(
                    'Ejabberd API returned error',
                    response.status_code,
                    response.reason,
                    error_msg)

        else:

            return response

    @staticmethod
    def __check_setup(self):

        is_setup = False

        if not os.path.isfile(self.__ejabberd_config_path):
            print(f"File {self.__ejabberd_config_path} not found, running setup.")
        else:
            is_setup = True

        return is_setup

    @staticmethod
    def setup(self):

        if not os.path.exists('secrets'):
            os.makedirs('secrets')

        self.__api_base_url = input("api_base_url, in ex. 'http://127.0.0.1:5280': ")
        self.__local_vhost = input("local_vhost, in ex. 'ejabberd.server': ")
        self.__admin_account = input("admin_account,  in ex. 'admin@ejabberd.server': ")
        self.__admin_pass = getpass.getpass("admin_pass, in ex. 'my_very_hard_secret_pass': ")

        if not os.path.exists(self.__ejabberd_config_path):
            with open(self.__ejabberd_config_path, 'w'): pass
            print(f"{self.__ejabberd_config_path} created!")

        with open(self.__ejabberd_config_path, 'a') as the_file:
            print("Writing ejabberd secrets parameters to " + self.__ejabberd_config_path)
            the_file.write(f'api_base_url: {self.__api_base_url}\n'+f'local_vhost: {self.__local_vhost}\n'+f'admin_account: {self.__admin_account}\n'+f'admin_pass: {self.__admin_pass}\n')

        return (self.__api_base_url, self.__local_vhost, self.__admin_account, self.__admin_pass)

    @staticmethod
    def __get_parameter(parameter, file_path ):

        with open( file_path ) as f:
            for line in f:
                if line.startswith( parameter ):
                    return line.replace(parameter + ":", "").strip()

        print(f'{file_path} Missing parameter {parameter}')
        sys.exit(0)

    @staticmethod
    def __json_allow_dict_attrs(json_object):
        """
        Makes it possible to use attribute notation to access a dicts
        elements, while still allowing the dict to act as a dict.
        """
        if isinstance(json_object, dict):
            return AttribAccessDict(json_object)
        return json_object
##
# Exceptions
##
class EjabberdAPIConfigError(Exception):
    """This class exception"""
    
class EjabberdError(Exception):
    """Base class for EjabberdAPI exceptions"""

class EjabberdIOError(IOError, EjabberdError):
    """Base class for EjabberdAPI I/O errors"""

class EjabberdNetworkError(EjabberdIOError):
    """Raised when network communication with the server fails"""
    pass
class EjabberdAPIError(EjabberdError):
    """Raised when the mastodon API generates a response that cannot be handled"""
    pass
class EjabberdServerError(EjabberdAPIError):
    """Raised if the Server is malconfigured and returns a 5xx error code"""
    pass
class EjabberdInternalServerError(EjabberdServerError):
    """Raised if the Server returns a 500 error"""
    pass

class EjabberdBadGatewayError(EjabberdServerError):
    """Raised if the Server returns a 502 error"""
    pass

class EjabberdServiceUnavailableError(EjabberdServerError):
    """Raised if the Server returns a 503 error"""
    pass

class EjabberdGatewayTimeoutError(EjabberdServerError):
    """Raised if the Server returns a 504 error"""
    pass
class EjabberdNotFoundError(EjabberdAPIError):
    """Raised when the ejabberd API returns a 404 Not Found error"""
    pass

class EjabberdUnauthorizedError(EjabberdAPIError):
    """Raised when the ejabberd API returns a 401 Unauthorized error

       This happens when an OAuth token is invalid or has been revoked,
       or when trying to access an endpoint that can't be used without
       authentication without providing credentials."""
    pass
