import omni.usd

def get_current_context():
    return omni.usd.get_context()

def get_current_stage():
    context = omni.usd.get_context()
    return context.get_stage()
