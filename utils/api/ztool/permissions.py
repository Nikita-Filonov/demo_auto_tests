def permission_error(action):
    """
    Used to get base error permission for ztool.
    """
    return {'error': f'Insufficient role permissions for this action: {action}'}
