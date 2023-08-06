# EjabberdAPI

Python wrapper for the [Ejabberd](https://www.ejabberd.im) API (WIP).  

# Sample usage:  

```
from ejabberdapi import Ejabberd  

ejabberd = Ejabberd("ejabberd_secrets_file")  
```

`ejabberd_secrets_file` is a txt file you must create with the following parameters:  

api_base_url: local Ejabberd node, API listening port. In ex. http://127.0.0.1:5280  
local_vhost: your local ejabberd vhost, in ex. ejabberd@localhost  
admin_account: the ejabberd admin account, in ex. admin@ejabberd.server  
admin_pass: ejabberd admin account password  

# Current implemented Ejabberd endpoints:  

- [check_account](https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#check-account)  
- [register](https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#register)  
- [unregister](https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#unregister)  
- [stats](https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#stats)  
- [status](https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#status)  
- [user_sessions_info](https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#user-sessions-info)  

* 29.8.2022. Added setup attribute

