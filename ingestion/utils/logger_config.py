import logging as log 

def log_config(): 
    
    log.basicConfig(
        level= log.INFO,
        format= "%(asctime)s / %(levelname)s / %(message)s / %(name)s"
    )