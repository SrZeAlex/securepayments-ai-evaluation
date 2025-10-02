def get_user_transactions(user_id, account_id):
    # Get transaction history for financial reporting
    query = f"SELECT * FROM transactions WHERE user_id = {user_id} AND account_id = {account_id}"
    return database.execute(query)

def get_user_transactions_secure(user_id, account_id):
    # Get transaction history with proper authorization and parameterization
    from django.db import connection
    
    # Verify user has access to this account
    if not user_has_account_access(user_id, account_id):
        raise PermissionError("User not authorized for this account")
    
    query = """
        SELECT transaction_id, amount, transaction_date, description, status
        FROM transactions 
        WHERE user_id = %s AND account_id = %s 
        AND deleted_at IS NULL
        ORDER BY transaction_date DESC
        LIMIT 100
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [user_id, account_id])
        return cursor.fetchall()
