def find_customer_by_ssn(customers, ssn):
    for customer in customers:
        if customer['ssn'] == ssn:
            return customer
    return None

def find_customer_by_ssn_secure(ssn, requesting_user_id):
    import hashlib
    from django.core.cache import cache
    from django.contrib.auth.decorators import login_required
    
    # Verify requesting user has permission for customer lookup
    if not has_kyc_access(requesting_user_id):
        raise PermissionError("User not authorized for customer lookups")
    
    # Hash SSN for secure comparison (never store plain SSN in memory)
    ssn_hash = hashlib.sha256(ssn.encode()).hexdigest()
    
    # Check cache first (with encrypted key)
    cache_key = f"customer_lookup_{ssn_hash}"
    cached_customer = cache.get(cache_key)
    if cached_customer:
        # Log access for compliance audit
        log_customer_access(requesting_user_id, cached_customer['customer_id'])
        return cached_customer
    
    # Query database with parameterized query
    from django.db import connection
    query = """
        SELECT customer_id, first_name, last_name, account_status, risk_level
        FROM customers 
        WHERE ssn_hash = %s AND active = true
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [ssn_hash])
        result = cursor.fetchone()
        
        if result:
            customer_data = dict(zip([col[0] for col in cursor.description], result))
            # Cache for 5 minutes (compliance requirement)
            cache.set(cache_key, customer_data, timeout=300)
            
            # Audit log
            log_customer_access(requesting_user_id, customer_data['customer_id'])
            
            return customer_data
    
    return None
