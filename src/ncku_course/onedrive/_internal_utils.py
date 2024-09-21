from .data import API_exception_mapping as exceptions, API_exception_description as desc
from .exceptions import APIError
from requests.models import Response



def extract_API_innererror(res : Response) -> str:
    """
    Extract inner error code from API error response
    """
    try:
        error = res.json()['error']
        codes = []
        #extract all level of codes
        while('innererror' in error): 
            if 'code' in error: codes.append(error['code'])
            error = error['innererror']
        if 'code' in error: codes.append(error['code'])
        
        # choose the most inner and valid code
        for code in codes[::-1]:
            if code in desc: return desc[code]
        raise
    
    except:
        return "Unknown Error(Unable to obtain more detailed error information)."
    
def handle_API_error(response : Response) -> APIError:
    """
    Handle API error
    """
    code = response.status_code
    
    if code in exceptions:
        message = extract_API_innererror(response)

        exception = exceptions[code] #choose API Exception class
        return exception(message)
    else:
        return APIError(f"Unknown API Error. With status code: {code}.")
